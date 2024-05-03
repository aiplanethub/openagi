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

    def _extract_task_from_response(llm_response: str):
        raise

    def _should_clarify(self, response: str) -> bool:
        """Whether to Ask clarifying questions"""
        raise NotImplementedError("Subclasses must implement this method.")

    def plan(self):
        raise NotImplementedError("Subclasses must implement this method.")
