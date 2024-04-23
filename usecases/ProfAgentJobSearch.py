from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.tools.integrations import (
    AskDocumentTool,
    DuckDuckGoSearchTool,
)

if __name__ == "__main__":
    agent_list = [
        Agent(
            agentName="RESEARCHER",  # name
            role="RESEARCHER",  # role
            goal="Find the most recent and relatable jobs based on the specifications given with the help of internet search and context from given Resume within context length.",
            backstory="A Job finder that can easily search for most relevant opportunities based on the given resume and job specifications within the context length.",
            capability="llm_task_executor",
            task="Give me 5 most recent job based on my resume in resume1.pdf file whose context you'll find in related to my expertise and make sure the opportunity is remote and has a salary of 8LPA or more.",
            output_consumer_agent=["HGI"],  # the consumer agent after executing task
            tools_list=[AskDocumentTool, DuckDuckGoSearchTool],
        )
    ]
    config = AzureChatOpenAIModel.load_from_yaml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffAgents(agent_list, [agent_list[0]], llm=azure_chat_model)