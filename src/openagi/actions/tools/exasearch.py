from openagi.actions.base import BaseAction
import os
from pydantic import Field
from openagi.exception import OpenAGIException

try:
   from exa_py import Exa
except ImportError:
  raise OpenAGIException("Install Exa Py with cmd `pip install exa_py`")

class ExaSearch(BaseAction):
    """
    Exa Search is a tool used when user needs to ask the question in terms of query to get response 
    """
    query: str = Field(..., description="User query or question ")
   
    def execute(self):
        api_key = os.environ["EXA_API_KEY"]
        
        exa = Exa(api_key = api_key)
        results = exa.search_and_contents(self.query, 
                                    text={"max_characters": 512}, 
                                )
        content = ""
        for idx in results.results:
            content += idx.text.strip()

        content = content.replace("<|endoftext|>","")
        content = content.replace("NaN","")
        return content