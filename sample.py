import os

from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.llms.openai import OpenAIModel
from openagi.planner.task_decomposer import TaskPlanner

os.environ["OPENAI_API_KEY"] = "sk-proj-xxxxxxxxxxxxxxxxx"
config = OpenAIModel.load_from_env_config()
llm = OpenAIModel(config=config)

config = AzureChatOpenAIModel.load_from_env_config()
llm = AzureChatOpenAIModel(config=config)


admin = Admin(
    llm=llm,
    actions=[DuckDuckGoSearch],
    planner=TaskPlanner(human_intervene=False),
)


res = admin.run(
    query="3 Day Trip to Bangalore.",
    description="You are a knowledgeable local guide with extensive information about the city, it's attractions and customs",
)


from rich.console import Console
from rich.markdown import Markdown

print("-" * 100)
Console().print(Markdown(res))


# from phi.assistant import Assistant
# from phi.tools.duckduckgo import DuckDuckGo

# assistant = Assistant(tools=[DuckDuckGo()], show_tool_calls=True)
# assistant.print_response("Create a blog article on the topic AI & Cyber Security.", markdown=True)
