import json
import logging
from typing import Any, Dict
from uuid import uuid4

from pydantic import BaseModel, Field

from openagi.storage.base import BaseStorage
from openagi.storage.chroma import ChromaStorage
from openagi.tasks.lists import TaskLists
from openagi.tasks.task import Task


class BaseMemory(BaseModel):
    session_id: str = Field(default_factory=lambda: uuid4().hex)
    storage: BaseStorage = Field(
        default_factory=lambda: ChromaStorage,
        description="Storage to be used for the Memory.",
        exclude=True,
    )

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.storage = ChromaStorage.from_kwargs(collection_name=self.session_id)
        logging.info(f"Session ID initialized: {self.session_id}")

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

    def save_planned_tasks(self, tasks: TaskLists) -> None:
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
