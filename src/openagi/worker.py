import logging
import re
from textwrap import dedent
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator

from openagi.actions.utils import run_action
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
        task_to_execute,
        supported_actions,
        observation,
    ):
        thoughts = dedent(
            f"""
        Question: {task_to_execute}
        supported_actions: {supported_actions}
        Observation: {observation}
        """.strip()
        )
        return thoughts

    def should_continue(self, llm_resp: str) -> Union[bool, Optional[str]]:
        output: Dict = get_last_json(llm_resp)
        output_key_exists = True if output.get(self.output_key) else False
        return (not output_key_exists, output)

    def execute_task(self, task: Task) -> Any:
        """
        Executes the specified task.
        """
        logging.info(f"Executing Task - {task.name} with worker - {self.role}[{self.id}]")
        iteration = 1
        task_to_execute = f"{task.description}"
        worker_description = f"{self.role} - {self.description}"
        supported_actions = [action.cls_doc() for action in self.actions]
        observations = None
        all_thoughts_and_obs = []

        # Initial setup for the first LLM run
        initial_thought_provokes = self.provoke_thought_obs(
            task_to_execute,
            supported_actions,
            observations,
        )
        te_vars = dict(
            worker_description=worker_description,
            thought_provokes=initial_thought_provokes,
            output_key=self.output_key,
            observations=observations,
        )

        prompt = WorkerAgentTaskExecution()
        prompt = prompt.from_template(te_vars)
        observations = self.llm.run(prompt)

        prev_action_result = None

        while iteration < self.max_iterations:
            continue_flag, output = self.should_continue(observations)
            if not continue_flag:
                logging.info(f"Output -- {output}")
                break
            logging.info(f"Output -- {output}")
            action = output.get("action")
            logging.info(f"Action -- {action}")

            if action:
                actions = get_act_classes_from_json([action])
                for act_cls, params in actions:
                    params["previous_action"] = prev_action_result if prev_action_result else None
                    # Include memory and llm in the params for the action
                    params["memory"] = self.memory
                    params["llm"] = self.llm
                    res = run_action(action_cls=act_cls, **params)
                    logging.info(f"Action Result -- {res}")
                    observations = res
                    prev_action_result = res  # Update prev_action_result for the next iteration

                # Append current thoughts and observations to all_thoughts_and_obs
                all_thoughts_and_obs.append(te_vars["thought_provokes"])
                all_thoughts_and_obs.append(f"Action taken: {action}")
                all_thoughts_and_obs.append(f"Observation: {observations}")

                # Generate thought prompt for the next iteration
                thought_prompt = self.provoke_thought_obs(
                    task_to_execute,
                    supported_actions,
                    observations,
                )
                all_thoughts_and_obs.append(thought_prompt)

                # Update te_vars with the new thought provokes including history
                te_vars["thought_provokes"] = "\n".join(all_thoughts_and_obs)
                prompt = WorkerAgentTaskExecution()
                prompt = prompt.from_template(te_vars)
                logging.info(f"\n{'*' * 100}\n{prompt}\n{'*' * 100}")
                observations = self.llm.run(prompt)

            else:
                logging.info("Action is None. Terminating the execution.")
                break

            iteration += 1

        logging.info(
            f"Task Execution Completed - {task.name} with worker - {self.role}[{self.id}] in {iteration} iterations"
        )

        return output
