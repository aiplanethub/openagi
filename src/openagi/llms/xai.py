import logging
from typing import Any
from openai import OpenAI
from openai._exceptions import AuthenticationError

from openagi.exception import OpenAGIException
from openagi.llms.base import LLMBaseModel, LLMConfigModel
from openagi.utils.yamlParse import read_from_env


class XAIConfigModel(LLMConfigModel):
    """Configuration model for Grok X-AI"""

    xai_api_key: str
    model_name: str = "grok-beta"
    base_url: str = "https://api.x.ai/v1"
    system_prompt: str = "You are an AI assistant. Use the supplied tools to assist the user."


class XAIModel(LLMBaseModel):
    """XAI- GROK service implementation of the LLMBaseModel.

    This class implements the specific logic required to work with XAI service.
    """

    config: Any
    system_prompt: str = "You are an AI assistant"

    def load(self):
        """Initializes the XAI instance with configurations."""
        self.llm = OpenAI(
            api_key = self.config.xai_api_key,
            base_url = self.config.base_url
        )
        return self.llm

    def run(self, prompt : Any):
        """Runs the XAI model with the provided input text.

        Args:
            input_text: The input text to process.

        Returns:
            The response from XAI service.
        """
        logging.info(f"Running LLM - {self.__class__.__name__}")
        if not self.llm:
            self.load()
        if not self.llm:
            raise ValueError("`llm` attribute not set.")
        try:
            chat_completion = self.llm.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"{self.system_prompt}",
                },
                {
                    "role": "user",
                    "content": f"{prompt}",
                },
                       ],
            model=self.config.model_name
            )
        except AuthenticationError:
            raise OpenAGIException("Authentication failed. Please check your XAI_API_KEY.")
        return chat_completion.choices[0].message.content

    @staticmethod
    def load_from_env_config() -> XAIConfigModel:
        """Loads the XAI configurations from a YAML file.

        Returns:
            An instance of XAIConfigModel with loaded configurations.
        """
        return XAIConfigModel(
            xai_api_key=read_from_env("XAI_API_KEY", raise_exception=True),
        )
