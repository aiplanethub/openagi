from queue import Queue
from typing import Dict, List

from openagi.tasks.task import Task


class TaskLists:
    def __init__(self) -> None:
        self.tasks = Queue()
        self.completed_tasks = Queue()

    def add_task(self, task: Task) -> None:
        """Adds a Task instance to the queue."""
        self.tasks.put(task)

    def add_tasks(self, tasks: List[Dict[str, str]]):
        for task in tasks:
            task["name"] = task["task_name"]
            worker_config = {
                "role": task["role"],
                "instructions": task["instruction"],
                "name": task["worker_name"],
                "supported_actions": task["supported_actions"]
            }
            task["worker_config"] = worker_config
            self.add_task(Task(**task))

    def get_tasks_queue(self) -> List:
        return self.tasks

    def get_tasks_lists(self):
        return [dict(task.model_fields.items()) for task in list(self.tasks.queue)]

    def get_next_unprocessed_task(self) -> Task:
        """Retrieves the next unprocessed task from the queue."""
        if not self.tasks.empty():
            return self.tasks.get_nowait()
        return None

    @property
    def all_tasks_completed(self) -> bool:
        """Checks if all tasks in the queue have been processed."""
        return self.tasks.empty()

    def add_completed_tasks(self, task: Task):
        self.completed_tasks.put(task)
