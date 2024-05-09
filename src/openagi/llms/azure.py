from typing import Any
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI  # Assuming this import is correct

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

    # def __init__(self, config: AzureChatConfigModel):
    #     super().__init__(config)

    def load(self):
        """Initializes the AzureChatOpenAI instance with configurations."""
        self.llm = AzureChatOpenAI(
            azure_deployment=self.config.deployment_name,
            model_name=self.config.model_name,
            openai_api_version=self.config.openai_api_version,
            openai_api_key=self.config.api_key,
            azure_endpoint=self.config.base_url,
        )
        return self.llm

    def run(self, input_data: str):
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
        message = HumanMessage(content=input_data)
        resp = self.llm([message])
        return resp.content

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
