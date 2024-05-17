from pydantic import BaseModel, ConfigDict, Field


class BaseStorage(BaseModel):
    """Base Storage class to be inherited by other storages, providing basic functionality and structure."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(title="BaseStorage", description="Name of the Storage.")

    def save_document(self):
        """Save documents to the with metadata."""
        raise NotImplementedError("Subclasses must implement this method.")

    def update_document(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def delete_document(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def query_documents(self):
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def from_kwargs(cls, **kwargs):
        raise NotImplementedError("Subclasses must implement this method.")
