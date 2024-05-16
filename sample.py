from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.actions.files import WriteFileAction, CreateFileAction
from openagi.planner.task_decomposer import TaskPlanner
from openagi.memory import Memory


config = AzureChatOpenAIModel.load_from_env_config()
llm = AzureChatOpenAIModel(config=config)


admin = Admin(
    llm=llm,
    actions=[CreateFileAction, WriteFileAction],
    planner=TaskPlanner(human_intervene=False),
    memory=Memory(),
)
print("Admin init")
print(admin.run(query="Create a chess game in python.", description="....."))