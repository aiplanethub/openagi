# Import required modules from the OpenAGI framework
from openagi.planner.task_decomposer import TaskPlanner  # For autonomous task planning
from openagi.agent import Admin  # Main agent class that orchestrates the process
from openagi.actions.tools.searchapi_search import SearchApiSearch  # Maps tool from SearchAPI Search
from openagi.llms.xai import XAIModel  # XAI language model integration
import os

# Set up the API key for the XAI model and Searchapi.io
# This should be replaced with your actual API key
os.environ['XAI_API_KEY'] = "<replace-with-your-key>" # get your key: https://console.x.ai/

SearchApiSearch.set_config({
    "api_key": "<replace with your key>",  # get your key: https://www.searchapi.io/
    "engine": "google_maps"
})

# Load XAI model configuration from environment variables
# This typically includes settings like model type, temperature, etc.
grok_config = XAIModel.load_from_env_config()

# Initialize the XAI language model with the loaded configuration
llm = XAIModel(config=grok_config)

# Create a task planner instance
# autonomous=True: The planner will execute tasks without waiting for approval
# human_intervene=False: No human intervention will be requested during execution
plan = TaskPlanner(
    autonomous=True,
    human_intervene=False
)

# Initialize the Admin agent
# This is the main orchestrator that combines:
# - actions: List of available tools (only SearchApiSearch in this case)
# - planner: The task planner that decides what actions to take
# - llm: The language model that will process the text and generate responses
admin = Admin(
    actions=[SearchApiSearch],
    planner=plan,
    llm=llm,
)

# Execute the agent with a specific query
# query: The question we want to answer
# description: Brief description of what the agent should do
res = admin.run(
    query="list down the hotels in the Budapest. I need 10 hotel names",  
    description="make sure to look for those hotel that are nearby Gellart in Budapest", 
)

# Print the result obtained from the agent
print(res)
