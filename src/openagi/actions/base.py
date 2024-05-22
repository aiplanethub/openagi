from typing import Any, Optional

from pydantic import BaseModel, Field

from openagi.llms.base import LLMBaseModel
from openagi.memory.memory import Memory


class BaseAction(BaseModel):
    """Base Actions class to be inherited by other actions, providing basic functionality and structure."""

    session_id: int = Field(default_factory=str, description="SessionID of the current run.")

    previous_action: Optional[Any] = Field(
        default=None,
        description="Observation or Result of the previous action that might needed to run the current action.",
    )
    llm: Optional[LLMBaseModel] = Field(description="LLM Model to be used.", default_factory=str)
    memory: Memory = Field(
        ...,
        description="Memory that stores the results of the earlier tasks executed for the current objective.",
    )

    def execute(self):
        """Executes the action"""
        raise NotImplementedError("Subclasses must implement this method.")

    @staticmethod
    def default_exclude_doc_fields():
        return ["llm", "memory", "session_id", "name", "description"]

    @classmethod
    def cls_doc(cls):
        return {
            "cls": {
                "kls": cls.__name__,
                "module": cls.__module__,
                "doc": cls.__doc__,
            },
            "params": {
                field_name: field.description
                for field_name, field in cls.model_fields.items()
                if field_name not in cls.default_exclude_doc_fields()
            },
        }
