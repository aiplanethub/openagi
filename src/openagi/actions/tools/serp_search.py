import logging
import os

from pydantic import Field
from serpapi import GoogleSearch

from openagi.actions.base import BaseAction


class GoogleSerpAPISearch(BaseAction):
    """Google Serp API Search Tool"""

    query: str = Field(..., description="User query to fetch web search results from Google")
    hl: str = Field("en", description="Google UI Language")
    gl: str = Field("us", description="Google Country")
    num: int = Field(default=5, description="Total results to be executed from the search")

    def execute(self):
        serp_api_key = os.environ["GOOGLE_SERP_API_KEY"]

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
        logging.debug(">>>>>>>>>SERPAPI RAN")
        return meta_data
