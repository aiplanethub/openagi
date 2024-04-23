from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.tools.integrations import AskDocumentTool, DuckDuckGoSearchTool

if __name__ == "__main__":
    agent_name = ["RESEARCHER", "WRITER"]
    agent_list = [
        Agent(
            agentName=agent_name[0],  # name
            role="RESEARCHER",  # role
            goal="Get all the legal precautions that need to be taken care.",
            backstory="Has the capability to advise it's customers on legal aspects",
            capability="search_executor",
            task="Read carefully the Purchase document and suggest which precautions I need to take care, with examples and it's legal consequences",
            output_consumer_agent=[agent_name[1]],  # the consumer agent after executing task
            tools_list=[DuckDuckGoSearchTool, AskDocumentTool],
        ),
        Agent(
            agentName=agent_name[1],
            role="SUMMARISER",
            goal="summarize input into presentable points",
            backstory="Expert in summarising the given text",
            capability="llm_task_executor",
            task="Summarize into points which documents will I need to complete the purchase of a restaurant?",
            output_consumer_agent=["HGI"],
        ),
    ]
    config = AzureChatOpenAIModel.load_from_yaml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffAgents(agent_list, [agent_list[0]], llm=azure_chat_model)
