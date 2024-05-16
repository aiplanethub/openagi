import chromadb
import logging

client = chromadb.Client()
collection = client.get_or_create_collection("agent_memory")            #TODO: Create storage class for memory, but we don't require it as of now. Support could be updated after release.
                                                                        # or create a vector storage class separately, must find use for it in others places as well.

def save_document(documents, metadatas, ids):
    """Save documents to the ChromaDB collection with metadata."""
    try:
        collection.add(documents=documents, metadatas=metadatas, ids=ids)
        logging.info("Documents added to the collection.")
    except Exception as e:
        logging.error(f"Error saving documents: {e}")

def update_document(ids, documents, metadatas):
    """Update documents in the ChromaDB collection."""
    try:
        collection.update(ids=ids, documents=documents, metadatas=metadatas)
        logging.info("Documents updated in the collection.")
    except Exception as e:
        logging.error(f"Error updating documents: {e}")

def delete_document(ids):
    """Delete documents from the ChromaDB collection."""
    try:
        collection.delete(ids=ids)
        logging.INFO("Documents deleted from the collection.")
    except Exception as e:
        logging.error(f"Error deleting documents: {e}")

def query_documents(query_texts, n_results):
    """Query the ChromaDB collection for relevant documents based on the query."""
    try:
        results = collection.query(query_texts=query_texts, n_results=n_results)
        logging.info(f"Query results: {results}")
        return results
    except Exception as e:
        logging.error(f"Error querying documents: {e}")
        return []
