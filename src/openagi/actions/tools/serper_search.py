from openagi.actions.base import BaseAction
from pydantic import Field
import http.client
import json
import os

class SerperSearch(BaseAction):
    """ Google Serper.dev Search Tool """

    query: str = Field(...,description="User query to fetch web search results from Google")

    def execute(self):
      serper_api_key = os.environ['SERPER_API_KEY']

      conn = http.client.HTTPSConnection("google.serper.dev")
      payload = json.dumps({
          "q": self.query
          })
      headers = {
          'X-API-KEY': serper_api_key,
          'Content-Type': 'application/json'
        }
      conn.request("POST", "/search", payload, headers)
      res = conn.getresponse()
      data = res.read().decode("utf-8")
      result = json.loads(data)
      meta_data = ""
      for info in result.get('organic'):
         meta_data += f"CONTEXT: {info['title']} \ {info['snippet']}"
         meta_data += f"Reference URL: {info['link']}"
      
      return meta_data