from openagi.init_agent import kickOffGenAIAgents
from openagi.agent import AIAgent
from openagi.tools.integrations import WikipediaTool, GoogleFinanceSearchTool, SerperSpecificSearchTool
from openagi.tools.integrations import ExaSearchTool
from openagi.llms.azure import AzureChatOpenAIModel

if __name__ == "__main__":
    AgentObjects = [
    AIAgent(
        agentName = "RESEARCHER",
        role = "Researches about Reliance stock",
        goal = "To gather all the necessary information about Reliance stock within given context length",
        backstory = "Has the capability to execute internet search tool",
        capability = "search_executor",
        task = "Search the internet for information about Reliance stock, its current price, historical performance, market trends, and news",
        output_consumer_agent = "ANALYZER",
        tools_list = [WikipediaTool, GoogleFinanceSearchTool, ExaSearchTool, SerperSpecificSearchTool]
    ),
    AIAgent(
        agentName = "ANALYZER",
        role = "Analyzes the gathered data",
        goal = "To analyze the data and calculate the possible future performance of the stock",
        backstory = "Expert in analyzing data and making predictions",
        capability = "tool_executor",
        task = "Analyze the data and calculate the possible future performance of the stock based on the gathered information",
        output_consumer_agent = "WRITER",
        tools_list = []
    ),
    AIAgent(
        agentName = "WRITER",
        role = "Writes the pros and cons of buying Reliance stock",
        goal = "To write the pros and cons of buying Reliance stock based on the analyzed data",
        backstory = "Expert in writing clear and concise text",
        capability = "llm_task_executor",
        task = "Write the pros and cons of buying Reliance stock based on the analyzed data",
        output_consumer_agent = "RECOMMENDER",
        tools_list = []
    ),
    AIAgent(
        agentName = "RECOMMENDER",
        role = "Provides recommendation",
        goal = "To provide a recommendation on whether to buy Reliance stock or not",
        backstory = "Expert in making recommendations based on analyzed data",
        capability = "llm_task_executor",
        task = "Provide a recommendation on whether to buy Reliance stock or not based on the pros and cons",
        output_consumer_agent = "HGI",
        tools_list = []
    ),
    ]
    config = AzureChatOpenAIModel.load_from_yml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffGenAIAgents(AgentObjects, [AgentObjects[0]], llm=azure_chat_model) 