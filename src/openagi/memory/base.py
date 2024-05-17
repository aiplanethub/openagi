from typing import Any, Dict
from uuid import uuid4

from pydantic import BaseModel, Field

from openagi.storage.base import BaseStorage
from openagi.storage.chroma import ChromaStorage
from openagi.tasks.lists import TaskLists
from openagi.tasks.task import Task

# TODO: Fix error handling


class BaseMemory(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    sessiond_id: str = Field(default=uuid4().hex)
    storage: BaseStorage = Field(
        default=ChromaStorage,
        description="Storage to be used for the Memory.",
        exclude=True,
    )

    def model_post_init(self, __context: Any) -> None:
        x = super().model_post_init(__context)
        self.storage = ChromaStorage.from_kwargs()
        return x

    def search(self, **kwargs) -> Dict[str, Any]:
        """Search for similar tasks based on a query."""
        return self.storage.query_documents(kwargs)

    def display_memory(self) -> Dict[str, Any]:
        """Retrieve and display the current memory state from the database."""
        result = self.storage.query_documents(self.session_id, n_results=2)
        if result:
            return result
        return {}

    def save_task(self, task: Task) -> None:
        """Save execution details into Memory."""
        document = f"Task: {task.name}, Description: {task.description}, Response: {task.result}"
        metadata = {
            "task_id": task.id,
            "session_id": self.sessiond_id,
        }

        return self.storage.save_document(
            id=task.id,
            document=document,
            metadata=metadata,
        )

    def save_planned_tasks(self, tasks: TaskLists):
        for task in tasks:
            self.save_task(task=task)
