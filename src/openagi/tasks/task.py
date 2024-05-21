from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


def get_default_id():
    return uuid4().hex


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

    @property
    def is_done(self):
        return bool(self.result)

    def set_result(self, result):
        self.result = result
