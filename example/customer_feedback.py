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
    feedback_collector = Worker(
        role="Customer Feedback Collector",
        instructions=(
            "1. Search for customer reviews of AirPods Pro on social media platforms like Twitter and Facebook.\n"
            "2. Look for reviews on popular e-commerce websites like Amazon and Best Buy.\n"
            "3. Collect feedback from technology review sites and forums such as Reddit and TechRadar.\n"
            "4. Identify and document common themes and sentiments in the collected feedback."
        ),
        actions=[DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )
    data_analyst = Worker(
        role="Data Analyst",
        instructions=(
            "1. Read the collected feedback data related to AirPods Pro.\n"
            "2. Use statistical analysis tools to identify key trends and recurring issues.\n"
            "3. Quantify overall customer sentiment towards the product.\n"
            "4. Generate actionable insights based on the analysis."
        ),
        actions=[ReadFileAction, DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )
    report_creator = Worker(
        role="Report Creator",
        instructions=(
            "1. Develop a detailed analysis report based on the data analyst's findings.\n"
            "2. Highlight key trends, issues, and overall customer sentiment.\n"
            "3. Provide specific recommendations for product improvement.\n"
            "4. Ensure the report is well-structured, clear, and includes visual elements like charts and graphs."
        ),
        actions=[ReadFileAction, DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
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
        description=(
            "1. Collect customer feedback on AirPods Pro from multiple online sources.\n"
            "2. Analyze the feedback to identify common themes, recurring issues, and overall customer sentiment.\n"
            "3. Develop a comprehensive report that provides actionable insights and recommendations for improving AirPods Pro.\n"
            "4. Ensure the report is detailed, well-organized, and visually appealing."
        ),
    )

    print("-" * 100)  # Separator
    Console().print(Markdown(res))


### Example 3: Marketing Campaign for Airpods pro 2

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                                                                          Comprehensive Customer Feedback Analysis Report: AirPods Pro                                                                          ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#                                                                                              Key Findings and Trends                                                                                              

#  1 Noise Cancellation: Highly praised by users.                                                                                                                                                                   
#  2 Sound Quality: Generally excellent feedback.                                                                                                                                                                   
#  3 Comfort: Mixed feedback with some users experiencing fit issues.                                                                                                                                               
#  4 Battery Life: Positively received by users.                                                                                                                                                                    
#  5 Price: A common concern; considered expensive by many.                                                                                                                                                         
#  6 Upgrades: Notable improvements in the Pro 2 version.                                                                                                                                                           
#  7 Fit Issues: Reported by several users, particularly on Amazon and Reddit.                                                                                                                                      

#                                                                                                 Overall Sentiment                                                                                                 

#  • Positive:                                                                                                                                                                                                      
#     • Noise cancellation                                                                                                                                                                                          
#     • Sound quality                                                                                                                                                                                               
#     • Battery life                                                                                                                                                                                                
#     • Upgrades                                                                                                                                                                                                    
#  • Negative:                                                                                                                                                                                                      
#     • Comfort                                                                                                                                                                                                     
#     • Price                                                                                                                                                                                                       
#     • Fit issues                                                                                                                                                                                                  

#                                                                                                Actionable Insights                                                                                                

#  1 Emphasize Noise Cancellation and Sound Quality: Highlight these features in marketing campaigns.                                                                                                               
#  2 Consider Promotional Offers or Discounts: Address price concerns by offering promotions or discounts.                                                                                                          
#  3 Address Fit Issues: Improve design or offer customizable fit options to enhance comfort.                                                                                                                       

