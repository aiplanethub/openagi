import http.client
import json
import os
import warnings
from pydantic import Field
from openagi.actions.base import BaseAction
from typing import ClassVar, Dict, Any
from openagi.exception import OpenAGIException

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

class SerperSearch(ConfigurableAction):
    """Google Serper.dev Search Tool"""
    query: str = Field(..., description="User query to fetch web search results from Google")
    
    def __init__(self, **data):
        super().__init__(**data)
        self._check_deprecated_usage()
    
    def _check_deprecated_usage(self):
        if 'SERPER_API_KEY' in os.environ and not self.get_config('api_key'):
            warnings.warn(
                "Using environment variables for API keys is deprecated and will be removed in a future version. "
                "Please use SerperSearch.set_config(api_key='your_key') instead of setting environment variables.",
                DeprecationWarning,
                stacklevel=2
            )
            self.set_config(api_key=os.environ['SERPER_API_KEY'])

    def execute(self):
        api_key = self.get_config('api_key')
        
        if not api_key:
            if 'SERPER_API_KEY' in os.environ:
                api_key = os.environ['SERPER_API_KEY']
                warnings.warn(
                    "Using environment variables for API keys is deprecated and will be removed in a future version. "
                    "Please use SerperSearch.set_config(api_key='your_key') instead of setting environment variables.",
                    DeprecationWarning,
                    stacklevel=2
                )
            else:
                raise OpenAGIException("API KEY NOT FOUND. Use SerperSearch.set_config(api_key='your_key') to set the API key.")

        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({"q": self.query})
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        result = json.loads(data)
        
        meta_data = ""
        for info in result.get("organic", []):
            meta_data += f"CONTEXT: {info.get('title', '')} \ {info.get('snippet', '')}\n"
            meta_data += f"Reference URL: {info.get('link', '')}\n\n"
            
        return meta_data.strip()