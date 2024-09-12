from pydantic import BaseModel

class SessionDict(BaseModel):
    session_id: str
    query: str
    description: str
    answer: str
    plan: str
    plan_feedback: str = "NA"
    ans_feedback: str = "NA"

    @classmethod
    def from_dict(cls, input_dict: dict):
        """Class method to initialize an instance from a dictionary."""
        return cls(**input_dict)


