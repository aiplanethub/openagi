from openagi.actions.base import BaseAction
import os
from pydantic import Field
from tavily import TavilyClient

class TavilyWebSearchQA(BaseAction):
    """
    Tavily Web Search QA is a tool used when user needs to ask the question in terms of query to get response 
    """
    query: str = Field(..., description="User query or question ")

    def execute(self):
        api_key = os.environ("TAVILY_API_KEY")
        
        client = TavilyClient(api_key=api_key)
        response = client.qna_search(query=self.query)
        return response