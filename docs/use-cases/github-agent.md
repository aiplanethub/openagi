# Github Agent

In this example, AI agents for specific tasks related to code retrieval from GitHub and test case generation. It imports modules and classes necessary for agent initialization and configuration.&#x20;

The script then initializes two AI agents with different roles and tasks:&#x20;

1. **DEVELOPER:** Efficiently searches and retrieves relevant information regarding repository and code snippets on GitHub.
2. **TESTCASE DEVELOPER**: Examines the provided Python code and provide test cases with adherence to best practices.

The example and result can be observed by executing&#x20;

`python usecase/ProfAgentGithub.py`.



In the code below, the Developer and TestCaseDeveloper Agents are configured with their goal, backstory, capability, task and the tools needed for each agent for the same

```python
from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.tools.integrations import GithubSearchTool

if __name__ == "__main__":
    agent_list = [
        Agent(
            agentName = "RESEARCHER",  # name
            role="DEVELOPER",  # role
            goal="Efficiently search and retrieve relevant information regarding repository and code snippets on GitHub.",
            backstory="Developed to enhance productivity for developers, this tool integrates with the GitHub API to provide streamlined access to code resources.",
            capability="search_executor",
            task="Retrieve the code for all the files in the respository.",
            output_consumer_agent=agent_names[1],  # the consumer agent after executing task
            tools_list=[GithubSearchTool],
        ),
        Agent(
            agentName="TESTCASEDEVELOPER",
            aggregator=0,
            onAggregationAction=None,
            creator=None,
            role="TESTCASEDEVELOPER",
            feedback=False,
            goal="To meticulously examine the provided Python code and provide test cases with adherence to best practices.",
            backstory="You are a seasoned software test case developer who developes unit, integration and functional test cases for the given program code",
            capability="llm_task_executor",
            agent_type="STATIC",
            multiplicity=0,
            task="Conduct a comprehensive test cases for the Python code, paying particular attention to functional and acceptance testing including edge cases. Also provide no of positive and edge test cases to enable the management to understand the quality of testing",
            output_consumer_agent="HGI",
            HGI_Intf=None,
            llm_api="azure",
            llm_resp_timer_value=1300,
            tools_list=[],
        ),
    ]
```

The Agents defines an AzureChatOpenAI configuration and then the framework executes its kick off using the code segment below:

```python
    config = AzureChatOpenAIModel.load_from_yml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffAgents(agent_list, [agent_list[0]], llm=azure_chat_model)
```

#### Output:

<figure><img src="https://lh7-us.googleusercontent.com/xCtlteamLuhXKm9P1v9CLbvoFn7gRPezdI2UVyNHwACDzuIgxzjaNBIBsZLkrkhrpc58ytbLOljCoPgHKmAA8pEp_S38mhDSEGgEdeJdmnOfACd26RokOnVOo1AZySPhCNf8y4briO85lgl89OetYrt3R9hBoBQk" alt=""><figcaption></figcaption></figure>

Code Example: usecases/ProfAgentGithub.py
