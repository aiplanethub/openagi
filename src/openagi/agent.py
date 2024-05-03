from typing import Optional

from pydantic import BaseModel, Field

from openagi.llms.azure import LLMBaseModel
from openagi.planner.task_decomposer import BasePlanner, TaskPlanner


class Admin(BaseModel):
    planner: BasePlanner = Field(
        default=TaskPlanner(),
        description="Type of planner to use for task decomposition.",
    )
    llm: Optional[LLMBaseModel] = Field(
        description="LLM Model to be used.",
    )
    st_memory = None
    lt_memory = None

    def _run_planner(self, query: str):
        self.planner.plan(query)

    def run(self, query: str):
        # Planning stage to create list of tasks
        tasks = self._run_planner(query=query)

        # Tasks execution
