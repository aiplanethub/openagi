import logging
from pathlib import Path
import re
from textwrap import dedent
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator

from openagi.actions.utils import run_action
from openagi.exception import OpenAGIException
from openagi.llms.base import LLMBaseModel
from openagi.memory.memory import Memory
from openagi.prompts.worker_task_execution import WorkerAgentTaskExecution
from openagi.tasks.task import Task
from openagi.utils.extraction import get_act_classes_from_json, get_last_json
from openagi.utils.helper import get_default_id

class Worker(BaseModel):
    id: str = Field(default_factory=get_default_id)
    role: Optional[str] = Field(description="Role of the worker.")
    instructions: Optional[str] = Field(description="Instructions the worker should follow.")
    llm: Optional[LLMBaseModel] = Field(
        description="LLM Model to be used.",
        default=None,
        exclude=True,
    )
    memory: Optional[Memory] = Field(
        default_factory=list,
        description="Memory to be used.",
        exclude=True,
    )
    actions: Optional[List[Any]] = Field(
        description="Actions that the Worker supports",
        default_factory=list,
    )
    max_iterations: int = Field(
        default=20,
        description="Maximum number of steps to achieve the objective.",
    )
    output_key: str = Field(
        default="final_output",
        description="Key to be used to store the output.",
    )
    force_output: bool = Field(
        default=True,
        description="If set to True, the output will be overwritten even if it exists.",
    )

    # Validate output_key. Should contain only alphabets and only underscore are allowed. Not alphanumeric
    @field_validator("output_key")
    @classmethod
    def validate_output_key(cls, v, values, **kwargs):
        if not re.match("^[a-zA-Z_]+$", v):
            raise ValueError(
                f"Output key should contain only alphabets and only underscore are allowed. Got {v}"
            )
        return v

    class Config:
        arbitrary_types_allowed = True

    def worker_doc(self):
        """Returns a dictionary containing information about the worker, including its ID, role, description, and the supported actions."""
        return {
            "worker_id": self.id,
            "role": self.role,
            "description": self.instructions,
            "supported_actions": [action.cls_doc() for action in self.actions],
        }

    def provoke_thought_obs(self, observation):
        thoughts = dedent(f"""Observation: {observation}""".strip())
        return thoughts

    def should_continue(self, llm_resp: str) -> Union[bool, Optional[Dict]]:
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
        cont, final_output = self.should_continue(output)
        if cont:
            prompt = (
                "\n".join(all_thoughts_and_obs)
                + f"Based on the previous action and observation, give me the output. {final_output}"
            )
            output = self.llm.run(prompt)
            cont, final_output = self.should_continue(output)
        if cont:
            raise OpenAGIException(
                f"LLM did not produce the expected output after {self.max_iterations} iterations."
            )
        return (cont, final_output)

    def save_to_memory(self, task: Task):
        """Saves the output to the memory."""
        return self.memory.update_task(task)

    def execute_task(self, task: Task, context: Any = None) -> Any:
        """Executes the specified task."""
        logging.info(
            f"{'>'*20} Executing Task - {task.name}[{task.id}] with worker - {self.role}[{self.id}] {'<'*20}"
        )
        iteration = 1
        task_to_execute = f"{task.description}"
        worker_description = f"{self.role} - {self.instructions}"
        all_thoughts_and_obs = []

        logging.debug("Provoking initial thought observation...")
        initial_thought_provokes = self.provoke_thought_obs(None)
        
        te_vars = dict(
            task_to_execute=task_to_execute,
            worker_description=worker_description,
            supported_actions=[action.cls_doc() for action in self.actions],
            thought_provokes=initial_thought_provokes,
            output_key=self.output_key,
            context=context,
            max_iterations=self.max_iterations,
        )

        logging.debug("Generating base prompt...")
        base_prompt = WorkerAgentTaskExecution().from_template(te_vars)
        prompt = f"{base_prompt}\nThought:\nIteration: {iteration}\nActions:\n"

        logging.debug("Running LLM with prompt...")
        observations = self.llm.run(prompt)
        logging.info(f"LLM execution completed. Observations: {observations}")
        all_thoughts_and_obs.append(prompt)

        max_iters = self.max_iterations + 1
        while iteration < max_iters:
            logging.info(f"---- Iteration {iteration} ----")
            logging.debug("Checking if task should continue...")
            continue_flag, output = self.should_continue(observations)

            logging.debug("Extracting action from output...")
            action = output.get("action") if output else None
            if action:
                action = [action]

            # Save to memory
            if output:
                logging.debug("Saving task result and actions to memory...")
                task.result = observations
                task.actions = str([action.cls_doc() for action in self.actions])
                self.save_to_memory(task=task)

            if not continue_flag:
                logging.info(f"Task completed. Output: {output}")
                break

            if not action:
                logging.warning(f"No action found in the output: {output}")
                observations = f"Action: {action}\n{observations} Unable to extract action. Verify the output and try again."
                all_thoughts_and_obs.append(observations)
                iteration += 1
                continue

            if action:
                action_json = f"```json\n{output}\n```\n"
                try:
                    logging.debug("Getting action classes from JSON...")
                    actions = get_act_classes_from_json(action)
                    logging.info(
                        f"Extracted actions: {[act_cls.__name__ for act_cls, _ in actions]}"
                    )
                except KeyError as e:
                    if "cls" in e or "module" in e or "kls" in e:
                        observations = f"Action: {action_json}\n{observations}"
                        all_thoughts_and_obs.append(action_json)
                        all_thoughts_and_obs.append(observations)
                        iteration += 1
                        continue
                    else:
                        raise e

                for act_cls, params in actions:
                    params["memory"] = self.memory
                    params["llm"] = self.llm
                    try:
                        logging.debug(f"Running action: {act_cls.__name__}...")
                        res = run_action(action_cls=act_cls, **params)
                        logging.info(f"Action '{act_cls.__name__}' completed. Result: {res}")
                    except Exception as e:
                        logging.error(f"Error running action: {e}")
                        observations = f"Action: {action_json}\n{observations}. {e} Try to fix the error and try again. Ignore if already tried more than twice"
                        all_thoughts_and_obs.append(action_json)
                        all_thoughts_and_obs.append(observations)
                        iteration += 1
                        continue

                    observation_prompt = f"Observation: {res}\n"
                    all_thoughts_and_obs.append(action_json)
                    all_thoughts_and_obs.append(observation_prompt)
                    observations = res

                logging.debug("Provoking thought observation...")
                thought_prompt = self.provoke_thought_obs(observations)
                all_thoughts_and_obs.append(f"\n{thought_prompt}\nActions:\n")

                prompt = f"{base_prompt}\n" + "\n".join(all_thoughts_and_obs)
                logging.debug(f"\nSTART:{'*' * 20}\n{prompt}\n{'*' * 20}:END")
                
                pth = Path(f"{self.memory.session_id}/logs/{task.name}-{iteration}.log")
                pth.parent.mkdir(parents=True, exist_ok=True)
                
                with open(pth, "w", encoding="utf-8") as f:
                    f.write(f"{prompt}\n")
                logging.debug("Running LLM with updated prompt...")
                observations = self.llm.run(prompt)
            iteration += 1
        else:
            if iteration == self.max_iterations:
                logging.info("---- Forcing Output ----")
                if self.force_output:
                    logging.debug("Forcing output...")
                    cont, final_output = self._force_output(observations, all_thoughts_and_obs)
                    if cont:
                        raise OpenAGIException(
                            f"LLM did not produce the expected output after {iteration} iterations for task {task.name}"
                        )
                    output = final_output
                    logging.debug("Saving final task result and actions to memory...")
                    task.result = observations
                    task.actions = str([action.cls_doc() for action in self.actions])
                    self.save_to_memory(task=task)
                else:
                    raise OpenAGIException(
                        f"LLM did not produce the expected output after {iteration} iterations for task {task.name}"
                    )

        logging.info(
            f"Task Execution Completed - {task.name} with worker - {self.role}[{self.id}] in {iteration} iterations"
        )
        return output, task