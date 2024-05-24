# News Agent

Be upto date on whats happening using News Agent

```python
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.planner.task_decomposer import TaskPlanner
from rich.console import Console
from rich.markdown import Markdown

# Set the AZURE_BASE_URL, AZURE_DEPLOYMENT_NAME, AZURE_MODEL_NAME, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_API_KEY as environment variables
config = AzureChatOpenAIModel.load_from_env_config()
llm = AzureChatOpenAIModel(config=config)


# Setup an Admin Agent
admin = Admin(
    llm=llm,
    actions=[DuckDuckGoSearch],  # Actions that the Agent can use to acheive the given objective
    planner=TaskPlanner(human_intervene=False),
)

# Run the Agent with a query and description of the query.
res = admin.run(
    query="Recent AI News Microsoft",
    description="",
)

# Print the results from the OpenAGI
Console().print(Markdown(res))
```
