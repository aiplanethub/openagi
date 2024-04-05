import logging
import os

from langchain import hub
from langchain.agents import (
    AgentExecutor,
    create_openai_functions_agent,
)
from langchain_community.agent_toolkits.polygon.toolkit import PolygonToolkit
from langchain_community.utilities.polygon import PolygonAPIWrapper
from pydantic import BaseModel, Field

from openagi.tools.base import BaseTool, tool


def polygon_toolkit(searchString, llm):
    os.environ["POLYGON_API_KEY"] = os.environ.get("POLYGON_API_KEY")
    instructions = """You are an assistant."""
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    prompt = base_prompt.partial(instructions=instructions)
    polygon = PolygonAPIWrapper()
    toolkit = PolygonToolkit.from_polygon_api_wrapper(polygon)
    agent = create_openai_functions_agent(llm, toolkit.get_tools(), prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=toolkit.get_tools(),
        verbose=True,
    )
    result = agent_executor.invoke({"input": searchString})
    logging.debug(result)
    return result


class PolygonInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class PolygonOutputSchema(BaseModel):
    response: str = Field(
        description="Response from the agent regarding action performed by Polygon."
    )


class PolygonSearchTool(BaseTool):
    name: str = "PolygonSearch Tool"
    description: str = "A tool which can be used to retrieve information regarding current Stock prices and their historical data using natural language."

    @tool(args_schema=PolygonInputSchema, output_schema=PolygonOutputSchema)
    def _run(self, search_str: str = None):
        return polygon_toolkit(searchString=search_str)
