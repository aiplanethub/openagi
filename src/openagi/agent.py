import logging
from typing import Any, Dict, List, Optional
from typing_extensions import Annotated
from pydantic.functional_validators import AfterValidator

from pydantic import BaseModel, Field, field_validator

from openagi.actions.base import BaseAction
from openagi.llms.azure import LLMBaseModel
from openagi.planner.task_decomposer import BasePlanner, TaskPlanner
from openagi.tasks.lists import TaskLists
from openagi.prompts.execution import TaskExecutor
from openagi.tasks.task import Task
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
    actions: Optional[List[Any]] = Field(
        description="Actions that the Agent supports",
        default_factory=list,
    )
    max_steps: int = Field(
        default=20,
        description="Maximum number of steps to achieve the objective.",
    )

    @field_validator("actions")
    @classmethod
    def actions_validator(cls, act_clss):
        for act_cls in act_clss:
            if not issubclass(act_cls, BaseAction):
                raise ValueError(f"{act_cls} is not a subclass of BaseAction")
        return act_clss

    def run_planner(self, query: str):
        if self.planner:
            if not getattr(self.planner, "llm", False):
                setattr(self.planner, "llm", self.llm)
        return self.planner.plan(query=query)

    def generate_tasks_list(self, planned_tasks):
        task_lists = TaskLists()
        task_lists.add_tasks(tasks=planned_tasks)
        logging.debug(f"Created total {task_lists.get_tasks_queue().qsize()} Tasks.")
        return task_lists

    def run(self, query: str, description: str):
        logging.info("Running Admin Agent...")
        # Planning stage to create list of tasks
        planned_tasks = self.run_planner(
            query=query,
        )
        logging.info("Tasks Planned")
        logging.debug(planned_tasks)
        print(planned_tasks)

        # Tasks List
        task_lists: TaskLists = self.generate_tasks_list(planned_tasks=planned_tasks)

        # Tasks execution
        cur_task = None
        steps = 0
        res = None
        _tasks_lists = task_lists.get_tasks_lists()
        while not task_lists.all_tasks_completed and steps <= self.max_steps:
            logging.info(f"Execuing Step {steps}")
            cur_task = task_lists.get_next_unprocessed_task()
            print(f"{cur_task=}")
            # Execute tasks using
            res = self.execute(query=query, task=cur_task, all_tasks=_tasks_lists)
            # Add task and res to STMemory
            # self.st_memory.add(curr_task)
            cur_task.set_result(res)
            steps += 1
            # TODO:
            # If task as not completed and failed:
            # Fail the whole processs & convey to the users

        # Final result
        return res

    def run_action(self, action_cls: str, **kwargs):
        try:
            logging.info(f"Running Action - {action_cls}")
            action: BaseAction = action_cls(**kwargs)  # Create an instance with provided kwargs
            return action.execute()
        except Exception:
            return None

    def execute(
        self,
        query: str,
        task: Task,
        all_tasks: TaskLists,
    ):
        # Get supported actions and convert to array of dict(actions)
        actions_dict: List[BaseAction] = []
        for act in self.actions:
            act: BaseAction
            actions_dict.append(act.cls_doc())
        te_vars = dict(
            objective=task.name,
            all_tasks=all_tasks,
            current_task_name=task.name,
            current_description=task.description,
            previous_task=None,  # self.st_memory.get_previous_task()
            supported_actions=actions_dict,
        )
        # TODO: Make TaskExecutor class customizable
        te = TaskExecutor.from_template(variables=te_vars)
        logging.info("TastExecutor Prompt initiated...")
        print(">>>", te)
        resp = self.llm.run(te)
        print(f"{resp=}")
        logging.debug(f"{resp=}")
        te_actions = get_last_json(resp)
        logging.debug(f"{te_actions}")
        print(f"{te_actions=}")
        actions = get_classes_from_json(te_actions)
        print(f"{actions=}")
        # Pass previous action result of the current task to the next action as previous_obs
        res = None
        for act_cls, params in actions:
            params["prev_obs"] = res
            res = self.run_action(action_cls=act_cls, **params)

        # TODO: Memory
        return res
