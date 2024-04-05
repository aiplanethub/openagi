from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms.azure import AzureChatOpenAIModel

if __name__ == "__main__":
    agent_name = ["Coder", "Reviewer"]
    agent_list = [
        Agent(
            agentName=agent_name[0],
            aggregator=0,
            onAggregationAction=None,
            creator=None,
            role="Coder",
            feedback=False,
            goal="To generate Python code for calculating the factorial of a number in a way that it can be easily copied and pasted by users for execution.Do not use any python libraries for it, hardcode it completely",
            backstory="You are a software developer working on a platform that provides code snippets for various programming tasks.",
            capability="llm_task_executor",
            agent_type="STATIC",
            multiplicity=0,
            task="Develop a Python script that calculates the factorial of a given number, presenting the code in a line-by-line format to ensure clarity and ease of use for users.",
            output_consumer_agent=[agent_name[1]],
            HGI_Intf=None,
            llm_resp_timer_value=2000,
            tools_list=[],
        ),
        Agent(
            agentName=agent_name[1],
            aggregator=0,
            onAggregationAction=None,
            creator=None,
            role="Reviewer",
            feedback=True,
            goal="To meticulously examine the provided Python code, identifying any potential issues, and providing feedback on its quality and adherence to best practices.",
            backstory="You are a seasoned software engineer responsible for reviewing Python code submissions within your team.",
            capability="llm_task_executor",
            agent_type="STATIC",
            multiplicity=0,
            task="Conduct a comprehensive review of the Python code, paying particular attention to logging, error conditions, and exception handling. Upon completion, provide a status report indicating whether any issues were found and detailing any necessary improvements.Do not include any code, only a report of the provided code is required.",
            output_consumer_agent=["HGI"],
            HGI_Intf=None,
            llm_resp_timer_value=1300,
            tools_list=[],
        ),
    ]
    config = AzureChatOpenAIModel.load_from_yml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffAgents(agent_list, [agent_list[0]], llm=azure_chat_model)
