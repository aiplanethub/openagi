# 🛠️ Tools

## What is Tool?

Tool is a functionality based on which the data is fetched to the Agent for further analysis and decision making. A wide array of tools is cataloged in the tools database, designed to support activities such as internet searches, email dispatch, interactions with Git repositories, and much more. Users have the flexibility to create their own tools and seamlessly integrate them into the framework's operations.

> Note: Some of the tools are not pre-installed with the OpenAGI library. If you encounter an `OpenAGIException` due to an Import Error, you'll need to manually install the required package to use the tool.

## Tool configuration

### 1. DuckDuckGoSearch Tool

The DuckDuckGoSearch tool is a tool that can be used to search for words, documents, images, videos, news, maps and text translation using the DuckDuckGo.com search engine. DuckDuckGo Search is a web search engine that _DuckDuckGo_ is an independent Google alternative that lets you search and browse the web, but it emphasises protecting user privacy and avoiding the filter bubble of personalised search results.

```python
from openagi.actions.tools.ddg_search import DuckDuckGoSearch

# Initialize the DuckDuckGo search tool
ddg_tool = DuckDuckGoSearch(
    query="Your search query"  # Required: The search term to look up
)

# Execute the search
result = ddg_tool.execute()
# Returns search results including web pages and content
```

### 2. Serper Search Tool

Serper is a low-cost Google Search API that can be used to add answer box, knowledge graph, and organic results data from Google Search. This tool is mainly helps user to query the Google results with less throughput and latency.&#x20;

**Setup API**

There are two ways to configure the API key:

1. Using the recommended configuration method:

```python
from openagi.actions.tools.serper_search import GoogleSerpAPISearch
GoogleSerpAPISearch.set_config(api_key='your-api-key')
```

2. Using environment variables (deprecated):

```python
import os
os.environ['GOOGLE_SERP_API_KEY'] = "<replace-with-your-api-key>"
```

Get your API key: [https://serper.dev/](https://serper.dev/)

Usage:

```python
from openagi.actions.tools.serp_search import GoogleSerpAPISearch

# Initialize the Serper search tool
serp_tool = GoogleSerpAPISearch(
    query="Your search query",  # Required: The search query to look up
    max_results=10             # Optional: Number of results to return (default: 10)
)

# Execute the search
result = serp_tool.execute()
# Returns formatted search results with titles, snippets, and URLs
```

The tool requires the following parameters:

* `query`: The search query string to look up on Google
* `max_results`: (Optional) Number of results to return, defaults to 10

The tool will return search results including titles, snippets, and URLs from Google search results.&#x20;

### 3. Google Search Tool

The Google Search Tool enables searching and extracting information from Google search results using the googlesearch-python library. This tool provides a simple way to scrape Google search results without requiring an API key.

**Installation**

```bash
pip install googlesearch-python
```

Usage:

```python
from openagi.actions.tools.google_search_tool import GoogleSearchTool

# Initialize the Google search tool
google_tool = GoogleSearchTool(
    query="Your search query",          # Required: The search query to look up
    max_results=10,                     # Optional: Number of results (default: 10, max: 15)
    lang="en"                           # Optional: Language for search results (default: "en")
)

# Execute the search
result = google_tool.execute()
# Returns formatted search results with titles, descriptions, and URLs
```

### 4. SearchApiSearch

[SearchApi.io](https://searchapi.io/) provides a real-time API to access search results from Google (default), Google Scholar, Bing, Baidu, and other search engines. Any existing or upcoming SERP engine that returns `organic_results` is supported. The default web search engine is `google`, but it can be changed to `bing`, `baidu`, `google_news`, `bing_news`, `google_scholar`, `google_patents`, and others.

**Setup API Key**

There are two ways to configure the API key:

1. Using the recommended configuration method:

```python
from openagi.actions.tools.searchapi_search import SearchApiSearch
SearchApiSearch.set_config(api_key='your-api-key', engine='google')  # engine is optional
```

2. Using environment variables (deprecated):

```python
import os
os.environ['SEARCHAPI_API_KEY'] = "<replace-with-your-api-key>"
```

Get your API key from [SearchApi.io](https://vscode-file/vscode-app/Applications/Aide.app/Contents/Resources/app/out/vs/code/electron-sandbox/workbench/workbench.html).

Usage:

```python
from openagi.actions.tools.searchapi_search import SearchApiSearch

# Configure API key (recommended way)
SearchApiSearch.set_config(api_key='your-api-key', engine='google')

# Initialize the SearchAPI tool
search_api_tool = SearchApiSearch(
    query="Your search query"  # Required: The search query to look up
)

# Execute the search
result = search_api_tool.execute()
# Returns search results from the configured search engine
```

The tool requires the following parameter:

* `query`: The search query string to look up

The tool will return search results including titles, snippets, and URLs from the configured search engine (defaults to Google).

Supported search engines include:

* Google (default)
* Google Scholar
* Bing
* Baidu
* Google News
* Bing News
* Google Patents

### 5. Github Search Tool

The Github SearchTool is used for retrieving information from Github repositories using natural language queries. This tool provides functionality for querying Github repositories for various information, such as code changes, commits, active pull requests, issues, etc., using natural language input. It is designed to be used as part of a larger AI-driven agent system.

#### Setup API

```python
import os

os.environ['GITHUB_ACCESS_TOKEN'] = "<add-your-access-token>"
```

Get your GitHub Access Token: [https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

```python
from openagi.actions.tools.github_search_tool import GitHubFileLoadAction

# Set GitHub access token in environment
import os
os.environ['GITHUB_ACCESS_TOKEN'] = "<your-github-token>"

# Initialize the GitHub search tool
github_tool = GitHubFileLoadAction(
    repo="username/repository",  # e.g., "aiplanethub/openagi"
    directory="path/to/files",   # e.g., "src/openagi/llms"
    extension=".py"              # File extension to filter
)

# Execute the search
result = github_tool.execute()
# Returns content and metadata of matching files
```

### 6. YouTube Search Tool

The YouTube Search tool allows users to search for videos on YouTube using natural language queries. This tool retrieves relevant video content based on user-defined search parameters, making it easier to find specific videos or topics of interest.

The YouTube Search tool does not require an API key but does require the installation of specific libraries. You need to install `yt-dlp` and `youtube-search` to use this tool.

```
pip install yt-dlp
pip install youtube-search
```

**Code Snippet** To initialize the YouTube Search tool, you can use the following code:

```python
from openagi.actions.tools.youtubesearch import YouTubeSearchTool

# Initialize the YouTube search tool
youtube_tool = YouTubeSearchTool(
    query="Your search query",  # Required: The keyword to search for
    max_results=5              # Optional: Number of results to return (default: 5)
)

# Execute the search
result = youtube_tool.execute()
# Returns video titles, descriptions, and URLs
```

The tool requires the following parameters:

* `query`: The search keyword or phrase to look up on YouTube
* `max_results`: (Optional) Number of video results to return, defaults to 5

The tool will return search results including:

* Video titles
* Video descriptions
* Video URLs (in format: [https://youtube.com/watch?v=VIDEO\_ID](https://vscode-file/vscode-app/Applications/Aide.app/Contents/Resources/app/out/vs/code/electron-sandbox/workbench/workbench.html))

### 7. Tavily QA Search Tool

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
from openagi.actions.tools.tavilyqasearch import TavilyWebSearchQA

# Configure API key (recommended way)
TavilyWebSearchQA.set_config(api_key='your-api-key')

# Initialize the Tavily QA search tool
tavily_tool = TavilyWebSearchQA(
    query="Your search query"  # Required: The question or query to search for
)

# Execute the search
result = tavily_tool.execute()
# Returns AI-generated answers based on web content
```

The tool requires the following parameter:

* `query`: The search query or question to look up

The tool will return comprehensive search results with AI-generated answers based on the most relevant web content found.&#x20;

### 8. Exa Search Tool

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
from openagi.actions.tools.exasearch import ExaSearch

# Configure API key (recommended way)
ExaSearch.set_config(api_key='your-api-key')

# Initialize the Exa search tool
exa_tool = ExaSearch(
    query="Your search query"  # Required: The search query to look up
)

# Execute the search
result = exa_tool.execute()
# Returns relevant content from search results
```

### 9. Unstructured PDF Loader Tool

The Unstructured PDF Loader tool is designed to extract content, including metadata, from PDF files. It utilizes the Unstructured library to partition the PDF and chunk the content based on titles. This tool is useful for processing large volumes of PDF documents and making their contents accessible for further analysis.

**Installation**

```
pip install unstructured
```

**Code Snippet**

```python
from openagi.actions.tools.unstructured_io import UnstructuredPdfLoaderAction

# Initialize the PDF loader tool with configuration
pdf_tool = UnstructuredPdfLoaderAction()
pdf_tool.set_config(filename="/path/to/your/file.pdf")

# Execute the loader
result = pdf_tool.execute()
# Returns structured content from PDF including metadata
```

### 10. Wikipedia Search Tool

The Wikipedia Search tool enables searching and retrieving information from Wikipedia articles. This tool provides functionality to search Wikipedia articles and retrieve summaries, with built-in handling for disambiguation pages.

**Installation**

```
pip install wikipedia-api
```

**Usage Example**

```python
from openagi.actions.tools.wikipedia_search import WikipediaSearch

# Initialize the Wikipedia search tool
wikipedia_tool = WikipediaSearch(
    query="Your search query",          # Required: The search query to look up
    max_results=3                       # Optional: Number of sentences to return (default: 3)
)

# Execute the search
result = wikipedia_tool.execute()
# Returns JSON string containing title, summary, and URL or disambiguation options

```



### 11. ElevenLabsTTS Tool

This tool is designed to seamlessly convert text to speech using ElevenLabs, allowing you to utilize any voice ID or customization options provided by the platform. It leverages the ElevenLabs API to transform the input text into speech, offering high-quality, multilingual text-to-speech conversions.

```
pip install elevenlabs
```

Usage:

```python
import os
import json
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from src.openagi.actions.tools.speech_tool import ElevenLabsTTS  

# Set your ElevenLabs API Key (Optional: Can also be set in .env file)
os.environ["ELEVENLABS_API_KEY"] = "your_api_key_here"

# Create an instance of ElevenLabsTTS
tts = ElevenLabsTTS(
    text="Hello, this is a test of ElevenLabs text-to-speech.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

# Execute the text-to-speech conversion
response = tts.execute()

# Print the response
print(json.loads(response))
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
