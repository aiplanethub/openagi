hdr_azure = """
from openagi.init_agent import kickOffAgents
from openagi.agent import Agent
from openagi.tools.integrations.duckducksearch import DuckDuckGoSearchTool
from openagi.llms.azure import AzureChatOpenAIModel
import logging


def onResultHGI(agentName, result, consumerAgent):
    feedback = "Pass"
    action = "None"
    logging.debug(f"{agentName}:TO:{consumerAgent}-> {result}")
    return result, feedback, action


if __name__ == "__main__":
    """


tail_azure = """config = AzureChatOpenAIModel.load_from_yml_config()
llm = AzureChatOpenAIModel(config=config)
kickOffAgents(agent_list, [agent_list[0]], llm=llm)"""


hdr_openai = """
from openagi.init_agent import kickOffAgents
from openagi.agent import Agent
from openagi.tools.integrations.duckducksearch import DuckDuckGoSearchTool
from openagi.llms import OpenAIModel

import logging


def onResultHGI(agentName, result, consumerAgent):
    feedback = "Pass"
    action = "None"
    logging.debug(f"{agentName}:TO:{consumerAgent}-> {result}")
    return result, feedback, action

if __name__ == "__main__":
    """

tail_openai = """    
config = OpenAIModel.load_from_yml_config()
llm = OpenAIModel(config=config)
kickOffAgents(agent_list, [agent_list[0]], llm=llm)"""
