from typing import Any
from langchain_core.messages import HumanMessage
from openagi.exception import OpenAGIException
from openagi.llms.base import LLMBaseModel, LLMConfigModel
from openagi.utils.yamlParse import read_from_env

try:
    from langchain_cerebras import ChatCerebras
except ImportError:
    raise OpenAGIException("Install langchain-cerebras with cmd `pip install langchain-cerebras`")

class CerebrasConfigModel(LLMConfigModel):
    
     """
    Configuration model for Cerebras.
    Reference: https://cloud.cerebras.ai
    
    Attributes:
        cerebras_api_key (str): API key for Cerebras.
        model_name (str): Name of the model to use. Default is 'llama3.1-8b'.
        temperature (float): Sampling temperature. Default is 0.7.
    
    Note:
        Available models as of December 2024: llama-3.3-70b, llama-3.1-70b, llama-3.1-8b
    """

    cerebras_api_key: str
    model_name: str = "llama3.1-8b"
    temperature: float = 0.7

class CerebrasModel(LLMBaseModel):
    """Cerebras LLM implementation of the LLMBaseModel."""

    config: Any

    def load(self):
        """Initializes the Cerebras LLM instance with configurations."""
        self.llm = ChatCerebras(
            api_key=self.config.cerebras_api_key,
            model_name=self.config.model_name,
            temperature=self.config.temperature
        )
        return self.llm

    def run(self, input_data: str):
        """Runs the Cerebras model with the provided input text."""
        if not self.llm:
            self.load()
        if not self.llm:
            raise ValueError("`llm` attribute not set.")
        message = HumanMessage(content=input_data)
        response = self.llm([message])
        return response.content

    @staticmethod
    def load_from_env_config() -> CerebrasConfigModel:
        """Loads the Cerebras configurations from environment variables."""
        return CerebrasConfigModel(
            cerebras_api_key=read_from_env("CEREBRAS_API_KEY", raise_exception=True),
            model_name=read_from_env("Cerebras_MODEL", raise_exception=False),
            temperature=read_from_env("Cerebras_TEMP", raise_exception=False)
        )
