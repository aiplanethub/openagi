from openagi.llms.azure import AzureChatOpenAIModel
from openagi.llms.openai import OpenAIModel


def loadLLM(llm="openai"):
    if llm == "openai":
        config = OpenAIModel.load_from_env_config()
        llm = OpenAIModel(config=config)
        return llm
    else:
        config = AzureChatOpenAIModel.load_from_env_config()
        llm = AzureChatOpenAIModel(config=config)
    return llm


def getLLM(sys):
    # total arguments
    n = len(sys.argv)
    print("Total arguments passed:", n)

    # Arguments passed
    print("\nName of Python script:", sys.argv[0])

    print("\nArguments passed:", end=" ")
    for i in range(1, n):
        print(sys.argv[i], end=" ")

    return loadLLM(sys.argv[1])
