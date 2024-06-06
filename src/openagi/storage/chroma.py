import logging
import tempfile
from pathlib import Path

import chromadb
from chromadb import HttpClient, PersistentClient
from pydantic import Field

from openagi.storage.base import BaseStorage


class ChromaStorage(BaseStorage):
    name: str = Field(default="ChromaDB Storage")
    client: chromadb.ClientAPI
    collection: chromadb.Collection

    @classmethod
    def get_default_persistent_path(cls):
        path = Path(tempfile.gettempdir()) / "openagi"
        return str(path.absolute())

    @classmethod
    def from_kwargs(cls, **kwargs):
        if kwargs.get("host", None) and kwargs.get("port", None):
            _client = HttpClient(host=kwargs["host"], port=kwargs["port"])
        else:
            persit_pth = kwargs.get("persist_path", cls.get_default_persistent_path())
            _client = PersistentClient(path=persit_pth)
            logging.info(f"Using Chroma persistent client with path: {persit_pth}")

        _collection = _client.get_or_create_collection(kwargs.get("collection_name"))
        logging.debug(f"Collection: Name - {_collection.name}, ID - {_collection.id}")
        return cls(client=_client, collection=_collection)

    def save_document(self, id, document, metadata):
        """Create a new document in the ChromaDB collection."""

        resp = self.collection.add(ids=id, documents=document, metadatas=metadata)
        return resp

    def update_document(self, id, document, metadata):
        """Update an existing document in the ChromaDB collection."""
        # if not isinstance(document, list):
        #     document = [document]
        # if not isinstance(metadata, list):
        #     metadata = [metadata]
        self.collection.update(ids=[id], documents=document, metadatas=metadata)
        logging.info("Document updated successfully.")

    def delete_document(self, id):
        """Delete a document from the ChromaDB collection."""
        self.collection.delete(ids=[id])
        logging.debug("Document deleted successfully.")

    def query_documents(self, **kwargs):
        """Query the ChromaDB collection for relevant documents based on the query."""
        results = self.collection.query(**kwargs)
        logging.debug(f"Queried results: {results}")
        return results
