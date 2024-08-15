---
description: >-
  Staying current with the latest developments is crucial, especially in the
  fast-paced world of technology and artificial intelligence. A News Agent can
  help you stay informed by gathering the latest n
---

# 📰 News Agent

Be upto date on what's happening using News Agent

**Import Required Libraries**

First, import the necessary libraries and modules. These modules will enable the agent to perform web searches, handle task planning, and display results in a readable format.

```python
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.planner.task_decomposer import TaskPlanner
from rich.console import Console
from rich.markdown import Markdown
import os
```

**Setup LLM**&#x20;

Set up the environment variables required for Azure OpenAI configuration. These environment variables include the base URL, deployment name, model name, API version, and API key. This configuration is essential for the Large Language Model (LLM) to function correctly.

```python
os.environ["AZURE_BASE_URL"] = "https://<replace-with-your-endpoint>.openai.azure.com/"
os.environ["AZURE_DEPLOYMENT_NAME"] = "<replace-with-your-deployment-name>"
os.environ["AZURE_MODEL_NAME"] = "gpt4-32k"
os.environ["AZURE_OPENAI_API_VERSION"] = "2023-05-15"
os.environ["AZURE_OPENAI_API_KEY"] = "<replace-with-your-key>"

config = AzureChatOpenAIModel.load_from_env_config()
llm = AzureChatOpenAIModel(config=config)
```

**Define Admin**&#x20;

Create an Admin instance to manage actions and execute tasks. The Admin will use the DuckDuckGoSearch tool to perform web searches and the TaskPlanner to manage task execution without human intervention.

```python
admin = Admin(
    llm=llm,
    actions=[DuckDuckGoSearch],
    planner=TaskPlanner(human_intervene=False),
)
```

**Execute Agent LLM**&#x20;

Run the Admin with a specific query to fetch the latest news about AI from the web. In this case, the query is set to find recent news related to "Recent AI News Microsoft." The Admin will process this query and return the relevant news articles.

```python
res = admin.run(
    query="Recent AI News Microsoft",
    description="",
)
```

**Print the Results**&#x20;

Finally, use the rich library to output the results in a readable format. The Markdown class helps in rendering the news content neatly in the console.

```python
Console().print(Markdown(res))
```

By following these steps, you can set up a News Agent that keeps you updated with the latest news in the field of artificial intelligence. This example uses the power of Azure's GPT-4 model and OpenAGI to perform efficient web searches and present the information in an easily digestible format.

### Sample Output

When the above code is executed, the output in the console might look like this:

```
# Recent AI News from Microsoft

## 1. Microsoft Unveils New AI Features in Office Suite
*Date: August 8, 2024*  
Microsoft has announced the integration of advanced AI features in its Office suite, aiming to enhance productivity and collaboration among users.

## 2. Microsoft AI Research Breakthroughs
*Date: August 7, 2024*  
Recent research from Microsoft AI has shown significant improvements in natural language processing, potentially revolutionizing how machines understand human language.

## 3. Microsoft Partners with OpenAI for New Developments
*Date: August 6, 2024*  
In a strategic partnership, Microsoft and OpenAI are set to collaborate on new AI technologies that promise to push the boundaries of artificial intelligence applications.
```

This output showcases the latest news articles related to Microsoft's developments in artificial intelligence, formatted neatly for readability.
