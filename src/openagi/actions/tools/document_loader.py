from openagi.actions.base import BaseAction
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from pydantic import Field
from typing import ClassVar, Dict, Any

class ConfigurableAction(BaseAction):
    config: ClassVar[Dict[str, Any]] = {}

    @classmethod
    def set_config(cls, *args, **kwargs):
        if args:
            if len(args) == 1 and isinstance(args[0], dict):
                cls.config.update(args[0])
            else:
                raise ValueError("If using positional arguments, a single dictionary must be provided.")
        cls.config.update(kwargs)

    @classmethod
    def get_config(cls, key: str, default: Any = None) -> Any:
        return cls.config.get(key, default)
    
class TextLoaderTool(ConfigurableAction):
    """Use this Action to load the content from .text file"""
    def execute(self):
        file_path = self.get_config('filename')        
        #print(file_path)
        loader = TextLoader(file_path=file_path)
        data = loader.load()
        page_content = data[0].page_content
        meta_data = data[0].metadata["source"]
        context = meta_data + " " + page_content
        return context

class CSVLoaderTool(ConfigurableAction):
    """Use this Action to load the content from .text file"""
    def execute(self):
        file_path = self.get_config('filename')
        content = ""
        loader = CSVLoader(file_path=file_path)
        data = loader.load()

        for i in range(len(data)):
            row_content = data[i].page_content
            row_no = data[i].metadata["row"]
            content += "row_no" + " " + str(row_no) + ": " + str(row_content)
        return content
