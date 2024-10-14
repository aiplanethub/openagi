import logging
from typing import Any, Dict, List
from uuid import uuid4
import os, shutil
from pydantic import BaseModel, Field

from openagi.storage.base import BaseStorage
from openagi.storage.chroma import ChromaStorage
from openagi.tasks.lists import TaskLists
from openagi.tasks.task import Task
from openagi.memory.sessiondict import SessionDict


class BaseMemory(BaseModel):
    session_id: str = Field(default_factory=lambda: uuid4().hex)
    storage: BaseStorage = Field(
        default_factory=lambda: ChromaStorage,
        description="Storage to be used for the Memory.",
        exclude=True,
    )
    ltm_storage: BaseStorage = Field(
        default_factory=lambda: ChromaStorage,
        description="Long-term storage to be used for the Memory.",
        exclude=True,
    )

    long_term: bool = Field(default=False, description="Whether or not to use long term memory")
    ltm_threshold: float = Field(default=0.6,
                                 description="Semantic similarity threshold for long term memory instance retrieval")

    long_term_dir: str = Field(default=None, description="Path to directory for long-term memory storage")

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.storage = ChromaStorage.from_kwargs(collection_name=self.session_id)

        # Setting the long_term_dir from environment variable if not provided
        if self.long_term_dir is None:
            self.long_term_dir = os.getenv("LONG_TERM_DIR", ".long_term_dir")

        # Ensuring the directory is hidden by prefixing with a dot if necessary
        if not os.path.basename(self.long_term_dir).startswith('.'):
            self.long_term_dir = os.path.join(os.path.dirname(self.long_term_dir),
                                              f".{os.path.basename(self.long_term_dir)}")

        if self.long_term:
            os.makedirs(self.long_term_dir, exist_ok=True)

            self.ltm_storage = ChromaStorage.from_kwargs(
                collection_name="long_term_memory",
                persist_path=self.long_term_dir
            )
            assert 1 >= self.ltm_threshold >= 0.7, "Semantic similarity threshold should be between 0.7 and 1"

        logging.info(f"Session ID initialized: {self.session_id}")
        if self.long_term:
            logging.info(f"Long-term memory enabled. Using directory: {self.long_term_dir}")

    @staticmethod
    def clear_long_term_memory(directory: str):
        """Clears all data from the specified long-term memory directory."""
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    logging.error(f'Failed to delete {file_path}. Reason: {e}')
            logging.info(f"Cleared all data from the long-term memory directory: {directory}")
        else:
            logging.warning(f"The long-term memory directory does not exist: {directory}")

    def search(self, query: str, n_results: int = 10, **kwargs) -> Dict[str, Any]:
        """
        Search for similar tasks based on a query.

        :param query: The query string to search for.
        :param n_results: The number of results to return.
        :return: A dictionary of search results.
        """
        query_data = {
            "query_texts": query,
            "n_results": n_results,
            "include": ["metadatas", "documents"],
            **kwargs,
        }
        resp = self.storage.query_documents(**query_data)

        return resp["documents"]

    def display_memory(self) -> Dict[str, Any]:
        """
        Retrieve and display the current memory state from the database.

        :return: A dictionary of the current memory state.
        """
        result = self.storage.query_documents(self.session_id, n_results=2)
        return result or {}

    def save_task(self, task: Task) -> None:
        """
        Save execution details into Memory.

        :param task: The task to be saved.
        """
        metadata = self._create_metadata(task)
        self.storage.save_document(
            id=task.id,
            document=task.result,
            metadata=metadata,
        )
        logging.info(f"Task saved: {task.id}")

    def save_planned_tasks(self, tasks: List[Task]) -> None:
        """
        Save a list of planned tasks into Memory.

        :param tasks: The list of tasks to be saved.
        """
        for task in tasks:
            self.save_task(task)

    def update_task(self, task: Task) -> None:
        """
        Update a task in the Memory.

        :param task: The task to be updated.
        """
        metadata = self._create_metadata(task)
        self.storage.update_document(
            id=task.id,
            document=task.result,
            metadata=metadata,
        )
        logging.info(f"Task updated: {task.id}")

    def _create_metadata(self, task: Task) -> Dict[str, Any]:
        """
        Create metadata dictionary for a given task.

        :param task: The task for which to create metadata.
        :return: A dictionary of metadata.
        """
        return {
            "task_id": task.id,
            "session_id": self.session_id,
            "task_name": task.name,
            "task_description": task.description,
            "task_actions": task.actions,
        }

    def add_ltm(self, session : SessionDict):
        """
        Add a session to the long term memory
        :param session: The SessionDict object that has all the details of the session
        :return: None
        """
        self.ltm_storage.save_document(
            id = session.session_id,
            document= session.query,
            metadata= session.model_dump()
        )
        logging.info(f"Long term memory added for session : {session.session_id}")

    def update_ltm(self, session: SessionDict) -> None:
        """
        Update an existing session in long-term memory.

        :param session: The SessionDict object containing updated details of the session.
        :return: None
        """
        self.ltm_storage.update_document(
            id=session.session_id,
            document=session.query,
            metadata=session.model_dump()
        )

        logging.info(f"Long-term memory updated for session: {session.session_id}")

    def get_ltm(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve and return the long-term memory based on a query.

        :param query: The query string to search for.
        :param n_results: The number of results to return.
        :return: A dictionary of search results.
        """
        query_data = {
            "query_texts": query,
            "n_results": n_results,
            "include": ["metadatas", "documents", "distances"],
        }
        response = self.ltm_storage.query_documents(**query_data)
        results = []
        # if "documents" in response and "distances" in response:
        for doc, metadata, distance in zip(response["documents"][0], response["metadatas"][0], response["distances"][0]):
            results.append({
                "document": doc,
                "metadata": metadata,
                "similarity_score": 1 - distance
            })
        if results:
            logging.info(f"Retrieved long-term memory for query: {query}\n{results[0]['document'][:250]}")
            return results

        logging.info(f"No documents found for query: {query}")
        return results
