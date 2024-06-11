from openagi.llms.base import LLMBaseModel, LLMConfigModel
from openagi.utils.yamlParse import read_from_env
from typing import Any
from langchain_core.messages import HumanMessage

try:
   from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
  raise OpenAGIException("Install langchain Google Gemini with cmd `pip install langchain-google-genai`")

class GeminiConfigModel(LLMConfigModel):
    """Configuration model for Gemini Chat model."""

    google_api_key: str
    model_name: str = "gemini-pro"
    temperature: float = 0.1

class GeminiModel(LLMBaseModel):
    """Chat Gemini Model implementation of the LLMBaseModel.

    This class implements the specific logic required to work with Chat Google Generative - Gemini Model.
    """

    config: Any

    def load(self):
        """Initializes the GeminiModel instance with configurations."""
        self.llm = ChatGoogleGenerativeAI(
            google_api_key = self.config.google_api_key,
            model = self.config.model_name,
            temperature= self.config.temperature
        )
        return self.llm
    
    def run(self, input_data: str):
        """Runs the Chat Gemini model with the provided input text.

        Args:
            input_data: The input text to process.

        Returns:
            The response from Gemini model with low inference latency.
        """
        if not self.llm:
            self.load()
        if not self.llm:
            raise ValueError("`llm` attribute not set.")
        message = HumanMessage(content=input_data)
        resp = self.llm([message])
        return resp.content
    
    @staticmethod
    def load_from_env_config() -> GeminiConfigModel:
        """Loads the GeminiModel configurations from a env file.

        Returns:
            An instance of GeminiConfigModel with loaded configurations.
        """
        return GeminiConfigModel(
            google_api_key = read_from_env("GOOGLE_API_KEY", raise_exception=True),
            model_name = read_from_env("Gemini_MODEL",raise_exception=True),
            temperature=read_from_env("Gemini_TEMP",raise_exception=True)
        )