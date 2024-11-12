# brave_search_tool.py

from openagi.actions.base import Tool
from openagi.config import get_config
from serpapi import GoogleSearch

class BraveSearchTool(Tool):
    """
    A tool for performing web searches using Brave Search.
    """

    def __init__(self, name="BraveSearch", description="A tool for performing web searches using Brave Search."):
        super().__init__(name, description)

    def _execute(self, query: str):
        # Get SerpApi API key from configuration
        config = get_config()
        api_key = config.get("serpapi", "api_key")

        # Perform Brave Search using SerpApi
        try:
            params = {
                "api_key": api_key,
                "engine": "brave",
                "q": query,
                "num": 5  # Number of results to retrieve
            }
            search = GoogleSearch(params)
            results = search.get_dict()

            # Extract and return search results
            organic_results = results.get("organic_results", [])
            formatted_results = [f"{result['title']}\n{result['link']}\n" for result in organic_results]
            return "\n".join(formatted_results)
        except Exception as e:
            return f"Error performing Brave Search: {e}"