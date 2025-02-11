import json
from typing import Any
from openagi.actions.base import ConfigurableAction
from pydantic import Field
from langchain.agents import initialize_agent, load_tools
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
import logging
import warnings
import os
from langchain_openai import ChatOpenAI

class DallEImageGenerator(ConfigurableAction):
    """Use this Action to generate images using DALL·E."""

    name: str = Field(
        default_factory=str,
        description="DallEImageGenerator Action to generate an image using OpenAI's DALL·E model.",
    )
    description: str = Field(
        default_factory=str,
        description="This action is used to create images based on textual descriptions using the DALL·E model.",
    )

    query: Any = Field(
        default_factory=str,
        description="User query, a string, describing the image to be generated.",
    )
    
    def _get_dalle_tool(self):
        tools = load_tools(["dalle-image-generator"])
        if 'OPENAI_API_KEY' not in os.environ:
            warnings.warn(
                "Dall-E expects to OPENAI_API_KEY. Please add it inside OPENAI_API_KEY environment.",
                DeprecationWarning,
                stacklevel=2
            )
            return json.dumps({"error": "Invalid or missing API key."})
        return initialize_agent(tools, llm=ChatOpenAI(), agent="zero-shot-react-description", verbose=True)

    def execute(self):
        logging.info(f"Generating image for prompt: {self.query}")
        agent = self._get_dalle_tool()
        
        try:
            result = DallEAPIWrapper().run(agent.run(self.query))
            return json.dumps(result)

        except Exception as e:
            logging.error(f"Error generating image: {str(e)}")
            return json.dumps({"error": f"Failed to generate image: {str(e)}"})
