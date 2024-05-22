from pydantic import Field
from openagi.actions.base import BaseAction



class SummarizerAction(BaseAction):
    """Summarizer Action"""

    criteria: str = Field(
        ...,
        description="Criteria in which the data should be compressed/summarized without loosing any key information",
    )

    def execute(self):
        return self.llm.run(
            f"Compress/Summarize the below content based on the below criteria.\nCRITERIA:\n{self.criteria}\n\nCONTENT:\n{self.previous_action}"
        )
