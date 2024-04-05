# JobSearch Agent

This code presents a Python script that sets up an AI agent, named "RESEARCHER," to find relevant job opportunities based on given specifications and a provided resume.

&#x20;It utilizes various tools for internet search and document comparison to fulfill its task. Upon finding the relevant job opportunities, The script configures the agent's role, goal, backstory, capabilities, and specific task to accomplish. Additionally, it initializes logging for debugging purposes and triggers the execution of the agent.

The example and result can be observed by executing “python usecase/ProfAgentJobSearch.py”.

#### Example Code:

In the code below: the agent is configured as a Researcher to find the related jobs as per the specification. The agent's goal, backstory, capability, task and the tools needed are included for the same.

```python
from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.tools.integrations import (
    DocumentCompareSearchTool,
    DuckDuckGoSearchTool,
    ExaSearchTool,
)

if __name__ == "__main__":
    agent_list = [
        Agent(
            agentName="RESEARCHER",  # name
            role="RESEARCHER",  # role
            goal="Find the most recent and relatable jobs based on the specifications given with the help of internet search and context from given Resume within context length.",
            backstory="A Job finder that can easily search for most relevant opportunities based on the given resume and job specifications.",
            capability="search_executor",
            task="Give me 5 most recent job based on my resume in resume.pdf file related to my expertise and make sure the opportunity is remote and has a salary of 8LPA or more.",
            output_consumer_agent="HGI",  # the consumer agent after executing task
            tools_list=[ExaSearchTool, DuckDuckGoSearchTool, DocumentCompareSearchTool],
        )
    ]
```

The Agents defines an AzureChatOpenAI configuration and then the framework executes its kick off using the code segment below:

```python
    config = AzureChatOpenAIModel.load_from_yml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffAgents(agent_list, [agent_list[0]], llm=azure_chat_model)
```

#### Output:

<figure><img src="../.gitbook/assets/image (21).png" alt=""><figcaption></figcaption></figure>

Code Example:[ ](https://github.com/aiplanethub/agents/blob/tool/usecases/ProfAgentJobSearch.py) usecases/ProfAgentJobSearch.py
