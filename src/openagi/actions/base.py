from typing import Any, Optional
from pydantic import BaseModel, Field
from abc import abstractmethod


class BaseAction(BaseModel):
    """Base Actions class to be inherited by other actions, providing basic functionality and structure."""

    name: str = Field(default="BaseAction", description="Name of the action.")
    description: str = Field(
        default="Base Action class to be used by other actions that get created.",
        description="Description of the action.",
    )
    param_docs: dict = Field(
        default_factory=dict,
        description="A dictionary to explain the input parameters to the execute",
    )
    previous_task: Optional[Any] = Field(
        default=None,
        description="Observation or Result of the previous action that might needed to run the current action.",
    )

    @abstractmethod
    def execute(self):
        """Executes the action"""
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def cls_doc(cls):
        return {
            "cls": {
                "kls": cls.__name__,
                "module": cls.__module__,
            },
            "params": {
                field_name: field.description for field_name, field in cls.model_fields.items()
            },
        }
