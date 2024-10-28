from typing import Any
try:
   from groq import Groq
except ImportError:
  raise OpenAGIException("Install groq using 'pip install groq' ")
from groq._exceptions import AuthenticationError

from openagi.exception import OpenAGIException
from openagi.llms.base import LLMBaseModel, LLMConfigModel
from openagi.utils.yamlParse import read_from_env

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
    system_prompt: str = "You are an AI assistant"

    def load(self):
        """Initializes the GroqModel instance with configurations."""
        self.llm = Groq(
                    api_key = self.config.groq_api_key
                )
        return self.llm
    
    def run(self,prompt:Any):
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
            model = self.config.model_name,
            temperature = self.config.temperature

            )
        except AuthenticationError:
            raise OpenAGIException("Authentication failed. Please check your GROQ_API_KEY.")
        return chat_completion.choices[0].message.content

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
