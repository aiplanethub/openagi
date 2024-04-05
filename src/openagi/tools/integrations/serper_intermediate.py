from pydantic import BaseModel, Field

from openagi.tools.base import BaseTool, tool


def googleSerperSearchIntermediateQuestions(searchString, llm):
    search = GoogleSerperAPIWrapper()
    tools = [
        Tool(
            name="Intermediate Answer",
            func=search.run,
            description="useful for when you need to ask with search",
        )
    ]
    self_ask_with_search = initialize_agent(
        tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=False
    )
    results = self_ask_with_search.run(searchString)
    finalResult = pprint.pp(results)
    logging.debug(finalResult)
    return results


class SerperIntermediateInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class SerperIntermediateOutputSchema(BaseModel):
    response: str = Field(
        description="Response from the agent regarding action performed by SerperIntermediate."
    )


class SerperIntermediateSearchTool(BaseTool):
    name: str = "SerperIntermediateSearch Tool"
    description: str = "A tool which can be useful for when you need to ask with search."

    @tool(args_schema=SerperIntermediateInputSchema, output_schema=SerperIntermediateOutputSchema)
    def _run(self, search_str: str = None):
        from openagi.tools.tools_db import googleSerperSearchIntermediateQuestions

        return googleSerperSearchIntermediateQuestions(searchString=search_str)
