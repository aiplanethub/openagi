from typing import Any
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

from openagi.llms.base import LLMBaseModel, LLMConfigModel
from openagi.utils.yamlParse import read_from_env

class HuggingFaceConfigModel(LLMConfigModel):
    """Configuration model for Hugging Face."""

    hf_token: str
    model_name: str


class HuggingFaceModel(LLMBaseModel):
    """Hugging Face service implementation of the LLMBaseModel.

    This class implements the specific logic required to work with Hugging Face service.
    """

    def __init__(self, config: HuggingFaceConfigModel):
        super().__init__(config)

    def load(self):
        """Initializes the Hugging Face model with configurations."""
        
        return self.llm

    def run(self, input_text: str):
        """Runs the Hugging Face model with the provided input text.

        Args:
            input_text: The input text to process.

        Returns:
            The response from Hugging Face service.
        """
        if not self.llm:
            self.load()
        if not self.llm:
            raise ValueError("`llm` attribute not set.")
        resp = self.llm(input_text)
        return resp[0]["generated_text"]

    @staticmethod
    def load_from_env_config() -> HuggingFaceConfigModel:
        """Loads the Hugging Face configurations from a YAML file.

        Returns:
            An instance of HuggingFaceConfigModel with loaded configurations.
        """
        return HuggingFaceConfigModel(
            hf_token = read_from_env("HUGGINGFACE_ACCESS_TOKEN",raise_exception=True),
            model_name=read_from_env("HUGGINGFACE_MODEL", raise_exception=True),
        )
