from openagi.actions.base import BaseAction
from pydantic import Field
from openagi.exception import OpenAGIException
from typing import ClassVar, Dict, Any
import os
import warnings

try:
    from exa_py import Exa
except ImportError:
    raise OpenAGIException("Install Exa Py with cmd `pip install exa_py`")

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

class ExaSearch(ConfigurableAction):
    """
    Exa Search is a tool used when user needs to ask the question in terms of query to get response 
    """
    query: str = Field(..., description="User query or question")
    
    def __init__(self, **data):
        super().__init__(**data)
        self._check_deprecated_usage()
    
    def _check_deprecated_usage(self):
        if 'EXA_API_KEY' in os.environ and not self.get_config('api_key'):
            warnings.warn(
                "Using environment variables for API keys is deprecated and will be removed in a future version. "
                "Please use ExaSearch.set_config(api_key='your_key') instead of setting environment variables.",
                DeprecationWarning,
                stacklevel=2
            )
            self.set_config(api_key=os.environ['EXA_API_KEY'])

    def execute(self):
        api_key = self.get_config('api_key')
        
        if not api_key:
            if 'EXA_API_KEY' in os.environ:
                api_key = os.environ['EXA_API_KEY']
                warnings.warn(
                    "Using environment variables for API keys is deprecated and will be removed in a future version. "
                    "Please use ExaSearch.set_config(api_key='your_key') instead of setting environment variables.",
                    DeprecationWarning,
                    stacklevel=2
                )
            else:
                raise OpenAGIException("API KEY NOT FOUND. Use ExaSearch.set_config(api_key='your_key') to set the API key.")

        exa = Exa(api_key=api_key)
        results = exa.search_and_contents(
            self.query,
            text={"max_characters": 512},
        )
        
        content = ""
        for idx in results.results:
            content += idx.text.strip()
        content = content.replace("<|endoftext|>", "")
        content = content.replace("NaN", "")
        return content