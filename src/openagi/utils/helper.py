from openagi.llms.openai import OpenAIModel


def get_default_llm():
    config = OpenAIModel.load_from_env_config()
    return OpenAIModel(config=config)
