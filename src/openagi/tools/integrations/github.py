import logging
import os

from langchain.agents import (
    AgentType,
    initialize_agent,
)
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper
from pydantic import BaseModel, Field

from openagi.tools.base import BaseTool, tool
from openagi.utils.yamlParse import read_yaml_config


def github_toolkit(searchString, llm):
    os.environ["GITHUB_APP_ID"] = read_yaml_config("GITHUB_APP_ID")
    os.environ["GITHUB_APP_PRIVATE_KEY"] = read_yaml_config("GITHUB_APP_PRIVATE_KEY")
    os.environ["GITHUB_REPOSITORY"] = read_yaml_config("GITHUB_REPOSITORY")
    github = GitHubAPIWrapper()
    toolkit = GitHubToolkit.from_github_api_wrapper(github)
    tools = toolkit.get_tools()
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    result = agent.run(searchString)
    logging.debug(result)
    return result


class GithubInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class GithubOutputSchema(BaseModel):
    response: str = Field(
        description="Response from the agent regarding action performed by Github."
    )


class GithubSearchTool(BaseTool):
    name: str = "GithubSearch Tool"
    description: str = "A tool which can be used to retrieve information regarding respective repository like code changes, commits, active PRs, issues, etc by using natural language."

    @tool(args_schema=GithubInputSchema, output_schema=GithubOutputSchema)
    def _run(self, search_str: str = None):
        return github_toolkit(searchString=search_str, llm=self.llm.llm)
