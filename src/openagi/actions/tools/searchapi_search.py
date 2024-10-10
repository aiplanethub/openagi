import logging
import os
import requests
from urllib.parse import urlencode
from typing import Any

from pydantic import Field

from openagi.actions.base import BaseAction
from openagi.exception import OpenAGIException


class SearchApiSearch(BaseAction):
    """SearchApi.io provides a real-time API to access search results from Google (default), Google Scholar, Bing, Baidu, and other search engines."""
    query: str = Field(
        ..., description="User query of type string used to fetch web search results from a search engine."
    )

    def execute(self):
        base_url = "https://www.searchapi.io/api/v1/search"
        searchapi_api_key = os.environ["SEARCHAPI_API_KEY"]
        engine = os.environ.get("SEARCHAPI_ENGINE") or "google"
        search_dict = {
            "q": self.query,
            "engine": engine,
            "api_key": searchapi_api_key
        }
        logging.debug(f"{search_dict=}")
        url = f"{base_url}?{urlencode(search_dict)}"
        response = requests.request("GET", url)
        json_response = response.json()

        # if not json_response:
        #     raise OpenAGIException(f"Unable to generate result for the query {self.query}")

        # logging.debug(json_response)

        organic_results = json_response.get("organic_results", [])

        meta_data = ""
        for organic_result in organic_results:
            meta_data += f"CONTEXT: {organic_result['title']} \ {organic_result['snippet']}"
            meta_data += f"Reference URL: {organic_result['link']}\n"
        return meta_data
