from openagi.actions.console import ConsolePrint
from openagi.actions.files import CreateFileAction, WriteFileAction
from openagi.actions.formatter import FormatterAction
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.actions.tools.serp_search import GoogleSerpAPISearch
from openagi.actions.obs_rag import MemoryRagAction

from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.llms.openai import OpenAIConfigModel, OpenAIModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
from openagi.agent import OutputFormat
import os

os.environ["OPENAI_API_KEY"] = "xxxx"

config = OpenAIModel.load_from_env_config()
llm = OpenAIModel(config=config)


admin = Admin(
    llm=llm,
    actions=[DuckDuckGoSearch],
    planner=TaskPlanner(human_intervene=False),
    memory=Memory(),
    # output_type=OutputFormat.markdown, # Defaults to markdown
)


# res = admin.run(
# query="Whats happening in France?",
# description="You are an expert News AI, who gives the best possible response.",
# )
res = admin.run(
    query="Create chess game in python.",
    description="You are an expert Python Coding AI, who gives the best possible response.",
)

from rich.console import Console
from rich.markdown import Markdown


print("-" * 100)
Console().print(Markdown(res))
