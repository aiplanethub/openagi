import logging

from exa_py import Exa
from langchain.agents import (
    tool,
)
import threading
from openagi.tools.integrations.duckducksearch import getDuckduckgoSearchResults
from openagi.utils.yamlParse import read_from_env

g_num_of_HGI = 0
lock = threading.Lock()

def getToolExecutionResults(
    agentName, role, goal, backstrory, task, capability, tools_list, llm_api
):
    if capability == "search_executor":
        indices = search_string_in_list(tools_list, "duckduckgo-search")
        if indices:
            results = getDuckduckgoSearchResults(goal + task)
            logging.info(f"executed duckduck search and results: {results}")
            return results
    else:
        return NotImplementedError("tool_execution to be implemtned")


def search_string_in_list(my_list, target_string):
    """
    Search for a string in a list.

    Parameters:
    - my_list (list): The list to search through.
    - target_string (str): The string to search for.

    Returns:
    - list: A list of indices where the target string is found.
    """
    indices = []
    for index, item in enumerate(my_list):
        if item == target_string:
            indices.append(index)
    return indices

def Number_of_HGI(my_list):
    """
    Search for a HGI in the list.

    Parameters:
    - my_list (list): The list to search through.

    Returns:
    - list: A list of indices where the target string is found.
    """
    target = "HGI"
    count = 0
    for item in my_list:
        if item == target:
            count += 1
    return count

def setGHGI(value):
    global g_num_of_HGI
    g_num_of_HGI = value
    logging.debug(f"Number of HGI set to: {g_num_of_HGI}")
    
def isLastHGI():
    global g_num_of_HGI
    with lock:
        g_num_of_HGI -= 1
        logging.debug(f"Number of HGI reduced to: {g_num_of_HGI}")
        if g_num_of_HGI == 0:
            return True
        else:
            return False

def ExaAdvToolSetup():
    exa = Exa(api_key=read_from_env("EXA_API_KEY", raise_exception=True))

    @tool
    def search(query: str, include_domains=None, start_published_date=None):
        """Search for a webpage based on the query.
        Set the optional include_domains (list[str]) parameter to restrict the search to a list of domains.
        Set the optional start_published_date (str) parameter to restrict the search to documents published after the date (YYYY-MM-DD).
        """
        return exa.search_and_contents(
            f"{query}",
            use_autoprompt=True,
            num_results=read_from_env("EXA_NUM_SEARCH_RESULTS", raise_exception=True),
            include_domains=include_domains,
            start_published_date=start_published_date,
        )

    @tool
    def find_similar(url: str):
        """Search for webpages similar to a given URL.
        The url passed in should be a URL returned from `search`.
        """
        return exa.find_similar_and_contents(url, num_results=5)

    @tool
    def get_contents(ids: list[str]):
        """Get the contents of a webpage.
        The ids passed in should be a list of ids returned from `search`.
        """
        return exa.get_contents(ids)

    tools = [search, get_contents, find_similar]
    return tools
