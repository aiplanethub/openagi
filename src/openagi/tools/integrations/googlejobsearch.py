import logging
import os
import pprint

from langchain_community.tools.google_jobs import GoogleJobsQueryRun
from langchain_community.utilities.google_jobs import GoogleJobsAPIWrapper
from pydantic import BaseModel, Field

from openagi.tools.base import BaseTool, tool


def googleJobsSearch(input):
    os.environ["SERP_API_KEY"] = os.environ.get("SERP_API_KEY")
    tool = GoogleJobsQueryRun(api_wrapper=GoogleJobsAPIWrapper())
    results = tool.run(input)
    pprint.pp(results)
    logging.debug(results)
    return results


class GoogleJobsInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class GoogleJobsOutputSchema(BaseModel):
    response: str = Field(description="Response from the GoogleJobsQuery engine.")


class GoogleJobSearchTool(BaseTool):
    name: str = "GoogleJobsSearch Tool"
    description: str = (
        "A tool that can be used to access the GoogleJobs API and search for jobs online "
    )

    @tool(args_schema=GoogleJobsInputSchema, output_schema=GoogleJobsOutputSchema)
    def _run(self, search_str: str = None):
        googleJobsSearch(searchString=search_str)
