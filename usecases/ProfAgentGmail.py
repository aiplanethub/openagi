from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.tools.integrations import GmailSearchTool

# Example Usage:


if __name__ == "__main__":
    agent_list = [
        Agent(
            agentName="RESEARCHER",  # name
            role="RESEARCHER",  # role
            goal="Send an email to the given context.",
            backstory="Has the capability to capability to send email using gmailtool",
            capability="search_executor",
            task="Create a new email with content on congraluations on your promotion to tanish@aiplanet.com and send it.",
            output_consumer_agent=["HGI"],  # the consumer agent after executing task
            tools_list=[GmailSearchTool],
        )
    ]

    config = AzureChatOpenAIModel.load_from_yaml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffAgents(agent_list, [agent_list[0]], llm=azure_chat_model)
