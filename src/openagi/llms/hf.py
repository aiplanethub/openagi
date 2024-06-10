from typing import Any
from langchain_core.messages import HumanMessage
from langchain_community.llms import HuggingFaceHub
from openagi.llms.base import LLMBaseModel, LLMConfigModel
from openagi.utils.yamlParse import read_from_env

class HuggingFaceConfigModel(LLMConfigModel):
    """Configuration model for Hugging Face."""
    api_token: str
    model_name: str = "huggingfaceh4/zephyr-7b-beta"
    temperature: float = 0.1
    max_new_tokens: int = 512

class HuggingFaceModel(LLMBaseModel):
    """Hugging Face service implementation of the LLMBaseModel.

    This class implements the specific logic required to work with Hugging Face service.
    """

    config: Any

    def load(self):
        """Initializes the GroqModel instance with configurations."""
        self.llm = HuggingFaceHub(
            huggingfacehub_api_token = self.config.api_token,
            repo_id= self.config.model_name, 
            model_kwargs={"temperature": self.config.temperature,
                          "max_new_tokens":self.config.max_new_tokens,
                          "repetition_penalty":1.2}
        )
        return self.llm
    
    def run(self, input_data: str):
        """Runs the HuggingFace model with the provided input text.

        Args:
            input_data: The input text to process.

        Returns:
            The response from HuggingFace model.
        """
        if not self.llm:
            self.load()
        if not self.llm:
            raise ValueError("`llm` attribute not set.")
        message = HumanMessage(content=input_data)
        resp = self.llm([message])
        return resp.content

    @staticmethod
    def load_from_env_config() -> HuggingFaceConfigModel:
        """Loads the Hugging Face configurations from a YAML file.

        Returns:
            An instance of HuggingFaceConfigModel with loaded configurations.
        """
        return HuggingFaceConfigModel(
            api_token = read_from_env("HUGGINGFACE_ACCESS_TOKEN",raise_exception=True),
            model_name=read_from_env("HUGGINGFACE_MODEL", raise_exception=True),
            temperature=read_from_env("TEMPERATURE",raise_exception=True),
            max_new_tokens= read_from_env("MAX_NEW_TOKENS",raise_exception=True)
        )