from typing import Any, Dict
from openagi.actions.base import BaseAction
from pydantic import Field


class HumanCLIInput(BaseAction):
    param_docs: Dict = Field(default={"query": "Query to ask the human."})

    def execute(self, query: str):
        response = input(query)
        return response
