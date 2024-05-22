import logging
from openagi.actions.base import BaseAction
from pydantic import Field
from pprint import pprint


class ConsolePrint(BaseAction):
    content: str = Field(
        ...,
        description="The content/data passed will be logged into the console using pprint.pprint() module.",
    )

    def execute(self):
        pprint(self.content)
        return self.content
