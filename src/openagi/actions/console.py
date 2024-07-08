from pprint import pprint

from pydantic import Field

from openagi.actions.base import BaseAction


class ConsolePrint(BaseAction):
    content: str = Field(
        ...,
        description="The content/data passed will be logged into the console using pprint.pprint() module.",
    )

    def execute(self):
        pprint(self.content)
        return self.content
