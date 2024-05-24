# LLM

Large Language Models (LLMs) serve as the backbone for executing Agentic workflows. LLMs excel at generating responses and, when combined with human-like planning, reasoning, and task decomposition, give rise to the concept of Agents. In OpenAGI, LLMs plan and reason to decompose task objectives into sub-tasks. They then execute these sub-tasks and return meaningful responses to the user.&#x20;

LLMs can be implemented within the Admin and utilize a Planner to execute tasks. Currently, OpenAGI supports two LLMs: OpenAI and Azure ChatOpenAI models.

### OpenAI Model

OpenAGI supports the GPT-3.5 model by default, represented as OpenAGI. To initialise this model, you need to insert the OpenAI API key inside the environment file and pass the configuration details as parameters to execute the LLM.

```python
import os
from openagi.llms.openai import OpenAIModel

os.environ['OPENAI_API_KEY'] = "sk-<replace-with-your-key>"

config = OpenAIModel.load_from_env_config()
llm = OpenAIModel(config=config)
```

### Azure ChatOpenAI Model

For a Large Language Model, context length is crucial. To utilize a large context, such as 32K from GPT-4, we employ the AzureOpenAI chat model. To initialise this model, you need to insert the parameter configuration inside the environment file and pass the configuration details as parameters to execute the LLM.

```python
import os
from openagi.llms.azure import AzureChatOpenAIModel

os.environ["AZURE_BASE_URL"]="https://<replace-with-your-endpoint>.openai.azure.com/"
os.environ["AZURE_DEPLOYMENT_NAME"] = "<replace-with-your-deployment-name>"
os.environ["AZURE_MODEL_NAME"]="gpt4-32k"
os.environ["AZURE_OPENAI_API_VERSION"]="2023-05-15"
os.environ["AZURE_OPENAI_API_KEY"]=  "<replace-with-your-key>"

config = AzureChatOpenAIModel.load_from_env_config()
llm = AzureChatOpenAIModel(config=config)
```

