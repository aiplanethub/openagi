from openagi.actions.files import WriteFileAction
from openagi.actions.tools.ddg_search import DuckDuckGoNewsSearch
from openagi.actions.tools.webloader import WebBaseContextTool
from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
from openagi.worker import Worker
from rich.console import Console
from dotenv import load_dotenv
import os
load_dotenv()
from rich.markdown import Markdown

if __name__ == "__main__":
    config = AzureChatOpenAIModel.load_from_env_config()
    llm = AzureChatOpenAIModel(config=config)

    # Team Members
    market_researcher = Worker(
        role="Market Research Specialist",
        instructions="Conduct market research to identify target audiences, key trends, and competitive landscape for the our new flagship phone Pineapple X smartphone. Use various online sources and tools to gather relevant data and insights.",
        actions=[
            DuckDuckGoNewsSearch,
            WebBaseContextTool,
        ],
    )
    content_creator = Worker(
        role="Content Creator",
        instructions="Develop compelling marketing content for the Pineapple X launch, including social media posts, blog articles, email newsletters, and advertisements. Focus on engaging the target audience and highlighting the product's unique selling points.",
        actions=[
            DuckDuckGoNewsSearch,
            WebBaseContextTool,
        ],
    )
    
    # Team Manager/Admin
    admin = Admin(
        planner=TaskPlanner(human_intervene=False),
        memory=Memory(),
        llm=llm,
    )
    admin.assign_workers([market_researcher, content_creator])

    res = admin.run(
        query="Create a marketing campaign for the launch of Pineapple X.",
        description="Conduct market research to identify target audiences, key trends, and the competitive landscape. Develop engaging marketing content for social media, website, email newsletters, and advertisements. Ensure the campaign effectively highlights Pineapple X's unique selling points and engages the target audience.",
    )


    print("-" * 100)  # Separator
    Console().print(Markdown(res))
