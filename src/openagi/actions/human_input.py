from typing import Any, Dict
from openagi.actions.base import BaseAction
from pydantic import Field


class HumanCLIInput(BaseAction):
    query: str = Field(..., description="Query to ask the user")

    def execute(self):
        ques_prompt = "Do you think this task is being executed as expected [y/n] or [yes/no]: "
        feedback = ''
        response = input(ques_prompt + self.query)

        if response not in ['y' , 'n' , 'yes' , 'no' , 'NO' ,'YES' , 'No' , 'Yes']:
            print("Please provide a valide answer something like : ('y' , 'n' , 'yes' , 'no' , 'NO' ,'YES' , 'No' , 'Yes')")
            response , feedback = self.execute()

        if response=='n':
            feedback = input('Do provide your feedback on what you think is needed to be modified: ')

        return response , feedback
