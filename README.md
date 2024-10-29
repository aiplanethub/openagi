<div align="center">
<h1 align="center">OpenAGI </h1>
<h2 align="center">Making the development of autonomous human-like agents accessible to all</h2>

<a href="https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11-3776AB.svg?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11-3776AB.svg?style=flat&logo=python&logoColor=white" alt="Python Versions"></a>
<a href="https://discord.gg/4aWV7He2QU"><img src="https://dcbadge.vercel.app/api/server/4aWV7He2QU?style=flat" alt="Discord" /></a>
<a href="https://twitter.com/aiplanethub"><img src="https://img.shields.io/twitter/follow/aiplanethub" alt="Twitter" /></a>

<p>OpenAGI aims to make human-like agents accessible to everyone, thereby paving the way towards open agents and, eventually, AGI for everyone. We strongly believe in the transformative power of AI and are confident that this initiative will significantly contribute to solving many real-life problems. Currently, OpenAGI is designed to offer developers a framework for creating autonomous human-like agents.</p>
<i><a href="https://discord.gg/4aWV7He2QU">👉 Join our Discord community!</a></i>
</div>

## Installation

1. Setup a virtual environment.

```bash
# For Mac and Linux users
python3 -m venv venv
source venv/bin/activate

# For Windows users
python -m venv venv
venv/scripts/activate
```

2. Install the openagi

```bash
pip install openagi
```

or 
```
git clone https://github.com/aiplanethub/openagi.git
pip install -e .
```

## To setup your credentials

Follow this quick [installation guide](https://openagi.aiplanet.com/getting-started/installation) to complete the setup.

## Documentation

For more queries find documentation for OpenAGI at [openagi.aiplanet.com](https://openagi.aiplanet.com/)

## Understand OpenAGI

![Thumbnails](https://github.com/aiplanethub/openagi/blob/dev/assets/openagi.png)

## Example (Manual Agent Execution)

Workers are used to create a Multi-Agent architecture.

Follow this example to create a **Trip Planner Agent** that helps you plan the itinerary to SF. 

```py
from openagi.agent import Admin
from openagi.planner.task_decomposer import TaskPlanner
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.llms.openai import OpenAIModel
from openagi.worker import Worker

plan = TaskPlanner(human_intervene=False)
action = DuckDuckGoSearch

import os
os.environ['OPENAI_API_KEY'] = "sk-xxxx"
config = OpenAIModel.load_from_env_config()
llm = OpenAIModel(config=config)

trip_plan = Worker(
        role="Trip Planner",
        instructions="""
        User loves calm places, suggest the best itinerary accordingly.
        """,
        actions=[action],
        max_iterations=10)

admin = Admin(
    llm=llm,
    actions=[action],
    planner=plan,
)
admin.assign_workers([trip_plan])

res = admin.run(
    query="Give me total 3 Days Trip to San francisco Bay area",
    description="You are a knowledgeable local guide with extensive information about the city, it's attractions and customs",
)
print(res)
```

## Example (Autonomous Multi-Agent Execution)

Lets build a **Sports Agent** now that can run autonomously without any Workers.

```py
from openagi.planner.task_decomposer import TaskPlanner
from openagi.actions.tools.tavilyqasearch import TavilyWebSearchQA
from openagi.agent import Admin
from openagi.llms.gemini import GeminiModel

import os
from getpass import getpass

# setup Gemini and Tavily API Key
os.environ['TAVILY_API_KEY'] = getpass("Enter Tavily API key:")
os.environ['GOOGLE_API_KEY'] = getpass("Enter your Gemini API key:")
os.environ['Gemini_MODEL'] = "gemini-1.5-flash"
os.environ['Gemini_TEMP'] = "0.1"

gemini_config = GeminiModel.load_from_env_config()
llm = GeminiModel(config=gemini_config)

# define the planner
plan = TaskPlanner(autonomous=True,human_intervene=True)

admin = Admin(
    actions = [TavilyWebSearchQA],
    planner = plan,
    llm = llm,
)
res = admin.run(
    query="I need cricket updates from India vs Sri lanka 2024 ODI match in Sri Lanka",
    description=f"give me the results of India vs Sri Lanka ODI and respective Man of the Match",
)
print(res)
``` 

## Long Term Memory like never before

With LTM, OpenAGI agents can now:

- Recall past interactions to provide continuity in conversations.
- Learn and adapt based on user inputs over time.
- Deliver contextually relevant responses by referencing previous conversations.
- Improve their accuracy and efficiency with each successive interaction.

```py
import os
from openagi.agent import Admin
from openagi.llms.openai import OpenAIModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
from openagi.worker import Worker
from openagi.actions.tools.ddg_search import DuckDuckGoSearch

memory = Memory(long_term=True)

os.environ['OPENAI_API_KEY'] = "-"
config = OpenAIModel.load_from_env_config()
llm = OpenAIModel(config=config)

web_searcher = Worker(
    role="Web Researcher",
    instructions="""
    You are tasked with conducting web searches using DuckDuckGo.
    Find the most relevant and accurate information based on the user's query.
    """,
    actions=[DuckDuckGoSearch], 
)

admin = Admin(
    actions=[DuckDuckGoSearch],
    planner=TaskPlanner(human_intervene=False),
    memory=memory,
    llm=llm,
)
admin.assign_workers([web_searcher])

query = input("Enter your search query: ")
description = f"Find accurate and relevant information for the query: {query}"

res = admin.run(query=query,description=description)
print(res)
```

## Use Cases:

- **Education:** In education, agents can provide personalized learning experiences. They adapt and tailor learning content based on student's progress, performance and interests. It can extend to automating various other administrative tasks and assist teachers in improving their productivity.
- **Finance and Banking:** Financial services can use agents for fraud detection, risk assessment, personalized banking advice, automating trading, and customer service. They help in analyzing large volumes of transactions to identify suspicious activities and offer tailored investment advice.
- **Healthcare:** Agents can be deployed to monitor patients, provide personalized health recommendations, manage patient data, and automate administrative tasks. They can also assist in diagnosing diseases based on symptoms and medical history.

## Get in Touch

For any queries/suggestions/support connect us at [openagi@aiplanet.com](mailto:openagi@aiplanet.com)

## Contribution guidelines

OpenAGI thrives in the rapidly evolving landscape of open-source projects. We wholeheartedly welcome contributions in various capacities, be it through innovative features, enhanced infrastructure, or refined documentation.

For a comprehensive guide on the contribution process, please click [here](https://github.com/aiplanethub/openagi/blob/main/dev/Readme.md).
