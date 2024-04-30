from openagi.init_agent import kickOffGenAIAgents
from openagi.agent import AIAgent
from openagi.tools.integrations import DocumentCompareSearchTool
from openagi.llms.azure import AzureChatOpenAIModel

if __name__ == "__main__":
    agent_list = ["RESEARCHER"]
    AgentObjects=[]
    AgentObjects = [
    AIAgent(
        agentName=agent_list[0],  # name
        role="RESEARCHER",  # role
        goal="Summarize two different documents to find the differences and similarities between them.",
        backstory="I am a researcher agent that can help you compare documents.",
        capability="search_executor",
        task="Compare the files GenAIuserManual and File_2 for similarities",
        output_consumer_agent="HGI",  # the consumer agent after executing task
        tools_list=[DocumentCompareSearchTool],
    )
    ]
    config = AzureChatOpenAIModel.load_from_yml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffGenAIAgents(AgentObjects, [AgentObjects[0]], llm=azure_chat_model)
