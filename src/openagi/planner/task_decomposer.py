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
from openagi.prompts.task_clarification import TaskClarifier
#from openagi.prompts.task_creator import MultiAgentTaskCreator, SingleAgentTaskCreator
from openagi.prompts.task_creator import TaskCreator
from openagi.prompts.self_assign import RoleSelfAssign
from openagi.worker import Worker
from openagi.utils.extraction import get_last_json,force_json_output

class TaskPlanner(BasePlanner):
    human_intervene: bool = Field(
        default=False, description="If human internvention is required or not."
    )
    input_action: Optional[BaseAction] = Field(
        default=HumanCLIInput,
        description="If `human_intervene` is enabled, which action to be performed.",
    )
    prompt: Optional[BasePrompt] = Field(
        description="Prompt to be used",
        default=None,
    )
    #workers: Optional[List[Worker]] = Field(
    #    default=None,
    #    description="List of workers to be used.",
    #)
    llm: Optional[LLMBaseModel] = Field(default=None, description="LLM Model to be used")
    
    retry_threshold: int = Field(
        default=3, description="Number of times to retry the task if it fails."
    )
    autonomous: bool = Field(
        default=True, description="Autonomous will self assign role and instructions and divide it among the workers"
    )

    """
    def get_prompt(self) -> None:
        if not self.prompt:
            if self.workers:
                self.prompt = MultiAgentTaskCreator(workers=self.workers)
            else:
                self.prompt = SingleAgentTaskCreator()
        logging.info(f"Using prompt: {self.prompt.__class__.__name__}")
        return self.prompt
    """
    def get_prompt(self) -> None:
        if not self.prompt:
            if self.autonomous:
                self.prompt = TaskCreator()
            else:
                self.prompt = RoleSelfAssign()
        
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

    def human_clarification(self, planner_vars) -> Dict:
        """
        Handles the human clarification process during task planning.

        This method is responsible for interacting with the human user to clarify any
        ambiguities or missing information in the task planning process. It uses a
        TaskClarifier prompt to generate a question for the human, and then waits for
        the human's response to update the planner variables accordingly.

        The method will retry the clarification process up to `self.retry_threshold`
        times before giving up and returning the current planner variables.

        Args:
            planner_vars (Dict): The current planner variables, which may be updated
                based on the human's response.

        Returns:
            Dict: The updated planner variables after the human clarification process.
        """

        clarifier_prompt = TaskClarifier.from_template(
            variables=planner_vars,
        )
        human_intervene = self.human_intervene
        max_tries = self.retry_threshold

        while human_intervene and max_tries > 0:
            max_tries -= 1

            resp = self.llm.run(clarifier_prompt)

            # extract json from response
            resp = get_last_json(resp, llm=self.llm)

            question_to_ask = resp.get("question", "")
            question_to_ask = question_to_ask.strip()

            if question_to_ask:
                human_intervene = self.input_action(ques_prompt=question_to_ask)
                human_resp = human_intervene.execute()
                planner_vars["objective"] = f"{planner_vars['objective']} {human_resp}"
            else:
                return planner_vars

        return planner_vars

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

        if self.human_intervene:
            planner_vars = self.human_clarification(planner_vars)

        
        prompt_template = self.get_prompt()

        prompt: str = prompt_template.from_template(variables=planner_vars)
        resp = self.llm.run(prompt)

        tasks = self._extract_task_with_retry(resp, prompt)

        if not tasks:
            raise LLMResponseError("No tasks found in the Planner response.")
    
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
        try:
            resp = self._extract_task_from_response(llm_response=llm_response)
            logging.debug(f"\n\nExtracted Task: {resp}\n\n")
            return resp
        except json.JSONDecodeError:
            logging.info(
                f"JSON parsing failed. Forcing the output..."
            )
            llm_response = force_json_output(resp_txt=resp,llm=self.llm)

        
        raise LLMResponseError("Failed to extract tasks after multiple retries.")