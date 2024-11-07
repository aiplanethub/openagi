from openagi.actions.base import ConfigurableAction
from pydantic import Field
from openagi.exception import OpenAGIException
import os
import warnings

try:
    from tavily import TavilyClient
except ImportError:
    raise OpenAGIException("Install Tavily with cmd `pip install tavily-python`")

class TavilyWebSearchQA(ConfigurableAction):
    """
    Tavily Web Search QA is a tool used when user needs to ask the question in terms of query to get response
    """
    query: str = Field(..., description="User query or question")
    
    def __init__(self, **data):
        super().__init__(**data)
        self._check_deprecated_usage()
    
    def _check_deprecated_usage(self):
        if 'TAVILY_API_KEY' in os.environ and not self.get_config('api_key'):
            warnings.warn(
                "Using environment variables for API keys is deprecated and will be removed in a future version. "
                "Please use TavilyWebSearchQA.set_config(api_key='your_key') instead of setting environment variables.",
                DeprecationWarning,
                stacklevel=2
            )
            self.set_config(api_key=os.environ['TAVILY_API_KEY'])

    def execute(self):
        api_key = self.get_config('api_key')
        
        if not api_key:
            if 'TAVILY_API_KEY' in os.environ:
                api_key = os.environ['TAVILY_API_KEY']
                warnings.warn(
                    "Using environment variables for API keys is deprecated and will be removed in a future version. "
                    "Please use TavilyWebSearchQA.set_config(api_key='your_key') instead of setting environment variables.",
                    DeprecationWarning,
                    stacklevel=2
                )
            else:
                raise OpenAGIException("API KEY NOT FOUND. Use TavilyWebSearchQA.set_config(api_key='your_key') to set the API key.")
        
        client = TavilyClient(api_key=api_key)
        response = client.qna_search(query=self.query)
        return response