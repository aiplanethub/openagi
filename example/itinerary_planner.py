from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.agent import Admin
from rich.console import Console
from rich.markdown import Markdown

# Set OPENAI_API_KEY as environment variable
# os.environ["OPENAI_API_KEY"] = "sk-proj-xxxxxxxxxxxxxxxxxx"

# Setup and run Admin Agent
response = Admin(actions=[DuckDuckGoSearch]).run(
    query="3 Days Trip to san francisco bay area",
    description="You are a knowledgeable local guide with extensive information about the city, it's attractions and customs",
)


# Print the results from the OpenAGI
print("-" * 100)  # Separator
Console().print(Markdown(response))

# The Agent did some research using the given actions and returned the below itinerary.
"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                                Itinerary                                                                                                                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Day 1:                                                                                                                                                                                                                                      

 • Breakfast at Jantz Cafe & Bakery                                                                                                                                                                                                         
 • Visit Golden Gate Park                                                                                                                                                                                                                   
 • Lunch at Fog Harbor Fish House                                                                                                                                                                                                           
 • Explore Fisherman's Wharf                                                                                                                                                                                                                
 • Dinner at La Société                                                                                                                                                                                                                     

Day 2:                                                                                                                                                                                                                                      

 • Breakfast at Lily                                                                                                                                                                                                                        
 • Visit Alcatraz Island                                                                                                                                                                                                                    
 • Lunch at Copas                                                                                                                                                                                                                           
 • Explore Chinatown                                                                                                                                                                                                                        
 • Dinner at State Bird Provisions                                                                                                                                                                                                          

Day 3:                                                                                                                                                                                                                                      

 • Breakfast at Tartine Bakery                                                                                                                                                                                                              
 • Visit Palace of Fine Arts                                                                                                                                                                                                                
 • Lunch at Zuni Cafe                                                                                                                                                                                                                       
 • Explore Mission District                                                                                                                                                                                                                 
 • Dinner at The Slanted Door                                                                                                                                                                                                               
"""
