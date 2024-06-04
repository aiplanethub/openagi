from uuid import uuid4
from openagi.llms.openai import OpenAIModel


def get_default_llm():
    config = OpenAIModel.load_from_env_config()
    return OpenAIModel(config=config)


def get_default_id():
    return uuid4().hex
