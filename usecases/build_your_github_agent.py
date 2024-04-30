from openagi.init_agent import kickOffGenAIAgents
from openagi.agent import AIAgent
from openagi.tools.integrations import GithubSearchTool

if __name__ == "__main__":
    agent_list = ["RESEARCHER", "TESTCASEDEVELOPER"]
    AgentObjects=[]
    AgentObjects = [
    AIAgent(
        agentName=agent_list[0],  # name
        role="DEVELOPER",  # role
        goal="Efficiently search and retrieve relevant information regarding repository and code snippets on GitHub.",
        backstory="Developed to enhance productivity for developers, this tool integrates with the GitHub API to provide streamlined access to code resources.",
        capability="search_executor",
        task="Retrieve the code for all the files in the respository.",
        output_consumer_agent=agent_list[1],  # the consumer agent after executing task
        tools_list=[GithubSearchTool],
    ),
    AIAgent(agentName=agent_list[1], aggregator=0, onAggregationAction=None,creator=None,
        role="TESTCASEDEVELOPER", feedback=False,
        goal="To meticulously examine the provided Python code and provide test cases with adherence to best practices.", 
        backstory="You are a seasoned software test case developer who developes unit, integration and functional test cases for the given program code", capability="llm_task_executor", 
        agent_type="STATIC", multiplicity=0, 
        task="Conduct a comprehensive test cases for the Python code, paying particular attention to functional and acceptance testing including edge cases. Also provide no of positive and edge test cases to enable the management to understand the quality of testing",
        output_consumer_agent="HGI",HGI_Intf=None,
        llm_api="azure",  llm_resp_timer_value=1300, tools_list=[]
    )
    ]
    kickOffGenAIAgents(AgentObjects,[AgentObjects[0]])
