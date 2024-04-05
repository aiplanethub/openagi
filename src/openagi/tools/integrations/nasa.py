import logging

from langchain.agents import (
    AgentType,
    initialize_agent,
)
from langchain_community.agent_toolkits.nasa.toolkit import NasaToolkit
from langchain_community.utilities.nasa import NasaAPIWrapper
from pydantic import BaseModel, Field

from openagi.tools.base import BaseTool, tool


def nasatool(searchString, llm):
    nasa = NasaAPIWrapper()
    toolkit = NasaToolkit.from_nasa_api_wrapper(nasa)
    agent = initialize_agent(
        toolkit.get_tools(), llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )
    result = agent.invoke(searchString)
    logging.debug(result)
    return result


class NasaInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class NasaOutputSchema(BaseModel):
    response: str = Field(
        description="Response from the agent regarding action performed by Nasa."
    )


class NasaSearchTool(BaseTool):
    name: str = "NasaSearch Tool"
    description: str = "A tool which can be used to retrieve information from Nasa's database like images, videos, documents, etc by using natural language."

    @tool(args_schema=NasaInputSchema, output_schema=NasaOutputSchema)
    def _run(self, search_str: str = None):
        from openagi.tools.tools_db import nasatool

        return nasatool(searchString=search_str)
