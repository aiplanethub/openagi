# JobSearch Agent

It utilize various tools for internet search and document comparison to fulfill its task. Upon finding the relevant job opportunities, The script configures the agent's role, goal, backstory, capabilities, and specific task to accomplish. Additionally, it initializes logging for debugging purposes and triggers the execution of the agent.

### Import the required document

```python
from openagi.actions.tools.serp_search import GoogleSerpAPISearch
from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
from rich.console import Console
from rich.markdown import Markdown
import os
```

### Setup LLM

```python
os.environ["AZURE_BASE_URL"]="https://<replace-with-your-endpoint>.openai.azure.com/"
os.environ["AZURE_DEPLOYMENT_NAME"] = "<replace-with-your-deployment-name>"
os.environ["AZURE_MODEL_NAME"]="gpt4-32k"
os.environ["AZURE_OPENAI_API_VERSION"]="2023-05-15"
os.environ["AZURE_OPENAI_API_KEY"]=  "<replace-with-your-key>"

config = AzureChatOpenAIModel.load_from_env_config()
llm = AzureChatOpenAIModel(config=config)

company_domain = input("What is the company domain?\n")
job_domain = input("What is the job domain?\n")
job_level = input("What level job are you looking for?\n")
job_location = input("In what location are you for the job?\n")

query = f"""
Need help finding a job description based on the following criteria:

Company Domain: {company_domain}
Job Domain: {job_domain}
Job Level: {job_level}
Job Location: {job_location}

Please provide a list of suitable job descriptions, including the key responsibilities, requirements, and any other relevant details.
"""
```

### Execute Agent LLM

```python
admin = Admin(
    llm=llm,
    actions=[GoogleSerpAPISearch],
    planner=TaskPlanner(human_intervene=False),
    memory=Memory(),
)

res = admin.run(
    query=query,
    description="You are an expert Internet searching agent , who gives best possible response.",
)

# Print the results from the OpenAGI
Console().print(Markdown(res))
```
