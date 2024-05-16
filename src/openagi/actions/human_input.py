from typing import Any, Dict
from openagi.actions.base import BaseAction
from pydantic import Field


class HumanCLIInput(BaseAction):
    ques_prompt : str = Field(... , default="Do you think this task is being executed as expected [y/n] or [yes/no]: " , description='question to be asked to human')

    def execute(self):
        response = input(self.ques_prompt)
        return response
