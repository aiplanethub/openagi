from typing import Any
from openai import AzureOpenAI  # Assuming this import is correct
from openai._exceptions import AuthenticationError

from openagi.exception import OpenAGIException
from openagi.llms.base import LLMBaseModel, LLMConfigModel
from openagi.utils.yamlParse import read_from_env


class AzureChatConfigModel(LLMConfigModel):
    """Configuration model for Azure Chat OpenAI."""

    base_url: str
    deployment_name: str
    model_name: str
    openai_api_version: str
    api_key: str
    


class AzureChatOpenAIModel(LLMBaseModel):
    """Azure's OpenAI service implementation of the LLMBaseModel.

    This class implements the specific logic required to work with Azure's OpenAI service.
    """

    config: Any
    system_prompt: str = "You are an AI assistant"

    def load(self):
        """Initializes the AzureChatOpenAI instance with configurations."""
        self.llm = AzureOpenAI(
            api_version=self.config.openai_api_version,
            azure_endpoint=self.config.base_url,
            azure_deployment=self.config.deployment_name,
            api_key=self.config.api_key
        )
        return self.llm

    def run(self, prompt : Any):
        """Runs the Azure Chat OpenAI model with the provided input text.

        Args:
            input_data: The input text to process.

        Returns:
            The response from Azure's OpenAI service.
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
            model = self.config.model_name
            )
        except AuthenticationError:
            raise OpenAGIException("Authentication failed. Please check your AZURE_OPENAI_API_KEY.")
        return chat_completion.choices[0].message.content


    @staticmethod
    def load_from_env_config() -> AzureChatConfigModel:
        """Loads the AzureChatOpenAI configurations from a YAML file.

        Returns:
            An instance of AzureChatConfigModel with loaded configurations.
        """
        return AzureChatConfigModel(
            base_url=read_from_env("AZURE_BASE_URL", raise_exception=True),
            deployment_name=read_from_env("AZURE_DEPLOYMENT_NAME", raise_exception=True),
            model_name=read_from_env("AZURE_MODEL_NAME", raise_exception=True),
            openai_api_version=read_from_env("AZURE_OPENAI_API_VERSION", raise_exception=True),
            api_key=read_from_env("AZURE_OPENAI_API_KEY", raise_exception=True),
        )
