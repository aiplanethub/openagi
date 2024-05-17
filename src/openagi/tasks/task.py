from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: str = Field(default=uuid4().hex)
    name: str = Field(..., description="Name of task being.")
    description: str = Field(..., description="Description of the individual task.")
    result: Optional[str] = Field(..., default_factory=str, description="Result of the task.")

    @property
    def is_done(self):
        return bool(self.result)

    def set_result(self, result):
        self.result = result
