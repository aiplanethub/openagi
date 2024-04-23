import logging
from openagi.init_agent import kickOffAgents
from openagi.agent import Agent
from openagi.tools.integrations import DuckDuckGoSearchTool
from openagi.llms.azure import AzureChatOpenAIModel

def onAggregationAction(agentName, consumerAgent, aggrSourceAgentList, aggrResultsList):
    result = ""
    for string in aggrResultsList:
        result += string.body + " "
    logging.debug(
        f"aggregation of messages::of {agentName} to {consumerAgent} {result}"
    )
    return result

if __name__ == "__main__":
    agent_list = [
    Agent(
        agentName="RESEARCHER1",  # name
        role="RESEARCH EXPERT",  # role
        goal="search for latest trends in  Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
        backstory="Has the capability to execute internet search tool",
        capability="search_executor",
        task="search internet for the goal for the trends after first half of 2023",
        output_consumer_agent=["WRITER"],  # the consumer agent after executing task
        tools_list=[DuckDuckGoSearchTool],
    ),
    Agent(
        agentName="RESEARCHER2",  # name
        role="RESEARCH EXPERT",  # role
        goal="search for latest trends in Covid-19  treatment that includes medicines, physical exercises, overall management and prevention aspects",
        backstory="Has the capability to execute internet search tool",
        capability="search_executor",
        task="search internet for the goal for the trends after first half of 2023",
        output_consumer_agent=["WRITER"],  # the consumer agent after executing task
        tools_list=[DuckDuckGoSearchTool],
    ),
    Agent(
        agentName="WRITER",
        role="SUMMARISING EXPERT",
        aggregator=2,
        onAggregationAction=onAggregationAction,
        goal="summarize input into presentable points",
        backstory="Expert in summarising the given text",
        capability="llm_task_executor",
        task="summarize points to present to health care professionals",
        output_consumer_agent=["EMAILER1", "EMAILER2"],
    ),
    Agent(
        agentName="EMAILER1",
        role="EMAIL CREATOR",
        goal="composes the email based on the content",
        backstory="Good in composing precise emails",
        capability="llm_task_executor",
        task="compose email based on summary to doctors  with subject-summary and details",
        output_consumer_agent=["HGI"],
    ),
    Agent(
        agentName="EMAILER2",
        role="EMAIL CREATOR",
        goal="composes the email based on the content",
        backstory="Good in composing precise emails",
        capability="llm_task_executor",
        task="compose email based on summary to general public with subject-summary and details",
        output_consumer_agent=["HGI"],
    )
    ]
    config = AzureChatOpenAIModel.load_from_yaml_config()
    llm = AzureChatOpenAIModel(config=config)
    kickOffAgents(agent_list,[agent_list[0],agent_list[1]], llm=llm)