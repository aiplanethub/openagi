import logging
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from openagi.actions.base import BaseAction
from openagi.llms.azure import LLMBaseModel
from openagi.planner.task_decomposer import BasePlanner, TaskPlanner
from openagi.tasks.lists import TaskLists
from openagi.prompts.execution import TaskExecutor
from openagi.utils.extraction import get_classes_from_json, get_last_json


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
    actions: Optional[BaseAction] = Field(
        default=None,
        description="Actions that the Agent supports",
    )
    max_steps: int = Field(
        default=20,
        description="Maximum number of steps to achieve the objective.",
    )

    def _run_planner(self, query: str,descripton:str):
        if self.planner:
            if not getattr(self.planner, "llm", False):
                setattr(self.planner, "llm", self.llm)
        return self.planner.plan(query=query,descripton=descripton)

    def run(self, query: str,description:str):
        # Planning stage to create list of tasks
        tasks = self._run_planner(
            query=query,
            description=description
        )

        # Tasks List
        task_lists = TaskLists()
        task_lists.add_tasks(tasks=tasks)
        logging.debug(f"Created total {task_lists.get_tasks().qsize()} Tasks.")

        # Tasks execution
        cur_task = None
        steps = 0
        while not task_lists.all_tasks_completed and steps <= self.max_steps:
            cur_task = task_lists.get_next_unprocessed_task()
            # Execute tasks using
            res = self.execute(cur_task)
            # Add task and res to STMemory
            # self.st_memory.add(curr_task)
            cur_task.set_result(res)
            steps += 1

    def execute(
        self,
        query,
        task,
        all_tasks,
    ):
        # Get supported actions and convert to array of dict(actions)
        actions_dict: List[BaseAction] = []
        for act in self.actions:
            act: BaseAction
            actions_dict.append(act.cls_doc)

        te_vars = dict(
            objective=task,
            all_tasks=all_tasks,
            current_task_name=task.name,
            current_description=task.description,
            previous_task=self.st_memory.get_previous_task(),
            supported_actions=actions_dict,
        )
        te = TaskExecutor.from_template(**te_vars)

        resp = self.llm.run(input_data=te)
        te_actions = get_last_json(resp)
        actions = get_classes_from_json(te_actions)

        res = None
        for act_cls, params in actions:
            params["prev_obs"] = res
            act = act_cls(**params)
            res = act()

        # TODO: Memory
        return res