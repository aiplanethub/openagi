# Memory

## What is Memory?

Memory is one of the important component of the Agentic framework, which gives the agents their own memory that to recall and remember the tasks executed nnd feedback received by the agent. It helps the agent make "informed decision" by recalling the previous actions and their observations. It can also store the current execution.\
\
Memory helps the agent to  not make the same mistake for similar task as it did earlier or to improving the overall experience of user by giving them a result based on recalled memory.

### Code Snippet

```python
from openagi.memory import Memory

memory = Memory()
```

Below we have shown how one can initiate and run using  query.

```python
# imports
from openagi.agent import Admin
from openagi.llms.openai import OpenAIModel
from openagi.planner.task_decomposer import TaskPlanner
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.memory import Memory

# Define LLM
config = OpenAIModel.load_from_env_config()
llm = OpenAIModel(config=config)

# Memory Usage
admin = Admin(
    llm=llm,
    actions=[DuckDuckGoSearch],
    planner=TaskPlanner(human_intervene=False),
    memory=Memory(),
)

# Run Admin
res = admin.run(
            query="sample query",
            description="sample description",
            )
```
