import os 
from openagi.actions.files import WriteFileAction, ReadFileAction
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.actions.tools.webloader import WebBaseContextTool
from openagi.agent import Admin
from openagi.llms.gemini import GeminiModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
from openagi.worker import Worker
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    os.environ['GOOGLE_API_KEY'] = ""
    os.environ['Gemini_MODEL'] = "gemini-1.5-flash"
    os.environ['Gemini_TEMP'] = "0.1"

    # Team Members
    feedback_collector = Worker(
    role="Customer Feedback Collector",
    instructions="Gather AirPods Pro customer reviews from social media, e-commerce sites, and tech forums. Identify common themes and sentiments in the feedback.",
    actions=[DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )

    data_analyst = Worker(
        role="Data Analyst",
        instructions="Analyze collected AirPods Pro feedback data. Identify key trends, quantify customer sentiment, and generate actionable insights.",
        actions=[ReadFileAction, DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )

    report_creator = Worker(
        role="Report Creator",
        instructions="Create a detailed analysis report on AirPods Pro feedback. Highlight key trends, issues, and customer sentiment. Provide specific improvement recommendations with visual elements.",
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
        description="Collect and analyze AirPods Pro customer feedback from various online sources. Identify trends, issues, and overall sentiment. Develop a comprehensive report with actionable insights and recommendations for product improvement.",
    )
    print("-" * 100)  # Separator
    Console().print(Markdown(res))


### Marketing Campaign for Airpods pro 2

#                                                                                                   Trends                                                                                              

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

