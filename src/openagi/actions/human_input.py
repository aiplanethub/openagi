from typing import Any
from openagi.actions.base import BaseAction, ActionConfig
from pydantic import Field


class HumanCLIInputActionConfig(ActionConfig):
    query: str = Field(
        description="Query to be included while taking input from the Humans via CLI.",
        strict=True,
    )


class HumanCLIInput(BaseAction):

    def execute(self, config: HumanCLIInputActionConfig):
        response = input(config.query)
        return response
