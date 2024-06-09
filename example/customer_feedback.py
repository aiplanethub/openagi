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
    feedback_collector = Worker(
        role="Customer Feedback Collector",
        instructions="Gather customer feedback specifically about AirPods Pro from various online platforms, including social media, review sites, and forums. Focus on identifying common themes and sentiments related to this product.",
        actions=[
            DuckDuckGoNewsSearch,
            WebBaseContextTool,
        ],
    )
    data_analyst = Worker(
        role="Data Analyst",
        instructions="Analyze the collected customer feedback data related to AirPods Pro to identify key trends, recurring issues, and overall customer sentiment. Use statistical tools to quantify the data and provide actionable insights.",
        actions=[
            DuckDuckGoNewsSearch,
            WebBaseContextTool,
        ],
    )
    report_creator = Worker(
        role="Report Creator",
        instructions="Develop a comprehensive customer feedback analysis report based on the data analysis for AirPods Pro. Highlight key findings, trends, and recommendations for improving the product. Ensure the report is well-structured and visually appealing.",
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
    admin.assign_workers([feedback_collector, data_analyst, report_creator])

    res = admin.run(
        query="Create a customer feedback analysis report for AirPods Pro.",
        description="Collect and analyze customer feedback specifically for AirPods Pro from multiple online sources. Identify common themes, recurring issues, and overall customer sentiment. Develop a comprehensive report that provides actionable insights and recommendations for improving the AirPods Pro. Ensure the report is detailed, well-organized, and visually appealing.",
    )


    print("-" * 100)  # Separator
    Console().print(Markdown(res))
