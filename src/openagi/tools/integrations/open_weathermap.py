from pydantic import BaseModel, Field

from openagi.tools.base import BaseTool, tool


class OpenWeatherMapInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class OpenWeatherMapOutputSchema(BaseModel):
    response: str = Field(
        description="Response from the agent regarding action performed by OpenWeatherMap."
    )


class OpenWeatherMapSearchTool(BaseTool):
    name: str = "OpenWeatherMapSearch Tool"
    description: str = "A tool which can be used to retrieve information about weather of any place in the world."

    @tool(args_schema=OpenWeatherMapInputSchema, output_schema=OpenWeatherMapOutputSchema)
    def _run(self, search_str: str = None):
        from openagi.tools.tools_db import open_weather_app

        return open_weather_app(searchString=search_str)
