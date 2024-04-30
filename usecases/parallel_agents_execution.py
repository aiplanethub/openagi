import logging
from openagi.init_agent import kickOffGenAIAgents
from openagi.agent import AIAgent
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
    agent_list=["RESEARCHER1", "RESEARCHER2" ,"WRITER", "EMAILER"]
    llm="azure"
    AgentObjects=[]
    AgentObjects = [
    AIAgent(agentName=agent_list[0], aggregator=0, onAggregationAction=None, creator=None, role="RESEARCHER", feedback=False, goal="search for latest trends in Carona treatment that includes medicines, physical exercises, overall management and prevention aspects",
                     backstory="backstory", capability="search_executor", agent_type="STATIC",  multiplicity=0, 
                     task="search internet for the goal for the trends in 2H 2023 onwards", output_consumer_agent=agent_list[2], HGI_Intf=onResultHGI, 
                      llm_resp_timer_value=20, tools_list=[DuckDuckGoSearchTool]),
    
    AIAgent(agentName=agent_list[1], aggregator=0, onAggregationAction=None, creator=None, role="RESEARCHER",feedback=False, goal="search for latest trends in Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
                     backstory="backstory", capability="search_executor", agent_type="STATIC",  multiplicity=0, 
                     task="search internet for the goal for the trends in 2H 2023 onwards", output_consumer_agent=agent_list[2], HGI_Intf=onResultHGI, 
                      llm_resp_timer_value=20, tools_list=[DuckDuckGoSearchTool]),
     
    AIAgent(agentName=agent_list[2], aggregator=2, onAggregationAction=onAggregationAction,creator=None,role="SUMMARISER", feedback=False, goal="summarize input into presentable points", backstory="backstory", capability="llm_task_executor", agent_type="STATIC",  
              multiplicity=0, task="summarize points to present to health care professionals and general public separately", output_consumer_agent=agent_list[3],HGI_Intf=onResultHGI,
              llm_resp_timer_value=130, tools_list=[]),   
    
    
    AIAgent(agentName=agent_list[3], aggregator=0, onAggregationAction=None,creator=None,role="EMAILER", feedback=False, goal="composes the email based on the contenct", backstory="backstory", capability="llm_task_executor", agent_type="STATIC",  
              multiplicity=0, task="composes email based on summary to doctors and general public separately into a file with subject-summary and details", output_consumer_agent="HGI",HGI_Intf=onResultHGI,
              llm_resp_timer_value=130, tools_list=[])
    ]
    config = AzureChatOpenAIModel.load_from_yml_config()
    llm = AzureChatOpenAIModel(config=config)
    kickOffGenAIAgents(AgentObjects,[AgentObjects[0], AgentObjects[1]], llm=llm)