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
        role="Market Research Analyst",
        instructions="Analyze the latest trends and market dynamics in renewable energy. Your role involves collecting and interpreting market data to provide insights on industry growth, technological advancements, and competitive landscape.",
        actions=[
            DuckDuckGoNewsSearch,
            WebBaseContextTool,
        ],
    )
    report_writer = Worker(
        role="Report Writer",
        instructions="Create a comprehensive market research report based on the provided data and analysis. You specialize in translating complex data into clear, actionable insights for business leaders and stakeholders.",
        actions=[
            DuckDuckGoNewsSearch,
            WebBaseContextTool,
        ],
    )
    content_editor = Worker(
        role="Content Editor",
        instructions="Review and refine the market research report for accuracy, clarity, and professional tone. Ensure the report is well-organized and free of grammatical errors. Format the document according to the company's style guide.",
        actions=[
            DuckDuckGoNewsSearch,
            WebBaseContextTool,
            WriteFileAction,
        ],
    )

    # Team Manager/Admin
    admin = Admin(
        planner=TaskPlanner(human_intervene=False),
        memory=Memory(),
        llm=llm,
    )
    admin.assign_workers([market_researcher, report_writer, content_editor])

    res = admin.run(
        query="Create a market research report on the latest trends in renewable energy.",
        description="Conduct a thorough analysis of the current renewable energy market. Identify key trends, recent technological advancements, and major players in the industry. Develop a detailed market research report that provides strategic insights for businesses looking to invest in renewable energy. Ensure the report is well-structured, informative, and professionally formatted.",
    )


    print("-" * 100)  # Separator
    Console().print(Markdown(res))