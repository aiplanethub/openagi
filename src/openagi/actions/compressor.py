from typing import Any
from pydantic import Field
from openagi.actions.base import BaseAction
from openagi.prompts.summarizer import SummarizerPrompt


class SummarizerAction(BaseAction):
    """Summarizer Action"""

    past_messages: Any = Field(
        ...,
        description="Messages/Data to be summarized",
    )

    def execute(self):
        summarizer: str = SummarizerPrompt.from_template({"past_messages": self.past_messages})
        return self.llm.run(summarizer)
