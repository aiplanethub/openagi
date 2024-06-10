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

