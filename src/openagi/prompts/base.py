from typing import Dict
from pydantic import BaseModel, Field


class BasePrompt(BaseModel):
    name: str = Field(default="BasePrompt", description="Name of the prompt.")
    description: str = Field(
        default="BasePrompt class to be used by other actions that get created.",
        description="Description of the prompt.",
    )
    param_docs: dict = Field(
        default={},
        description="A dictionary to explain the parameters that the promp supports.",
    )
    base_prompt: str = Field(...)

    def get_prompt(self):
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def from_template(cls, variables: Dict):
        return cls.base_prompt.format(**variables)
