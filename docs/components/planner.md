# Planner

## What is Planner?

Planner is one of the important component of any Agent framework, which enables the agent to divide a task into multiple subtasks based on the requirement. We call this step as **Task Decomposition.**&#x20;

The  `Planner` in the `OpenAGI` contains essential modules and components that handle task planning and decomposition. These components are designed to work together to break down complex tasks into manageable sub-tasks, which are then executed by Admin.&#x20;

Below is a detailed explanation of the attributes and functionality of the modules within the  `Planner`.

## Attributes



<table><thead><tr><th width="185">Parameter</th><th width="195">Optional Parameter</th><th>Description</th></tr></thead><tbody><tr><td>human_intervene</td><td>Yes</td><td>It indicates the framework that after generating output, it should ask human for feedback and make changes to output based on that.</td></tr><tr><td>input_action</td><td>Yes</td><td>It shows how user can provide feedback to the Admin during execution.</td></tr></tbody></table>

&#x20;&#x20;

### Code Snippet

The primary component, `TaskPlanner`, allows for the decomposition of tasks into smaller sub-tasks and the planning of their execution. This modular approach facilitates efficient task management and execution within the OpenAGI framework.

```python
from openagi.planner.task_decomposer import TaskPlanner

planner = TaskPlanner(human_intervene=False)
```

Below we have shown how one can initiate and run using  query.

```python
# imports
from openagi.agent import Admin
from openagi.llms.openai import OpenAIModel
from openagi.planner.task_decomposer import TaskPlanner
from openagi.actions.tools.ddg_search import DuckDuckGoSearch

# Define LLM
config = OpenAIModel.load_from_env_config()
llm = OpenAIModel(config=config)

# Planner Usage
admin = Admin(
    llm=llm,
    actions=[DuckDuckGoSearch],
    planner=TaskPlanner(human_intervene=False),
)

# Run Admin
res = admin.run(
            query="sample query",
            description="sample description",
            )
```
