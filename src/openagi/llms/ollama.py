from typing import Any
from langchain_core.messages import HumanMessage
from openagi.exception import OpenAGIException
from openagi.llms.base import LLMBaseModel, LLMConfigModel
from openagi.utils.yamlParse import read_from_env

try:
   from langchain_ollama.chat_models import ChatOllama
except ImportError:
  raise OpenAGIException("Install langchain groq with cmd `pip install langchain-ollama`")


class OllamaConfigModel(LLMConfigModel):
    """Configuration model for Ollama model"""

    model_name:str = "mistral"

class OllamaModel(LLMBaseModel):
    """Ollama LLM implementation of the LLMBaseModel.

    This class implements the specific logic required to work with Ollama LLM that runs model locally on CPU.
    """

    config: Any

    def load(self):
        """Initializes the Ollama instance with configurations."""
        self.llm = ChatOllama(
            model = self.config.model_name,
            temperature=0   
        )
        return self.llm

    def run(self, input_data: str):
        """Runs the Ollama model with the provided input text.

        Args:
            input_data: The input text to process.

        Returns:
            The response from Ollama LLM service.
        """
        if not self.llm:
            self.load()
        if not self.llm:
            raise ValueError("`llm` attribute not set.")
        message = HumanMessage(content=input_data)
        resp = self.llm([message])
        return resp.content

    @staticmethod
    def load_from_env_config() -> OllamaConfigModel:
        """Loads the Ollama configurations from a YAML file.

        Returns:
            An instance of OllamaConfigModel with loaded configurations.
        """
        return OllamaConfigModel(
            model_name = read_from_env("OLLAMA_MODEL",raise_exception=True),
        )
