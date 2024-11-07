from openagi.actions.base import ConfigurableAction
from pydantic import Field
from openagi.exception import OpenAGIException
import os
import warnings

try:
    from exa_py import Exa
except ImportError:
    raise OpenAGIException("Install Exa Py with cmd `pip install exa_py`")

class ExaSearch(ConfigurableAction):
    """Exa Search tool for querying and retrieving information.
    
    This action uses the Exa API to perform searches and retrieve relevant content
    based on user queries. Requires an API key to be configured before use.
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


    def execute(self) -> str:
        api_key: str = self.get_config('api_key')
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
        
        content_parts = []
        for result in results.results:
            content_parts.append(result.text.strip())

        content = "".join(content_parts)
        return (
            content.replace("<|endoftext|>", "")
                  .replace("NaN", "")
        )
