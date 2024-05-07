import logging
from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.tools.integrations import DuckDuckGoSearchTool

def onResultHGI(agentName, result, consumerAgent):
    feedback = "Pass"
    action = "None"
    logging.debug(f"{agentName}:TO:{consumerAgent}-> {result}")
    return result, feedback, action

if __name__ == "__main__":
    agent_name = ["RESEARCHER", "WRITER", "EMAILER"]
    agent_list = [
        Agent(
            agentName=agent_name[0],
            aggregator=0,  # Number of messages that need to be aggregated
            onAggregationAction=None,  # Funtion to be called for aggregation
            creator=None,  # Used to indicate dynamic agent's object name ex:Agent2,3
            role="RESEARCHER",  # Role
            feedback=False,  # Boolean
            goal="search for latest trends in COVID-19 treatment that includes medicines, physical exercises, overall management and prevention aspects",
            backstory="backstory",
            capability="search_executor",
            agent_type="STATIC",  # Indicates it will get instantiated as part of system initial bring up
            multiplicity=0,  # Number indicates concurrent requests that the agent can support
            task="search internet for the goal for the trends in 2H 2023 onwards",
            output_consumer_agent=[agent_name[1]],  # The consumer agent after executing task
            HGI_Intf=onResultHGI,  # Callback function for human intervention- human tool
            llm_api=None,  # LLM to be used
            llm_resp_timer_value=20,  # LLM timer
            tools_list=[DuckDuckGoSearchTool],  # Tool
        ),
        Agent(
            agentName=agent_name[1],
            aggregator=0,
            onAggregationAction=None,
            creator=None,
            role="SUMMARISER",
            feedback=False,
            goal="summarize input into presentable points",
            backstory="backstory",
            capability="llm_task_executor",
            agent_type="STATIC",
            multiplicity=0,
            task="summarize points to present to health care professionals and general public separately",
            output_consumer_agent=[agent_name[2]],
            HGI_Intf=onResultHGI,
            llm_resp_timer_value=130,
            tools_list=[],
        ),
        Agent(
            agentName=agent_name[2],
            aggregator=0,
            onAggregationAction=None,
            creator=None,
            role="EMAILER",
            feedback=False,
            goal="composes the email based on the content",
            backstory="An email content composer that can be used to compose email",
            capability="llm_task_executor",
            agent_type="STATIC",
            multiplicity=0,
            task="compose email based on summary received to doctors and general public separately with subject-summary and details",
            output_consumer_agent=["HGI"],
            HGI_Intf=onResultHGI,
            llm_resp_timer_value=130,
            tools_list=[],
        ),
    ]
    config = AzureChatOpenAIModel.load_from_env_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffAgents(agent_list, [agent_list[0]], llm=azure_chat_model)
