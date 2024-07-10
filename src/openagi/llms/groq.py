from typing import Any
from langchain_core.messages import HumanMessage
from openagi.exception import OpenAGIException
from openagi.llms.base import LLMBaseModel, LLMConfigModel
from openagi.utils.yamlParse import read_from_env

try:
   from langchain_groq import ChatGroq
except ImportError:
  raise OpenAGIException("Install langchain groq with cmd `pip install langchain-groq`")

class GroqConfigModel(LLMConfigModel):
    """Configuration model for Groq Chat model."""

    groq_api_key: str
    model_name: str = "mixtral-8x7b-32768"
    temperature: float = 0.1

class GroqModel(LLMBaseModel):
    """Chat Groq Model implementation of the LLMBaseModel.

    This class implements the specific logic required to work with Chat Groq Model.
    """

    config: Any

    def load(self):
        """Initializes the GroqModel instance with configurations."""
        self.llm = ChatGroq(
            model_name = self.config.model_name,
            groq_api_key = self.config.groq_api_key,
            temperature = self.config.temperature
        )
        return self.llm
    
    def run(self, input_data: str):
        """Runs the Chat Groq model with the provided input text.

        Args:
            input_data: The input text to process.

        Returns:
            The response from Groq model with low inference latency.
        """
        if not self.llm:
            self.load()
        if not self.llm:
            raise ValueError("`llm` attribute not set.")
        message = HumanMessage(content=input_data)
        resp = self.llm([message])
        return resp.content
    
    @staticmethod
    def load_from_env_config() -> GroqConfigModel:
        """Loads the GroqModel configurations from a env file.

        Returns:
            An instance of GroqConfigModel with loaded configurations.
        """
        return GroqConfigModel(
            groq_api_key=read_from_env("GROQ_API_KEY", raise_exception=True),
            model_name = read_from_env("GROQ_MODEL",raise_exception=True),
            temperature=read_from_env("GROQ_TEMP",raise_exception=True)
        )
