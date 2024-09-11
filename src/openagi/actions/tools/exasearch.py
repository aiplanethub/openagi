from openagi.actions.base import BaseAction
from pydantic import Field
from openagi.exception import OpenAGIException
from typing import ClassVar, Dict, Any

try:
    from exa_py import Exa
except ImportError:
    raise OpenAGIException("Install Exa Py with cmd `pip install exa_py`")

class ConfigurableAction(BaseAction):
    config: ClassVar[Dict[str, Any]] = {}

    @classmethod
    def set_config(cls, **kwargs):
        cls.config.update(kwargs)

    @classmethod
    def get_config(cls, key: str, default: Any = None) -> Any:
        return cls.config.get(key, default)

class ExaSearch(ConfigurableAction):
    """
    Exa Search is a tool used when user needs to ask the question in terms of query to get response 
    """
    query: str = Field(..., description="User query or question")

    def execute(self):
        api_key = self.get_config('api_key')
        if not api_key:
            raise OpenAGIException("EXA API key not set. Use ExaSearch.set_config(api_key='your_key') to set the API key.")

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