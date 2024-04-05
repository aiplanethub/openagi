from langchain_community.tools import YouTubeSearchTool
from pydantic import BaseModel, Field

from openagi.tools.base import BaseTool, tool


def getYoutubeSearchResults(searchString):
    tool = YouTubeSearchTool()
    result = tool.run(searchString)
    return result


class YoutubeSearchInputSchema(BaseModel):
    search_str: str = Field(description="Query used to search videos for on Youtube")


class YoutubeSearchOutputSchema(BaseModel):
    response: str = Field(description="Response from the YoutubeSearch tool.")


class YoutubeSearchTool(BaseTool):
    name: str = "YoutubeSearch Tool"
    description: str = (
        "A tool that can be used to search for videos on YouTube based on specific queries."
    )

    @tool(args_schema=YoutubeSearchInputSchema, output_schema=YoutubeSearchOutputSchema)
    def _run(self, search_str: str = None):
        getYoutubeSearchResults(searchString=search_str)
