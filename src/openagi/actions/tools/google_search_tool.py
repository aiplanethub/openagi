from openagi.actions.base import ConfigurableAction
from pydantic import Field
from openagi.exception import OpenAGIException
import logging

try:
   from googlesearch import search
except ImportError:
  raise OpenAGIException("Install googlesearch-python with cmd `pip install googlesearch-python`")

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
        