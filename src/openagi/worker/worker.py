from typing import Any, List, Optional

from pydantic import BaseModel, Field

from openagi.llms.base import LLMBaseModel
from openagi.memory.memory import Memory


class Worker(BaseModel):
    role: str
    backstory: Optional[str]
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
