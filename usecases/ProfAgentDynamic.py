import logging

from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.tools.integrations import DuckDuckGoSearchTool, GmailSearchTool


def onResultHGI(agentName, result, consumerAgent):
    feedback = "Pass"
    action = "None"
    logging.debug(f"{agentName}:TO:{consumerAgent}-> {result}")
    return result, feedback, action


if __name__ == "__main__":
    agent_name = ["RESEARCHER", "WRITER", "EMAILER"]
    
    research_agent = Agent(
        agentName=agent_name[0],
        aggregator=0,
        onAggregationAction=None,
        creator=None,
        role="RESEARCHER",
        feedback=False,
        goal="search for latest trends in Carona treatment that includes medicines, physical exercises, overall management and prevention aspects",
        backstory="backstory",
        capability="search_executor",
        agent_type="STATIC",
        multiplicity=0,
        task="search internet for the goal for the trends in 2H 2023 onwards",
        output_consumer_agent=[agent_name[1]],
        HGI_Intf=None,
        llm_resp_timer_value=20,
        tools_list=[DuckDuckGoSearchTool],
    )

    mailer_agent = Agent(
        agentName=agent_name[2],
        aggregator=0,
        onAggregationAction=None,
        creator=None,
        role="EMAILER",
        feedback=False,
        goal="composes the email based on the contenct",
        backstory="backstory",
        capability="llm_task_executor",
        agent_type="DYNAMIC",
        multiplicity=0,
        task="compose email based on summary received from SUMMARIZER agent and send it to user at tanish@aiplanet.com",
        output_consumer_agent=["HGI"],
        HGI_Intf=None,
        llm_resp_timer_value=1300,
        tools_list=[GmailSearchTool],
    )

    writer_agent = Agent(
        agentName=agent_name[1],
        aggregator=0,
        onAggregationAction=None,
        creator=mailer_agent,
        role="SUMMARISER",
        feedback=False,
        goal="summarize input into presentable points",
        backstory="backstory",
        capability="llm_task_executor",
        agent_type="STATIC",
        multiplicity=0,
        task="summarize points to present to health care professionals and general public separately",
        output_consumer_agent=[agent_name[2]],
        HGI_Intf=None,
        llm_resp_timer_value=1030,
        tools_list=[],
    )

    agent_list = [research_agent, writer_agent, mailer_agent]
    config = AzureChatOpenAIModel.load_from_yml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffAgents(
        agent_list,
        [agent_list[0]],
        DynamicAgentObjectsList=[mailer_agent],
        llm=azure_chat_model,
    )
