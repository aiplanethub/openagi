# VectorStore

The Vector Store provides a structured way to store, update, delete, and query documents using various storage backends. It is designed to be inherited by specific storage implementations that define the actual methods for handling data.

The storage can serve as a backend for Memory to retain the activities of the Agent Execution. The storage class will be instantiated together with the memory class.&#x20;

OpenAGI Uses ChromaDB as default storage backend for Memory.

When the Base Storage Class is inherited, it will have basic methods implemented as below:

```python
from pydantic import BaseModel, ConfigDict, Field

from openagi.storage.base import BaseStorage

class NewStorage(BaseModel):

    name: str = Field(title="<storage name>", description="<description>.")

    def save_document(self):
        """Save documents to the with metadata."""
        ...

    def update_document(self):
        ...

    def delete_document(self):
        ...

    def query_documents(self):
        ...

    @classmethod
    def from_kwargs(cls, **kwargs):
        raise NotImplementedError("Subclasses must implement this method.")
```

