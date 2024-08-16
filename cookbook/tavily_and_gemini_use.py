"""
!pip install openagi
!pip install tavily-python
!pip install langchain-google-genai
!pip install yt-dlp youtube-search
"""

from openagi.planner.task_decomposer import TaskPlanner
from openagi.actions.tools.tavilyqasearch import TavilyWebSearchQA
from openagi.agent import Admin
from openagi.llms.gemini import GeminiModel

import os
from getpass import getpass

# setup Gemini and Tavily API Key
os.environ['TAVILY_API_KEY'] = getpass("Enter Tavily API key:")

os.environ['GOOGLE_API_KEY'] = getpass("Enter your Gemini API key:")
os.environ['Gemini_MODEL'] = "gemini-1.5-flash"
os.environ['Gemini_TEMP'] = "0.7"

gemini_config = GeminiModel.load_from_env_config()
llm = GeminiModel(config=gemini_config)

# define the planner
plan = TaskPlanner(autonomous=True,human_intervene=True)

admin = Admin(
    actions = [TavilyWebSearchQA],
    planner = plan,
    llm = llm,
)

res = admin.run(
    query="I need cricket updates from India vs Sri lanka 2024 ODI match in Sri Lanka",
    description=f"give me the results of India vs Sri Lanka ODI and respective Man of the Match",
)
print(res)
