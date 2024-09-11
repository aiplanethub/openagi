from openagi.actions.base import BaseAction
from pydantic import Field
from openagi.exception import OpenAGIException
from typing import ClassVar, Dict, Any

try:
    from tavily import TavilyClient
except ImportError:
    raise OpenAGIException("Install Tavily with cmd `pip install tavily-python`")

class ConfigurableAction(BaseAction):
    config: ClassVar[Dict[str, Any]] = {}

    @classmethod
    def set_config(cls, **kwargs):
        cls.config.update(kwargs)

    @classmethod
    def get_config(cls, key: str, default: Any = None) -> Any:
        return cls.config.get(key, default)

class TavilyWebSearchQA(ConfigurableAction):
    """
    Tavily Web Search QA is a tool used when user needs to ask the question in terms of query to get response
    """
    query: str = Field(..., description="User query or question")

    def execute(self):
        api_key = self.get_config('api_key')
        if not api_key:
            raise OpenAGIException("Tavily API key not set. Use TavilyWebSearchQA.set_config(api_key='your_key') to set the API key.")
        
        client = TavilyClient(api_key=api_key)
        response = client.qna_search(query=self.query)
        return response