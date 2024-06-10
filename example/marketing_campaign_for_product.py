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
    config = AzureChatOpenAIModel.load_from_env_config()
    llm = AzureChatOpenAIModel(config=config)

    # Team Members
    market_researcher = Worker(
        role="Market Research Specialist",
        instructions="Conduct market research to identify target audiences, key trends, and competitive landscape for the our new flagship phone Pineapple X smartphone. Use various online sources and tools to gather relevant data and insights.",
        actions=[DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )
    content_creator = Worker(
        role="Content Creator",
        instructions="Develop compelling marketing content for the Pineapple X launch, including social media posts, blog articles, email newsletters, and advertisements. Focus on engaging the target audience and highlighting the product's unique selling points.",
        actions=[ReadFileAction, DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )

    reviewer = Worker(
        role="Review and Editing Specialist",
        instructions="Review the marketing campaign for clarity, engagement, grammatical accuracy, and alignment with company values and refine it to ensure perfection. A meticulous editor with an eye for detail, ensuring every piece of content is clear, engaging, and grammatically perfect.",
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
        query="Create a marketing campaign for the launch of Pineapple X.",
        description="Conduct market research to identify target audiences, key trends, and the competitive landscape. Develop engaging marketing content for social media, website, email newsletters, and advertisements. Ensure the campaign effectively highlights Pineapple X's unique selling points and engages the target audience.",
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