from openagi.init_agent import kickOffGenAIAgents
from openagi.agent import AIAgent
from openagi.tools.integrations import DuckDuckGoSearchTool 
from openagi.tools.integrations import DocumentCompareSearchTool
from openagi.llms.azure import AzureChatOpenAIModel

if __name__ == "__main__":
    agent_list = ["RESEARCHER", "WRITER"]
    AgentObjects=[]
    AgentObjects = [
    AIAgent(
        agentName=agent_list[0],  # name
        role="RESEARCHER",  # role
        goal="Get all the legal precautions that need to be taken care.",
        backstory="Has the capability to advise it's customers on legal aspects",
        capability="search_executor",
        task="Read carefully the Purchase document and suggest which precautions I need to take care, with examples and it's legal consequences",
        output_consumer_agent=agent_list[1],  # the consumer agent after executing task
        tools_list=[DuckDuckGoSearchTool, DocumentCompareSearchTool],
    ),
    AIAgent(
        agentName=agent_list[1],
        role="SUMMARISER",
        goal="summarize input into presentable points",
        backstory="Expert in summarising the given text",
        capability="llm_task_executor",
        task="Summarize into points which documents will I need to complete the purchase of a restaurant?",
        output_consumer_agent="HGI",
    )
    ]
    config = AzureChatOpenAIModel.load_from_yml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffGenAIAgents(AgentObjects, [AgentObjects[0]], llm=azure_chat_model)
