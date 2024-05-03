from queue import Queue
from typing import List

from openagi.tasks.task import Task


class TaskLists:
    def __init__(self) -> None:
        self.tasks = Queue()

    def add_task(self, task: Task) -> None:
        """Adds a Task instance to the queue."""
        self.tasks.put(task)

    def add_tasks(self, tasks: List[Task]):
        for task in tasks:
            self.add_task(task)

    def get_next_unprocessed_task(self) -> Task:
        """Retrieves the next unprocessed task from the queue."""
        if not self.tasks.empty():
            return self.tasks.get_nowait()
        return None

    def all_tasks_processed(self):
        """Checks if all tasks in the queue have been processed."""
        return self.tasks.empty()
