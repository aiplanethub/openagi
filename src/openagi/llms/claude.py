from openagi.llms.base import LLMBaseModel, LLMConfigModel
from openagi.utils.yamlParse import read_from_env
from typing import Any

from langchain_core.messages import HumanMessage

from openagi.exception import OpenAGIException
try:
   from langchain_anthropic import ChatAnthropic
except ImportError:
  raise OpenAGIException("Install Langchain Anthropic to use Claude LLM `pip install langchain-anthropic`")

class ChatAnthropicConfigModel(LLMConfigModel):
    """
    Configuration model Anthropic model. This provides opus, sonnet SOTA models
    """
    anthropic_api_key: str
    temperature: float = 0.5
    model_name: str = "claude-3-5-sonnet-20240620"

class ChatAnthropicModel(LLMBaseModel):
    """
    Define the Claude LLM from Anthropic using Langchain LLM integration
    """
    config: Any

    def load(self):
        """Initializes the ChatAnthropic instance with configurations."""
        self.llm = ChatAnthropic(
            model_name = self.config.model_name,
            api_key = self.config.anthropic_api_key,
            temperature = self.config.temperature
        )
        return self.llm

    def run(self, input_data: str):
        """
        Runs the Chat Anthropic model with the provided input text.
        Args:
            input_data: The input text to process.
        Returns:
            The response from Anthropic - Claude LLM.
        """

        if not self.llm:
            self.load()
        if not self.llm:
            raise ValueError("`llm` attribute not set.")
        
        message = HumanMessage(content=input_data)
        response = self.llm([message])
        return response.content

    @staticmethod
    def load_from_env_config() -> ChatAnthropicConfigModel:
        """Loads the ChatAnthropic configurations from a env file.

        Returns:
            An instance of ChatAnthropicConfigModel with loaded configurations.
        """
        return ChatAnthropicConfigModel(
            anthropic_api_key = read_from_env("ANTHROPIC_API_KEY", raise_exception=True),
            model_name = read_from_env("CLAUDE_MODEL_NAME",raise_exception=False),
            temperature = read_from_env("TEMPERATURE",raise_exception=False)
        )
