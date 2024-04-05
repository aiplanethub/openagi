import logging

from openagi.tools.base import BaseTool, tool
from openagi.tools.custom_tools.custom_tool_db import proxyToolkit
from pydantic import BaseModel, Field


class ProxyInputSchema(BaseModel):
    input_str: str = Field(description="Input to be returned.")


class ProxyOutputSchema(BaseModel):
    response: str = Field(description="Returns the input.")


class ProxyTool(BaseTool):
    name: str = "Proxy Tool"
    description: str = "A tool that returns the input."

    @tool(args_schema=ProxyInputSchema, output_schema=ProxyOutputSchema)
    def _run(self, input_str: str = None):
        logging.debug(f"Proxy tool called with some input of length {len(input_str)}.")
        print("custom tool executed")
        return proxyToolkit(input_str)
