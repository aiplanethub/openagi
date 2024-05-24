---
description: Lets build our first Agent use cases.
---

# Quickstart

In this quickstart, we'll explore one of the use cases to demonstrate the execution of the Agent. We'll focus on querying Search Engines tools like `DuckDuckGoSearchTool` to gather the  information on 3 Days Trip to San Francisco and Bay area based on recent days.&#x20;

Agents excel at autonomously performing multiple tasks, making decisions on the fly, and communicating with other agents. For this use case, we will let `Admin` Agent to auto-decompose or `Plan` the task and use tools as the supported `Actions`.&#x20;

### 1. Import required modules

To get started, we need to initialise a few methods from the modules.

* Admin
* Action
* Large Language Model
* Planner

```python
from openagi.agent import Admin
from openagi.actions.files import WriteFileAction
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
```

### 2. Setting LLM configuration

To authenticate your requests to the OpenAI API (by default OpenAI Model will be used), you need to set your API key as an environment variable. This is essential for ensuring secure and authorised access to the API services.&#x20;

```python
import os
os.environ["OPENAI_API_KEY"] = "sk-proj-xxxxxxxxxxxxxxxxxx"
```

Replace `sk-proj-xxxxxxxxxxxxxxxxxx` with your actual OpenAI API key.

### 3. Setup Tools and Action

An action is a functionality that enables the Agent to fetch, process, and store data for further analysis and decision making.

* \``DuckDuckGoSearch`: This tool fetches real-time data using the DuckDuckGo search engine, providing up-to-date information.
* `WriteFileAction`: This action saves the written file to the specified location, ensuring data persistence.

```python
from openagi.actions.files import WriteFileAction
from openagi.actions.tools.ddg_search import DuckDuckGoSearch

actions = [
        DuckDuckGoSearch,
        WriteFileAction,
]
```

### 4. Execute the Admin Agent

The Admin Agent serves as the central part for decision-maker, comprehending task specifications in form of supported actions and executing them in a human-like manner.

In order to execute the agent, user needs to specify their query and description to get the response from the Admin agent.&#x20;

```python
from openagi.agent import Admin

admin = Admin(
    actions=actions,  
)

result = admin.run(
    query="3 Days Trip to san francisco bay area",
    description="You are a knowledgeable local guide with extensive information about the city, it's attractions and customs",
)

print(result)
```
