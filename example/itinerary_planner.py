from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.agent import Admin
from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.planner.task_decomposer import TaskPlanner
from rich.console import Console
from rich.markdown import Markdown

config = AzureChatOpenAIModel.load_from_env_config()
llm = AzureChatOpenAIModel(config=config)

plan = TaskPlanner(autonomous=True) 

admin = Admin(
    actions = [DuckDuckGoSearch],
    planner = plan,
    llm=llm,
    
)
res = admin.run(
    query="3 Days Trip to san francisco bay area",
    description=
   "You are a knowledgeable local guide with extensive information about the city, it's attractions and customs.  Do not use a quality assurance agent and output it without writing in the file.", 
)
print(res)
    


# Print the results from the OpenAGI
print("-" * 100)  # Separator
Console().print(Markdown(res))

# The Agent did some research using the given actions and returned the below itinerary.
"""

Day 1:

- Breakfast at Mama's on Washington Square
- Explore Golden Gate Park
- Lunch at The Cliff House
- Walk across the Golden Gate Bridge
- Dinner at Kokkari Estiatorio

Day 2:

- Breakfast at Brenda's French Soul Food
- Take a ferry to Alcatraz Island
- Lunch at The Buena Vista Cafe (try their famous Irish Coffee)
- Explore Fisherman's Wharf and Pier 39
- Ride a cable car to Nob Hill
- Dinner at House of Prime Rib

Day 3:

- Breakfast at Tartine Bakery
- Visit the Palace of Fine Arts
- Lunch at Tony's Pizza Napoletana in North Beach
- Explore Chinatown
- Dinner at Nopa

Note: Don't forget to make reservations for popular restaurants in advance!                                                                                                                                                                                                          
"""
