from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod


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
    previous_obs: Optional[Any] = None

    @abstractmethod
    def execute(self):
        """Executes the action"""
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def cls_doc(cls):
        {
            "cls": {
                "kls": cls.__class__,
                "module": cls.__module__,
            },
            "params": cls.param_docs,
        }
