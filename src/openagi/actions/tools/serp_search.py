import logging
import os
import warnings
from typing import Any, ClassVar, Dict
from pydantic import Field, field_validator
from serpapi import GoogleSearch
from openagi.actions.base import BaseAction
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

class GoogleSerpAPISearch(ConfigurableAction):
    """Google Serp API Search Tool"""
    query: str = Field(
        ..., description="User query of type string used to fetch web search results from Google."
    )
    max_results: Any = Field(
        default=10,
        description="Total results, an integer, to be executed from the search. Defaults to 10",
    )
    
    def __init__(self, **data):
        super().__init__(**data)
        self._check_deprecated_usage()
    
    def _check_deprecated_usage(self):
        if 'GOOGLE_SERP_API_KEY' in os.environ and not self.get_config('api_key'):
            warnings.warn(
                "Using environment variables for API keys is deprecated and will be removed in a future version. "
                "Please use GoogleSerpAPISearch.set_config(api_key='your_key') instead of setting environment variables.",
                DeprecationWarning,
                stacklevel=2
            )
            # Automatically migrate the environment variable to config
            self.set_config(api_key=os.environ['GOOGLE_SERP_API_KEY'])
    
    def execute(self):
        api_key = self.get_config('api_key')
        
        if not api_key:
            if 'GOOGLE_SERP_API_KEY' in os.environ:
                api_key = os.environ['GOOGLE_SERP_API_KEY']
                warnings.warn(
                    "Using environment variables for API keys is deprecated and will be removed in a future version. "
                    "Please use GoogleSerpAPISearch.set_config(api_key='your_key') instead of setting environment variables.",
                    DeprecationWarning,
                    stacklevel=2
                )
            else:
                raise OpenAGIException("API KEY NOT FOUND. Use GoogleSerpAPISearch.set_config(api_key='your_key') to set the API key.")

        search_dict = {
            "q": self.query,
            "hl": "en",
            "gl": "us",
            "num": self.max_results,
            "api_key": api_key,
        }
        logging.debug(f"{search_dict=}")
        search = GoogleSearch(search_dict)
        
        max_retries = 3
        retries = 1
        result = None
        
        while retries < max_retries and not result:
            try:
                result = search.get_dict()
            except TypeError:
                logging.error("Error during GoogleSearch.", exc_info=True)
                continue
            retries += 1
            
        if not result:
            raise OpenAGIException(f"Unable to generate result for the query {self.query}")
            
        logging.debug(result)
        logging.info(f"NOTE: REMOVE THIS BEFORE RELEASE:\n{result}\n")
        
        if error := result.get("error", NotImplemented):
            raise OpenAGIException(
                f"Error while running action {self.__class__.__name__}: {error}"
            )
            
        meta_data = ""
        for info in result.get("organic_results", []):
            meta_data += f"CONTEXT: {info.get('title', '')} \ {info.get('snippet', '')}\n"
            meta_data += f"Reference URL: {info.get('link', '')}\n\n"
            
        return meta_data.strip()