import logging
from openagi.actions.base import BaseAction
from pydantic import Field
from pprint import pprint


class ConsolePrint(BaseAction):
    content: str = Field(..., description="Prints to the console using pprint.pprint() module.")

    def execute(self):
        logging.info("Printing content to console...")
        pprint(self.content)
        return self.content
