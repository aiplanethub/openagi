from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field, BaseModel


class Task(BaseModel):
    id: UUID = Field(default=uuid4)
    name: str = Field(..., description="Name of task being.")
    description: str = Field(..., description="Description of the individual task.")
    result: Optional[str] = Field(..., default_factory=str, description="Result of the task.")

    @property
    def is_done(self):
        return bool(self.result)

    def set_result(self, result):
        self.result = result
