# 🛠️ Tools

## What is Tool?

Tool is a functionality based on which the data is fetched to the Agent for further analysis and decision making. A wide array of tools is cataloged in the tools database, designed to support activities such as internet searches, email dispatch, interactions with Git repositories, and much more. Users have the flexibility to create their own tools and seamlessly integrate them into the framework's operations.

> Note: Some of the tools are not pre-installed with the OpenAGI library. If you encounter an `OpenAGIException` due to an Import Error, you'll need to manually install the required package to use the tool.

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
```

Get your GitHub Access Token: [https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

```python
from openagi.actions.tools import GitHubFileLoadAction
from openagi.agent import Admin
from openagi.llms import OpenAIModel
from openagi.planner.task_decomposer import TaskPlanner

admin = Admin(
    llm = llm,
    actions=[GitHubFileLoadAction],
    planner=TaskPlanner(),
)
```

### 5. YouTube Search Tool

The YouTube Search tool allows users to search for videos on YouTube using natural language queries. This tool retrieves relevant video content based on user-defined search parameters, making it easier to find specific videos or topics of interest.

The YouTube Search tool does not require an API key but does require the installation of specific libraries. You need to install `yt-dlp` and `youtube-search` to use this tool.

```
pip install yt-dlp
pip install youtube-search
```

**Code Snippet** To initialize the YouTube Search tool, you can use the following code:

```python
from openagi.actions.tools import YouTubeSearch
from openagi.agent import Admin
from openagi.llms import OpenAIModel
from openagi.planner.task_decomposer import TaskPlanner

admin = Admin(
    llm=llm,
    actions=[YouTubeSearch],
    planner=TaskPlanner(),
)
```

### 6. Tavily QA Search Tool

The Tavily QA Search tool is designed to provide answers to user queries by fetching data from various online sources. This tool enhances the capability of the agent to retrieve precise information and answer questions effectively.

**Installation**

```
pip install tavily-python
```

For the Tavily QA Search tool, you also need to set up the API key in your environment variables:

```python
import os

# Set the Tavily API key in the environment variable
os.environ['TAVILY_API_KEY'] = "<replace-with-your-tavily-api-key>"
```

**Code Snippet** To initialize the Tavily QA Search tool, you can use the following code:

```python
from openagi.actions.tools import TavilyWebSearchQA
from openagi.agent import Admin
from openagi.llms import OpenAIModel
from openagi.planner.task_decomposer import TaskPlanner

admin = Admin(
    llm=llm,
    actions=[TavilyQASearch],
    planner=TaskPlanner(),
)
```

### 7. Exa Search Tool

The Exa Search tool allows users to query the Exa API to retrieve relevant responses based on user-defined questions. This tool is particularly useful for extracting information and insights from various data sources using natural language queries.

**Installation**

```
pip install exa-py
```

To use the Exa Search tool, you need to set up the API key in your environment variables. Here’s how to do that:

```python
import os

# Set the Exa API key in the environment variable
os.environ['EXA_API_KEY'] = "<replace-with-your-exa-api-key>"
```



**Code Snippet**

```python
from openagi.actions.tools import ExaSearch
from openagi.agent import Admin
from openagi.llms import OpenAIModel
from openagi.planner.task_decomposer import TaskPlanner

admin = Admin(
    llm=llm,
    actions=[ExaSearch],
    planner=TaskPlanner(),
)
```

### 8. Unstructured PDF Loader Tool

The Unstructured PDF Loader tool is designed to extract content, including metadata, from PDF files. It utilizes the Unstructured library to partition the PDF and chunk the content based on titles. This tool is useful for processing large volumes of PDF documents and making their contents accessible for further analysis.

**Installation**

```
pip install unstructured
```

**Code Snippet**

```python
from openagi.actions.tools import UnstructuredPdfLoaderAction
from openagi.agent import Admin
from openagi.llms import OpenAIModel
from openagi.planner.task_decomposer import TaskPlanner

admin = Admin(
    llm=llm,
    actions=[UnstructuredPdfLoaderAction],
    planner=TaskPlanner(),
)
```

### How to build a custom Tool?

In OpenAGI, building a custom tool is straightforward by wrapping your custom logic inside a class that inherits from `BaseAction` and implementing the `execute` method. This setup allows you to encapsulate the necessary configurations and operations within the custom tool, making it easy to integrate and use within the OpenAGI framework.

#### Syntax

1. **Import Necessary Modules:**
   * Begin by importing the necessary modules from `pydantic` and `openagi`. `Field` is used to define parameters, and `BaseAction` is the base class for creating custom actions in OpenAGI.
2. **Define the Custom Tool Class:**
   * Create a class `CustomToolName` that inherits from `BaseAction`. This class represents your custom tool.
   * Within the class, define a variable `vars` using `Field()` from `pydantic`. This variable will hold any parameters required by your tool. Replace `dtype` with the actual data type of the parameter (e.g., `str`, `int`, `List[str]`).
3. **Implement the `execute` Method:**
   * The `execute` method is where the core logic of your tool will be implemented. This method will be called when the tool is executed.
   * Inside the `execute` method, write the code necessary, this might include loading data, processing it, and returning the desired output.
   * Make sure the execute function returns `str` data.&#x20;

```python
from pydantic import Field
from openagi.actions.base import BaseAction

class CustomToolName(BaseAction):
    """
    docstring for the tool is must
    """
    vars: dtype = Field() #define the required parameters for your tool. 
    
    def execute(self):
        # tool integration code
        return "str data"
```

#### **Example**

In this custom tool integration example, we will implement the Unstructured IO data loading tool. This custom tool provides the flexibility to act as a wrapper for Unstructured IO as an action tool in OpenAGI.&#x20;

The `execute` function is where the magic happens; if any variables or parameters need to be defined, they should be declared within the Custom Tool class. This setup ensures that all necessary configurations and parameters are encapsulated within the tool, allowing for seamless and efficient data loading and processing.

```python
from pydantic import Field
from openagi.actions.base import BaseAction

from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title


class UnstructuredPdfLoaderAction(BaseAction):
    """
    Use this Action to extract content from PDFs including metadata.
    Returns a list of dictionary with keys 'type', 'element_id', 'text', 'metadata'.
    """
    file_path: str = Field(
        default_factory=str,
        description="File or pdf file url from which content is extracted.",
    )

    def execute(self):        
        elements = partition_pdf(self.file_path, extract_images_in_pdf=True)
        chunks = chunk_by_title(elements)

        dict_elements = []
        for element in chunks:
            dict_elements.append(element.to_dict())

        with open("ele.txt", "w") as f:
            f.write(str(dict_elements))

        return str(dict_elements)
```

For more examples of Tools integration, check reference code snippets here: [https://github.com/aiplanethub/openagi/tree/main/src/openagi/actions/tools](https://github.com/aiplanethub/openagi/tree/main/src/openagi/actions/tools)
