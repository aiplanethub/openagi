from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.tools.integrations import DocumentCompareSearchTool

if __name__ == "__main__":
    agent_list = [
        Agent(
            agentName="RESEARCHER",  # name
            role="RESEARCHER",  # role
            goal="Summarize two different documents to find the key differences between them and return it in bullet points.",
            backstory="You are a professional document comparison agent with the ability to analyze and summarize the key differences between two documents.",
            capability="llm_task_executor",
            task="find similarities based on their skills , Tanishk_v18 and Tanish_v5_de files and give results in bullet points.",
            output_consumer_agent=["HGI"],  # the consumer agent after executing task
            tools_list=[DocumentCompareSearchTool],
        )
    ]
    config = AzureChatOpenAIModel.load_from_env_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffAgents(agent_list, [agent_list[0]], llm=azure_chat_model)
