from openagi.agent import AIAgent
from openagi.init_agent import kickOffGenAIAgents
from openagi.llms.azure import AzureChatOpenAIModel

if __name__ == "__main__":
    agent_list = ["Coder", "Test case Developer"]
    AgentObjects = [
        AIAgent(
            agentName=agent_list[0],
            aggregator=0,
            onAggregationAction=None,
            creator=None,
            role="Coder",
            feedback=False,
            goal="write python code for fastAPI usage with routes and all the functions of FastAPI in a way that it can be easily copied and pasted by users for execution.Do not use any python libraries for it, hardcode it completely",
            backstory="You are a software developer working on a platform that provides code snippets for various programming tasks.",
            capability="llm_task_executor",
            agent_type="STATIC",
            multiplicity=0,
            task="Develop a Python script for the above presenting the code in a line-by-line format to ensure clarity and ease of use for users.",
            output_consumer_agent=agent_list[1],
            HGI_Intf=None,
            llm_resp_timer_value=2000,
            tools_list=[],
        ),
        AIAgent(
            agentName=agent_list[1],
            aggregator=0,
            onAggregationAction=None,
            creator=None,
            role="Test Case developer",
            feedback=False,
            goal="To meticulously examine the provided Python code and provide test caeses with adherence to best practices.",
            backstory="You are a seasoned software test case deloper who developes unit, initegration and functional tases for the given program code",
            capability="llm_task_executor",
            agent_type="STATIC",
            multiplicity=0,
            task="Conduct a comprehensive test cases for the Python code, paying particular attention to functional and acceptance testing including edge cases. Also provide no of positive and edge test cases to enable the management to understand the quality of testing",
            output_consumer_agent="HGI",
            HGI_Intf=None,
            llm_resp_timer_value=1300,
            tools_list=[],
        ),
    ]
    config = AzureChatOpenAIModel.load_from_yml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffGenAIAgents(AgentObjects, [AgentObjects[0]], llm=azure_chat_model)
