from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.tools.integrations import (
    DocumentCompareSearchTool,
)


if __name__ == "__main__":
    agent_list = [
        Agent(
            agentName="RESUME_COMPARE",
            role="RESUME_ANALYZER",
            goal="Give a thorough analysis of the resume in bullet points.",
            backstory="You are a seasoned Resume reveiwer who excels in giving recommendations in improving a resume",
            capability="search_executor",
            task="Analyze the resume in resume.pdf file and provide a detailed report in bullet points highlighting the strengths, weaknesses, and areas for improvement.",
            output_consumer_agent=["HGI"],
            tools_list=[DocumentCompareSearchTool],
        )
    ]
    config = AzureChatOpenAIModel.load_from_yaml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffAgents(agent_list, [agent_list[0]], llm=azure_chat_model)