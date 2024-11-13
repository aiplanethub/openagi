# Import required modules from the OpenAGI framework
from openagi.planner.task_decomposer import TaskPlanner  # For autonomous task planning
from openagi.agent import Admin  # Main agent class that orchestrates the process
from openagi.actions.tools.document_loader import TextLoaderTool  # Tool for reading text files
from openagi.llms.xai import XAIModel  # XAI language model integration
import os

# Configure the text loader tool to read from a specific file
# This tool will look for answers in the specified file path
TextLoaderTool.set_config({
    "filename": "src/answer.txt"  # Path to the file containing the answer
})

# Set up the API key for the XAI model
# This should be replaced with your actual API key
os.environ['XAI_API_KEY'] = "<replace-with-key>"

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
# - actions: List of available tools (only TextLoaderTool in this case)
# - planner: The task planner that decides what actions to take
# - llm: The language model that will process the text and generate responses
admin = Admin(
    actions=[TextLoaderTool],
    planner=plan,
    llm=llm,
)

# Execute the agent with a specific query
# query: The question we want to answer
# description: Brief description of what the agent should do
res = admin.run(
    query="who is Virat kohli friend",  # The question about Virat Kohli's friends
    description="read from file",  # Instructs the agent to read the answer from the file
)

# Print the result obtained from the agent
print(res)
