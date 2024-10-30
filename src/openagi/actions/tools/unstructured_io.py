import logging
from pydantic import Field
from openagi.exception import OpenAGIException
from openagi.actions.base import BaseAction
from typing import ClassVar, Dict, Any

try:
   from unstructured.partition.pdf import partition_pdf
   from unstructured.chunking.title import chunk_by_title
except ImportError:
  raise OpenAGIException("Install Unstructured with cmd `pip install 'unstructured[all-docs]'`")

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
    
class UnstructuredPdfLoaderAction(ConfigurableAction):
    """
    Use this Action to extract content from PDFs including metadata.
    Returns a list of dictionary with keys 'type', 'element_id', 'text', 'metadata'.
    """

    def execute(self):
        file_path = self.get_config('filename')    
        logging.info(f"Reading file {file_path}")
        
        elements = partition_pdf(file_path, extract_images_in_pdf=True)

        chunks = chunk_by_title(elements)

        dict_elements = []
        for element in chunks:
            dict_elements.append(element.to_dict())

        with open("ele.txt", "w") as f:
            f.write(str(dict_elements))

        return str(dict_elements)
