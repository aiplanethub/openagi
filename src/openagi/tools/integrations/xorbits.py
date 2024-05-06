import logging

import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_xorbits_agent
from pydantic import BaseModel, Field

from openagi.tools.base import BaseTool, tool
from openagi.utils.yamlParse import read_from_env


def xorbits_toolkit(searchString, llm):
    xorbotsCSVFileName = read_from_env("xorbotsCSVFileName")
    data = pd.read_csv(xorbotsCSVFileName)
    agent = create_xorbits_agent(llm, data, verbose=True, handle_parsing_errors=True)
    result = agent.run(searchString)
    logging.debug(result)
    return result


class XorbitsInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class XorbitsOutputSchema(BaseModel):
    response: str = Field(
        description="Response from the agent regarding action performed by Xorbits."
    )


class XorbitsSearchTool(BaseTool):
    name: str = "XorbitsSearch Tool"
    description: str = "A tool which can be used to retrieve information from files by performing pandas or numpy code by using natural language."

    @tool(args_schema=XorbitsInputSchema, output_schema=XorbitsOutputSchema)
    def _run(self, search_str: str = None):
        return xorbits_toolkit(searchString=search_str)
