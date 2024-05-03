import json
import re
from typing import Optional, Union

from pydantic import Field

from openagi.actions.base import BaseAction
from openagi.actions.human_input import HumanCLIInput
from openagi.planner.base import BasePlanner
from openagi.llms.azure import LLMBaseModel
from openagi.prompts.base import BasePrompt


class TaskPlanner(BasePlanner):
    human_intervene: bool = Field(
        default_factory=True, description="If human internvention is required or not."
    )
    actions: Optional[BaseAction] = Field(
        default_factory=HumanCLIInput(),
        description="If `human_intervene` is enabled, which action to be performed.",
    )
    prompt: BasePrompt = Field(
        description="Prompt to be used"
    )  # TODO: Add default planner
    llm: LLMBaseModel = Field(description="LLM Model to be used")

    def _extract_task_from_response(llm_response: str) -> Union[str, None]:
        def get_last_json(string):
            """
            Extracts the last JSON element from a string enclosed between `json` markers using regex.

            Args:
                string: The string containing the JSON data.

            Returns:
                The last JSON element as a string, or None if no valid JSON is found.
            """

            # Regular expression to find JSON blocks enclosed within ```json ``` markers
            pattern = re.compile(r"```json\s*(.+?)\s*```", re.DOTALL)

            # Find all matches
            matches = pattern.findall(string)

            if not matches:
                return None

            # Try to parse the last match as JSON
            try:
                return json.loads(matches[-1])
            except json.JSONDecodeError:
                return None

        return get_last_json(llm_response)

    def _should_clarify(self, response: str) -> bool:
        return super()._should_clarify(response)

    def plan(self, query: str):
        self.prompt.format
