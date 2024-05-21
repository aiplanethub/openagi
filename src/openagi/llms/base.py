from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class LLMConfigModel(BaseModel):
    """Base configuration model for all LLMs.

    This class can be extended to include more fields specific to certain LLMs.
    """

    class Config:
        protected_namespaces = ()

    pass  # Common fields could be defined here, if any.


class LLMBaseModel(BaseModel):
    """Abstract base class for language learning models.

    Attributes:
        config: An instance of LLMConfigModel containing configuration.
        llm: Placeholder for the actual LLM instance, to be defined in subclasses.
    """

    config: Any
    llm: Any = None

    @abstractmethod
    def load(self):
        """Initializes the LLM instance with configurations."""
        pass

    @abstractmethod
    def run(self, input_data: Any):
        """Interacts with the LLM service using the provided input.

        Args:
            input_data: The input to process by the LLM. The format can vary.

        Returns:
            The result from processing the input data through the LLM.
        """
        pass

    @staticmethod
    @abstractmethod
    def load_from_env_config():
        """Loads configuration values from a YAML file."""
        pass
