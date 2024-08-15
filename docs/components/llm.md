# 🧠 LLM

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

### Groq Model

Groq is an inference engine specifically designed for applications requiring low latency and rapid responses. It uses open-source models such as Mistral, Gemma, and Llama 2, delivering hundreds of tokens per second, making it faster than other models. To initialize this model, you need to insert the Groq API key along with the model name and temperature in the environment variables.

Get the API key from here: [https://console.groq.com/keys](https://console.groq.com/keys)

```python
import os
from openagi.llms.groq import GroqModel

os.environ['GROQ_API_KEY'] = '<groq-api-key>'
os.environ['GROQ_MODEL'] = '<model-name>'
os.environ['GROQ_TEMP'] = '<temperature>'

config = GroqModel.load_from_env_config()
llm = GroqModel(config=config)
```

### Gemini Model

This model includes the Gemini family models from Google, which includes `Gemini-1.0-pro` and `Gemini-pro`.  To initialize this model, you need to insert the Google API key along with the model name and the temperature.

Get the API key from here: [https://ai.google.dev/](https://ai.google.dev/)

```python
import os
from openagi.llms.gemini import GeminiModel

os.environ['GOOGLE_API_KEY'] = '<google-api-key>'
os.environ['Gemini_MODEL'] = '<model-name>'
os.environ['Gemini_TEMP'] = '<temperature>'

config = GeminiModel.load_from_env_config()
llm = GeminiModel(config=config)
```

### Ollama Model

Ollama allows you to run models locally, providing a straightforward way to integrate them into your applications.**Installation Steps:**

1. **Download Ollama**: Visit [Ollama's download page](https://ollama.com/download) to get the appropriate version for your operating system (macOS, Linux, or Windows).
2.  **Install Ollama**: Use the following command to install Ollama via pip:

    ```
    pip install ollama
    ```

**Basic Ollama Commands:**

*   To load the Llama2 model locally:

    ```
    ollama pull mistral
    ```
*   To load the Gemma model locally:

    ```
    ollama pull gemma
    ```
*   To display all the models that are installed:

    ```
    ollama list
    ```

For more commands, refer to the [Ollama GitHub repository](https://github.com/ollama/ollama).

**Running the Model:**Before executing the Ollama model, ensure that the model is running locally in your terminal. You can start the Llama2 model with the following command:

```
ollama run mistral
```

This setup allows you to utilize the Ollama model effectively within your applications, similar to other models supported by OpenAGI. This format aligns with the existing documentation style and provides clear instructions for users to get started with the Ollama model.

```python
import os
from openagi.llms.azure.ollama  import OllamaModel
    
llm = OllamaModel(model="mistral")
```
