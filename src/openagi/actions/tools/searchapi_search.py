import logging
import os
import requests
from urllib.parse import urlencode
from typing import Any

from pydantic import Field

from openagi.actions.base import BaseAction
from openagi.exception import OpenAGIException
from typing import ClassVar, Dict, Any
import warnings

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

class SearchApiSearch(BaseAction):
    """SearchApi.io provides a real-time API to access search results from Google (default), Google Scholar, Bing, Baidu, and other search engines."""
    query: str = Field(
        ..., description="User query of type string used to fetch web search results from a search engine."
    )

    def __init__(self, **data):
        super().__init__(**data)
        self._check_deprecated_usage()

    def _check_deprecated_usage(self):
        if 'SEARCHAPI_API_KEY' in os.environ and not self.get_config('api_key'):
            warnings.warn(
                "Using environment variables for API keys is deprecated and will be removed in a future version. "
                "Please use SearchApiSearch.set_config(api_key='your_key') instead of setting environment variables.",
                DeprecationWarning,
                stacklevel=2
            )
            self.set_config(api_key=os.environ['SEARCHAPI_API_KEY'])

    def execute(self):
        base_url = "https://www.searchapi.io/api/v1/search"
        api_key = self.get_config('api_key')

        search_dict = {
            "q": self.query,
            "engine": "google",
            "api_key": api_key
        }

        logging.debug(f"{search_dict=}")

        url = f"{base_url}?{urlencode(search_dict)}"
        response = requests.request("GET", url)
        json_response = response.json()

        organic_results = json_response.get("organic_results", [])

        meta_data = ""
        for organic_result in organic_results:
            meta_data += f"CONTEXT: {organic_result['title']} \ {organic_result['snippet']}"
            meta_data += f"Reference URL: {organic_result['link']}\n"
        return meta_data
