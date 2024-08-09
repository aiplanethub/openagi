import logging
import inspect
import importlib.util
import pkgutil
from enum import Enum
from textwrap import dedent
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator

from openagi.actions.base import BaseAction
from openagi.actions.compressor import SummarizerAction
from openagi.actions.formatter import FormatterAction
from openagi.actions.obs_rag import MemoryRagAction
from openagi.actions.utils import run_action
from openagi.exception import OpenAGIException
from openagi.llms.azure import LLMBaseModel
from openagi.memory.memory import Memory
from openagi.planner.task_decomposer import BasePlanner, TaskPlanner
from openagi.prompts.worker_task_execution import WorkerAgentTaskExecution
from openagi.tasks.lists import TaskLists
from openagi.utils.extraction import (
    find_last_r_failure_content,
    get_act_classes_from_json,
    get_last_json,
)
from openagi.utils.helper import get_default_llm
from openagi.utils.tool_list import get_tool_list
from openagi.worker import Worker


class OutputFormat(str, Enum):
    markdown = "markdown"
    raw_text = "raw_text"


class Admin(BaseModel):
    planner: Optional[BasePlanner] = Field(
        description="Type of planner to use for task decomposition.",
        default=None,
    )
    llm: Optional[LLMBaseModel] = Field(
        description="LLM Model to be used.",
        default=None,
    )
    memory: Optional[Memory] = Field(
        default_factory=list, description="Memory to be used.", exclude=True
    )
    actions: Optional[List[Any]] = Field(
        description="Actions that the Agent supports", default_factory=list
    )
    max_iterations: int = Field(
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
    summarize_task_context: bool = Field(
        default=True,
        description="If set to True, the task context will be summarized and passed to the next task else the task context will be passed as is.",
    )
    output_key: str = Field(
        default="final_output",
        description="Key to be used to store the output.",
    )

    def model_post_init(self, __context: Any) -> None:
        model = super().model_post_init(__context)

        if not self.llm:
            self.llm = get_default_llm()

        if not self.planner:
            self.planner = TaskPlanner(workers=self.workers)

        if not self.memory:
            self.memory = Memory()

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
        if workers:
            for worker in workers:
                if not getattr(worker, "llm", False):
                    setattr(worker, "llm", self.llm)
                if not getattr(worker, "memory", False):
                    setattr(worker, "memory", self.memory)

        if not self.workers:
            self.workers = workers
        else:
            self.workers.extend(workers)

    def run_planner(self, query: str, descripton: str):
        if self.planner:
            if not getattr(self.planner, "llm", False):
                setattr(self.planner, "llm", self.llm)

            setattr(self.planner, "workers", self.workers)

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
            supported_workers=workers_dict,
        )

    def _generate_tasks_list(self, planned_tasks):
        task_lists = TaskLists()
        task_lists.add_tasks(tasks=planned_tasks)
        logging.debug(f"Created {task_lists.get_tasks_queue().qsize()} Tasks.")
        return task_lists

    def get_previous_task_contexts(self, task_lists: TaskLists):
        task_summaries = []
        logging.info("Retrieving completed task contexts...")
        t_list = task_lists.completed_tasks.queue
        for indx, task in enumerate(t_list):
            memory = run_action(
                action_cls=MemoryRagAction,
                task=task,
                llm=self.llm,
                memory=self.memory,
                query=task.id,
            )
            if memory and self.summarize_task_context:
                params = {
                    "past_messages": memory,
                    "llm": self.llm,
                    "memory": self.memory,
                    "instructions": "Include summary of all the thoughts, but include all the relevant points from the observations without missing any.",
                }
                memory = run_action(action_cls=SummarizerAction, **params)
                if not memory:
                    raise Exception("No memory returned after summarization.")
            task_summaries.append(f"\n{indx+1}. {task.name} - {task.description}\n{memory}")
        else:
            logging.warning("No Tasks to summarize.")
        if task_summaries:
            return "\n".join(task_summaries).strip()
        return "None"

    def _get_worker_by_id(self, worker_id: str):
        for worker in self.workers:
            if worker.id == worker_id:
                return worker
        raise ValueError(f"Worker with id {worker_id} not found.")

    def worker_task_execution(self, query: str, description: str, task_lists: TaskLists):
        res = None

        while not task_lists.all_tasks_completed:
            cur_task = task_lists.get_next_unprocessed_task()
            worker = self._get_worker_by_id(cur_task.worker_id)
            res, task = worker.execute_task(
                cur_task,
                context=self.get_previous_task_contexts(task_lists=task_lists),
            )
            self.memory.update_task(task)
            task_lists.add_completed_tasks(task)

        logging.info("Finished Execution...")

        if self.output_format == OutputFormat.markdown and res:
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

    def _provoke_thought_obs(self, observation):
        thoughts = dedent(f"""Observation: {observation}""".strip())
        return thoughts

    def _should_continue(self, llm_resp: str) -> Union[bool, Optional[Dict]]:
        output: Dict = get_last_json(llm_resp, llm=self.llm, max_iterations=self.max_iterations)
        output_key_exists = bool(output and output.get(self.output_key))
        return (not output_key_exists, output)

    def _force_output(
        self, llm_resp: str, all_thoughts_and_obs: List[str]
    ) -> Union[bool, Optional[str]]:
        """Force the output once the max iterations are reached."""
        prompt = (
            "\n".join(all_thoughts_and_obs)
            + "Based on the previous action and observation, give me the output."
        )
        output = self.llm.run(prompt)
        cont, final_output = self._should_continue(output)
        if cont:
            prompt = (
                "\n".join(all_thoughts_and_obs)
                + f"Based on the previous action and observation, give me the output. {final_output}"
            )
            output = self.llm.run(prompt)
            cont, final_output = self._should_continue(output)
        if cont:
            raise OpenAGIException(
                f"LLM did not produce the expected output after {self.max_iterations} iterations."
            )
        return (cont, final_output)

    def auto_workers_assignment(self, query: str, description: str, task_lists: TaskLists):
        """
        Autonomously generates the Workers with the

        Args:
            query (str): The query to be processed.
            description (str): A description of the task.
            task_lists (TaskLists): The task lists to be processed.

        Returns:
            str: JSON of the list of Workers that needs to be executed
        """

        worker_dict = {}

        # all_thoughts_and_obs = []
        # output = None
        # previous_task_context = None
        workers = []
        worker_dict = {}
        main_task_list = TaskLists()
        while not task_lists.all_tasks_completed:
            cur_task = task_lists.get_next_unprocessed_task()
            print(cur_task)
            logging.info(f"**** Executing Task - {cur_task.name} [{cur_task.id}] ****")

            # task_to_execute = f"{cur_task.name}. {cur_task.description}"
            # worker_description = f"{cur_task.role} - {cur_task.instructions}"

            # print(task_to_execute)
            # print(worker_description)
            worker_config = cur_task.worker_config

            worker_instance = None
            if worker_config["role"] not in worker_dict:
                worker_instance = Worker(
                    role=worker_config["role"],
                    instructions=worker_config["instructions"],
                    llm=self.llm,
                    actions=self.get_supported_actions_for_worker(
                        worker_config["supported_actions"]
                    ),
                )
                worker_dict[worker_config["role"]] = worker_instance
            else:
                worker_instance = worker_dict[worker_config["role"]]
            workers.append(worker_instance)
            cur_task.worker_id = worker_instance.id
            main_task_list.add_task(cur_task)

        task_lists = main_task_list
        self.assign_workers(workers=workers)

        if self.workers:
            return self.worker_task_execution(
                query=query,
                description=description,
                task_lists=task_lists,
            )

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
        all_thoughts_and_obs = []
        output = None
        previous_task_context = None

        while not task_lists.all_tasks_completed:
            iteration = 1
            max_iterations = self.max_iterations

            cur_task = task_lists.get_next_unprocessed_task()
            logging.info(f"**** Executing Task - {cur_task.name} [{cur_task.id}] ****")

            task_to_execute = f"{cur_task.name}. {cur_task.description}"
            agent_description = "Task executor"

            logging.debug("Provoking initial thought observation...")
            initial_thought_provokes = self._provoke_thought_obs(None)

            te_vars = dict(
                task_to_execute=task_to_execute,
                worker_description=agent_description,
                supported_actions=[action.cls_doc() for action in self.actions],
                thought_provokes=initial_thought_provokes,
                output_key=self.output_key,
                context=previous_task_context,
                max_iterations=max_iterations,
            )

            logging.debug("Generating base prompt...")
            base_prompt = WorkerAgentTaskExecution().from_template(te_vars)
            prompt = f"{base_prompt}\nThought:\nIteration: {iteration}\nActions:\n"

            logging.debug("Running LLM with prompt...")
            observations = self.llm.run(prompt)
            logging.info(f"LLM execution completed. Observations: {observations}")
            all_thoughts_and_obs.append(prompt)

            while iteration < max_iterations:
                logging.info(f"---- Iteration {iteration} ----")
                continue_flag, output = self._should_continue(observations)

                if not continue_flag:
                    logging.info(f"Task completed. Output: {output}")
                    break

                resp_json = get_last_json(observations)

                output = resp_json.get(self.output_key) if resp_json else None
                if output:
                    cur_task.result = output
                    cur_task.actions = te_vars["supported_actions"]
                    self.memory.update_task(cur_task)

                action_json = resp_json.get("action") if resp_json else None

                if action_json and not isinstance(action_json, list):
                    action_json = [action_json]

                if not action_json:
                    logging.warning(f"No action found in the output: {output}")
                    observations = f"Action: {action_json}\n{observations} Unable to extract action. Verify the output and try again."
                    all_thoughts_and_obs.append(observations)
                    iteration += 1
                elif action_json:
                    actions = get_act_classes_from_json(action_json)

                    for act_cls, params in actions:
                        params["previous_action"] = None  # Modify as needed
                        params["llm"] = self.llm
                        params["memory"] = self.memory
                        try:
                            logging.debug(f"Running action: {act_cls.__name__}...")
                            res = run_action(action_cls=act_cls, **params)
                            logging.info(f"Action '{act_cls.__name__}' completed. Result: {res}")
                        except Exception as e:
                            logging.error(f"Error running action: {e}")
                            observations = f"Action: {action_json}\n{observations}. {e} Try to fix the error and try again. Ignore if already tried more than twice"
                            all_thoughts_and_obs.append(observations)
                            iteration += 1
                            continue

                        observation_prompt = f"Observation: {res}\n"
                        all_thoughts_and_obs.append(observation_prompt)
                        observations = res

                    logging.debug("Provoking thought observation...")
                    thought_prompt = self._provoke_thought_obs(observations)
                    all_thoughts_and_obs.append(f"\n{thought_prompt}\nActions:\n")

                    prompt = f"{base_prompt}\n" + "\n".join(all_thoughts_and_obs)
                    logging.debug(f"\nSTART:{'*' * 20}\n{prompt}\n{'*' * 20}:END")
                    logging.debug("Running LLM with updated prompt...")
                    observations = self.llm.run(prompt)
                    iteration += 1
            else:
                if iteration == max_iterations:
                    logging.info("---- Forcing Output ----")
                    cont, final_output = self._force_output(observations, all_thoughts_and_obs)
                    if cont:
                        raise OpenAGIException(
                            f"LLM did not produce the expected output after {iteration} iterations for task {cur_task.name}"
                        )
                    output = final_output
                    cur_task.result = output
                    cur_task.actions = te_vars["supported_actions"]
                    self.memory.update_task(cur_task)
                    task_lists.add_completed_tasks(cur_task)

            previous_task_context = self.get_previous_task_contexts(task_lists)
            task_lists.add_completed_tasks(cur_task)

        logging.info("Finished Execution...")

        if self.output_format == OutputFormat.markdown:
            logging.info("Output Formatting...")
            output_formatter = FormatterAction(
                content=output,
                format_type=OutputFormat.markdown,
                llm=self.llm,
                memory=self.memory,
            )
            output = output_formatter.execute()

        logging.debug(f"Execution Completed for Session ID - {self.memory.session_id}")
        return output

    def run(self, query: str, description: str):
        logging.info("Running Admin Agent...")
        logging.info(f"SessionID - {self.memory.session_id}")

        planned_tasks = self.run_planner(query=query, descripton=description)

        logging.info("Tasks Planned...")
        logging.debug(f"{planned_tasks=}")

        task_lists: TaskLists = self._generate_tasks_list(planned_tasks=planned_tasks)

        self.memory.save_planned_tasks(tasks=list(task_lists.tasks.queue))

        if self.planner.autonomous:
            return self.auto_workers_assignment(
                query=query, description=description, task_lists=task_lists
            )
        else:
            if self.workers:
                return self.worker_task_execution(
                    query=query,
                    description=description,
                    task_lists=task_lists,
                )
            else:
                return self.single_agent_execution(
                    query=query, description=description, task_lists=task_lists
                )

    def _can_task_execute(self, llm_resp: str) -> Union[bool, Optional[str]]:
        content: str = find_last_r_failure_content(text=llm_resp)
        if content:
            return False, content
        return True, content

    def get_supported_actions_for_worker(self, actions_list: List[str]):
        """
        This function takes a list of action names (strings) and returns a list of class objects
        from the modules within the 'tools' folder that match these action names and inherit from BaseAction.

        :param actions_list: List of action names as strings.
        :return: List of matching class objects.
        """
        matching_classes = []
        tool_list = get_tool_list()
        # Iterate through all modules in the tools package
        for action in tool_list:
            if action.__name__ in actions_list:
                matching_classes.append(action)

        return matching_classes
