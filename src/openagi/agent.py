import logging
from enum import Enum
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, field_validator

from openagi.actions.base import BaseAction
from openagi.actions.formatter import FormatterAction
from openagi.actions.obs_rag import MemoryRagAction
from openagi.exception import ExecutionFailureException, LLMResponseError, OpenAGIException
from openagi.llms.azure import LLMBaseModel
from openagi.memory.memory import Memory
from openagi.planner.task_decomposer import BasePlanner, TaskPlanner
from openagi.prompts.execution import TaskExecutor
from openagi.tasks.lists import TaskLists
from openagi.tasks.task import Task
from openagi.utils.extraction import (
    find_last_r_failure_content,
    get_act_classes_from_json,
    get_last_json,
)
from openagi.utils.helper import get_default_llm
from openagi.worker import Worker


class OutputFormat(str, Enum):
    markdown = "markdown"
    raw_text = "raw_text"


class Admin(BaseModel):
    """
    The `Admin` class is responsible for managing the overall execution. It handles task planning, task execution, and memory management.

    The class has the following key responsibilities:
    - Initializing and configuring the planner, LLM, and memory components.
    - Validating the list of actions supported by the agent.
    - Assigning workers to the agent.
    - Running the planner to generate a list of tasks to achieve the given objective.
    - Executing the tasks either in a single-agent mode or with multiple workers.
    - Formatting the final result based on the specified output format.
    - Providing utility methods to run individual actions.
    """

    planner: Optional[BasePlanner] = Field(
        description="Type of planner to use for task decomposition."
    )
    llm: Optional[LLMBaseModel] = Field(description="LLM Model to be used.")
    memory: Optional[Memory] = Field(
        default_factory=list, description="Memory to be used.", exclude=True
    )
    actions: Optional[List[Any]] = Field(
        description="Actions that the Agent supports", default_factory=list
    )
    max_steps: int = Field(
        default=20, description="Maximum number of steps to achieve the objective."
    )
    output_format: OutputFormat = Field(
        default=OutputFormat.markdown,
        description="Format to be converted the result while returning.",
    )
    workers: List[Worker] = Field(
        default_factory=list,
        description="List of workers managed by the Admin agent.",
    )

    def model_post_init(self, __context: Any) -> None:
        model = super().model_post_init(__context)

        if not self.planner:
            self.planner = TaskPlanner(workers=self.workers)

        if not self.memory:
            self.memory = Memory()

        if not self.llm:
            self.llm = get_default_llm()

        self.actions = self.actions or []
        default_actions = [MemoryRagAction]
        self.actions.extend(default_actions)

        return model

    @field_validator("actions")
    @classmethod
    def actions_validator(cls, act_clss):
        for act_cls in act_clss:
            if not issubclass(act_cls, BaseAction):
                raise ValueError(f"{act_cls} is not a subclass of BaseAction")
        return act_clss

    def assign_workers(self, workers: List[Worker]):
        if not self.workers:
            self.workers = workers
        else:
            self.workers.extend(workers)

    def run_planner(self, query: str, descripton: str):
        """
        Runs the planner to generate a plan for the given query and description, using the supported actions and workers.

        Args:
            query (str): The query to plan for.
            description (str): The description of the task to plan for.

        Returns:
            The result of the planner's plan() method, which is likely a list of actions to execute.
        """
        if self.planner:
            if not getattr(self.planner, "llm", False):
                setattr(self.planner, "llm", self.llm)
        logging.info("Thinking...")
        actions_dict: List[BaseAction] = []

        for act in self.actions:
            actions_dict.append(act.cls_doc())

        workers_dict = []
        for worker in self.workers:
            workers_dict.append(worker.worker_doc())

        return self.planner.plan(
            query=query,
            description=descripton,
            supported_actions=actions_dict,
            workers=self.workers,
        )

    def generate_tasks_list(self, planned_tasks):
        """
        Generates a list of tasks to be executed by the agent.

        Args:
            planned_tasks (list): A list of tasks to be executed.

        Returns:
            TaskLists: A TaskLists object containing the generated tasks.
        """
        task_lists = TaskLists()
        task_lists.add_tasks(tasks=planned_tasks)
        logging.debug(f"Created total {task_lists.get_tasks_queue().qsize()} Tasks.")
        return task_lists

    def worker_task_execution(self, query: str, description: str, task_lists: TaskLists):
        ...

    def single_agent_execution(self, query: str, description: str, task_lists: TaskLists):
        """
        Executes a single agent's tasks for the given query and description, updating the task lists and memory as necessary.

        Args:
            query (str): The query to be processed.
            description (str): A description of the task.
            task_lists (TaskLists): The task lists to be processed.

        Returns:
            str: The final result of the task execution.
        """
        # Tasks execution
        cur_task = None
        prev_task = None
        steps = 0
        _tasks_lists = task_lists.get_tasks_lists()
        while not task_lists.all_tasks_completed:
            print(f"{'*'*100}{'*'*100}")

            logging.info(f"Execuing Step {steps}")
            cur_task = task_lists.get_next_unprocessed_task()
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

    def run(self, query: str, description: str):
        """
        Runs the Admin Agent, which is responsible for planning and executing tasks based on a given query and description.

        Args:
            query (str): The query to be processed.
            description (str): The description of the query.

        Returns:
            The result of the task execution, either from the worker task execution or the single agent execution.
        """
        logging.info("Running Admin Agent...")
        logging.info(f"SessionID - {self.memory.session_id}")

        # Planning stage to create list of tasks
        planned_tasks = self.run_planner(query=query, descripton=description)

        logging.info("Tasks Planned...")
        logging.debug(f"{planned_tasks=}")

        # Tasks List
        task_lists: TaskLists = self.generate_tasks_list(planned_tasks=planned_tasks)

        self.memory.save_planned_tasks(tasks=list(task_lists.tasks.queue))

        if self.workers:
            return self.worker_task_execution(
                query=query,
                description=description,
                task_lists=task_lists,
            )

        return self.single_agent_execution(
            query=query,
            description=description,
            task_lists=task_lists,
        )

    def _run_action(self, action_cls: str, **kwargs):
        """
        Runs the specified action with the provided keyword arguments.

        Args:
            action_cls (str): The class name of the action to be executed.
            **kwargs: Keyword arguments to be passed to the action class constructor.

        Returns:
            The result of executing the action.
        """
        logging.info(f"Running Action - {action_cls}")
        kwargs["memory"] = self.memory
        kwargs["llm"] = self.llm
        action: BaseAction = action_cls(**kwargs)  # Create an instance with provided kwargs
        res = action.execute()
        return res

    def _can_task_execute(self, llm_resp: str) -> Union[bool, Optional[str]]:
        """
        Checks if a given LLM response can be executed as a task.

        Args:
            llm_resp (str): The LLM response to check.

        Returns:
            Union[bool, Optional[str]]: True if the task can be executed, False otherwise. If False, the second return value contains the reason why the task cannot be executed.
        """
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
        """
        Executes a given task by running the necessary actions and returning the result.

        Args:
            query (str): The original query or objective that the task is trying to solve.
            task (Task): The current task to be executed.
            all_tasks (TaskLists): A list of all tasks that have been defined.
            prev_task (Task): The previous task that was executed, if any.

        Returns:
            tuple: A tuple containing the result of the task execution and the last action executed.
        """
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

        if not te_actions:
            raise LLMResponseError("No Actions found in the model response.")

        res = None

        logging.debug(f"{te_actions}")
        if not te_actions:
            logging.warning("No Actions to execute...")
            return res, None

        actions = get_act_classes_from_json(te_actions)
        # Pass previous action result of the current task to the next action as previous_obs
        for act_cls, params in actions:
            params["previous_action"] = prev_task.result if prev_task else None
            res = self._run_action(action_cls=act_cls, **params)

        return res
