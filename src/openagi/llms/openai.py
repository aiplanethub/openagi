import logging
from typing import Any
from openai import OpenAI
from openai._exceptions import AuthenticationError

from openagi.exception import OpenAGIException
from openagi.llms.base import LLMBaseModel, LLMConfigModel
from openagi.utils.yamlParse import read_from_env


class OpenAIConfigModel(LLMConfigModel):
    """Configuration model for OpenAI."""

    model_name: str = "gpt-4o"
    openai_api_key: str
    system_prompt: str = "You are an AI assistant"


class OpenAIModel(LLMBaseModel):
    """OpenAI service implementation of the LLMBaseModel.

    This class implements the specific logic required to work with OpenAI service.
    """

    config: Any
    system_prompt: str = "You are an AI assistant"

    def load(self):
        """Initializes the OpenAI instance with configurations."""
        self.llm = OpenAI(
            api_key=self.config.openai_api_key
        )
        return self.llm

    def run(self, prompt : Any):
        """Runs the OpenAI model with the provided input text.

        Args:
            input_text: The input text to process.

        Returns:
            The response from OpenAI service.
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
            raise OpenAGIException("Authentication failed. Please check your OPENAI_API_KEY.")
        return chat_completion.choices[0].message.content


    @staticmethod
    def load_from_env_config() -> OpenAIConfigModel:
        """Loads the OpenAI configurations from a YAML file.

        Returns:
            An instance of OpenAIConfigModel with loaded configurations.
        """
        return OpenAIConfigModel(
            openai_api_key=read_from_env("OPENAI_API_KEY", raise_exception=True),
        )
