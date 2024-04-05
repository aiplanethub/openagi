from langchain import hub
from langchain.agents import (
    AgentExecutor,
    create_openai_functions_agent,
)
from langchain_community.agent_toolkits import (
    GmailToolkit,
)
from pydantic import BaseModel, Field

from openagi.tools.base import BaseTool, tool
from openagi.utils.yamlParse import read_yaml_config


def gmail_toolkit(searchString, llm):
    credentials = read_yaml_config("GMAIL_CREDS")
    toolkit = GmailToolkit()
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    instructions = "Use the Gmail API to search for emails in your inbox and return the results."
    prompt = base_prompt.partial(instructions=instructions)
    agent = create_openai_functions_agent(llm, toolkit.get_tools(), prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=toolkit.get_tools(),
        verbose=True,
    )
    result = agent_executor.invoke({"input": searchString})
    return result


class GmailInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class GmailOutputSchema(BaseModel):
    response: str = Field(
        description="Response from the agent regarding action performed by gmail."
    )


class GmailSearchTool(BaseTool):
    name: str = "GmailSearch Tool"
    description: str = (
        "A tool which can be used to perform actions on gmail by using natural language"
    )

    @tool(args_schema=GmailInputSchema, output_schema=GmailOutputSchema)
    def _run(self, search_str: str = None):
        return gmail_toolkit(searchString=search_str, llm=self.llm.llm)
