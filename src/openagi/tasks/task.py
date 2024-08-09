from typing import Optional, Dict, Any

from pydantic import BaseModel, Field

from openagi.utils.helper import get_default_id


class Task(BaseModel):
    id: str = Field(default_factory=get_default_id)
    name: str = Field(..., description="Name of task being.")
    description: str = Field(..., description="Description of the individual task.")
    result: Optional[str] = Field(..., default_factory=str, description="Result of the task.")
    actions: Optional[str] = Field(
        ...,
        default_factory=str,
        description="Actions undertaken to acheieve the task. Usually set after the current task is executed.",
    )
    worker_id: Optional[str] = Field(
        description="WorkerId associated to accomplish the given task using supported actions.",
        default_factory=str,
    )
    worker_config: Optional[Dict[str, Any]] = Field(
        description="Stores workers configuration values"
    )
    @property
    def is_done(self):
        return bool(self.result)

    def set_result(self, result):
        self.result = result
