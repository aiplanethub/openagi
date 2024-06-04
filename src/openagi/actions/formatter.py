from typing import Any

from pydantic import Field

from openagi.actions.base import BaseAction


class FormatterAction(BaseAction):
    """Content Formatter Action"""

    content: Any = Field(..., description="Data/Content to be formatted.")
    format_type: str = Field(
        default="markdown",
        description="Type to which the content will be formatted to. It will be modified to the supported formats and returned. Supported Formats - markdown/plan-text",
    )

    def execute(self):
        return self.llm.run(
            f"Format and return the below response in {self.format_type} format without removing any content. You can rephrase if required.\n{self.content}"
        )
