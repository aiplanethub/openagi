import logging

from langchain_community.llms import Ollama
from openagi.agent import AIAgent
from openagi.init_agent import kickOffGenAIAgents
from openagi.llms.base import LLMBaseModel, LLMConfigModel
from openagi.tools.integrations import DuckDuckGoSearchTool
from openagi.utils.yamlParse import read_yaml_config


class OllamaConfigModel(LLMConfigModel):
    """Configuration model for OLLAMA."""

    model_name: str


class OllamaModel(LLMBaseModel):
    """Ollama implementation of the LLMBaseModel.

    This class implements the specific logic required to work with Ollama.
    """

    def __init__(self, config: OllamaConfigModel):
        super().__init__(config)

    def load(self):
        """Initializes the Ollama instance with configurations."""
        ollama_model = getattr(self.config, "model_name", "llama2")
        print(f">>> {ollama_model=}")
        self.llm = Ollama(model=ollama_model)
        return self.llm

    def run(self, input_text: str):
        """Runs the Ollama model with the provided input text.

        Args:
            input_text: The input text to process.

        Returns:
            The response from Azure's OpenAI service.
        """
        if not self.llm:
            self.load()
        resp = self.llm.invoke(input_text)
        return resp

    @staticmethod
    def load_from_yml_config():
        return OllamaConfigModel(model_name=read_yaml_config("OLLAMA_MODEL_NAME") or "llama2")


def onResultHGI(agentName, result, consumerAgent):
    feedback = "Pass"
    action = "None"
    logging.debug(f"{agentName}:TO:{consumerAgent}-> {result}")
    return result, feedback, action


# Example Usage:
if __name__ == "__main__":
    AgentObjects = []

    AgentObjects = [
        AIAgent(
            agentName="RESEARCHER",  # name
            role="RESEARCH EXPERT",  # role
            goal="search for latest trends in Carona and Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
            backstory="Has the capability to execute internet search tool",
            capability="search_executor",
            task="search internet for the goal for the trends after first half of 2023",
            output_consumer_agent="WRITER",  # the consumer agent after executing task
            tools_list=[DuckDuckGoSearchTool],
        ),
        AIAgent(
            agentName="WRITER",
            role="SUMMARISING EXPERT",
            goal="summarize input into presentable points",
            backstory="Expert in summarising the given text",
            capability="llm_task_executor",
            task="summarize points to present to health care professionals and general public separately",
            output_consumer_agent="EMAILER",
        ),
        AIAgent(
            agentName="EMAILER",
            role="EMAIL CREATOR",
            goal="composes the email based on the content",
            backstory="Good in composing precise emails",
            capability="llm_task_executor",
            task="composes email based on summary to doctors and general public separately into a file with subject-summary and details",
            output_consumer_agent="HGI",
        ),
    ]
    config = OllamaModel.load_from_yml_config()
    azure_chat_model = OllamaModel(config=config)

    kickOffGenAIAgents(AgentObjects, [AgentObjects[0]], llm=azure_chat_model)
