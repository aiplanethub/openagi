# Manual Task Planned by User

## Using Mistral and Tavily

from openagi.planner.task_decomposer import TaskPlanner
from openagi.actions.tools.tavilyqasearch import TavilyWebSearchQA
from openagi.agent import Admin
from openagi.llms.mistral import MistralModel

import os
from getpass import getpass

# setup Gemini and Tavily API Key
os.environ['TAVILY_API_KEY'] = getpass("Tavily API Key: ")
os.environ['MISTRAL_API_KEY'] = getpass("Mistral API Key: ")

gemini_config = MistralModel.load_from_env_config()
llm = MistralModel(config=gemini_config)

# define the planner
plan = TaskPlanner(autonomous=True,human_intervene=True)

admin = Admin(
    actions = [TavilyWebSearchQA],
    planner = plan,
    llm = llm,
)

already_planned = [{'worker_name': 'CricketNewsScraper', 'role': 'Cricket Data Extractor', 'instruction': 'Retrieve the latest cricket updates for the India vs Sri Lanka ODI series in 2024 from reliable sources.', 'task_id': '1', 'task_name': 'FetchCricketUpdates', 'description': "Use TavilyWebSearchQA to search for 'India vs Sri Lanka ODI series 2024 results' and extract the relevant information. Focus on finding the match scores, Man of the Match, and other key details. Handle any potential errors by retrying the search or providing a fallback message.", 'supported_actions': ['TavilyWebSearchQA']}, {'worker_name': 'CricketResultSummarizer', 'role': 'Data Processor', 'instruction': 'Analyze the retrieved cricket data and summarize the results for the user.', 'task_id': '2', 'task_name': 'SummarizeCricketResults', 'description': 'Use MemoryRagAction to access the results from the previous task. Extract the match scores, Man of the Match, and other key details. Format the information in a clear and concise manner for the user.', 'supported_actions': ['MemoryRagAction']}]

res = admin.run(
    query="I need cricket updates from India vs Sri lanka 2024 ODI match in Sri Lanka",
    description=f"give me the results of India vs Sri Lanka ODI and respective Man of the Match",
    planned_tasks = already_planned
)
print(res)