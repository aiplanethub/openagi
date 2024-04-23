from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.tools.integrations import DuckDuckGoSearchTool

if __name__ == "__main__":
    agent_list = [
        Agent(
            agentName="EVENT_RESEARCHER",
            role="Searches for detailed information about the pre-marriage event",
            goal="Gather all possible information about the pre-marriage event of Mukesh Ambani's son including event details, dates, location, guests, and special moments",
            backstory="Has the capability to execute internet search tools and scrape websites for up-to-date information",
            capability="search_executor",
            task="Use internet search tools to find articles, news reports, and YouTube videos related to the pre-marriage event of Mukesh Ambani's son",
            output_consumer_agent=["CONTENT_ANALYZER"],
            tools_list=[DuckDuckGoSearchTool],
        ),
        Agent(
            agentName="CONTENT_ANALYZER",
            role="Analyzes and summarizes the information",
            goal="Analyze the collected data to identify key points and insights about the event, focusing on aspects that would interest newspaper readers",
            backstory="Skilled in processing and summarizing complex information for clarity and conciseness",
            capability="llm_task_executor",
            task="Summarize the gathered information, highlighting the most newsworthy elements such as special guests, event highlights, and any unique ceremonies or traditions observed",
            output_consumer_agent=["ARTICLE_WRITER"],
            tools_list=[],
        ),
        Agent(
            agentName="ARTICLE_WRITER",
            role="Composes the newspaper article",
            goal="Write a compelling newspaper article incorporating the summarized information, ensuring it is engaging and informative for the readers",
            backstory="Expert in crafting engaging and informative newspaper articles, adept at storytelling and presenting facts in an interesting way",
            capability="llm_task_executor",
            task="Compose the newspaper article based on the summarized information, focusing on making it reader-friendly, engaging, and informative, with a clear structure and captivating headline",
            output_consumer_agent=["HGI"],
            tools_list=[],
        ),
    ]
    config = AzureChatOpenAIModel.load_from_yaml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffAgents(agent_list, [agent_list[0]], llm=azure_chat_model)
