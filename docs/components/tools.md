# Tools

## What is Tool?

Tool is a functionality based on which the data is fetched to the Agent for further analysis and decision making. A wide array of tools is cataloged in the tools database, designed to support activities such as internet searches, email dispatch, interactions with Git repositories, and much more. Users have the flexibility to create their own tools and seamlessly integrate them into the framework's operations.

## How to integrate with existing tools of OpenAGI

The tool integration examples can be found under the folder mentioned below.

```
src/openagi/tools/integrations
```

The following example shows the implementation of the necessary functions/classes to integrate any tool with OpenAGI framework. The definition includes the actual function which need to be executed and framework provided to make the tool available as a class to include as part of the tool\_list in agent configuration. At run time, LLM that is configured for the agent is used to generate the required parameters for the tool. If multiple tools are used, the output of all the tools are concatenated and passed to the agent for processing.

The run method shown below is called from the framework for executing the tool.

```python
import logging
from langchain_community.tools import (
    WikipediaQueryRun,
)  # langchain tool integration
from langchain_community.utilities import WikipediaAPIWrapper
from pydantic import BaseModel, Field  # basic icludes

from openagi.tools.base import BaseTool, tool


def wikipediaTool(searchString):  # tool as a function
    api_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=10000)
    tool = WikipediaQueryRun(api_wrapper=api_wrapper)
    results = tool.run(searchString)
    logging.debug(results)
    return results


class WikipediaToolInputSchema(BaseModel):  # f
    search_str: str = Field(description="Query used to search the Wikipedia API")


class WikipediaToolOutputSchema(BaseModel):  # description of the tool
    response: str = Field(description="Response from the Wikipedia tool.")


class WikipediaTool(BaseTool):  # class name used to pass in agent configuration
    name: str = "Wikipedia Tool"
    description: str = (
        "A tool designed to Tool that searches the Wikipedia API for a specific query."
    )

    @tool(args_schema=WikipediaToolInputSchema, output_schema=WikipediaToolOutputSchema)
    def _run(self, search_str: str = None):  # called by the framework to execute the tool
        return wikipediaTool(searchString=search_str)
```

## Tool configuration

```python
Agent(
    agentName="RESEARCHER",
    role="Researches about Reliance stock",
    goal="To gather all the necessary information about Reliance stock",
    backstory="Has the capability to execute internet search tool",
    capability="search_executor",
    task="Search the internet for information about Reliance stock, its current price, historical performance, market trends, and news",
    output_consumer_agent="ANALYZER",
    tools_list=[WikipediaTool, YahooFinanceTool, SerperSpecificSearchTool],
)
```

The provided example illustrates that the agent is equipped with four tools. The framework operates sequentially, generating the necessary parameters from other attributes. The subsequent sections detail the function of each tool and include corresponding examples from a range of use cases.

### 1. DuckDuckGoSearch Tool

The DuckDuckGoSearch tool is a tool that can be used to search for words, documents, images, videos, news, maps and text translation using the DuckDuckGo.com search engine. DuckDuckGo Search is a web search engine that _DuckDuckGo_ is an independent Google alternative that lets you search and browse the web, but it emphasises protecting user privacy and avoiding the filter bubble of personalised search results.

```python
from openagi.tools.integrations import DuckDuckGoSearchTool

Agent(
    agentName="RESEARCHER",  # name
    role="RESEARCHER",  # role
    goal="search for latest trends in Corona and Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
    backstory="Has the capability to execute internet search tool",
    capability="search_executor",
    task="search internet for the goal for the trends after first half of 2023",
    output_consumer_agent=agent_list[1],  # the consumer agent after executing task
    tools_list=[DuckDuckGoSearchTool],
)
```

### 2. GoogleFinanceSearch Tool

The GoogleFinanceSearch tool is a tool that uses the Google Finance Tool to get information from the Google Finance page.

Google Finance is a comprehensive platform designed to cater to the needs of investors and professionals. It provides users with real-time stock market data, enabling them to track historical performance and create watchlists of stocks of interest. Additionally, users can stay informed about relevant financial news and headlines, ensuring they are up-to-date with developments that may impact their investment decisions

#### Dependencies:

1. SERPER\_API\_KEY

Example of application in: usecases\ProfAgentMarket.py

```python
from openagi.tools.integrations import GoogleFinanceSearchTool

Agent(
    agentName="RESEARCHER", # name
    role="RESEARCHER",  # role
    goal="Research for Finance data from the Google Finance page",
    backstory="I am a researcher agent and I can search for finance data from the Google Finance page",
    capability="search_executor",
    task="give me google's current stock value",
    output_consumer_agent="HGI",  # the consumer agent after executing task
    tools_list=[GoogleFinanceSearchTool],
)
```

### 3. ExaSearch Tool

The ExaSearch tool is a tool which can be used to do a Exa Search. Exa (formerly Metaphor Search) is a search engine fully designed for use by LLMs. Search for documents on the internet using natural language queries, then retrieve cleaned HTML content from desired documents. Unlike keyword-based search (Google), Exa's neural search capabilities allow it to semantically understand queries and return relevant documents.

#### Dependencies:

1. SERPER\_API\_KEY

Example of application in: usecases/ProfAgentExaSearchGmail.py

```python
from openagi.tools.integrations import exaSearchTool

Agent(
    agentName= "RESEARCHER",
    role="RESEARCHER",  # role
    goal="search for latest trends in Corona and Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
    backstory="Has the capability to execute internet search tool",
    capability="search_executor",
    task="search internet for the goal for the trends after first half of 2023",
    output_consumer_agent=agent_list[1],  # the consumer agent after executing task
    tools_list=[exaSearchTool],
)
```

### 4. GithubSearchTool

The GithubSearchTool is used for retrieving information from Github repositories using natural language queries. This tool provides functionality for querying Github repositories for various information, such as code changes, commits, active pull requests, issues, etc., using natural language input. It is designed to be used as part of a larger AI-driven agent system.

#### Dependencies:

1. GITHUB\_APP\_ID
2. GITHUB\_APP\_PRIVATE\_KEY
3. GITHUB\_REPOSITORY

GITHUB\_APP\_PRIVATE\_KEY: Follow the documentation by github to obtain private pem key [Github Docs](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/managing-private-keys-for-github-apps#generating-private-keys). Keep your `.pem` file in the main directory of Agents repository.

Example of application in: usecases/ProfAgentGithub.py

```python
from openagi.tools.integrations import GithubSearchTool

Agent(
    agentName="RESEARCHER",  # name
    role="RESEARCHER",  # role
    goal="Efficiently search and retrieve relevant information regarding repository and code snippets on GitHub.",
    backstory="Developed to enhance productivity for developers, this tool integrates with the GitHub API to provide streamlined access to code resources.",
    capability="search_executor",
    task="List all the code files and the content of files in the repository.",
    output_consumer_agent="HGI",  # the consumer agent after executing task
    tools_list=[GithubSearchTool],
)
```

### 5. YahooFinanceTool

YahooFinanceTools is a tool designed to explore financial news articles on Yahoo Finance.

**Dependencies**:

1. SERPER\_API\_KEY

Example of application in: usecases\ProfAgentMarket.py

```python
from openagi.tools.integrations import YahooFinanceTool

Agent(
    agentName="RESEARCHER",  # name
    role="RESEARCHER",  # role
    goal="Research for Finance data from the Google Finance page",
    backstory="I am a researcher agent and I can search for finance data from the Google Finance page",
    capability="search_executor",
    task="give me google's current stock value",
    output_consumer_agent="HGI",  # the consumer agent after executing task
    tools_list=[YahooFinanceTool],
)
```

### 6. Wikipedia Tool

Wikipedia tool is a tool designed to Tool that searches the Wikipedia API for a specific query. Wikipedia is a multilingual free online encyclopedia written and maintained by a community of volunteers.

Example of application in: usecases/ProfAgentStocks.py

```python
from openagi.tools.integrations import WikipediaTool

Agent(
    agentName="RESEARCHER",  # name
    role="RESEARCHER",  # role
    goal="search for latest trends in Corona and Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
    backstory="Has the capability to execute internet search tool",
    capability="search_executor",
    task="search internet for the goal for the trends after first half of 2023",
    output_consumer_agent=agent_list[1],  # the consumer agent after executing task
    tools_list=[WikipediaTool],
)
```

### 7. GmailSearch Tool

GmailSearch Tool is a tool which can be used to perform actions on gmail by using natural language. For example, this tool can be used to send emails on behalf of the associated account.

**Dependencies**:

1. **Credentials**: A credentials file containing the credentials of the User is needed for the tool.

GMAIL\_CREDS: Follow steps in given documentation to get `credential.json` and save it in your main directory of Agents repository. [Google For Developers](https://developers.google.com/gmail/api/quickstart/python)

Example of application in: usecases/ProfAgentGmail.py

```python
from openagi.tools.integrations import GmailSearchTool

Agent(
    agentName="RESEARCHER", 
    role="RESEARCHER",  # role
    goal="Send an email to the given context.",
    backstory="Has the capability to capability to send email using gmailtool",
    capability="search_executor",
    task="Create a new email with content on congraluations on your promotion to tanish@aiplanet.com and send it.",
    output_consumer_agent="HGI",  # the consumer agent after executing task
    tools_list=[GmailSearchTool],
)
```

## How to create a custom tool?

### **Integrating Custom Tool**

Agents are equipped to run any user-defined tool designed to perform tasks like pulling data from internal sources or applying particular procedures to data for processing purposes. The subsequent example details the necessary configurations, implementations, and the corresponding application `ProfAgentCustomTool` found in the use case directory. The user is expected to define a custom tool as an API for the agent to utilize, and it should be provided as outlined below.

### Custom Tool Definition

The function for the custom tool needs to be established within the file

<pre><code><strong>"src/openagi/tools/custom_tools/custom_tool_db.py"
</strong></code></pre>

```python
def proxyToolkit(input_str):
    logging.debug("proxy tool is executed\n")
    return input_str
```

### Custom Tool Configuration for usage in OpenAGI

The user is required to create a class that encapsulates the functionality and modular design, enabling it to be invoked by the agent's execution framework, as demonstrated below. Consult the file named `src/genai_agents/custom_tools/ProxyTool.py` for guidance. It is essential that the class and file names match the name of the tool the user intends to include in the agent's `tool_list`, as outlined in the subsequent section.

```python
import logging
from openagi.tools.base import BaseTool, tool
from pydantic import BaseModel, Field
from openagi.tools.custom_tools.custom_tool_db import proxyToolkit

class ProxyInputSchema(BaseModel):
    input_str: str = Field(description="Input to be returned.")


class ProxyOutputSchema(BaseModel):
    response: str = Field(description="Returns the input.")


class ProxyTool(BaseTool):
    name: str = "Proxy Tool"
    description: str = "A tool that returns the input."

    @tool(args_schema=ProxyInputSchema, output_schema=ProxyOutputSchema)
    def _run(self, input_str: str = None):
        logging.debug(f"Proxy tool called with some input of length {len(input_str)}.")
        print("custom tool executed")
        return proxyToolkit(input_str)

```

### Agent Configuration

The tool outlined below demonstrates how to use the configured class named “ProxyTool” for the execution of the proxyToolkit, as specified in the agent's configuration.

> tools\_list=\[DuckDuckGoSearchTool, ProxyTool]

```python
from openagi.init_agent import kickOffAgents
from openagi.agent import AIAgent
from openagi.tools.integrations import DuckDuckGoSearchTool
from openagi.tools.custom_tools.ProxyTool import ProxyTool  # import class
from openagi.llms.azure import AzureChatOpenAIModel

if __name__ == "__main__":
    agent_list = [
        AIAgent(
            agentName="RESEARCHER",  # name
            role="RESEARCHER",  # role
            goal="search for latest trends in Carona and Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
            backstory="Has the capability to execute internet search tool",
            capability="search_executor",
            task="search internet for the goal for the trends after first half of 2023",
            output_consumer_agent=agent_names[1],  # the consumer agent after executing task
            tools_list=[DuckDuckGoSearchTool, ProxyTool],
        ),
        AIAgent(
            agentName="WRITER",
            role="SUMMARISER",
            goal="summarize input into presentable points",
            backstory="Expert in summarising the given text",
            capability="llm_task_executor",
            task="summarize points to present to health care professionals and general public separately",
            output_consumer_agent=agent_names[2],
        ),
        AIAgent(
            agentName="EMAILER",
            role="EMAILER",
            goal="composes the email based on the content",
            backstory="Good in composing precise emails",
            capability="llm_task_executor",
            task="composes email based on summary to doctors and general public separately into a file with subject-summary and details",
            output_consumer_agent="HGI",
        ),
    ]

```

The Agents defines an AzureChatOpenAI configuration and then the framework executes its kick off using the code segment below for Azure OpenAI:

```python
config = AzureChatOpenAIModel.load_from_yml_config()
azure_chat_model = AzureChatOpenAIModel(config=config)
kickOffAgents(agent_list, [agent_list[0]], llm=azure_chat_model)
```
