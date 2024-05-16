class DuckDuckGoWrapper():
    """
    pip install duckduckgo-search
    """
    try:
        from duckduckgo_search import DDGS
        client = DDGS()
    except ImportError:
        raise ImportError("In order to use Search Tool from DuckDuckGo, you need to install ")
   
    region: str = "wt-wt"
    safesearch: str = "moderate"
    time: str = "y"
    max_results: int = 4
    backend: str = "api"

    def search_tool(self, query):
        result = self.client.text(
            query,
            region=self.region,
            safesearch=self.safesearch,
            timelimit=self.time,
            max_results=self.max_results,
            backend=self.backend,
        )
        return result