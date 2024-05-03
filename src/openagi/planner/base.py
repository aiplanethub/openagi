from typing import Optional

from pydantic import BaseModel, Field

from openagi.actions.base import BaseAction
from openagi.prompts.base import BasePrompt


class BasePlanner(BaseModel):
    human_intervene: bool = Field(
        default_factory=True,
        description="If human internvention is required or not.",
    )
    actions: Optional[BaseAction] = Field(
        description="If `human_intervene` is enabled, which action to be performed.",
    )
    prompt: BasePrompt = Field(description="Prompt to be used")

    @staticmethod
    def _parse_task_from_response(llm_response: str):
        raise

    def _should_ask_human(self, response: str):
        """Ask clarifying questions"""

    def plan(self):
        raise NotImplementedError("Subclasses must implement this method.")
