import json
import logging
import re
from typing import Dict, List, Optional, Union

from pydantic import Field

from openagi.actions.base import BaseAction
from openagi.actions.human_input import HumanCLIInput
from openagi.exception import LLMResponseError
from openagi.llms.azure import LLMBaseModel
from openagi.planner.base import BasePlanner
from openagi.prompts.base import BasePrompt
from openagi.prompts.constants import CLARIFIYING_VARS
from openagi.prompts.task_creator import MultiAgentTaskCreator, SingleAgentTaskCreator
from openagi.utils.extraction import get_last_json
from openagi.worker import Worker


class TaskPlanner(BasePlanner):
    human_intervene: bool = Field(
        default=True, description="If human internvention is required or not."
    )
    input_action: Optional[BaseAction] = Field(
        default=HumanCLIInput,
        description="If `human_intervene` is enabled, which action to be performed.",
    )
    prompt: Optional[BasePrompt] = Field(
        description="Prompt to be used",
        default_factory=str,
    )
    workers: Optional[List[Worker]] = Field(
        default=None, description="List of workers to be used."
    )
    llm: Optional[LLMBaseModel] = Field(default=None, description="LLM Model to be used")
    retry_threshold: int = Field(
        default=3, description="Number of times to retry the task if it fails."
    )

    def get_prompt(self) -> None:
        if not self.prompt:
            if self.workers:
                self.prompt = SingleAgentTaskCreator()
            else:
                self.prompt = MultiAgentTaskCreator(workers=self.workers)
        logging.info(f"Using prompt: {self.prompt.__class__.__name__}")
        return self.prompt

    def _extract_task_from_response(self, llm_response: str) -> Union[str, None]:
        """
        Extracts the last JSON object from the given LLM response string.

        Args:
            llm_response (str): The LLM response string to extract the JSON from.

        Returns:
            Union[str, None]: The last JSON object extracted from the response, or None if no JSON was found.
        """
        return get_last_json(llm_response)

    def _should_clarify(self, query: Optional[str]) -> bool:
        """
        Determines whether the given query should be clarified.

        Returns:
            bool: True if the query should be clarified, False otherwise.
        """
        if query and len(query) > 0:
            return True
        return False

    def extract_ques_and_task(self, ques_prompt):
        """
        Extracts the question to be asked to the human and the remaining task from the given question prompt.

        Args:
            ques_prompt (str): The question prompt containing the question to be asked to the human and the remaining task.

        Returns:
            Tuple[str, str]: The task and the question to be asked to the human.
        """
        start = CLARIFIYING_VARS["start"]
        end = CLARIFIYING_VARS["end"]
        # pattern to find question to be asked to human
        regex = rf"{start}(.*?){end}"

        # Find all matches in the text
        matches = re.findall(regex, ques_prompt)

        # remove <clarify from human>...</clarify from human> part from the prompt
        task = re.sub(regex, "", ques_prompt)
        if not matches:
            return None, None

        question = matches[-1]
        if question and question.strip():
            f"OpenAGI: {question}\nYou: "
        return task, question

    def plan(
        self,
        query: str,
        description: str,
        supported_actions: List[Dict],
        *args,
        **kwargs,
    ) -> Dict:
        """
        Plans a task by querying a large language model (LLM) and extracting the resulting tasks.

        Args:
            query (str): The objective or query to plan for.
            description (str): A description of the task or problem to solve.
            supported_actions (List[Dict]): A list of dictionaries describing the actions that can be taken to solve the task.
            *args: Additional arguments to pass to the LLM.
            **kwargs: Additional keyword arguments to pass to the LLM.

        Returns:
            Dict: A dictionary containing the planned tasks.
        """
        planner_vars = dict(
            objective=query,
            task_descriptions=description,
            supported_actions=supported_actions,
            *args,
            **kwargs,
        )
        prompt_template = self.get_prompt()
        prompt: str = prompt_template.from_template(variables=planner_vars)

        print(f"\n\nOpenAGI: {prompt}\n\n")
        resp = self.llm.run(prompt)
        prompt, ques_to_human = self.extract_ques_and_task(resp)

        while self.human_intervene and self._should_clarify(ques_to_human):
            human_intervene = self.input_action(ques_prompt=ques_to_human)
            human_resp = human_intervene.execute()
            prompt = f"{prompt}\n{ques_to_human}\n{human_resp}"
            resp = self.llm.run(prompt)
            prompt, ques_to_human = self.extract_ques_and_task(resp)

        tasks = self._extract_task_with_retry(resp, prompt)

        if not tasks:
            raise LLMResponseError("No tasks found in the Planner response.")

        print(f"\n\nTasks: {tasks}\n\n")
        return tasks

    def _extract_task_with_retry(self, llm_response: str, prompt: str) -> Dict:
        """
        Attempts to extract a task from the given LLM response, retrying up to a specified threshold if the response is not valid JSON.

        Args:
            llm_response (str): The response from the language model.
            prompt (str): The prompt used to generate the LLM response.

        Returns:
            Dict: The extracted task, or raises an exception if the task could not be extracted after multiple retries.

        Raises:
            LLMResponseError: If the task could not be extracted after multiple retries.
        """
        retries = 0
        while retries < self.retry_threshold:
            try:
                return self._extract_task_from_response(llm_response=llm_response)
            except json.JSONDecodeError:
                retries += 1
                logging.info(
                    f"Retrying task extraction {retries}/{self.retry_threshold} due to an error parsing the JSON response."
                )
                llm_response = self.llm.run(prompt)

        raise LLMResponseError("Failed to extract tasks after multiple retries.")
