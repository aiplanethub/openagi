import logging
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
    role: str
    description: Optional[str]
    llm: Optional[LLMBaseModel] = Field(description="LLM Model to be used.", default=None)
    memory: Optional[Memory] = Field(
        default_factory=list, description="Memory to be used.", exclude=True
    )
    actions: Optional[List[Any]] = Field(
        description="Actions that the Worker supports", default_factory=list
    )
    max_iterations: int = Field(
        default=20, description="Maximum number of steps to achieve the objective."
    )
    output_key: str = Field(
        default="final_output", description="Key to be used to store the output."
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
        """
        Returns a dictionary containing information about the worker, including its ID, role, description, and the supported actions.
        """
        return {
            "worker_id": self.id,
            "role": self.role,
            "description": self.description,
            "supported_actions": [action.cls_doc() for action in self.actions],
        }

    @staticmethod
    def get_last_final_output(text):
        """
        Finds the content of the last <r_failure> tag in the given text.

        Args:
            text (str): The text to search for the <r_failure> tag.

        Returns:
            str or None: The content of the last <r_failure> tag, or None if no matches are found.
        """
        pattern = r"<r_failure>(.*?)</r_failure>"
        matches = list(re.finditer(pattern, text, re.DOTALL))
        if matches:
            last_match = matches[-1]
            return last_match.group(1)
        else:
            return None

    def provoke_thought_obs(
        self,
        observation,
    ):
        thoughts = dedent(
            f"""
        Observation: {observation}
        """.strip()
        )
        return thoughts

    def should_continue(self, llm_resp: str) -> Union[bool, Optional[Dict]]:
        print(f"LLM Response: {llm_resp}")
        output: Dict = get_last_json(llm_resp)
        output_key_exists = bool(output and output.get(self.output_key))
        return (not output_key_exists, output)

    def _force_output(
        self, llm_resp: str, all_thoughts_and_obs: List[str]
    ) -> Union[bool, Optional[str]]:
        """Force the output once the max iterations are reached.
        Make an llm call with a prompt suffixed, that will force the output.
        """
        prompt = (
            "\n".join(all_thoughts_and_obs)
            + "Based on the previous action and observation, give me the output."
        )
        output = self.llm.run(prompt)

        # Extract the output
        cont, final_output = self.get_last_final_output(output)

        # If cont is True, rerun the llm call with the prompt suffixed with the output.
        if cont:
            prompt = (
                "\n".join(all_thoughts_and_obs)
                + f"Based on the previous action and observation, give me the output. {final_output}"
            )
            output = self.llm.run(prompt)
            cont, final_output = self.get_last_final_output(output)
        if cont:
            raise OpenAGIException(
                f"LLM did not produce the expected output after {self.max_iterations} iterations."
            )
        return (cont, final_output)

    def execute_task(self, task: Task, context: Any) -> Any:
        """
        Executes the specified task.
        """
        logging.info(
            f"{'>'*50} Executing Task - {task.name} with worker - {self.role}[{self.id}] {'<'*50}"
        )
        iteration = 1
        task_to_execute = f"{task.description}"
        worker_description = f"{self.role} - {self.description}"
        all_thoughts_and_obs = []

        # Initial setup for the first LLM run
        initial_thought_provokes = self.provoke_thought_obs(None)
        te_vars = dict(
            task_to_execute=task_to_execute,
            worker_description=worker_description,
            supported_actions=[action.cls_doc() for action in self.actions],
            thought_provokes=initial_thought_provokes,
            output_key=self.output_key,
            context=context,
        )

        base_prompt = WorkerAgentTaskExecution().from_template(te_vars)
        prompt = f"{base_prompt}\nThought:\nActions:\n"

        observations = self.llm.run(prompt)
        all_thoughts_and_obs.append(prompt)

        max_iters = self.max_iterations + 1
        while iteration < max_iters:
            logging.info(f"---- Iteration {iteration} ----")
            continue_flag, output = self.should_continue(observations)
            if not continue_flag:
                logging.info(f"Output: {output}")
                break

            action = output.get("action") if output else None
            if action:
                actions = get_act_classes_from_json([action])
                for act_cls, params in actions:
                    # Include memory and llm in the params for the action
                    params["memory"] = self.memory
                    params["llm"] = self.llm
                    res = run_action(action_cls=act_cls, **params)
                    logging.info(f"Action Result -- {res}")

                    # Append the action and observation to the prompt
                    action_json = f"```json\n{action}\n```\n"
                    observation_prompt = f"Observation: {res}\n"
                    all_thoughts_and_obs.append(action_json)
                    all_thoughts_and_obs.append(observation_prompt)
                    observations = res

                # Create a new thought prompt based on the latest observation
                thought_prompt = self.provoke_thought_obs(observations)
                all_thoughts_and_obs.append(f"\n{thought_prompt}\nActions:\n")

                # Update the prompt with all previous thoughts and observations
                prompt = f"{base_prompt}\n" + "\n".join(all_thoughts_and_obs)
                logging.debug(f"\nSTART:{'*' * 20}\n{prompt}\n{'*' * 20}:END")
                observations = self.llm.run(prompt)
            iteration += 1
        else:
            if iteration == self.max_iterations:
                logging.info("---- Forcing Output ----")
                if self.force_output:
                    cont, final_output = self._force_output(observations, all_thoughts_and_obs)
                    if cont:
                        raise OpenAGIException(
                            f"LLM did not produce the expected output after {iteration} iterations for task {task.name}"
                        )
                    output = final_output
                else:
                    raise OpenAGIException(
                        f"LLM did not produce the expected output after {iteration} iterations for task {task.name}"
                    )

        logging.info(
            f"Task Execution Completed - {task.name} with worker - {self.role}[{self.id}] in {iteration} iterations"
        )

        return output
