---
description: Lets build our first Agent use cases.
---

# 🚀 Quickstart

In this quickstart, we'll explore one of the use cases to demonstrate the execution of the Agent. We'll focus on querying Search Engines tools like `DuckDuckGoSearchTool` to gather the  information on 3 Days Trip to San Francisco and Bay area based on recent days.&#x20;

Agents excel at autonomously performing multiple tasks, making decisions on the fly, and communicating with other agents. For this use case, we will let `Admin` Agent to auto-decompose or `Plan` the task and use tools as the supported `Actions`.&#x20;

### 1. Import required modules

To get started, we need to initialize a few methods from the modules.

* Admin
* Worker
* Action
* Large Language Model
* Memory
* Planner

```python
from openagi.agent import Admin
from openagi.worker import Worker
from openagi.actions.files import WriteFileAction
from openagi.actions.tools.ddg_search import DuckDuckGoNewsSearch
from openagi.actions.tools.webloader import WebBaseContextTool
from openagi.llms.openai import OpenAIModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
```

### 2. Setting LLM configuration

To authenticate your requests to the OpenAI API (by default OpenAI Model will be used), you need to set your API key as an environment variable. This is essential for ensuring secure and authorised access to the API services.&#x20;

```python
import os
os.environ["OPENAI_API_KEY"] = "sk-proj-xxxxxxxxxxxxxxxxxx"

config = OpenAIModel.load_from_env_config()
llm = OpenAIModel(config=config)
```

Replace `sk-proj-xxxxxxxxxxxxxxxxxx` with your actual OpenAI API key.

### 3. Setup Workers with Tools and Action

Workers are specialized classes tasked with executing the assignments given by the "Admin" class. They use tools such as internet news search engines, LLMs, and document writers to complete their tasks, individually and in cohesion (for complex tasks like writing blog articles).

An action is a functionality that enables the Agent to fetch, process, and store data for further analysis and decision-making.

* `DuckDuckGoNewsSearch`: This tool fetches real-time news data using the DuckDuckGo search engine, providing up-to-date information.
* `WebBaseContextTool`: This tool is used to extract information from Web Pages. It also provides a way to load and optionally summarize the content of a webpage.
* `WriteFileAction`: This action saves the written file to the specified location, ensuring data persistence.

```python
# Declare the Worker objects

# Initialize the researcher who uses DuckDuckGo to search a topic and extract information from the web pages.
researcher = Worker(
    role="Researcher",
    instructions="sample instruction.",
    actions=[
        DuckDuckGoNewsSearch,
        WebBaseContextTool,
    ],
)
# initialize the writer who writes the content of the topic using the tools provided
writer = Worker(
    role="Writer",
    instructions="sample instruction.",
    actions=[
        DuckDuckGoNewsSearch,
        WebBaseContextTool,
    ],
)
# initialize the reviewer who reviews the content written by the writer and saves the content into a file using the write file action tool.
reviewer = Worker(
    role="Reviewer",
    instructions="sample instruction.",
    actions=[
        DuckDuckGoNewsSearch,
        WebBaseContextTool,
        WriteFileAction,
    ],
)
```

### 4. Execute the Admin Agent

The Admin Agent serves as the central part for decision-maker, comprehending task specifications in form of supported actions and executing them in a human-like manner.

In order to execute the agent, user needs to specify their query and description to get the response from the Admin agent.&#x20;

```python
# define the Admin with Planner, Memory and LLM. Further assign the workers in order
admin = Admin(
    planner=TaskPlanner(human_intervene=False),
    memory=Memory(),
    llm=llm,
)

# Assign sub-tasks to workers
admin.assign_workers([researcher, writer, reviewer])

result = admin.run(
    query="Write an article on places to visit in Spain.",
    description="You are a knowledgeable local guide with extensive information about Spain, its attractions and customs.",
)

print(result)
```
