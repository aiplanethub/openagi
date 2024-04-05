import logging

from langchain.agents import (
    AgentExecutor,
    OpenAIFunctionsAgent,
)
from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field

from openagi.tools.base import BaseTool, tool
from openagi.tools.utils import ExaAdvToolSetup


def exaSearch(searchString, llm):
    tools = ExaAdvToolSetup()
    system_message = SystemMessage(
        content="You are a web researcher who answers user questions within the context length by looking up information on the internet and retrieving contents of helpful documents. Cite your sources."
    )

    agent_prompt = OpenAIFunctionsAgent.create_prompt(system_message)
    agent = OpenAIFunctionsAgent(llm=llm.llm, tools=tools, prompt=agent_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    results = agent_executor.run(searchString)
    logging.debug(results)
    return results


class exaSearchInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class exaSearchOutputSchema(BaseModel):
    response: str = Field(
        description="Response from the agent regarding action performed by exaSearch."
    )


class ExaSearchTool(BaseTool):
    name: str = "exaSearchSearch Tool"
    description: str = "A tool which can be used to do a Exa Search."

    @tool(args_schema=exaSearchInputSchema, output_schema=exaSearchOutputSchema)
    def _run(self, search_str: str = None):
        return exaSearch(searchString=search_str, llm=self.llm)
