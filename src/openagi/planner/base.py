from typing import Dict, Optional, List

from pydantic import BaseModel, Field

from openagi.actions.base import BaseAction
from openagi.prompts.base import BasePrompt


class BasePlanner(BaseModel):
    human_intervene: bool = Field(
        default=True,
        description="If human internvention is required or not.",
    )
    input_action: Optional[BaseAction] = Field(
        description="If `human_intervene` is enabled, which action to be performed.",
    )
    prompt: BasePrompt = Field(description="Prompt to be used")

    def _extract_task_from_response(llm_response: str):
        raise

    def human_clarification(self, response: str) -> bool:
        """Whether to Ask clarifying questions"""
        raise NotImplementedError("Subclasses must implement this method.")

    def plan(self, query: str, description: str, long_term_context: str, supported_actions: List[BaseAction],*args,
        **kwargs,) -> Dict:
        raise NotImplementedError("Subclasses must implement this method.")
