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

from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    config = AzureChatOpenAIModel.load_from_env_config()
    llm = AzureChatOpenAIModel(config=config)

    # Team Members
    market_researcher = Worker(
        role="Market Research Specialist",
        instructions="""
        1. Identify target demographics and analyze current smartphone market trends for Pineapple X.
        2. Conduct a competitive analysis of major smartphone brands in Pineapple X's market segment.
        3. Compile a report summarizing findings, including Pineapple X's unique selling points and potential marketing angles.
        """,
        actions=[DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )

    content_creator = Worker(
        role="Content Creator",
        instructions="""
        1. Review the market research report to understand target audiences and Pineapple X's unique selling points.
        2. Develop diverse content for the Pineapple X launch, including social media posts, blog articles, an email newsletter, and advertisement concepts.
        3. Ensure all content aligns with Pineapple X's brand voice and effectively communicates its unique selling points.
        """,
        actions=[ReadFileAction, DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )

    reviewer = Worker(
        role="Review and Editing Specialist",
        instructions="""
        1. Review all marketing content for grammatical accuracy, clarity, brand alignment, and effectiveness in highlighting Pineapple X's unique selling points.
        2. Provide feedback and make necessary edits to refine the content.
        3. Ensure consistency across all marketing materials and compile a final report summarizing the changes.
        """,
        actions=[ReadFileAction, DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )
    
    # Team Manager/Admin
    admin = Admin(
        planner=TaskPlanner(human_intervene=False),
        memory=Memory(),
        llm=llm,
    )
    admin.assign_workers([market_researcher, content_creator, reviewer])

    res = admin.run(
        query="Create a comprehensive marketing campaign for the launch of Pineapple X smartphone.",
        description="""
        1. Conduct market research to identify target audiences and analyze the competitive landscape.
        2. Develop engaging marketing content across multiple channels (social media, blog, email, ads).
        3. Review and refine all materials to ensure a cohesive, high-quality campaign that highlights Pineapple X's unique selling points.
        """,
    )

    print("-" * 100)  # Separator
    Console().print(Markdown(res))



### Output

# Welcome to the official launch of the Pineapple X smartphone! Discover the next generation of mobile technology with our latest features:

# 1. **Unparalleled Camera Technology**: Capture every moment with our AI-enhanced triple-lens camera system.
# 2. **Lightning-Fast 5G Connectivity**: Experience blazing-fast internet speeds with 5G.
# 3. **Eco-Friendly Materials**: Our commitment to sustainability means Pineapple X is made with eco-friendly materials.
# 4. **Improved Battery Life**: Stay connected longer with our enhanced battery technology.
# 5. **High-Performance Gaming**: Enjoy seamless gaming with our high-performance processor.
# 6. **E-SIM Technology**: Experience the convenience of E-SIM technology with Pineapple X.

# Join us in embracing the future of mobile technology. Order your Pineapple X today!