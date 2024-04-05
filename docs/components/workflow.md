# Workflow

### Parallel Execution of Agents

The parallel execution configuration allows us to simultaneously execute two researcher agents in the The following depicts the parallel execution of “RESEARCHER1” and “RESEARCHER2” by the Professional Agent, which triggers the execution of the agents. For example this can be detailed as:

1. Researcher1: This is used to search the internet based on the goal for the medical trends from 2023 onwards
2. Researcher2: This has the same goal as that of Researcher2, and is executed in parallel to it
3. Writer: This agent processes the information collected from the Researcher agents executed parallel to create succinct summaries tailored for healthcare professionals and the general public.
4. Emailer: This agent, which takes the summaries from the Writer agent as input to craft distinct emails as per the task of the use case.

<figure><img src="../.gitbook/assets/image (28).png" alt=""><figcaption><p>Parallel Agents</p></figcaption></figure>

The code illustrates a scenario involving four agents, where two agents operate in parallel, as indicated by the second parameter in the kickOffGenAIAgents function. It permits the third agent to collect and combine the outcomes using the "onAggregationAction" function, which consolidates the results from the two parallel agents.

```python
import logging
from openagi.init_agent import kickOffAgents
from openagi.agent import Agent
from openagi.tools.integrations import DuckDuckGoSearchTool
from openagi.llms.azure import AzureChatOpenAIModel

#human tool integration
def onResultHGI(agentName, result, consumerAgent):
    feedback="Pass"
    action = "None"
    logging.debug(f"{agentName}:TO:{consumerAgent}-> {result}")
    return result, feedback, action

#control for the user to perform aggregation  
def onAggregationAction(agentName, consumerAgent, aggrSourceAgentList, aggrResultsList):
    result=""
    for string in aggrResultsList:
        result += string.body + " "        
    logging.debug(f'aggregation of messages::of {agentName} to {consumerAgent} {result}')
    return result
  
  
# Example Usage:
if __name__ == "__main__":
    agents_list = [
    Agent(agentName="RESEARCHER1", aggregator=0, onAggregationAction=None, creator=None, role="RESEARCHER", feedback=False, goal="search for latest trends in COVID-19 treatment that includes medicines, physical exercises, overall management and prevention aspects",
                     backstory="backstory", capability="search_executor", agent_type="STATIC",  multiplicity=0, 
                     task="search internet for the goal for the trends in 2H 2023 onwards", output_consumer_agent=agent_list[2], HGI_Intf=onResultHGI, 
                      llm_resp_timer_value=20, tools_list=[DuckDuckGoSearchTool]),
    
    Agent(agentName="RESEARCHER2", aggregator=0, onAggregationAction=None, creator=None, role="RESEARCHER",feedback=False, goal="search for latest trends in Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
                     backstory="backstory", capability="search_executor", agent_type="STATIC",  multiplicity=0, 
                     task="search internet for the goal for the trends in 2H 2023 onwards", output_consumer_agent=agent_list[2], HGI_Intf=onResultHGI, 
                      llm_resp_timer_value=20, tools_list=[DuckDuckGoSearchTool]),
     
    Agent(agentName="WRITER", aggregator=2, onAggregationAction=onAggregationAction,creator=None,role="SUMMARISER", feedback=False, goal="summarize input into presentable points", backstory="backstory", capability="llm_task_executor", agent_type="STATIC",  
              multiplicity=0, task="summarize points to present to health care professionals and general public separately", output_consumer_agent=agent_list[3],HGI_Intf=onResultHGI,
              llm_resp_timer_value=130, tools_list=[]),   
    
    
    Agent(agentName="EMAILER", aggregator=0, onAggregationAction=None,creator=None,role="EMAILER", feedback=False, goal="composes the email based on the contenct", backstory="backstory", capability="llm_task_executor", agent_type="STATIC",  
              multiplicity=0, task="composes email based on summary to doctors and general public separately into a file with subject-summary and details", output_consumer_agent="HGI",HGI_Intf=onResultHGI,
              llm_resp_timer_value=130, tools_list=[])
    ]
```

The Agents defines an AzureChatOpenAI configuration and then the framework executes its kick off using the code segment below:

```python
config = AzureChatOpenAIModel.load_from_yml_config()
llm = AzureChatOpenAIModel(config=config)
kickOffAgents(agents_list,[agents_list[0], agents_list[1]], llm=llm)
```

### Aggregated Execution of Agents

In the previous example the `WRITER` agent has to wait for the messages from both `RESEARCHER1` and `RESEARCHER2` to perform the task. The example and result can be observed by executing `python usecase/ProfAgentAggr.py`

1. Researcher1: This is used to search the internet based on the goal for the medical trends from 2023 onwards
2. Researcher2: This has the same goal as that of Researcher2, and is executed in aggregated way to it
3. Writer: This agent processes the information collected from the Researcher agents executed parallel to create succinct summaries tailored for healthcare professionals and the general public.
4. Emailer: This agent, which takes the summaries from the Writer agent as input to craft distinct emails as per the task of the use case

Refer to the previous example. Writer agent will aggregate the output from Researcher1 agent and Researcher2 agent and performs its task. The user need to configure a call back function for aggregation of outputs of Researcher1 and Researcher2.

### Configuration for using multiple LLMs

The tool allows for the integration of various Large Language Models (LLMs) into the solution. Developers have the flexibility to incorporate Azure OpenAI, OpenAI, or any other model by passing them as arguments to agents. Below is an example demonstrating how to configure and use this feature.

```python
import logging
from openagi.init_agent import kickOffAgents
from openagi.agent import Agent
from openagi.tools.integrations import DuckDuckGoSearchTool
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.llms.openai import OpenAIModel

#human tool integration
def onResultHGI(agentName, result, consumerAgent):
    feedback="Pass"
    action = "None"
    logging.debug(f"{agentName}:TO:{consumerAgent}-> {result}")
    return result, feedback, action

#control for the user to perform aggregation  
def onAggregationAction(agentName, consumerAgent, aggrSourceAgentList, aggrResultsList):
    result=""
    for string in aggrResultsList:
        result += string.body + " "        
    logging.debug(f'aggregation of messages::of {agentName} to {consumerAgent} {result}')
    return result
  
if __name__ == "__main__":
    
    config_azure = AzureChatOpenAIModel.load_from_yml_config()
    llm_azure = AzureChatOpenAIModel(config=config_azure)
    
    config_openai = OpenAIModel.load_from_yml_config()
    llm_openai= OpenAIModel(config=config_openai)
    
    agent_list = [
    Agent(agentName="RESEARCHER1", aggregator=0, onAggregationAction=None, creator=None, role="RESEARCHER", feedback=False, goal="search for latest trends in COVID-19 treatment that includes medicines, physical exercises, overall management and prevention aspects",
                     backstory="backstory", capability="search_executor", agent_type="STATIC",  multiplicity=0, 
                     task="search internet for the goal for the trends in 2H 2023 onwards", output_consumer_agent=agent_list[2], HGI_Intf=onResultHGI, llm=llm_azure, 
                      llm_resp_timer_value=20, tools_list=[DuckDuckGoSearchTool]),
    
    Agent(agentName="RESEARCHER2", aggregator=0, onAggregationAction=None, creator=None, role="RESEARCHER",feedback=False, goal="search for latest trends in Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
                     backstory="backstory", capability="search_executor", agent_type="STATIC",  multiplicity=0, 
                     task="search internet for the goal for the trends in 2H 2023 onwards", output_consumer_agent=agent_list[2], HGI_Intf=onResultHGI, llm=llm_openai, 
                      llm_resp_timer_value=20, tools_list=[DuckDuckGoSearchTool]),
     
    Agent(agentName="WRITER", aggregator=2, onAggregationAction=onAggregationAction,creator=None,role="SUMMARISER", feedback=False, goal="summarize input into presentable points", backstory="backstory", capability="llm_task_executor", agent_type="STATIC",  
              multiplicity=0, task="summarize points to present to health care professionals and general public separately", output_consumer_agent=agent_list[3],HGI_Intf=onResultHGI,
              llm=llm_openai,  llm_resp_timer_value=130, tools_list=[]),   
    
    Agent(agentName="EMAILER", aggregator=0, onAggregationAction=None,creator=None,role="EMAILER", feedback=False, goal="composes the email based on the contenct", backstory="backstory", capability="llm_task_executor", agent_type="STATIC",  
              multiplicity=0, task="composes email based on summary to doctors and general public separately into a file with subject-summary and details", output_consumer_agent="HGI",HGI_Intf=onResultHGI,
              llm=llm_azure, llm_resp_timer_value=130, tools_list=[])     
    ]
    
    kickOffAgents(agent_list,[agent_list[0], agent_list[1]], llm=llm_azure)
```

### Feedback Execution of Agents

The agent whose attribute is set to send “feedback” allows the agent to send feedback once get and the results. Flexible architecture will be supported in future. The basic example to illustrate the capability can be seen by executing “python usecase/ProfAgentFeedback\_Review.py”

In this Feedback Use Case, to illustrate the feedback mechanism there are two Agents:

1. Coder: The goal of the Coder Agent is to generate code snippets for various programming tasks
2. Reviewer: The goal of the Reviewer agent is to review the code snippets generated by the Coder agent and review them. In case of issues, agents sends message to change the code based on the feedback.

#### Example:

In the below code segment,agent1 and agent2 are the two configured agents. agent2 incorporates the feedback mechanism to allow the developer to send feedback and get different results accordingly. Based on the feedback generated by agent2, the final answer obtained will be personalized as per the feedback provided by the developer.

```python
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.init_agent import kickOffAgents
from openagi.agent import Agent

if __name__ == "__main__":
   
    agent_list = [
    Agent(agentName="Coder", aggregator=0, onAggregationAction=None, creator=None, 
                     role="Coder", feedback=False, goal="To generate Python code for calculating the factorial of a number in a way that it can be easily copied and pasted by users for execution.Do not use any python libraries for it, hardcode it completely",
                     backstory="You are a software developer working on a platform that provides code snippets for various programming tasks.", 
                     capability="llm_task_executor", agent_type="STATIC",  multiplicity=0,  
                     task="Develop a Python script that calculates the factorial of a given number, presenting the code in a line-by-line format to ensure clarity and ease of use for users.", output_consumer_agent=agent_list[1], HGI_Intf=None, llm_api=llm, 
                      llm_resp_timer_value=2000, tools_list=[]),
        
    Agent(agentName="Reviewer", aggregator=0, onAggregationAction=None,creator=None,role="Reviewer", feedback=True,
              goal="To meticulously examine the provided Python code, identifying any potential issues, and providing feedback on its quality and adherence to best practices.", 
              backstory="You are a seasoned software engineer responsible for reviewing Python code submissions within your team.", capability="llm_task_executor", 
              agent_type="STATIC", multiplicity=0, 
              task="Conduct a comprehensive review of the Python code, paying particular attention to logging, error conditions, and exception handling. Upon completion, provide a status report indicating whether any issues were found and detailing any necessary improvements.Do not include any code, only a report of the provided code is required.",
              output_consumer_agent="HGI",HGI_Intf=None,
              llm_api=llm,  llm_resp_timer_value=1300, tools_list=[])   
    ]
```

The Agents defines an AzureChatOpenAI configuration and then the framework executes its kick off using the code segment below:

```python
config = AzureChatOpenAIModel.load_from_yml_config()
llm = AzureChatOpenAIModel(config=config)
kickOffAgents(agent_list,[agent_list[0], agent_list[1]], llm=llm)
```

### Configuration for Multilevel Agent Communication&#x20;

The following diagram shows the example that uses parallel, aggregation and parallel  configuration of agents. In this example both 'RESEARCHER1' and 'RESEARCHER2' will get triggered by the user and their responses will be aggregated by "WRITER". The response of the "WRITER" agent will go to "EMAILER1" and "EMAILER2".  Eventually the "HGI" gets the two responses.

<figure><img src="../.gitbook/assets/image (45).png" alt=""><figcaption></figcaption></figure>

Example

```python
import logging
from openagi.init_agent import kickOffAgents
from openagi.agent import Agent
from openagi.tools.integrations import DuckDuckGoSearchTool
from openagi.llms.azure import AzureChatOpenAIModel

def onAggregationAction(agentName, consumerAgent, aggrSourceAgentList, aggrResultsList):
    result = ""
    for string in aggrResultsList:
        result += string.body + " "
    logging.debug(
        f"aggregation of messages::of {agentName} to {consumerAgent} {result}"
    )
    return result

if __name__ == "__main__":
    agent_list = [
    Agent(
        agentName="RESEARCHER1",  # name
        role="RESEARCH EXPERT",  # role
        goal="search for latest trends in  Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
        backstory="Has the capability to execute internet search tool",
        capability="search_executor",
        task="search internet for the goal for the trends after first half of 2023",
        output_consumer_agent=["WRITER"],  # the consumer agent after executing task
        tools_list=[DuckDuckGoSearchTool],
    ),
    Agent(
        agentName="RESEARCHER2",  # name
        role="RESEARCH EXPERT",  # role
        goal="search for latest trends in Covid-19  treatment that includes medicines, physical exercises, overall management and prevention aspects",
        backstory="Has the capability to execute internet search tool",
        capability="search_executor",
        task="search internet for the goal for the trends after first half of 2023",
        output_consumer_agent=["WRITER"],  # the consumer agent after executing task
        tools_list=[DuckDuckGoSearchTool],
    ),
    Agent(
        agentName="WRITER",
        role="SUMMARISING EXPERT",
        aggregator=2,
        onAggregationAction=onAggregationAction,
        goal="summarize input into presentable points",
        backstory="Expert in summarising the given text",
        capability="llm_task_executor",
        task="summarize points to present to health care professionals",
        output_consumer_agent=["EMAILER1", "EMAILER2"],
    ),
    Agent(
        agentName="EMAILER1",
        role="EMAIL CREATOR",
        goal="composes the email based on the content",
        backstory="Good in composing precise emails",
        capability="llm_task_executor",
        task="compose email based on summary to doctors  with subject-summary and details",
        output_consumer_agent=["HGI"],
    ),
    Agent(
        agentName="EMAILER2",
        role="EMAIL CREATOR",
        goal="composes the email based on the content",
        backstory="Good in composing precise emails",
        capability="llm_task_executor",
        task="compose email based on summary to general public with subject-summary and details",
        output_consumer_agent=["HGI"],
    )
    ]
    config = AzureChatOpenAIModel.load_from_yml_config()
    llm = AzureChatOpenAIModel(config=config)
    kickOffAgents(agent_list,[agent_list[0],agent_list[1]], llm=llm)
```
