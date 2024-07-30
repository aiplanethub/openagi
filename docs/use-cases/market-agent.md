---
description: >-
  This example uses OpenAGI to create trip itineraries by leveraging an OpenAI
  model through an Admin agent, with results displayed using Markdown via the
  rich library.
---

# 📅 Itinerary Planner

**Import Required Libraries**

First, import the necessary libraries and modules. These modules will enable the agent to perform web searches, handle task planning, write files, and display results in a readable format.

```python
from openagi.actions.files import WriteFileAction
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.agent import Admin
from openagi.llms.openai import OpenAIModel
from openagi.planner.task_decomposer import TaskPlanner
from rich.console import Console
from rich.markdown import Markdown
import os
```

**Setup LLM**

Set up the environment variables required for the OpenAI configuration. These environment variables include the API key necessary for accessing the OpenAI services. This configuration is essential for the Large Language Model (LLM) to function correctly.

```python
# Set up the environment variables for OpenAI
os.environ["OPENAI_API_KEY"] = "sk-proj-xxxxxxxxxxxxxxxxxx"

# Initialize the OpenAI Model
config = OpenAIModel.load_from_env_config()
llm = OpenAIModel(config=config)
```

**Define Admin**

Create an Admin instance to manage actions and execute tasks. The Admin will use the DuckDuckGoSearch tool to perform web searches, the WriteFileAction to save results, and the TaskPlanner to manage task execution without human intervention.

```python
# Set up the Admin Agent
admin = Admin(
    llm=llm,
    actions=[
        DuckDuckGoSearch,
        WriteFileAction,
    ],
    planner=TaskPlanner(
        human_intervene=False,
    ),
)
```

**Execute Agent LLM**

Run the Admin with a specific query to create an itinerary for a trip to the San Francisco Bay Area. The Admin will process this query and return a detailed itinerary based on the latest information available.

```python
# Execute the Agent to create an itinerary
   response = Admin(actions=[DuckDuckGoSearch]).run(
    query="3 Days Trip to san francisco bay area",
    description="You are a knowledgeable local guide with extensive information about the city, it's attractions and customs",
)
```

**Print the Results**

Finally, use the rich library to output the results in a readable format. The Markdown class helps in rendering the itinerary content neatly in the console.

```python
# Print the results from OpenAGI using rich library
Console().print(Markdown(res))
```

By following these steps, you can set up a News Agent that helps you plan activities or trips effectively. This example uses the power of the OpenAI model and OpenAGI to perform efficient web searches and present the information in an easily digestible format, ensuring you stay informed and well-prepared.
