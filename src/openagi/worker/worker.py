from typing import Optional
from pydantic import BaseModel, Field
from openagi.llms.base import LLMBaseModel
from openagi.actions.base import BaseAction


class Worker(BaseModel):
    description: str = Field(..., description="Capabilities of the Worker")
    
    actions: Optional[BaseAction] = Field(
        default_factory=[], description="Tools available for Worker"
    )
    llm: Optional[LLMBaseModel] = Field(
        description="LLM Model to be used.",
    )

    def __init__(self):
        super().__init__()
        