from typing import Dict
from pydantic import BaseModel, Field


class BasePrompt(BaseModel):
    name: str = Field(default="BasePrompt", description="Name of the prompt.")
    description: str = Field(
        default="BasePrompt class to be used by other actions that get created.",
        description="Description of the prompt.",
    )
    base_prompt: str = Field(default_factory=str, description="Base prompt to be used.")

    def get_prompt(self):
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def prompt_variables(cls):
        return {field_name: field.description for field_name, field in cls.model_fields.items()}

    @classmethod
    def from_template(cls, variables: Dict):
        x = cls(**variables)
        for k, v in variables.items():
            placeholder = "{" + f"{k}" + "}"
            x.base_prompt = x.base_prompt.replace(placeholder, f"{v}")
        # return x.base_prompt.format(**variables)
        return x.base_prompt
