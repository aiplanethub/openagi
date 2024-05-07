from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.tools.integrations import (
    DuckDuckGoSearchTool,
    GoogleFinanceSearchTool,
    YoutubeSearchTool,
)

# Example Usage:
if __name__ == "__main__":
    agent_name = ["Investment Advisor", "SUMMARISER"]
    task = """
        Collect and summarize recent news articles, press
        releases, and market analyses related to the stock and
        its industry.
        Pay special attention to any significant events, market
        sentiments, and analysts' opinions. Also include upcoming 
        events like earnings and others.
        Your final answer MUST be a report that includes a
        comprehensive summary of the latest news, any notable
        shifts in market sentiment, and potential impacts on 
        the stock.
        Also make sure to return the stock ticker.
        Make sure to use the most recent data as possible.
        Selected company by the customer:Nokia"""

    agent_list = [
        Agent(
            agentName=agent_name[0],  # name
            role="Private Investment Advisor",  # role
            goal="Impress your customers with full analyses over stocks and completer investment recommendations",
            backstory="You're the most experienced investment advisor and you combine various analytical insights to formulate strategic investment advice. You are now working for a super important customer you need to impress.",
            capability="search_executor",
            task=task,
            output_consumer_agent=["HGI"],  # the consumer agent after executing task
            tools_list=[DuckDuckGoSearchTool, YoutubeSearchTool, GoogleFinanceSearchTool],
        ),
        Agent(
            agentName=agent_name[1],
            role="SUMMARISER",
            goal="summarize input into presentable points",
            backstory="backstory",
            capability="llm_task_executor",
            task="summarize points to present to leadership team and general public separately",
            output_consumer_agent=["HGI"],
        ),
    ]
    config = AzureChatOpenAIModel.load_from_env_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffAgents(agent_list, [agent_list[0]], llm=azure_chat_model)
