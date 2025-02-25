import json
import logging
import os
import warnings
from typing import Any

from openagi.actions.base import ConfigurableAction
from pydantic import Field
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper

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

    def execute(self):
        logging.info(f"Generating image for prompt: {self.query}")
        if 'OPENAI_API_KEY' not in os.environ:
            warnings.warn(
                "Dall-E expects an OPENAI_API_KEY. Please add it to your environment variables.",
                UserWarning,
                stacklevel=2
            )
            return json.dumps({"error": "Dall-E requires an OPENAI_API_KEY. Please add it to your environment variables."})
        
        try:
            # Use the query directly without the LLM chain
            dalle_wrapper = DallEAPIWrapper()
            result = dalle_wrapper.run(self.query)
            return json.dumps(result)

        except Exception as e:
            logging.error(f"Error generating image: {str(e)}")
            return json.dumps({"error": f"Failed to generate image: {str(e)}"})