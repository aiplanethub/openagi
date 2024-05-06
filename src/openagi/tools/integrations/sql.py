import logging

from langchain_community.agent_toolkits import (
    create_sql_agent,
)
from langchain_community.utilities.sql_database import SQLDatabase
from pydantic import BaseModel, Field

from openagi.tools.base import BaseTool, tool
from openagi.utils.yamlParse import read_from_env


def sql_toolkit(searchString, llm):
    sqlLiteDBName = read_from_env("sqlLiteDBName")
    db = SQLDatabase.from_uri(sqlLiteDBName)
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
    result = agent_executor.invoke(searchString)
    logging.debug(result)
    return result


class SqlInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class SqlOutputSchema(BaseModel):
    response: str = Field(
        description="Response from the agent regarding action performed by Sql."
    )


class SqlSearchTool(BaseTool):
    name: str = "SqlSearch Tool"
    description: str = "A tool which can be used to retrieve information regarding respective repository like code changes, commits, active PRs, issues, etc by using natural language."

    @tool(args_schema=SqlInputSchema, output_schema=SqlOutputSchema)
    def _run(self, search_str: str = None):
        from openagi.tools.tools_db import sql_toolkit

        return sql_toolkit(searchString=search_str)
