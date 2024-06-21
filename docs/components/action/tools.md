# Tools

## What is Tool?

Tool is a functionality based on which the data is fetched to the Agent for further analysis and decision making. A wide array of tools is cataloged in the tools database, designed to support activities such as internet searches, email dispatch, interactions with Git repositories, and much more. Users have the flexibility to create their own tools and seamlessly integrate them into the framework's operations.

## Tool configuration

### 1. DuckDuckGoSearch Tool

The DuckDuckGoSearch tool is a tool that can be used to search for words, documents, images, videos, news, maps and text translation using the DuckDuckGo.com search engine. DuckDuckGo Search is a web search engine that _DuckDuckGo_ is an independent Google alternative that lets you search and browse the web, but it emphasises protecting user privacy and avoiding the filter bubble of personalised search results.

```python
from openagi.actions.tools import DuckDuckGoSearch
from openagi.agent import Admin
from openagi.llms import OpenAIModel
from openagi.planner.task_decomposer import TaskPlanner

admin = Admin(
    llm = llm,
    actions=[DuckDuckGoSearch],
    planner=TaskPlanner(),
)
```

### 2. Serper Search Tool

Serper is a low-cost Google Search API that can be used to add answer box, knowledge graph, and organic results data from Google Search. This tool is mainly helps user to query the Google results with less throughput and latency.&#x20;

#### Setup API

```python
import os

os.environ['SERPER_API_KEY'] = "<replace-with-your-api-key>"
```

Get your API key: [https://serper.dev/](https://serper.dev/)

```python
from openagi.actions.tools import SerperSearch
from openagi.agent import Admin
from openagi.llms import OpenAIModel
from openagi.planner.task_decomposer import TaskPlanner

admin = Admin(
    llm = llm,
    actions=[SerperSearch],
    planner=TaskPlanner(),
)
```

### 3.  Google Serp API Search

Serp API is yet another solution to integrate search data. SERP stands for _Search Engine Results Page_. It refers to the page displayed by a search engine in response to a user's query.

#### Setup API

```python
import os

os.environ['GOOGLE_SERP_API_KEY'] = "<replace-with-your-api-key>"
```

Get your API key: [https://serpapi.com/manage-api-key/](https://serpapi.com/manage-api-key/)

```python
from openagi.actions.tools import GoogleSerpAPISearch
from openagi.agent import Admin
from openagi.llms import OpenAIModel
from openagi.planner.task_decomposer import TaskPlanner

admin = Admin(
    llm = llm,
    actions=[SerperSearch],
    planner=TaskPlanner(),
)
```

### 4. Github Search Tool

The Github SearchTool is used for retrieving information from Github repositories using natural language queries. This tool provides functionality for querying Github repositories for various information, such as code changes, commits, active pull requests, issues, etc., using natural language input. It is designed to be used as part of a larger AI-driven agent system.

#### Setup API

```python
import os

os.environ['GITHUB_ACCESS_TOKEN'] = "<add-your-access-token>"
os.environ['GITHUB_PRIVATE_KEY'] = "<your-private-id>"
```

Get your API key:&#x20;

```python
from openagi.actions.tools import GithubSearchTool
from openagi.agent import Admin
from openagi.llms import OpenAIModel
from openagi.planner.task_decomposer import TaskPlanner

admin = Admin(
    llm = llm,
    actions=[GithubSearchTool],
    planner=TaskPlanner(),
)
```

