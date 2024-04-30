from openagi.init_agent import kickOffGenAIAgents
from openagi.agent import AIAgent
from openagi.tools.integrations.duckducksearch import DuckDuckGoSearchTool
from openagi.llms.azure import AzureChatOpenAIModel

if __name__ == "__main__":
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
    config = AzureChatOpenAIModel.load_from_yml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffGenAIAgents(AgentObjects, [AgentObjects[0]], llm=azure_chat_model)
