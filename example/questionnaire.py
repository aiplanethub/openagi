from openagi.actions.tools.document_loader import DocumentLoader
from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
from rich.console import Console
from rich.markdown import Markdown
import os

if __name__ == "__main__":    
    config = AzureChatOpenAIModel.load_from_env_config()
    llm = AzureChatOpenAIModel(config=config)

    file_path = input("Select file to make a questionnaire:\n")
    
    query = f"""
Load the following file {file_path} and create a questionnaire with the information.
"""
    admin = Admin(
        llm=llm,
        actions=[DocumentLoader],
        planner=TaskPlanner(human_intervene=False),
        memory=Memory(),
    )

    res = admin.run(
        query=query,
        description="",
    )

    # Print the results from the OpenAGI
    print("-" * 100)  # Separator
    Console().print(Markdown(res))