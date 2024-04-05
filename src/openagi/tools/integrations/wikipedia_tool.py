import logging

from langchain_community.tools import (
    WikipediaQueryRun,
)
from langchain_community.utilities import WikipediaAPIWrapper
from pydantic import BaseModel, Field

from openagi.tools.base import BaseTool, tool


def wikipediaTool(searchString):
    api_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=10000)
    tool = WikipediaQueryRun(api_wrapper=api_wrapper)
    results = tool.run(searchString)
    logging.debug(results)
    return results


class WikipediaToolInputSchema(BaseModel):
    search_str: str = Field(description="Query used to search the Wikipedia API")


class WikipediaToolOutputSchema(BaseModel):
    response: str = Field(description="Response from the Wikipedia tool.")


class WikipediaTool(BaseTool):
    name: str = "Wikipedia Tool"
    description: str = (
        "A tool designed to Tool that searches the Wikipedia API for a specific query."
    )

    @tool(args_schema=WikipediaToolInputSchema, output_schema=WikipediaToolOutputSchema)
    def _run(self, search_str: str = None):
        return wikipediaTool(searchString=search_str)
