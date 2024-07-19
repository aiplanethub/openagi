from openagi.actions.tools.serp_search import GoogleSerpAPISearch
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
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

    websearcher = Worker(
        role="SW",
        instructions="""
        You are an Expert Python SW Developer with deep knowledge of job markets.
        - Focus on SDE2 (Software Development Engineer II) positions
        - Look for roles requiring 2+ years of Python experience
        - Consider various industries and company sizes
        - Pay attention to job descriptions, required skills, and company culture
        """,
        actions=[DuckDuckGoSearch],
    )

    admin = Admin(
        actions=[DuckDuckGoSearch],
        planner=TaskPlanner(human_intervene=False),
        memory=Memory(),
        llm=llm,
    )
    admin.assign_workers([websearcher])

    res = admin.run(
        query="""
        Provide a list of at least 10 SDE2 job opportunities suitable for candidates with 2+ years of Python experience.
        For each job, include:
        1. Company name and location
        2. Job title
        3. Key responsibilities
        4. Required skills
        5. Any standout perks or benefits
        6. Application link or process (if available)
        """,
        description="""
        You are an expert Internet Job Searching agent. Your task is to:
        - Find the most relevant and high-quality job opportunities
        - Ensure jobs match the specified experience level and skill set
        - Provide a diverse range of companies and industries
        - Verify the credibility of job postings
        - Organize the information in a clear, easy-to-read format
        - Highlight any unique or particularly attractive aspects of each role
        """,
    )

    # Print the results from the OpenAGI
    print("-" * 100)  # Separator
    Console().print(Markdown(res))


# The Agent did some research using the given actions and job positions.

"""
 # Job Listings                                                                                                                       
                                                                                                                                      
 ## Amazon                                                                                                                            
                                                                                                                                      
 ### Position: SDE II                                                                                                                 
 - **Location**: Multiple US geographic markets                                                                                       
 - **Compensation**: $129,300/year to $223,600/year                                                                                   
 - **Link**: [Amazon SDE II Job](https://www.amazon.jobs/en/jobs/2667280/sde-ii)                                                      
 - **Unique Aspects**:                                                                                                                
   - Competitive base pay reflecting the cost of labor across several US geographic markets                                           
   - Pay based on a number of factors including market location, job-related knowledge, skills, and experience                        
                                                                                                                                      
 ### Position: SDE2                                                                                                                   
 - **Location**: Multiple US geographic markets                                                                                       
 - **Compensation**: $129,300/year to $223,600/year                                                                                   
 - **Link**: [Amazon SDE2 Job](https://www.amazon.jobs/en/jobs/2667189/sde2-amazon)                                                   
 - **Unique Aspects**:                                                                                                                
   - Base pay reflecting the cost of labor across different US geographic markets                                                     
   - Total compensation company with pay based on various factors like location, knowledge, skills, and experience                    
                                                                                                                                      
 ## Google                                                                                                                            
                                                                                                                                      
 ### Position: SDE II                                                                                                                 
 - **Location**: Not specified                                                                                                        
 - **Compensation**: Not specified                                                                                                    
 - **Link**: [Google SDE II Interview Experience](https://medium.com/@kajol_singh/google-interview-experience-sde-ii-11758d86c5ab)    
 - **Unique Aspects**:                                                                                                                
   - Challenging phone interview involving solving complex problems with dynamic programming and trees                                
   - Insight into Google's interview process and expectations                                                                         
                                                                                                                                      
 ## Microsoft                                                                                                                         
                                                                                                                                      
 ### Position: SDE II                                                                                                                 
 - **Location**: Not specified                                                                                                        
 - **Compensation**: Not specified                                                                                                    
 - **Link**: [Microsoft SDE II Interview Experience](https://www.geeksforgeeks.org/microsoft-interview-experience-for-sde-ii/)        
 - **Unique Aspects**:                                                                                                                
   - Detailed experience of Microsoft's interview process                                                                             
   - Insight into the recruitment and next steps   
   
   """