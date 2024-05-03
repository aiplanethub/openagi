from typing import Optional

from pydantic import Field

from openagi.actions.base import BaseAction
from openagi.actions.human_input import HumanCLIInput
from openagi.planner.base import BasePlanner
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

    @staticmethod
    def _parse_task_from_response(llm_response: str):
        raise

    def plan(self, query: str):
        return super().plan()
