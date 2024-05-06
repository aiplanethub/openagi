from transformers import pipeline
from openagi.llms.base import LLMBaseModel, LLMConfigModel
from openagi.utils.yamlParse import read_from_env

class HuggingFaceConfigModel(LLMConfigModel):
    """Configuration model for Hugging Face."""

    huggingface_model: str


class HuggingFaceModel(LLMBaseModel):
    """Hugging Face service implementation of the LLMBaseModel.

    This class implements the specific logic required to work with Hugging Face service.
    """

    def __init__(self, config: HuggingFaceConfigModel):
        super().__init__(config)

    def load(self):
        """Initializes the Hugging Face model with configurations."""
        self.llm = pipeline("text-generation", model=self.config.huggingface_model)
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
        return resp[0]['generated_text']

    @staticmethod
    def load_from_yaml_config() -> HuggingFaceConfigModel:
        """Loads the Hugging Face configurations from a YAML file.

        Returns:
            An instance of HuggingFaceConfigModel with loaded configurations.
        """
        return HuggingFaceConfigModel(
            huggingface_model=read_from_env("HUGGINGFACE_MODEL", raise_exception=True),
        )
