from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms import AzureChatOpenAIModel
from openagi.tools.integrations import DuckDuckGoSearchTool, GoogleFinanceSearchTool

if __name__ == "__main__":
    agent_name = ["RESEARCHER", "SUMMARIZER"]
    agent_list = [
        Agent(
            agentName=agent_name[0],
            role="RESEARCHER",
            goal="Get information on current trends and updates of given stock today.",
            backstory="Has the capability to execute the tools an collects the data.",
            capability="search_executor",
            task="Collect information Wipro stock",
            output_consumer_agent=[agent_name[1]],
            tools_list=[DuckDuckGoSearchTool, GoogleFinanceSearchTool],
        ),
        Agent(
            agentName=agent_name[1],
            role="SUMMARIZER",
            goal="Summarize the received data as 5 bullet points.",
            backstory="Expert in using data provided.",
            capability="llm_task_executor",
            task="Provide recommendation on whether to buy the Wipro stock or not with 5 bullet points based on information received.",
            output_consumer_agent=["HGI"],
        ),
    ]
    config = AzureChatOpenAIModel.load_from_yaml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffAgents(agent_list, [agent_list[0]], llm=azure_chat_model)