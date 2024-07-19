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
        role="Market Research Analyst",
        instructions="""
        Analyze trends in renewable energy:
        - Focus on major sectors (solar, wind, etc.)
        - Collect data on market size, growth, and key players
        - Research technological advancements and policies
        - Examine competitive landscape and emerging markets
        Compile findings for the report writer.
        """,
        actions=[DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )

    report_writer = Worker(
        role="Report Writer",
        instructions="""
        Create a market research report based on the analyst's data:
        - Include an executive summary and clear sections
        - Use visuals to present data effectively
        - Provide analysis of each major renewable energy sector
        - Discuss industry trends, challenges, and opportunities
        - Offer actionable insights for potential investors
        Save the draft for editing.
        """,
        actions=[ReadFileAction, DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )

    content_editor = Worker(
        role="Content Editor",
        instructions="""
        Review and refine the market research report:
        - Ensure consistency in tone and formatting
        - Check for errors and improve clarity
        - Verify data accuracy and proper citations
        - Format according to company style guide
        - Create a table of contents
        Finalize the polished report.
        """,
        actions=[ReadFileAction, DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )

    # Team Manager/Admin
    admin = Admin(
        planner=TaskPlanner(human_intervene=False),
        memory=Memory(),
        llm=llm,
    )
    admin.assign_workers([market_researcher, report_writer, content_editor])

    res = admin.run(
        query="""
        Create a market research report on renewable energy trends:
        - Cover major sectors, market size, and growth projections
        - Include technological advancements and key players
        - Analyze policies, emerging markets, and challenges
        - Provide insights for potential investors
        """,
        description="""
        Lead the team in producing a high-quality renewable energy market report:
        - Oversee the research and writing process
        - Ensure collaboration and timely completion
        - Verify the report's accuracy, clarity, and value
        Deliver a report that guides strategic decision-making in renewable energy.
        """
    )

    print("-" * 100)  # Separator
    Console().print(Markdown(res))



### Output

#  The comprehensive market research report on renewable energy includes sections on trends, technological innovations, major players, regulatory impacts, and future potential. Key highlights are:                
                                                                                                                                                                                                                  
#  1. **Trends and Projections**: Renewables are expected to surpass coal by 2025.                                                                                                                                  
#  2. **Technological Innovations**: Advancements in high-efficiency solar technologies, AI, big data, and distributed energy storage systems.                                                                      
#  3. **Major Players**: Leading companies like NextEra Energy and Brookfield Renewable Partners.                                                                                                                   
#  4. **Regulatory and Investment Impacts**: Historic investments and the importance of reskilling the workforce.                                                                                                   
#  5. **Future Potential**: Innovations in solar, wind, bioenergy, and green hydrogen technologies.