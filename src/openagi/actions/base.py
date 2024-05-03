from typing import Any, Dict
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod


class BaseAction(ABC):
    """Base Actions class to be inherited by other actions, providing basic functionality and structure."""

    name: str = Field(default="BaseAction", description="Name of the action.")
    description: str = Field(
        default="Base Action class to be used by other actions that get created.",
        description="Description of the action.",
    )
    param_docs: dict = Field(
        default_factory={},
        description="A dictionary to explain the input parameters to the execute",
    )

    @abstractmethod
    def execute(self):
        """Executes the action"""
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def docs(cls) -> Dict[str, str]:
        """Returns a dictionary documenting the parameters required for the execute method,
        based on the param fields.
        """
        return cls.param_docs
