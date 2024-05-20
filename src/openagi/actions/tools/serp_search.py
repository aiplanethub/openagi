import logging
import os

from pydantic import Field
from serpapi import GoogleSearch

from openagi.actions.base import BaseAction


class GoogleSerpAPISearch(BaseAction):
    """Google Serp API Search Tool"""

    query: str = Field(..., description="User query to fetch web search results from Google")
    hl: str = Field(default="en", description="Google UI Language")
    gl: str = Field(default="us", description="Google Country")
    num: int = Field(default=5, description="Total results to be executed from the search")

    def execute(self):
        # serp_api_key = os.environ["GOOGLE_SERP_API_KEY"]
        serp_api_key = "efac1e5eb066c940d6e3437abe66b435812bfc0cc843b79b850033255e7a6490"

        search = GoogleSearch(
            {
                "q": self.query,
                "hl": self.hl,
                "gl": self.gl,
                "num": self.num,
                "api_key": serp_api_key,
            }
        )

        result = search.get_dict()
        meta_data = ""
        for info in result.get("organic_results"):
            meta_data += f"CONTEXT: {info['title']} \ {info['snippet']}"
            meta_data += f"Reference URL: {info['link']}"
        return meta_data
