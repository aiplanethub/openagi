from copy import deepcopy
import logging
import tempfile
from pathlib import Path
from typing import Any
from uuid import uuid4

import chromadb
import chromadb.api
from pydantic import Field

from openagi.storage.base import BaseStorage


class ChromaStorage(BaseStorage):
    name: str = Field(default="ChromaDB Storage")
    client: Any = Field(default=None, exclude=True)  # Exclude non-serializable fields
    collection: chromadb.Collection = Field(default_factory=chromadb.Collection, exclude=True)

    # def __deepcopy__(self, memo):
    #     # Custom deepcopy method to handle non-serializable fields
    #     cls = self.__class__
    #     result = cls.__new__(cls)
    #     memo[id(self)] = result
    #     for k, v in self.__dict__.items():
    #         if k not in ["client", "collection"]:  # Avoid copying non-serializable fields
    #             setattr(result, k, deepcopy(v, memo))
    #     return result

    @classmethod
    def get_default_persistent_path(cls):
        pth = Path(tempfile.gettempdir()) / "openagi"
        return str(pth.absolute())

    @classmethod
    def from_kwargs(cls, **kwargs):
        client = None
        if kwargs.get("host", None) and kwargs.get("port", None):
            client = chromadb.HttpClient(
                host=kwargs.get("host", None),
                port=kwargs.get("port", None),
            )
        else:
            client = chromadb.PersistentClient(
                kwargs.get("persist_path", None) or cls.get_default_persistent_path()
            )
        print(client, "<<<<")
        collection = client.get_or_create_collection(
            kwargs.get("collection_name", f"openagi-chroma-{uuid4()}")
        )
        return cls(client=client, collection=collection)

    def save_document(self, documents, metadatas, ids):
        """Save documents to the ChromaDB collection with metadata."""
        try:
            self.collection.add(documents=documents, metadatas=metadatas, ids=ids)
            logging.info("Documents added to the collection.")
        except Exception as e:
            logging.error(f"Error saving documents: {e}")

    def update_document(self, ids, documents, metadatas):
        """Update documents in the ChromaDB collection."""
        try:
            self.collection.update(ids=ids, documents=documents, metadatas=metadatas)
            logging.info("Documents updated in the collection.")
        except Exception as e:
            logging.error(f"Error updating documents: {e}")

    def delete_document(self, ids):
        """Delete documents from the ChromaDB collection."""
        try:
            self.collection.delete(ids=ids)
            logging.INFO("Documents deleted from the collection.")
        except Exception as e:
            logging.error(f"Error deleting documents: {e}")

    def query_documents(self, query_texts, n_results):
        """Query the ChromaDB collection for relevant documents based on the query."""
        try:
            results = self.collection.query(query_texts=query_texts, n_results=n_results)
            logging.info(f"Query results: {results}")
            return results
        except Exception as e:
            logging.error(f"Error querying documents: {e}")
            return []
