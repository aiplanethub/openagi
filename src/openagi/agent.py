from enum import Enum
import logging
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, field_validator

from openagi.actions.base import BaseAction
from openagi.actions.compressor import SummarizerAction
from openagi.actions.formatter import FormatterAction
from openagi.actions.obs_rag import MemoryRagAction
from openagi.exception import ExecutionFailureException, OpenAGIException
from openagi.llms.azure import LLMBaseModel
from openagi.memory.memory import Memory
from openagi.planner.task_decomposer import BasePlanner, TaskPlanner
from openagi.prompts.execution import TaskExecutor
from openagi.tasks.lists import TaskLists
from openagi.tasks.task import Task
from openagi.utils.extraction import (
    find_last_r_failure_content,
    get_classes_from_json,
    get_last_json,
)


class OutputFormat(str, Enum):
    markdown = "markdown"
    raw_text = "raw_text"


class Admin(BaseModel):
    planner: BasePlanner = Field(
        default=TaskPlanner(),
        description="Type of planner to use for task decomposition.",
    )
    llm: LLMBaseModel = Field(
        description="LLM Model to be used.",
    )
    memory: Optional[Memory] = Field(
        default_factory=list,
        description="Memory to be used.",
        exclude=True,
    )
    actions: Optional[List[Any]] = Field(
        description="Actions that the Agent supports",
        default_factory=list,
    )
    max_steps: int = Field(
        default=20,
        description="Maximum number of steps to achieve the objective.",
    )
    output_format: OutputFormat = Field(
        default=OutputFormat.markdown,
        description="Format to be converted the result while returning.",
    )

    def model_post_init(self, __context: Any) -> None:
        resp = super().model_post_init(__context)

        if not self.memory:
            self.memory = Memory()

        # Actions
        self.actions = self.actions or []
        default_actions = [MemoryRagAction]
        self.actions.extend(default_actions)

        return resp

    @field_validator("actions")
    @classmethod
    def actions_validator(cls, act_clss):
        for act_cls in act_clss:
            if not issubclass(act_cls, BaseAction):
                raise ValueError(f"{act_cls} is not a subclass of BaseAction")
        return act_clss

    def run_planner(self, query: str, descripton: str):
        if self.planner:
            if not getattr(self.planner, "llm", False):
                setattr(self.planner, "llm", self.llm)
        logging.info("Thinking...")
        actions_dict: List[BaseAction] = []
        for act in self.actions:
            actions_dict.append(act.cls_doc())
        return self.planner.plan(
            query=query, description=descripton, supported_actions=actions_dict
        )

    def generate_tasks_list(self, planned_tasks):
        task_lists = TaskLists()
        task_lists.add_tasks(tasks=planned_tasks)
        logging.debug(f"Created total {task_lists.get_tasks_queue().qsize()} Tasks.")
        return task_lists

    def run(self, query: str, description: str):
        logging.info("Running Admin Agent...")
        logging.info(f"SessionID - {self.memory.session_id}")

        # Planning stage to create list of tasks
        planned_tasks = self.run_planner(query=query, descripton=description)
        if not planned_tasks:
            raise OpenAGIException("Failed to Plan Tasks. Please Try Again...")
        logging.info("Tasks Planned...")
        logging.debug(f"{planned_tasks=}")

        # Tasks List
        task_lists: TaskLists = self.generate_tasks_list(planned_tasks=planned_tasks)

        self.memory.save_planned_tasks(tasks=list(task_lists.tasks.queue))

        # Tasks execution
        cur_task = None
        prev_task = None
        steps = 0
        _tasks_lists = task_lists.get_tasks_lists()
        while not task_lists.all_tasks_completed:
            print(f"{'*'*100}{'*'*100}")

            logging.info(f"Execuing Step {steps}")
            cur_task = task_lists.get_next_unprocessed_task()
            # Execute tasks using
            res, actions = self.execute_task(
                query=query,
                task=cur_task,
                all_tasks=_tasks_lists,
                prev_task=prev_task,
            )
            if res:
                cur_task.result = str(res)
                cur_task.actions = str(actions)
                prev_task = cur_task.model_copy()
                self.memory.update_task(prev_task)
            steps += 1

        # Final result
        logging.info("Finished Execution...")
        # print(f"\n ******** Final Response *******\n{res}\n\n")
        if self.output_format == OutputFormat.markdown:
            logging.info("Output Formatting...")
            output_formatter = FormatterAction(
                content=res,
                format_type=OutputFormat.markdown,
                llm=self.llm,
                memory=self.memory,
            )
            res = output_formatter.execute()
        logging.debug(f"Execution Completed for Session ID - {self.memory.session_id}")
        return res

    def _run_action(self, action_cls: str, **kwargs):
        logging.info(f"Running Action - {action_cls}")
        kwargs["memory"] = self.memory
        kwargs["llm"] = self.llm
        action: BaseAction = action_cls(**kwargs)  # Create an instance with provided kwargs
        res = action.execute()
        return res

    def _can_task_execute(self, llm_resp: str) -> Union[bool, Optional[str]]:
        content: str = find_last_r_failure_content(text=llm_resp)
        if content:
            return False, content
        return True, content

    def execute_task(
        self,
        query: str,
        task: Task,
        all_tasks: TaskLists,
        prev_task: Task,
    ):
        logging.info(f"{'>'*10} Starting execution of `{task.name} [{task.id}]` {'<'*10}")
        logging.info(f"Description - {task.description}")
        # Get supported actions and convert to array of dict(actions)
        actions_dict: List[BaseAction] = []
        for act in self.actions:
            actions_dict.append(act.cls_doc())

        prev_task_str = (
            f"{prev_task.name}\n{prev_task.description}. Previous_Action: {prev_task.actions} Previous_Result: {prev_task.result}"
            if prev_task
            else None
        )
        te_vars = dict(
            objective=query,
            all_tasks=all_tasks,
            current_task_name=task.name,
            current_description=task.description,
            previous_task=prev_task_str,
            supported_actions=actions_dict,
        )
        # TODO: Make TaskExecutor class customizable
        te = TaskExecutor.from_template(variables=te_vars)
        logging.info("TastExecutor Prompt initiated...")
        logging.debug(f"{te=}")
        resp = self.llm.run(te)
        logging.debug(f"{resp=}")
        execute, content = self._can_task_execute(llm_resp=resp)
        if not execute and content:
            raise ExecutionFailureException(
                f"Execution Failed - {content}; for the task {task.name} [{str(task.id)}]."
            )
        te_actions = get_last_json(resp)
        res = None

        logging.debug(f"{te_actions}")
        if not te_actions:
            logging.warning("No Actions to execute...")
            return res, None

        actions = get_classes_from_json(te_actions)
        # Pass previous action result of the current task to the next action as previous_obs
        for act_cls, params in actions:
            params["previous_action"] = prev_task.result if prev_task else None
            res = self._run_action(action_cls=act_cls, **params)

        return res, actions
