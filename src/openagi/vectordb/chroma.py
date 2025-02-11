from dataclasses import dataclass
from typing import List, Optional, Any, Iterable
import warnings
import subprocess
import sys
import os
from langchain_core.documents import Document

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
warnings.filterwarnings("ignore")

@dataclass
class VectorDbConfig:
    """Configuration class for vector database settings"""
    collection_name: str
    persist_directory: str = ""
    embedding_function: Optional[Any] = None

class ChromaVectorDb:
    
    def __init__(self, collection_name: str, persist_directory: str = "", embedding_function: Optional[Any] = None):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embedding_function = embedding_function
        self.client = None
        self._initialize_dependencies()
        self.load()

    def _initialize_dependencies(self):
        """Initialize and check for required dependencies"""
        try:
            from langchain_community.vectorstores import Chroma
        except ImportError:
            user_agree = input("Required libraries missing. Would you like to install langchain-community? [y/N]: ")
            if user_agree.lower() == 'y':
                subprocess.check_call([sys.executable, "-m", "pip", "install", "langchain-community"])
            else:
                raise ImportError("Required 'langchain-community' is not installed.")

    def load(self):
        """Initialize and load the Chroma vector store"""
        try:
            from langchain_community.vectorstores import Chroma
            
            if not self.embedding_function:
                raise ValueError("No embedding function provided. Please provide an embedding function during initialization.")
            
            if self.persist_directory:
                self.client = Chroma(
                    collection_name=self.collection_name,
                    embedding_function=self.embedding_function,
                    persist_directory=self.persist_directory
                )
            else:
                self.client = Chroma(
                    collection_name=self.collection_name,
                    embedding_function=self.embedding_function
                )
            return self.client
            
        except Exception as e:
            raise Exception(f"Failed to load the Chroma Vectorstore: {e}")

    def add_documents(self, documents: List[Document], **kwargs) -> List[str]:
        if not self.client:
            raise ValueError("Vector store not initialized. Call load() first.")
        
        try:
            # Test embedding with first document
            test_text = documents[0].page_content
            try:
                self.embedding_function.embed_query(test_text)
            except Exception as embed_err:
                raise ValueError(f"Embedding test failed: {str(embed_err)}")
            
            return self.client.add_documents(documents, **kwargs)
        except Exception as e:
            if "401" in str(e):
                raise Exception("Authentication error with HuggingFace API. Please check your API key.")
            raise

    def add_texts(self, 
                 texts: Iterable[str], 
                 metadatas: Optional[List[dict]] = None,
                 ids: Optional[List[str]] = None,
                 **kwargs) -> List[str]:
        if not self.client:
            raise ValueError("Vector store not initialized. Call load() first.")
        return self.client.add_texts(texts, metadatas=metadatas, ids=ids, **kwargs)

    def update_document(self, document_id: str, document: Document) -> None:
        if not self.client:
            raise ValueError("Vector store not initialized. Call load() first.")
        self.client.update_document(document_id, document)

    def delete(self, ids: Optional[List[str]] = None, **kwargs) -> None:
        if not self.client:
            raise ValueError("Vector store not initialized. Call load() first.")
        self.client.delete(ids, **kwargs)

    def similarity_search(self, 
                        query: str, 
                        k: int = 4, 
                        **kwargs) -> List[Document]:
        if not self.client:
            raise ValueError("Vector store not initialized. Call load() first.")
        return self.client.similarity_search(query, k=k, **kwargs)

    @classmethod
    def from_config(cls, config: VectorDbConfig):
        return cls(
            collection_name=config.collection_name,
            persist_directory=config.persist_directory,
            embedding_function=config.embedding_function
        )

    @classmethod
    def load_from_kwargs(cls, kwargs: dict):
        config = VectorDbConfig(**kwargs)
        return cls.from_config(config)
    
