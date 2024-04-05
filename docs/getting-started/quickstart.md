---
description: Lets build our first Agent use cases.
---

# Quickstart

In this quickstart, we'll explore one of the use cases to demonstrate the execution of the Agent. We'll focus on querying Search Engines tools like `DuckDuckGoSearchTool` to gather the latest information on Corona and Cancer treatments, covering aspects such as medications, physical exercises, overall management, and prevention.

Agents excel at autonomously performing multiple tasks, making decisions on the fly, and communicating with other agents. For this use case, we'll utilise multiple agents: one to curate the data, another to summarise it, and a third to compose an email based on the content.

### 1. Import required modules

To get started, we need to initialise a few methods from the modules.

* Agent
* Tools
* Large Language Model
* Agent Initialisation- KickOffAgents

For instance, `DuckDuckSearchTool` serves as the designated Tool, while `AIAgent`assigns roles and instructs the agent to execute tasks. The `Large Language model` acts as the cognitive center of agents, aiding in reasoning, and `Agent initialization` initiates the Agent operations.

```python
from openagi.agent import Agent
from openagi.tools.integrations.duckducksearch import DuckDuckGoSearchTool
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.init_agent import kickOffAgents
```

### 2. Agent objects creation

Initially, we initialize the Agent object, followed by breaking down tasks into objectives and tasks for the agents. It is also imperative to define and label the capabilities of each agent. Parameters are then set to initialize each individual task.

Check the parameters information in this [section](../components/agent-attributes.md).

```python
if __name__ == "__main__":
    agent_list = [
        Agent(
            agentName="RESEARCHER",  # name
            role="RESEARCH EXPERT",  # role
            goal="search for latest trends in Carona and Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
            backstory="Has the capability to execute internet search tool",
            capability="search_executor",
            task="search internet for the goal for the trends after first half of 2023",
            output_consumer_agent="WRITER",  # the consumer agent after executing task
            tools_list=[DuckDuckGoSearchTool],
        ),
        Agent(
            agentName="WRITER",
            role="SUMMARISING EXPERT",
            goal="summarize input into presentable points",
            backstory="Expert in summarising the given text",
            capability="llm_task_executor",
            task="summarize points to present to health care professionals and general public separately",
            output_consumer_agent="EMAILER",
        ),
        Agent(
            agentName="EMAILER",
            role="EMAIL CREATOR",
            goal="composes the email based on the content",
            backstory="Good in composing precise emails",
            capability="llm_task_executor",
            task="composes email based on summary to doctors and general public separately into a file with subject-summary and details",
            output_consumer_agent="HGI",
        ),
    ]

```

### 3. Setting LLM configuration

In this phase, the configuration for the AzureChatModel is defined and set to be implemented further during kick-off. OpenAI Support is also provided.

As stated in the Installation guide, all the credentials for the LLM need to be included in `OPENAGI_CONFIG_PATH` and stored in the config.yaml file. This is where we configure the LLM model to execute the operation.

#### Configuration for OpenAI

```python
config = OpenAIModel.load_from_yml_config()
llm = OpenAIModel(config=config)
```

#### Or Configuration for AzureChat OpenAI

<pre class="language-python"><code class="lang-python"><strong>config = AzureChatOpenAIModel.load_from_yml_config()
</strong>llm = AzureChatOpenAIModel(config=config)
</code></pre>

### 4. Kick-off the execution

In this phase, the program is activated by supplying a list of agents and specifying which agents should be initiated first.

Specifically, the "RESEARCHER" agent is launched initially. Dynamic agents can be incorporated as the third parameter. The first parameter pertains to all agent objects, while the second parameter is related to agents triggered by the user.

The execution of agents in parallel initiates multiple agents simultaneously.

```python
kickOffAgents(agent_list, [agent_list[0]], llm=llm)
```

### 5. Run your Agent

#### Lets merge the code and execute the following program.

```python
from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms import AzureChatOpenAIModel
from openagi.tools.integrations import DuckDuckGoSearchTool


if __name__ == "__main__":
    agent_list = [
        Agent(
            agentName="RESEARCHER",  # name
            role="RESEARCH EXPERT",  # role
            goal="search for latest trends in Carona and Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
            backstory="Has the capability to execute internet search tool",
            capability="search_executor",
            task="search internet for the goal for the trends after first half of 2023",
            output_consumer_agent="WRITER",  # the consumer agent after executing task
            tools_list=[DuckDuckGoSearchTool],
        ),
        Agent(
            agentName="WRITER",
            role="SUMMARISING EXPERT",
            goal="summarize input into presentable points",
            backstory="Expert in summarising the given text",
            capability="llm_task_executor",
            task="summarize points to present to health care professionals and general public separately",
            output_consumer_agent="EMAILER",
        ),
        Agent(
            agentName="EMAILER",
            role="EMAIL CREATOR",
            goal="composes the email based on the content",
            backstory="Good in composing precise emails",
            capability="llm_task_executor",
            task="composes email based on summary to doctors and general public separately into a file with subject-summary and details",
            output_consumer_agent="HGI",
        ),
    ]
    config = AzureChatOpenAIModel.load_from_yml_config()
    llm = AzureChatOpenAIModel(config=config)
    kickOffAgents(agent_list, [agent_list[0]], llm=llm)
```

For more example use cases, check out our GitHub Repo:

[https://github.com/aiplanethub/openagi/tree/main/usecases](https://github.com/aiplanethub/openagi/tree/main/usecases)
