from langchain.agents import (
    initialize_agent,
    load_tools,
)
from langchain_openai import AzureChatOpenAI


# TODO: @tanish-aiplanet look into this
# issues - not working
def DallEImageGenerator(inputString):
    llm_2 = AzureChatOpenAI(
        model_name="gpt4-32k", openai_api_version="2023-05-15", azure_deployment="gpt4-inference"
    )
    llm = llm_2
    tools = load_tools(["dalle-image-generator"])
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=False)
    image = agent.run(inputString)
    return image
