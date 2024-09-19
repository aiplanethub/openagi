import json
from typing import Any,Dict
from openagi.actions.base import BaseAction
from pydantic import Field
from duckduckgo_search import DDGS
import logging

class DuckDuckGoSearch(BaseAction):
    """Use this Action to search DuckDuckGo for a query."""

    name: str = Field(
        default_factory=str,
        description="DuckDuckGoSearch Action to search over duckduckgo using the query.",
    )
    description: str = Field(
        default_factory=str,
        description="This action is used to search for words, documents, images, videos, news, maps and text translation using the DuckDuckGo.com search engine.",
    )

    query: Any = Field(
        default_factory=str,
        description="User query, a string, to fetch web search results from DuckDuckGo",
    )

    max_results: int = Field(
        default=10,
        description="Total results, in int, to be executed from the search. Defaults to 10.",
    )

    def _get_ddgs(self):
        return DDGS()

    def execute(self):
        if self.max_results > 15:
            logging.info("Over threshold value... Limiting the Max results to 15")
            self.max_results = 15
        
        result = self._get_ddgs().text(
            self.query,
            max_results=self.max_results,
        )
        return json.dumps(result)
    
    @classmethod
    def from_user_config(cls, config: Dict[str, Any]) -> 'DuckDuckGoSearch':
        """
        Create a DuckDuckGoSearch instance from a user-provided configuration dictionary.
        
        :param config: A dictionary containing user-specified configuration.
        :return: An instance of DuckDuckGoSearch.
        """
        return cls(**config)


class DuckDuckGoNewsSearch(DuckDuckGoSearch):
    """Use this Action to get the latest news from DuckDuckGo."""

    def execute(self):
        ddgs = self._get_ddgs()
        return json.dumps(
            ddgs.news(keywords=self.query, max_results=(self.max_results)), indent=2
        )

if __name__ == "__main__":
    user_config = {
        "query": "Python programming",
        "max_results": 5
    }
    action = DuckDuckGoSearch
    print(action.execute("query",max_results=15))