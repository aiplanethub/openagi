from typing import Any, Optional
from pydantic import BaseModel, Field
from openagi.llms.base import LLMBaseModel
from openagi.tools.base import BaseTool


class Worker(BaseModel):
    role: str = Field(..., description="Role of the worker")
    backstory: Optional[str] = Field(
        default=None, description="Backstory for the worker"
    )
    tools: Optional[BaseTool] = Field(
        default_factory=[], description="Tools available for Worker"
    )
    llm: Optional[LLMBaseModel] = Field(
        description="LLM Model to be used.",
    )
    st_memory: Optional[Any] = None
