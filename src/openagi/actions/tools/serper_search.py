import http.client
import json
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

    def execute(self):
        api_key = self.get_config('api_key')
        if not api_key:
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