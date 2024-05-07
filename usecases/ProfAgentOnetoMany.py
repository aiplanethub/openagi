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
        agentName="RESEARCHER",  # name
        role="RESEARCH EXPERT",  # role
        goal="search for latest trends in COVID-19 and Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
        backstory="Has the capability to execute internet search tool",
        capability="search_executor",
        task="search internet for the goal for the trends after first half of 2023",
        output_consumer_agent=["WRITER1", "WRITER2"],  # the consumer agent after executing task
        tools_list=[DuckDuckGoSearchTool],
        llm="openai"
    ),
    Agent(
        agentName="WRITER1",
        role="SUMMARISING EXPERT",
        goal="summarize input into presentable points",
        backstory="Expert in summarising the given text",
        capability="llm_task_executor",
        task="summarize points to present to health care professionals",
        output_consumer_agent=["EMAILER"],
    ),
    Agent(
        agentName="WRITER2",
        role="SUMMARISING EXPERT",
        goal="summarize input into presentable points",
        backstory="Expert in summarising the given text",
        capability="llm_task_executor",
        task="summarize points to present to general public",
        output_consumer_agent=["EMAILER"],
    ),
    Agent(
        agentName="EMAILER",
        aggregator=2,
        onAggregationAction=onAggregationAction,
        role="EMAIL CREATOR",
        goal="composes the email based on the content",
        backstory="Good in composing precise emails",
        capability="llm_task_executor",
        task="composes email based on summary to doctors and general public separately into a file with subject-summary and details",
        output_consumer_agent=["HGI"],
    )
    ]
    config = AzureChatOpenAIModel.load_from_env_config()
    llm = AzureChatOpenAIModel(config=config)
    kickOffAgents(agent_list,[agent_list[0]], llm=llm)