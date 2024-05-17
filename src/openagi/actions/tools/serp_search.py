from openagi.actions.base import BaseAction
from pydantic import Field
import http.client
import json
import os

class SerpSearch(BaseAction):
    """ Google Serp Search Tool """

    query: str = Field(...,description="User query to fetch web search results from Google")

    def execute(self):
       serp_api_key = os.environ['SERP_API_KEY']

       conn = http.client.HTTPSConnection("google.serper.dev")
       payload = json.dumps({
          "q": self.query
          })
       headers = {
          'X-API-KEY': serp_api_key,
          'Content-Type': 'application/json'
        }
       conn.request("POST", "/search", payload, headers)
       res = conn.getresponse()
       data = res.read().decode("utf-8")
       return json.loads(data)