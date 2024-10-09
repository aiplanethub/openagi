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
    plan = TaskPlanner(autonomous=True) 

    
    
    admin = Admin(
        actions = [DuckDuckGoSearch],
        memory=Memory(),
        llm=llm,
    )
    

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

#  To refine and ensure cohesion in the Pineapple X marketing campaign, the following strategies should be considered:                                                                                          
                                                                                                                                                                                                              
#  1. **Social Media**: Utilize top strategies such as engaging content, influencer partnerships, and interactive posts.                                                                                        
#  2. **Blog**: Create informative and engaging blog posts that highlight unique features and benefits.                                                                                                         
#  3. **Email**: Implement best practices for email marketing, including personalized content and clear calls to action.                                                                                        
#  4. **Advertising**: Leverage successful advertising strategies, such as targeted ads and compelling visuals.                                                                                                 
                                                                                                                                                                                                              
#  By integrating these strategies, the Pineapple X marketing campaign can achieve greater coherence and effectiveness.    

# Join us in embracing the future of mobile technology. Order your Pineapple X today!