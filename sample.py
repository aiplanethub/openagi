from openagi.actions.console import ConsolePrint
from openagi.actions.files import CreateFileAction, WriteFileAction
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner

config = AzureChatOpenAIModel.load_from_env_config()
llm = AzureChatOpenAIModel(config=config)


admin = Admin(
    llm=llm,
    actions=[CreateFileAction, WriteFileAction, DuckDuckGoSearch, ConsolePrint],
    planner=TaskPlanner(human_intervene=False),
    memory=Memory(),
)

description = """
Create a list of detailed itineraries for a 3-day trip to Bangalore, India. Include the following:

Popular tourist attractions to visit each day.
Recommended restaurants and cafes for breakfast, lunch, and dinner.
Options for local experiences or activities unique to Bangalore.
Any travel tips or advice for getting around the city.

"""

print("Admin init")
print(admin.run(query="Create a list of itineries in bangalore.", description=description))
