import logging
from openagi.init_agent import kickOffGenAIAgents
from openagi.agent import AIAgent
from openagi.tools.integrations import DuckDuckGoSearchTool
from openagi.llms.azure import AzureChatOpenAIModel
from dotenv import load_dotenv

load_dotenv()

def onResultHGI(agentName, result, consumerAgent):
    feedback="Pass"
    action = "None"
    logging.debug(f"{agentName}:TO:{consumerAgent}-> {result}")
    return result, feedback, action
  
if __name__ == "__main__":
    agent_list=["RESEARCHER", "WRITER", "EMAILER"]
    llm="local"
    AgentObjects=[]

    agent1 = AIAgent(agentName=agent_list[0], aggregator=0, onAggregationAction=None, creator=None, role="RESEARCHER", feedback=False, goal="search for latest trends in Carona treatment that includes medicines, physical exercises, overall management and prevention aspects",
                     backstory="backstory", capability="search_executor", agent_type="STATIC",  multiplicity=0, 
                     task="search internet for the goal for the trends in 2H 2023 onwards", output_consumer_agent=agent_list[1], HGI_Intf=None, llm_api=llm, 
                      llm_resp_timer_value=20, tools_list=[DuckDuckGoSearchTool])
    
    agent3 = AIAgent(agentName=agent_list[2], aggregator=0, onAggregationAction=None,creator=None,role="EMAILER", feedback=False, goal="composes the email based on the contenct", backstory="backstory", capability="llm_task_executor", agent_type="DYNAMIC",  
              multiplicity=0, task="composes email based on summary to doctors and general public separately into a file with subject-summary and details", output_consumer_agent="HGI",HGI_Intf=None,
              llm_api=llm,  llm_resp_timer_value=1300, tools_list=[])
        
    agent2 = AIAgent(agentName=agent_list[1], aggregator=0, onAggregationAction=None,creator=agent3,role="SUMMARISER", feedback=False, goal="summarize input into presentable points", backstory="backstory", capability="llm_task_executor", agent_type="STATIC",  
              multiplicity=0, task="summarize points to present to health care professionals and general public separately", output_consumer_agent=agent_list[2],HGI_Intf=None,
              llm_api=llm,  llm_resp_timer_value=1030, tools_list=[])  
    
    
    AgentObjects=[agent1, agent2, agent3]
    config = AzureChatOpenAIModel.load_from_yml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffGenAIAgents(AgentObjects,[AgentObjects[0]], DynamicAgentObjectsList=[agent3], llm=azure_chat_model)