from openagi.tools.base import BaseTool


class GoogleSerperSearchTool(BaseTool):
    name = "Google Serper Search"

    def _run(self, search_str: str = None):
        from openagi.tools.tools_db import getSerperScrape

        return getSerperScrape(searchString=search_str)
