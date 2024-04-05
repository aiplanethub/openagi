import os

from langchain.agents import (
    AgentType,
    initialize_agent,
    load_tools,
)
from pydantic import BaseModel, Field

from openagi.tools.base import BaseTool, tool
from openagi.utils.yamlParse import read_yaml_config


def googleFinanceStockSearch(searchString, llm):
    os.environ["SERPAPI_API_KEY"] = read_yaml_config("SERPER_API_KEY", raise_exception=True)
    os.environ["SERP_API_KEY"] = read_yaml_config("SERPER_API_KEY", raise_exception=True)
    tools = load_tools(["google-scholar", "google-finance"], llm=llm)
    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False
    )
    results = agent.run(searchString)
    return results


class GoogleFinanceStockInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class GoogleFinanceStockOutputSchema(BaseModel):
    response: str = Field(description="Response from the GoogleFinanceStockSearchtool engine.")


class GoogleFinanceSearchTool(BaseTool):
    name: str = "GoogleFinanceStockSearch Tool"
    description: str = (
        "A tool that uses the Google Finance Tool to get information from the Google Finance page"
    )

    @tool(args_schema=GoogleFinanceStockInputSchema, output_schema=GoogleFinanceStockOutputSchema)
    def _run(self, search_str: str = None):
        googleFinanceStockSearch(searchString=search_str, llm=self.llm.llm)
