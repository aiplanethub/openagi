from langchain.agents import (
    AgentType,
    initialize_agent,
)
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from pydantic import BaseModel, Field

from openagi.tools.base import BaseTool
from openagi.tools.base import tool as tool_decorator


def yahooFinanceNews(searchString, llm):
    tools = [YahooFinanceNewsTool()]
    tool = initialize_agent(
        tools,
        llm,
        handle_parsing_errors=True,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
    )
    results = tool.run(searchString)
    return results


class YahooFinanceInputSchema(BaseModel):
    search_str: str = Field(description="Query used to search for news on Yahoo Finance")


class YahooFinanceOutputSchema(BaseModel):
    response: str = Field(description="Response from the YahooFinance tool.")


class YahooFinanceTool(BaseTool):
    name: str = "Yahoo Finance News Tool"
    description: str = "A tool designed to explore financial news articles on Yahoo Finance."

    @tool_decorator(args_schema=YahooFinanceInputSchema, output_schema=YahooFinanceOutputSchema)
    def _run(self, search_str: str = None):
        from openagi.tools.tools_db import yahooFinanceNews

        yahooFinanceNews(searchString=search_str)
