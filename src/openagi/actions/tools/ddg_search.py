from typing import Any
from openagi.actions.base import BaseAction
from pydantic import Field
from duckduckgo_search import DDGS


class DuckDuckGoSearch(BaseAction):
    """Search Tool to fetch results from  DuckDuckGo"""

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

    def execute(self):
        result = DDGS().text(
            self.query,
            max_results=self.max_results,
        )
        return result
