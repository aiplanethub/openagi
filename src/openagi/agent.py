import logging
from typing import Any, Optional

from pydantic import BaseModel, Field

from openagi.llms.azure import LLMBaseModel
from openagi.planner.task_decomposer import BasePlanner, TaskPlanner
from openagi.tasks.lists import TaskLists


class Admin(BaseModel):
    planner: BasePlanner = Field(
        default=TaskPlanner(),
        description="Type of planner to use for task decomposition.",
    )
    llm: Optional[LLMBaseModel] = Field(
        description="LLM Model to be used.",
    )
    st_memory: Optional[Any] = None
    lt_memory: Optional[Any] = None

    def _run_planner(self, query: str):
        if self.planner:
            if not getattr(self.planner, "llm", False):
                setattr(self.planner, "llm", self.llm)
        return self.planner.plan(query=query)

    def run(self, query: str):
        # Planning stage to create list of tasks
        tasks = self._run_planner(
            query=query,
        )

        # Tasks List
        task_lists = TaskLists()
        task_lists.add_tasks(tasks=tasks)
        logging.debug(f"Created total {task_lists.get_tasks().qsize()} Tasks.")

        # Tasks execution
