---
description: >-
  This example uses OpenAGI to create trip itineraries by leveraging an OpenAI
  model through an Admin agent, with results displayed using Markdown via the
  rich library.
---

# Itinerary Planner

**Import Required Libraries**

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

```python
# Set up the environment variables for OpenAI
os.environ["OPENAI_API_KEY"] = "sk-proj-xxxxxxxxxxxxxxxxxx"

# Initialize the OpenAI Model
config = OpenAIModel.load_from_env_config()
llm = OpenAIModel(config=config)
```

**Define Admin**

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

```python
# Execute the Agent to create an itinerary
res = admin.run(
    query="3 Days Trip to San Francisco Bay Area",
    description="You are a knowledgeable local guide with extensive information about the city, its attractions, and customs.",
)
```

**Print the Results**

```python
# Print the results from OpenAGI using rich library
Console().print(Markdown(res))
```
