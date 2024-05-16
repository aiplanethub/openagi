from openagi.actions.base import BaseAction
from openagi.actions.tools.utils import DuckDuckGoWrapper

class DuckDuckGoSearch(BaseAction):
    """ Search Tool to fetch results from  DuckDuckGo """
    
    def execute(self,query):
        search_results = DuckDuckGoWrapper.search_tool(query)
        return ",".join(search_results)