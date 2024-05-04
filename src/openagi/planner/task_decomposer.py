import json
import re
from typing import Dict, Optional, Union

from pydantic import Field

from openagi.actions.base import BaseAction
from openagi.actions.human_input import HumanCLIInput
from openagi.llms.azure import LLMBaseModel
from openagi.planner.base import BasePlanner
from openagi.prompts.base import BasePrompt
from openagi.prompts.custom_prompt import TaskCreator


class TaskPlanner(BasePlanner):
    human_intervene: bool = Field(
        default=True, description="If human internvention is required or not."
    )
    actions: Optional[BaseAction] = Field(
        default=HumanCLIInput,
        description="If `human_intervene` is enabled, which action to be performed.",
    )
    prompt: BasePrompt = Field(
        default=TaskCreator(), description="Prompt to be used"
    )  # TODO: Add default planner
    llm: Optional[LLMBaseModel] = Field(
        default=None, description="LLM Model to be used"
    )

    def _extract_task_from_response(self, llm_response: str) -> Union[str, None]:
        def get_last_json(string):
            """
            Extracts the last JSON element from a string that might contain multiple JSON objects by iterating from the end.

            Args:
                string: The string containing potential JSON data.

            Returns:
                The last JSON element as a parsed object, or None if no valid JSON is found.
            """
            # Brute force approach: try to parse each substring from the back
            for i in range(len(string), 0, -1):
                for j in range(0, i):
                    substring = string[j:i]
                    try:
                        # Try to parse the substring as JSON
                        potential_json = json.loads(substring)
                        # If parsing is successful, return the JSON object
                        return potential_json
                    except json.JSONDecodeError:
                        continue  # If not successful, continue trying other substrings

            return None  # Return None if no valid JSON is found after all attempts

        return get_last_json(llm_response)

    def _should_clarify(self, response: str) -> bool:
        # TODO: Setup a way for human intervention
        return False

    def plan(self, query: str) -> Dict:
        prompt: str = self.prompt.base_prompt
        prompt = prompt.replace("{objective}", query)
        resp = self.llm.run(prompt)
        while self.human_intervene and self._should_clarify(resp):
            pass
        tasks = self._extract_task_from_response(llm_response=resp)
        return tasks
