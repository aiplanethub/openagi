from pydantic import Field

from openagi.actions.base import BaseAction


class HumanCLIInput(BaseAction):
    ques_prompt: str = Field(
        default="Do you think this task is progressing as expected [y/n] or [yes/no]: ",
        description="question to be asked to human",
    )

    def execute(self):
        response = input(f"Agent: {self.ques_prompt}\nYou: ")
        return response
