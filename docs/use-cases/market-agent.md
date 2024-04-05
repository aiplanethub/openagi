# Market Agent

In this example, AI agents are being initialized and configured for specific tasks related to detailed financial research and reporting of a specific company. It imports modules and classes necessary for agent initialization and configuration.&#x20;

The code initializes and configures several AI agents with distinct roles, each aimed at achieving a particular goal in a coordinated manner. The agents and their roles are defined as follows:

1. RESEARCHER: The Role of the Researcher Agent in the use case is to retrieve all the financial information of a specific company in the past, present as well as the future forecasting of the same. It performs a through search through the internet using a variety of web tools to obtain the information.
2. SUMMARISER: The Summarizer is to summarize and articulate the provided input from the RESEARCHER into clear and presentable points, and clearly provide recommendations whether to buy the stock for the short, medium and long term purpose.&#x20;

The example and result can be observed by executing usecases\ProfAgentMarket.py

#### Example Code

In the code below, the Researcher and Summariser Agents are configured with their goal, backstory, capability, task and the tools needed for each agent for the same:

```python
from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms import AzureChatOpenAIModel
from openagi.tools.integrations import DuckDuckGoSearchTool, GoogleFinanceSearchTool

if __name__ == "__main__":
    agent_list = [
        Agent(
            agentName="RESEARCHER",
            role="RESEARCHER",
            goal="Get information on current trends and updates of given stock today.",
            backstory="Has the capability to execute the tools an collects the data.",
            capability="search_executor",
            task="Collect information Wipro stock",
            output_consumer_agent=agent_names[1],
            tools_list=[DuckDuckGoSearchTool, GoogleFinanceSearchTool],
        ),
        Agent(
            agentName="SUMMARIZER",
            role="SUMMARIZER",
            goal="Summarize the received data as 5 bullet points.",
            backstory="Expert in using data provided.",
            capability="llm_task_executor",
            task="Provide recommendation on whether to buy the Wipro stock or not with 5 bullet points based on information received.",
            output_consumer_agent="HGI",
        ),
    ]
```

The Agents defines an AzureChatOpenAI configuration and then the framework executes its kick off using the code segment below:

```python
    config = AzureChatOpenAIModel.load_from_yml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffAgents(agent_list, [agent_list[0]], llm=azure_chat_model)
```

#### Output

<figure><img src="../.gitbook/assets/image (8).png" alt=""><figcaption></figcaption></figure>

Code Example: usecases/ProfAgentMarket.py
