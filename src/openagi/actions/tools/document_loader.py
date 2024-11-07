from typing import Any
from openagi.actions.base import ConfigurableAction
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from pydantic import Field

class TextLoaderTool(ConfigurableAction):
    """Load content from a text file.
    
    This action loads and processes content from .txt files, combining
    metadata and content into a single context string.
    """
    
    def execute(self) -> str:
        file_path: str = self.get_config('filename')
        loader = TextLoader(file_path=file_path)
        documents = loader.load()
        
        if not documents:
            return ""
            
        page_content = documents[0].page_content
        source = documents[0].metadata["source"]
        return f"{source} {page_content}"

class PDFLoaderTool(ConfigurableAction):
    """Load content from a PDF file.
    
    This action loads and processes content from .pdf files, combining
    metadata and content into a single context string.
    """
    
    def execute(self) -> str:
        file_path: str = self.get_config('filename')
        loader = PyPDFLoader(file_path=file_path)
        documents = loader.load()
        
        if not documents:
            return ""
            
        page_content = documents[0].page_content
        source = documents[0].metadata["source"]
        return f"{source} {page_content}"

class CSVLoaderTool(ConfigurableAction):
    """Load content from a CSV file.
    
    This action loads and processes content from .csv files, combining
    row numbers and content into a formatted string representation.
    """
    
    def execute(self) -> str:
        file_path: str = self.get_config('filename')
        loader = CSVLoader(file_path=file_path)
        documents = loader.load()
        
        content_parts = []
        for idx, doc in enumerate(documents):
            row_content = doc.page_content
            row_number = doc.metadata["row"]
            content_parts.append(f"row_no {row_number}: {row_content}")
            
        return "".join(content_parts)