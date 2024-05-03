from uuid import UUID, uuid4

from pydantic import Field


class Task:
    id: UUID = Field(default_factory=uuid4)
    description: str = Field(..., description="Description of the individual task.")
    result: str = Field(..., description="Result of the task.")

    @property
    def is_completed(self):
        return bool(self.result)
