# 🗂 Planner

## What is Planner?

Planner is one of the important component of any Agent framework, which enables the agent to divide a task into multiple subtasks based on the requirement. We call this step as **Task Decomposition.**&#x20;

The `Planner` in the `OpenAGI` contains essential modules and components that handle task planning and decomposition. These components are designed to work together to break down complex tasks into manageable sub-tasks, which are then executed by Admin.&#x20;

Below is a detailed explanation of the attributes and functionality of the modules within the  `Planner`.

## Attributes



<table><thead><tr><th width="185">Parameter</th><th width="195">Optional Parameter</th><th>Description</th></tr></thead><tbody><tr><td>human_intervene</td><td>No</td><td>It indicates the framework that after generating output, it should ask human for feedback and make changes to output based on that.</td></tr><tr><td>autonomous</td><td>No</td><td>Autonomous will self assign role and instructions and divide it among the workers. The default is `False`</td></tr><tr><td>input_action</td><td>Yes</td><td>It shows how user can provide feedback to the Admin during execution.</td></tr><tr><td>prompt</td><td>Yes</td><td>An optional prompt to be used for task planning.</td></tr><tr><td>workers</td><td>Yes</td><td>Workers can represent different agents or processes that handle specific subtasks, enabling parallel execution and improving efficiency. If no workers are specified, the planner will operate without additional parallel processing capabilities.</td></tr><tr><td>llm</td><td>Yes</td><td>This parameter allows the user to specify the Large Language Model (LLM) that will be used for generating responses and planning tasks.</td></tr><tr><td>retry_threshold</td><td>Yes</td><td>This parameter defines the maximum number of times the planner will attempt to retry a task if it fails to execute successfully. The default value is <code>3.</code></td></tr></tbody></table>

&#x20;&#x20;

### Code Snippet

The primary component, `TaskPlanner`, allows for the decomposition of tasks into smaller sub-tasks and the planning of their execution. This modular approach facilitates efficient task management and execution within the OpenAGI framework.

```python
from openagi.planner.task_decomposer import TaskPlanner

planner = TaskPlanner(human_intervene=False)
# make TaskPlanner autonomous = True for auto creating workers
# Autonomous Multi Agent Architecture
# plan = TaskPlanner(autonomous=True,human_intervene=True)
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
