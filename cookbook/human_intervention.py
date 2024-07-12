from openagi.actions.files import WriteFileAction, ReadFileAction
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.actions.tools.webloader import WebBaseContextTool
from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
from openagi.worker import Worker
from rich.console import Console
from rich.markdown import Markdown

if __name__ == "__main__":
    import os
    
    # Set Azure environment variables
    os.environ["AZURE_BASE_URL"] = "<your azure base url>"
    os.environ["AZURE_DEPLOYMENT_NAME"] = "<deployment name>"
    os.environ["AZURE_MODEL_NAME"] = "<model name>"
    os.environ["AZURE_OPENAI_API_KEY"] = "<your openai api key>"

    # Load Azure ChatOpenAIModel configuration
    config = AzureChatOpenAIModel.load_from_env_config()
    llm = AzureChatOpenAIModel(config=config)

    # Team Members
    feedback_collector = Worker(
        role="Customer Feedback Collector",
        instructions="Gather customer feedback specifically about AirPods Pro from various online platforms, including social media, review sites, and forums. Focus on identifying common themes and sentiments related to this product.",
        actions=[DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )
    data_analyst = Worker(
        role="Data Analyst",
        instructions="Analyze the collected customer feedback data related to AirPods Pro to identify key trends, recurring issues, and overall customer sentiment. Use statistical tools to quantify the data and provide actionable insights.",
        actions=[ReadFileAction, DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )
    report_creator = Worker(
        role="Report Creator",
        instructions="Develop a comprehensive customer feedback analysis report based on the data analysis for AirPods Pro. Highlight key findings, trends, and recommendations for improving the product. Ensure the report is well-structured and visually appealing.",
        actions=[ReadFileAction, DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )

    # Team Manager/Admin
    admin = Admin(
        planner=TaskPlanner(human_intervene=True),
        memory=Memory(),
        llm=llm,
    )

    # Debug: Print worker roles and IDs
    for worker in [feedback_collector, data_analyst, report_creator]:
        print(f"Worker Role: {worker.role}, Worker ID: {id(worker)}")

    admin.assign_workers([feedback_collector, data_analyst, report_creator])

    res = admin.run(
        query="Create a customer feedback analysis report for AirPods Pro.",
        description="Collect and analyze customer feedback specifically for AirPods Pro from multiple online sources. Identify common themes, recurring issues, and overall customer sentiment. Develop a comprehensive report that provides actionable insights and recommendations for improving the AirPods Pro. Ensure the report is detailed, well-organized, and visually appealing.",
    )

    print("-" * 100)  # Separator
    Console().print(Markdown(res))
