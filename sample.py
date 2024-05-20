from openagi.actions.console import ConsolePrint
from openagi.actions.files import CreateFileAction, WriteFileAction
from openagi.actions.formatter import FormatterAction
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.actions.tools.serp_search import GoogleSerpAPISearch
from openagi.actions.obs_rag import MemoryRagAction

from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
from openagi.agent import OutputFormat

config = AzureChatOpenAIModel.load_from_env_config()
llm = AzureChatOpenAIModel(config=config)


admin = Admin(
    llm=llm,
    actions=[DuckDuckGoSearch],
    planner=TaskPlanner(human_intervene=False),
    memory=Memory(),
    output_type=OutputFormat.markdown,
)


res = admin.run(
    query="3 days Itinaries in Bangalore",
    description="You are an expert Itinary AI, who gives the best possible response.",
)

from rich.console import Console
from rich.markdown import Markdown

Console().print(Markdown(res))
