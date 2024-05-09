from typing import Any, Dict
from openagi.actions.base import BaseAction
from pydantic import Field


class HumanCLIInput(BaseAction):
    query: str = Field(..., description="Query to ask the user")

    def execute(self):
        response = input(self.query)
        return response
