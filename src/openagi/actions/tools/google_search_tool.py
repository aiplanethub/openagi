from openagi.actions.base import BaseAction
from pydantic import Field
from openagi.exception import OpenAGIException
import logging
import requests
from bs4 import BeautifulSoup
from typing import ClassVar, Dict, Any

try:
   from googlesearch import search
except ImportError:
  raise OpenAGIException("Install googlesearch-python with cmd `pip install googlesearch-python`")

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
    
class GoogleSearchTool(ConfigurableAction):
    """
    Google Search is a tool used for scraping the Google search engine. Extract information from Google search results.
    """
    query: str = Field(..., description="User query or question ")

    max_results: int = Field(
        default=10,
        description="Total results, in int, to be executed from the search. Defaults to 10. The limit should be 10 and not execeed more than 10",
    )

    lang: str = Field(
        default="en",
        description = "specify the langauge for your search results."
    )

    def execute(self):
        if self.max_results > 15:
            logging.info("Over threshold value... Limiting the Max results to 15")
            self.max_results = 15
        
        context = ""
        search_results = search(self.query,num_results=self.max_results,lang=self.lang,advanced=True)
        for info in search_results:
            context += f"Title: {info.title}. Description: {info.description}. URL: {info.url}"
        
        return context
        