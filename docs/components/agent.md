# Agent

## What is an Agent?

Imagine a scenario where you have a team of virtual assistants, each specialized in a different task. For instance, one assistant collects data, another analyzes it, and a third composes reports based on the findings. Now, think of these assistants as Agents, capable of autonomously performing their tasks and seamlessly communicating with one another to accomplish complex objectives.

Agents are decision-makers that understand the specifications of tasks and execute them in a more human-like manner. Agents can also communicate between multiple agents and performs the multiple tasks in loop.

## Type of Agents

OpenAGI consists of two different types of Agents: Static and Dynamic.

### Static

Static Agent is an Agent type Whether the agent is created at the initialisation of the program. The Agent type is configured within AIAgent, as an attribute: `agent_type="STATIC"`

```
agent1 = Agent(
        agent_type="STATIC",
        .... #other agents attributes
)
```

### Dynamic

Dynamic Agent is an Agent type that is dynamically created during the declaration of Agents object. The Agent type is configured within AIAgent, as an attribute: `agent_type="DYNAMIC"`

```
agent2 = Agent(
        agent_type="DYNAMIC",
        .... #other agents attributes
)
```

## How to create an Agent?

Real-world issues demand that agents have the ability to carry out tasks concurrently, compile data from multiple agents for task execution, initiate an agent for a specific task such as feedback, and activate several agents at the onset of the solution.

The objective can be achieved through the OpenAGI is by deploying a trio of agents.

Lets understand this step-by-step:

<figure><img src="../.gitbook/assets/image (27).png" alt=""><figcaption><p>Solution diagram</p></figcaption></figure>

### Define Agent agentName and Roles

> Agent 1: **Researcher**

The first agent, which employs search engines using tools like 'DuckDuckGo search tool' to gather information related to the latest developments in cancer and COVID-19 treatments and forwards it to the second agent.

> Agent 2: **Writer**

**T**he second agent, which processes the information collected from the first agent to create succinct summaries tailored for healthcare professionals and the general public.

> Agent 3: **Emailer**

**T**he third agent, which takes the summaries from the second agent as input to craft distinct emails as per the task of the use case.

Note: The label assigned for the Agent Name i.e., Researcher, Writer and Emailer can be set to anything meaningful based on your use cases.

### Initialisation of Agent Objects

Agent Objects comprise a list of agents collaborating to accomplish a series of tasks.

The user needs to create the list of agents.

### Assign Agent Attributes in Sequential Execution

It's crucial to clearly define and label the capabilities of each agent. For example, we might label the agent responsible `RESEARCHER`as the `search_executor`. We also need to designate which agent will receive the output once a task is completed. Agents are limited to specific capabilities like search execution and `LLM` task execution. For instance, the `RESEARCHER` agent sends a message to the `WRITER` agent, which then forwards it to the `EMAILER` for printing, as the recipient is `HGI`.

> The value “HGI” indicates human agent which is the final receiver of the output from the agent

```python
#Agent objects configuration as a list
agent_list = [
    Agent(
        agentName="RESEARCHER",
        role="RESEARCH EXPERT",
        goal="search for latest trends in Carona and Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
        backstory="Has the capability to execute internet search tool",
        capability="search_executor",
        task="search internet for the goal for the trends after first half of 2023",
        output_consumer_agent=agent_names[1],  # the consumer agent after executing task
        tools_list=[DuckDuckGoSearchTool],
    ),
    Agent(
        agentName="WRITER",
        role="SUMMARISING EXPERT",
        goal="summarize input into presentable points",
        backstory="Expert in summarising the given text",
        capability="llm_task_executor",
        task="summarize points to present to health care professionals and general public separately",
        output_consumer_agent=agent_names[2],
    ),
    Agent(
        agentName="EMAILER",
        role="EMAIL CREATOR",
        goal="composes the email based on the content",
        backstory="Good in composing precise emails",
        capability="llm_task_executor",
        task="composes email based on summary to doctors and general public separately into a file with subject-summary and details",
        output_consumer_agent="HGI",  # To be consumed by Human agent - output will be printed
    ),
]
```

### Integration of Large Language Model

For Azure:

```python
config = AzureChatOpenAIModel.load_from_yml_config()
llm = AzureChatOpenAIModel(config=config)
```

For OpenAI

```python
config = OpenAIModel.load_from_yml_config()
llm = OpenAIModel(config=config)
```

### Kick-Off the Agent Execution

During this step the program gets triggered by passing the agents list and which list of agents to be started first.

In this case the agent “RESEARCHER” is started first. The dynamic agents shall be added as the 3rd parameter i.e. the first parameter refers to all the agent objects. second paramteer refers agents that get triggred by the user. The parallel agents execution triggers multiple agents as mentioned earlier.

```python
kickOffAgents(agent_list, [agent_list[0]], llm=llm)
```

That's it! That's how you can build an Agent with minimal effort.
