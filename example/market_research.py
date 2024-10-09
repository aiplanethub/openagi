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

    
    plan = TaskPlanner(autonomous=True) 
    
    admin = Admin(
        actions = [DuckDuckGoSearch],
        planner = plan,
        llm=llm,
    )
    

    res = admin.run(
    query="""
    Create a comprehensive market research report on renewable energy trends. The report should cover major sectors within renewable energy, assess current market size, and provide growth projections. Include an analysis of technological advancements and profiles of key industry players. Examine relevant policies, explore emerging markets, and discuss challenges facing the industry. Provide valuable insights for potential investors considering entering the renewable energy market.
    """,
    description="""
    Lead the team in producing this high-quality renewable energy market report. Oversee the research and writing process, ensure effective collaboration among team members, and manage timely completion of all sections. Verify the report's accuracy, clarity, and overall value to readers. The final deliverable should be a strategic resource that guides decision-making in the renewable energy sector.
    """
)

    print("-" * 100)  # Separator
    Console().print(Markdown(res))



### Output

#  The comprehensive market research report on renewable energy includes sections on trends, technological innovations, major players, regulatory impacts, and future potential. Key highlights are:                
                                                                                                                                                                                                                  
#  1. **Major Players**: Leading companies like NextEra Energy and Brookfield Renewable Partners.                                                                                                                    
#  2. **Technological Innovations**: Advancements in high-efficiency solar technologies, AI, big data, and distributed energy storage systems.                                                                      
#  3. **Trends and Projections**: Renewables are expected to surpass coal by 2025.                                                                                                                                  
#  4. **Regulatory and Investment Impacts**: Historic investments and the importance of reskilling the workforce.                                                                                                   
#  5. **Future Potential**: Innovations in solar, wind, bioenergy, and green hydrogen technologies.