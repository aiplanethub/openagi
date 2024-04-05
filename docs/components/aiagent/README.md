# AIAgent

Within this system, an agent is described as an entity that engages with its surroundings by utilizing sensors to observe and actuators to interact. This engagement is a continual cycle of sensing, thinking, and acting. The agents in this system are equipped with a broad spectrum of tools and a logic engine (LLM) that enables them to execute tasks based on set parameters.

The agents have the capability to communicate with one another and make use of the tools provided to them. After completing a task, an agent forwards the outcome to another agent for subsequent processing. Each agent has required and optional characteristics, which are detailed in subsequent sections. Communication among agents is managed through priority queues, supporting different execution methods like parallel, sequential, aggregate, or dynamic execution, details of which are further discussed in later sections.

A human user initiates the agent's execution, and the final output is generally presented to the user as a printed message in the current release.

For more details on the specific attributes of agents, refer to the Agent Configuration section.

<pre class="language-python"><code class="lang-python">from openagi.agent import AIAgent

<strong>AIAgent(
</strong>        agentName=agent_list[2],
        aggregator=2,
        onAggregationAction=onAggregationAction,
        creator=None,
        role="SUMMARISER",
        feedback=False,
        goal="summarize input into presentable points",
        backstory="backstory",
        capability="llm_task_executor",
        agent_type="STATIC",
        multiplicity=0,
        task="summarize points to present to health care professionals and general public separately",
        output_consumer_agent=agent_list[3],
        HGI_Intf=onResultHGI,
        llm_api=llm,
        llm_resp_timer_value=130,
        tools_list = [WikipediaTool, GoogleFinanceSearchTool, exaSearchTool, SerperSpecificSearchTool],
    )
</code></pre>

