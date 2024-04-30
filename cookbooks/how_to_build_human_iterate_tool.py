import logging
from openagi.init_agent import kickOffGenAIAgents
from openagi.agent import AIAgent
from openagi.llms.azure import AzureChatOpenAIModel

def onResultHGI(agentName, result, consumerAgent):
    feedback = "Pass"
    action = "None"
    logging.debug(f"{agentName}:TO:{consumerAgent}-> {result}")
    return result, feedback, action
    
if __name__ == "__main__":
    AgentObjects = [
    AIAgent(
        agentName = "CODER",
        role = "Codes the Python script for adding two numbers",
        goal = "Create a Python script to add two numbers",
        backstory = "Has the capability to execute Python code generation tasks",
        capability = "llm_task_executor",
        task = "Create Python code to add two numbers",
        output_consumer_agent = "HGI",
        HGI_Intf=onResultHGI,
    ),
    ]
    config = AzureChatOpenAIModel.load_from_yml_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffGenAIAgents(AgentObjects, [AgentObjects[0]], llm=azure_chat_model)
