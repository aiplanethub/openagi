import logging
from .storage import save_document, query_documents, delete_document

class BaseMemory:
    def __init__(self):
        pass
    def add_document(self, document, metadata, document_id):
        """Add a document to the memory."""
        try:
            save_document([document], [metadata], [document_id])
        except Exception as e:
            logging.error(f"Error adding document: {e}")

    def get_documents(self, query, n_results=1):
        """Retrieve documents based on a query."""
        try:
            return query_documents([query], n_results)
        except Exception as e:
            logging.error(f"Error querying documents: {e}")
            return []

    def delete_document(self, document_id):
        """Delete a document from the memory."""
        try:
            delete_document([document_id])
        except Exception as e:
            logging.error(f"Error deleting document: {e}")