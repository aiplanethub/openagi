# News Agent

Be upto date on what's happening using News Agent

**Import Required Libraries**

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

Set up the environment variables and configure the Azure OpenAI model.

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

Create an admin to manage the actions and execute the task.

```python
admin = Admin(
    llm=llm,
    actions=[DuckDuckGoSearch],
    planner=TaskPlanner(human_intervene=False),
)
```

**Execute Agent LLM**&#x20;

Run the admin with a specific query to get the latest news.

```python
res = admin.run(
    query="Recent AI News Microsoft",
    description="",
)
```

**Print the Results**&#x20;

Output the results using the `rich` library.

```python
Console().print(Markdown(res))
```

