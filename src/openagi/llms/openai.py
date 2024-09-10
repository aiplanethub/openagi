import logging
from typing import Any
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from openagi.llms.base import LLMBaseModel, LLMConfigModel
from openagi.utils.yamlParse import read_from_env


class OpenAIConfigModel(LLMConfigModel):
    """Configuration model for OpenAI."""

    model_name: str = "gpt-4o"
    openai_api_key: str


class OpenAIModel(LLMBaseModel):
    """OpenAI service implementation of the LLMBaseModel.

    This class implements the specific logic required to work with OpenAI service.
    """

    config: Any

    def load(self):
        """Initializes the OpenAI instance with configurations."""
        self.llm = ChatOpenAI(
            openai_api_key=self.config.openai_api_key,
            model_name=self.config.model_name,
        )
        return self.llm

    def run(self, input_text: str):
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
        message = HumanMessage(content=input_text)
        resp = self.llm([message])
        return resp.content

    @staticmethod
    def load_from_env_config() -> OpenAIConfigModel:
        """Loads the OpenAI configurations from a YAML file.

        Returns:
            An instance of OpenAIConfigModel with loaded configurations.
        """
        return OpenAIConfigModel(
            openai_api_key=read_from_env("OPENAI_API_KEY", raise_exception=True),
        )
