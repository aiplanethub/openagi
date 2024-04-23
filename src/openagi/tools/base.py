from typing import Any, Callable, Type

from pydantic import BaseModel, Field
import asyncio
from openagi.llms.base import LLMBaseModel


def tool(args_schema: Type[BaseModel], output_schema: Type[BaseModel] = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        # Ensure we're accessing the correct attribute for Pydantic fields
        func.description = func.__doc__
        func.args = {
            field_name: field.description
            for field_name, field in args_schema.model_fields.items()
        }
        func.output_schema = {
            field_name: field.description
            for field_name, field in output_schema.model_fields.items()
        }

        def wrapper(self, *args, **kwargs) -> Any:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return func(self, *args, **kwargs)

        # Attach metadata to the wrapper function to ensure it's accessible
        wrapper.args = func.args
        wrapper.output_schema = func.output_schema
        return wrapper

    return decorator


class BaseToolInputSchema(BaseModel):
    data: str = Field(description="Data to be passed")


class BaseToolOutputSchema(BaseModel):
    response: str = Field(description="Data returned from the tool")


class BaseTool:
    """Baseclass for tools"""

    name: str = "Hello"
    description: str = "Base tool description"
    llm: LLMBaseModel = None

    @tool(args_schema=BaseToolInputSchema, output_schema=BaseToolOutputSchema)
    def _run(self, data: str):
        """Method description."""
        raise NotImplementedError

    @classmethod
    def get_tool_info(cls):
        tool_info = {
            "tool_name": cls.name,
            "description": cls.description,
            "args": cls._run.args if hasattr(cls._run, "args") else {},
            "output": (cls._run.output_schema if hasattr(cls._run, "output_schema") else None),
            "cls": {
                "kls": cls.__name__,
                "module": cls.__module__,
            },
        }
        return tool_info
