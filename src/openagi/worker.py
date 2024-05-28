from typing import Any, List, Optional

from pydantic import BaseModel, Field

from openagi.llms.base import LLMBaseModel
from openagi.memory.memory import Memory
from openagi.utils.helper import get_default_id


class Worker(BaseModel):
    id: str = Field(default_factory=get_default_id)
    role: str
    description: Optional[str]
    llm: Optional[LLMBaseModel] = Field(description="LLM Model to be used.")
    memory: Optional[Memory] = Field(
        default_factory=list, description="Memory to be used.", exclude=True
    )
    actions: Optional[List[Any]] = Field(
        description="Actions that the Worker supports", default_factory=list
    )
    max_steps: int = Field(
        default=20, description="Maximum number of steps to achieve the objective."
    )

    class Config:
        arbitrary_types_allowed = True

    def worker_doc(self):
        """
        Returns a dictionary containing information about the worker, including its ID, role, description, and the supported actions.
        """
        return {
            "worker_id": self.id,
            "role": self.role,
            "description": self.description,
            "supported_actions": [action.cls_doc() for action in self.actions],
        }
