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
    no_of_ques = input("Number of question's you want in questionnaire:\n")
    
    query = f"""
Help me create a questionnaire based on the information provided in the attached file.

File Path: {file_path}

Number of Questions Needed: {no_of_ques}

Requirements:

- Do not provide any hints in the questions.
- Ensure all questions are distinct from each other.
"""

    admin = Admin(
        llm=llm,
        actions=[DocumentLoader],
        planner=TaskPlanner(human_intervene=False),
        memory=Memory(),
    )

    res = admin.run(
        query=query,
        description="You are an expert AI agent , who is able to understand the information in the file",
    )

    # Print the results from the OpenAGI
    print("-" * 100)  # Separator
    Console().print(Markdown(res))