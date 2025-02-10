from openagi.exception import OpenAGIException
from openagi.llms.base import LLMBaseModel, LLMConfigModel
from openagi.utils.yamlParse import read_from_env
from typing import Any, Optional
from langchain_core.messages import HumanMessage

try:
    from langchain_sambanova import ChatSambaNovaCloud
except ImportError:
    raise OpenAGIException("Install langchain-sambanova with cmd `pip install langchain-sambanova`")

class SambaNovaConfigModel(LLMConfigModel):
    """Configuration model for SambaNova."""
    
    sambanova_api_key: str
    base_url: str
    project_id: str
    model: str = "Meta-Llama-3.3-70B-Instruct"
    temperature: float = 0.7
    max_tokens: int = 1024
    top_p: float = 0.01
    streaming: bool = False

class SambaNovaModel(LLMBaseModel):
    """SambaNova implementation of the LLMBaseModel."""
    
    config: Any

    def load(self):
        """Initializes the SambaNova client with configurations."""
        self.llm = ChatSambaNovaCloud(
            base_url=self.config.base_url,
            project_id=self.config.project_id,
            api_key=self.config.sambanova_api_key,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            top_p=self.config.top_p,
            streaming=self.config.streaming
        )
        return self.llm

    def run(self, input_data: str):
        """Processes input using SambaNova model."""
        if not self.llm:
            self.load()
        message = HumanMessage(content=input_data)
        resp = self.llm([message])
        return resp.content

    @staticmethod
    def load_from_env_config() -> SambaNovaConfigModel:
        """Loads configurations from environment variables."""
        return SambaNovaConfigModel(
            sambanova_api_key=read_from_env("SAMBANOVA_API_KEY", raise_exception=True),
            base_url=read_from_env("SAMBANOVA_BASE_URL", raise_exception=True),
            project_id=read_from_env("SAMBANOVA_PROJECT_ID", raise_exception=True),
            model=read_from_env("SAMBANOVA_MODEL", default="Meta-Llama-3.3-70B-Instruct"),
            temperature=float(read_from_env("SAMBANOVA_TEMPERATURE", default=0.7)),
            max_tokens=int(read_from_env("SAMBANOVA_MAX_TOKENS", default=1024)),
            top_p=float(read_from_env("SAMBANOVA_TOP_P", default=0.01)),
            streaming=bool(read_from_env("SAMBANOVA_STREAMING", default=False))
        )