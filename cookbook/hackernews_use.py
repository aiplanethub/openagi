"""
Example demonstrating how to use the HackerNews tool in OpenAGI
both with the Agent system and directly.

Requirements:
!pip install openagi
"""

from openagi.planner.task_decomposer import TaskPlanner
from openagi.actions.tools.hackernews import HackerNewsTopStories
from openagi.agent import Admin
from openagi.llms.gemini import GeminiModel

import os
from getpass import getpass

# Setup Gemini API Key
os.environ['GOOGLE_API_KEY'] = getpass("Enter your Gemini API key:")
os.environ['Gemini_MODEL'] = "gemini-1.5-flash"
os.environ['Gemini_TEMP'] = "0.7"

# Initialize Gemini model
gemini_config = GeminiModel.load_from_env_config()
llm = GeminiModel(config=gemini_config)

# Define the planner
plan = TaskPlanner(autonomous=True, human_intervene=True)

# Initialize Admin agent with HackerNews tool
admin = Admin(
	actions=[HackerNewsTopStories],
	planner=plan,
	llm=llm,
)

# Run the agent to get HackerNews updates
res = admin.run(
	query="Get me the top 5 trending stories from Hacker News",
	description="Fetch the top 5 stories from Hacker News and provide a summary of each story including title, author, score, and number of comments"
)
print("\nHacker News Top Stories Results:")
print(res)

# Example of direct tool usage without the agent
print("\nDirect Tool Usage Example:")
hn_stories = HackerNewsTopStories(
	name="Hacker News Top Stories",
	num_stories=3
)
stories = hn_stories.execute()

print("\nTop 3 HackerNews Stories (Direct Access):")
for idx, story in enumerate(stories, 1):
	print(f"\n{idx}. {story['title']}")
	print(f"   URL: {story['url']}")
	print(f"   Score: {story['score']}")
	print(f"   Author: {story['author']}")
	print(f"   Comments: {story['comments_count']}")