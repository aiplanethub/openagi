# ExaSeach/GmailAgent

This code presents a system of AI agents designed to perform various tasks related to researching and disseminating information on specific topics. Here's a short description:

The code initializes and configures several AI agents with distinct roles, each aimed at achieving a particular goal in a coordinated manner. The agents and their roles are defined as follows:

1\. RESEARCHER: This agent's role is to search for the latest trends in the treatment of both Corona and Cancer. It aims to gather information on medicines, physical exercises, overall management, and prevention aspects related to these diseases. The agent utilizes internet search tools to accomplish its task.

2\. SUMMARISER: Once the RESEARCHER agent gathers information, the SUMMARISER agent's role is to summarize the collected data into concise and presentable points. These summaries are intended for healthcare professionals and the general public separately.

3\. EMAILER: The EMAILER agent composes emails based on the summarized points. It is skilled at composing precise emails and formulates messages tailored to doctors and the general public. The emails are structured into files with subject-summaries and details.

4\. GMAILER: Finally, the GMAILER agent sends emails using the GmailSearchTool. It is proficient in sending emails relevant to the context provided. In this case, it sends emails to the recipient "tanish@aiplanet.com".

#### Example Code:

In the code below, the Researcher, Summariser, Emailer and Gmailer Agent are configured with their goal, backstory, capability, task and the tools needed for each agent for the same.

```python
from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.tools.integrations import ExaSearchTool, GmailSearchTool

if __name__ == "__main__":
    agent_list = [
        Agent(
            agentName="RESEARCHER",  # name
            role="RESEARCHER",  # role
            goal="search for latest trends in Carona and Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
            backstory="Has the capability to execute internet search tool",
            capability="search_executor",
            task="search internet for the goal for the trends after first half of 2023",
            output_consumer_agent=agent_names[1],  # the consumer agent after executing task
            tools_list=[ExaSearchTool],
        ),
        Agent(
            agentName="WRITER",
            role="SUMMARISER",
            goal="summarize input into presentable points",
            backstory="Expert in summarising the given text",
            capability="llm_task_executor",
            task="summarize points to present to health care professionals and general public separately",
            output_consumer_agent=agent_names[2],
        ),
        Agent(
            agentName="EMAILER",
            role="EMAILER",
            goal="composes the email based on the content",
            backstory="Good in composing precise emails",
            capability="llm_task_executor",
            task="composes email based on summary to doctors and general public separately into a file with subject-summary and details",
            output_consumer_agent=agent_names[3],
        ),
        Agent(
            agentName="GMAILER",
            role="GMAILER",
            goal="Send the email using GmailSearchTool",
            backstory="Good in sending emails to the given context.",
            capability="llm_task_executor",
            task="send emails to the receipient tanish@aiplanet.com",
            output_consumer_agent="HGI",
            tools_list=[GmailSearchTool],
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

<div align="center">

<figure><img src="../.gitbook/assets/image (26).png" alt="" width="563"><figcaption></figcaption></figure>

</div>

Code Example: usecases/ProfAgentExaSearchGmail.py
