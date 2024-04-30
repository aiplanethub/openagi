from openagi.init_agent import kickOffGenAIAgents
from openagi.agent import AIAgent
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.tools.integrations import ExaSearchTool, GmailSearchTool

if __name__ == "__main__":
    agent_list = ["RESEARCHER", "WRITER", "EMAILER", "GMAILER"]
    AgentObjects=[]
    AgentObjects = [
    AIAgent(
        agentName=agent_list[0],  # name
        role="RESEARCHER",  # role
        goal="search for latest trends in Carona and Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
        backstory="Has the capability to execute internet search tool",
        capability="search_executor",
        task="search internet for the goal for the trends after first half of 2023",
        output_consumer_agent=agent_list[1],  # the consumer agent after executing task
        tools_list=[ExaSearchTool],
    ),
    AIAgent(
        agentName=agent_list[1],
        role="SUMMARISER",
        goal="summarize input into presentable points",
        backstory="Expert in summarising the given text",
        capability="llm_task_executor",
        task="summarize points to present to health care professionals and general public separately",
        output_consumer_agent=agent_list[2],
    ),
    AIAgent(
        agentName=agent_list[2],
        role="EMAILER",
        goal="composes the email based on the content",
        backstory="Good in composing precise emails",
        capability="llm_task_executor",
        task="composes email based on summary to doctors and general public separately into a file with subject-summary and details",
        output_consumer_agent=agent_list[3],
    ),
    AIAgent(
        agentName=agent_list[3],
        role="GMAILER",
        goal="Send the email using GmailSearchTool",
        backstory="Good in sending emails to the given context.",
        capability="llm_task_executor",
        task= "send emails to the receipient tanish@aiplanet.com",
        output_consumer_agent="HGI",  
        tools_list=[GmailSearchTool],
    )
    ]
    config = AzureChatOpenAIModel.load_from_yml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffGenAIAgents(AgentObjects,[AgentObjects[0]], llm=azure_chat_model)
