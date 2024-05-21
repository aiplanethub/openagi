import logging
import os
from typing import Any

from pydantic import Field, field_validator
from serpapi import GoogleSearch

from openagi.actions.base import BaseAction
from openagi.exception import OpenAGIException


class GoogleSerpAPISearch(BaseAction):
    """Google Serp API Search Tool"""

    query: str = Field(
        ..., description="User query of type string used to fetch web search results from Google."
    )
    hl: str = Field(default="en", description="Google UI Language. Defaults to `en`")
    gl: str = Field(default="us", description="Google Country. Defaults to `us`")
    max_results: Any = Field(
        default=10,
        description="Total results, an integer, to be executed from the search. Defaults to 10",
    )

    @field_validator("max_results")
    @classmethod
    def actions_validator(cls, max_results):
        if not max_results or not isinstance(max_results, int):
            logging.warning("Max Results set to 10(default).")
            max_results = 10
        return max_results

    def execute(self):
        serp_api_key = os.environ["GOOGLE_SERP_API_KEY"]
        print(self.query, "<<<<")
        search_dict = {
            "q": self.query,
            "hl": self.hl,
            "gl": self.gl,
            "num": self.max_results,
            "api_key": serp_api_key,
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

        meta_data = ""
        for info in result.get("organic_results"):
            meta_data += f"CONTEXT: {info['title']} \ {info['snippet']}"
            meta_data += f"Reference URL: {info['link']}"
        return meta_data
