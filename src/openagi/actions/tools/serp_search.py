import logging
import os
from typing import Any

from pydantic import Field, field_validator
from serpapi import GoogleSearch

from openagi.actions.base import BaseAction


class GoogleSerpAPISearch(BaseAction):
    """Google Serp API Search Tool"""

    query: str = Field(..., description="User query to fetch web search results from Google")
    hl: str = Field(default="en", description="Google UI Language")
    gl: str = Field(default="us", description="Google Country")
    max_results: Any = Field(
        default=10, description="Total results to be executed from the search"
    )

    @field_validator("max_results")
    @classmethod
    def actions_validator(cls, max_results):
        if not max_results and not isinstance(max_results, int):
            logging.warning("Max Results set to 10(default).")
            max_results = 10
        return max_results

    def execute(self):
        serp_api_key = os.environ["GOOGLE_SERP_API_KEY"]

        search = GoogleSearch(
            {
                "q": self.query,
                "hl": self.hl,
                "gl": self.gl,
                "num": self.max_results,
                "api_key": serp_api_key,
            }
        )

        max_retries = 3
        retries = 1
        result = search.get_dict()

        while retries < max_retries and not result:
            result = search.get_dict()

        meta_data = ""
        for info in result.get("organic_results"):
            meta_data += f"CONTEXT: {info['title']} \ {info['snippet']}"
            meta_data += f"Reference URL: {info['link']}"
        return meta_data
