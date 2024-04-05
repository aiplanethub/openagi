import logging
import os

from langchain_community.utilities import GoogleSerperAPIWrapper
from pydantic import BaseModel, Field

from openagi.tools.base import BaseTool, tool
from openagi.utils.yamlParse import read_yaml_config


class SerperSpecificInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


def getSerperScrapeForSpecificTypeAndPeriod(searchString, type="news", tbs="qdr:m"):
    os.environ["SERPAPI_API_KEY"] = read_yaml_config("SERPER_API_KEY", raise_exception=True)
    search = GoogleSerperAPIWrapper(type=type, tbs=tbs)
    logging.debug(f"searchString: {searchString}, type: {type}, tbs: {tbs}")
    output = search.results(searchString)
    return output


class SerperSpecificOutputSchema(BaseModel):
    response: str = Field(
        description="Response from the agent regarding action performed by SerperSpecific."
    )


class SerperSpecificSearchTool(BaseTool):
    name: str = "SerperSpecificSearch Tool"
    description: str = "A tool which can be used to scrape information from the search engine for a specific type and period using natural language"

    @tool(args_schema=SerperSpecificInputSchema, output_schema=SerperSpecificOutputSchema)
    def _run(self, search_str: str = None):
        return getSerperScrapeForSpecificTypeAndPeriod(searchString=search_str)
