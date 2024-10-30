from openagi.actions.base import BaseAction
from pydantic import Field
from openagi.exception import OpenAGIException
import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

try:
   from googlesearch import search
except ImportError:
  raise OpenAGIException("Install googlesearch-python with cmd `pip install googlesearch-python`")

class GoogleSearch(BaseAction):
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
        search_results = search(self.query, num=self.max_results,stop=self.max_results)
        for url in search_results:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(url, headers=headers, timeout=5)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                title = soup.title.string.strip() if soup.title else "No title found"
                
                meta_desc = soup.find('meta', {'name': ['description', 'Description']})
                description = meta_desc['content'].strip() if meta_desc else "No description found"
                
                if description == "No description found":
                    first_p = soup.find('p')
                    if first_p:
                        description = first_p.get_text().strip()[:200] + "..."
                else:
                  context += f"Title: {title}. Description: {description}. URL: {url}"
            except Exception as e:
                return (f"Error processing {url}: {str(e)}")
        
        return context