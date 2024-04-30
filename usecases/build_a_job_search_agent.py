from openagi.init_agent import kickOffGenAIAgents
from openagi.agent import AIAgent 
from openagi.tools.integrations import ExaSearchTool, DocumentCompareSearchTool
from openagi.tools.integrations import DuckDuckGoSearchTool
from openagi.llms.azure import AzureChatOpenAIModel

if __name__ == "__main__":
    agent_list = ["RESEARCHER"]
    AgentObjects=[]
    AgentObjects = [
    AIAgent(
        agentName=agent_list[0],  # name
        role="RESEARCHER",  # role
        goal="Find the most recent and relatable jobs based on the specifications given with the help of internet search and context from given Resume within context length.",
        backstory="A Job finder that can easily search for most relevant opportunities based on the given resume and job specifications.",
        capability="search_executor",
        task="Give me 5 most recent job based on my resume in resume.pdf file related to my expertise and make sure the opportunity is remote and has a salary of 8LPA or more.",
        output_consumer_agent = "HGI",  # the consumer agent after executing task
        tools_list=[ExaSearchTool, DuckDuckGoSearchTool, DocumentCompareSearchTool],
    )
    ]
    config = AzureChatOpenAIModel.load_from_yml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffGenAIAgents(AgentObjects, [AgentObjects[0]], llm=azure_chat_model)