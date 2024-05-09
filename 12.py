from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.actions.files import CreateFileAction, WriteFileAction

config = AzureChatOpenAIModel.load_from_env_config()
llm = AzureChatOpenAIModel(config=config)


a = Admin(llm=llm, actions=[CreateFileAction, WriteFileAction])
print("Admin init")
print(a.run("Create a chess game in python."))
