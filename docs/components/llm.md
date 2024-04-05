# LLM

Large Language Models serve as the backbone for executing Agent tasks. The tools within the agents fetch the data, which is then passed as context to the LLM. This context triggers the KickOffAgent to execute the required tasks accordingly. Currently, OpenAGI supports two LLMs: OpenAI and Azure ChatOpenAI model.

> LLM is passed into kickOffGenAIAgents to execute the agents response.&#x20;

### OpenAIModel

OpenAGI supports the GPT-3.5 model by default, represented as OpenAGI. To initialize this model, you need to insert the OpenAI API key inside the `agentConfig.yaml` file and pass the configuration details as parameters to execute the LLM.

```
from openagi.llms.openai import OpenAIModel 

config = OpenAIModel.load_from_yml_config()
llm = OpenAIModel(config=config)
```

#### Params Configuration

```
OPENAI_API_KEY: sk-abcd #replace with your key
```

### Azure ChatOpenAI Model

For a Large Language Model, context length is crucial. To utilize a large context, such as 32K from GPT-4, we employ the AzureOpenAI chat model. To initialize this model, you need to insert the parameter configuration inside the `agentsConfig.yaml` file and pass the configuration details as parameters to execute the LLM.

```
from openagi.llms.azure import AzureChatOpenAIModel 

config = AzureChatOpenAIModel.load_from_yml_config() 
azure_chat_model = AzureChatOpenAIModel(config=config)
```

#### Params Configuration

```
BASE_URL: "https://<abcd>.openai.azure.com/" #replace with your endpoint
DEPLOYMENT_NAME: "abcd" #replace with your API key
MODEL_NAME: "gpt4-32k" 
OPENAI_API_VERSION: "2023-05-15"
AZURE_OPENAI_API_KEY: abcdefg #replace with your Azure API key
```

Note, AZURE\_OPENAI\_API\_KEY and OPENAI\_API\_KEY are not enclosed within the quotes. Whereas the secrets configuration such as base url, deployment name are enclosed within the quotes.&#x20;
