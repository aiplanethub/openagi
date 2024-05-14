import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection("agent_memory")

document_ids = []

def save_document(documents, metadatas, ids):
    """Save documents to the ChromaDB collection with metadata."""
    try:
        collection.add(documents=documents, metadatas=metadatas, ids=ids)
        document_ids.extend(ids)  # Keep track of the document IDs
        print("Documents added to the collection.")
    except Exception as e:
        print(f"Error saving documents: {e}")

def update_document(ids, documents, metadatas):
    """Update documents in the ChromaDB collection."""
    try:
        collection.update(ids=ids, documents=documents, metadatas=metadatas)
        print("Documents updated in the collection.")
    except Exception as e:
        print(f"Error updating documents: {e}")

def delete_document(ids):
    """Delete documents from the ChromaDB collection."""
    try:
        collection.delete(ids=ids)
        print("Documents deleted from the collection.")
    except Exception as e:
        print(f"Error deleting documents: {e}")

def query_documents(query_texts, n_results):
    """Query the ChromaDB collection for relevant documents based on the query."""
    try:
        results = collection.query(query_texts=query_texts, n_results=n_results)
        print("Query results:", results)
        return results
    except Exception as e:
        print(f"Error querying documents: {e}")
        return []

def clear_collection():
    """Clear all documents from the collection for testing purposes."""
    try:
        collection.delete(ids=document_ids)
        document_ids.clear()
        print("Collection cleared.")
    except Exception as e:
        print(f"Error clearing collection: {e}")
