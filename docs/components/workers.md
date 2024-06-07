# Workers

### What is a Worker?

Workers are special type of classes, responsible for carrying out the tasks assigned by the class "Admin". They utilize tools such as internet search engines, LLMs, and document writers to perform their tasks. Additionally, they can determine which tools to use from a predefined set.

Similarly to how a large task like writing a blog is decomposed into smaller steps such as researching, drafting, and publishing, the admin can define a large task and split it into smaller tasks that are then assigned to the workers.

### Attributes

Workers possess attributes that facilitate the execution and completion of smaller, independent tasks.

<table><thead><tr><th width="160">Attribute</th><th width="204">Optional Parameter</th><th>Description</th></tr></thead><tbody><tr><td>role</td><td></td><td>It is a string input that defines the Functionality or Responsibility of the worker. </td></tr><tr><td>instructions</td><td></td><td>A paragraph about how the LLM should behave related to its role can also include the backstory and other relevant details that might aid in generating the output.</td></tr><tr><td>actions</td><td>Yes</td><td>This configurable parameter takes a list that lets us specify the set of tools available to the worker. The worker may or may not use these tools. If no tools are specified, or if the action list is empty, the worker defaults to the actions set by the admin.</td></tr><tr><td>llm</td><td>Yes</td><td>This parameter is configurable, allowing the worker to either use a specified LLM or default to the LLM designated by the admin.</td></tr><tr><td>max_iterations</td><td>Yes</td><td>This parameter specifies the maximum number of iterations, as an integer, allowed to achieve the objective of the given task.</td></tr><tr><td>force_output</td><td>Yes</td><td>This boolean parameter determines whether to force an output or answer after reaching the maximum iteration limit.</td></tr></tbody></table>

### Code Snippet

```python
from openagi.worker import Worker

worker = Worker(
        role=role,
        instructions=instructions,
        actions=actions,
        llm=llm,
        max_iterations=max_iterations,
        force_output=force_output
    )
```

Below we have shown how one can initiate and run a simple admin-worker query.

```python
from openagi.actions.files import WriteFileAction
from openagi.actions.tools.ddg_search import DuckDuckGoNewsSearch
from openagi.actions.tools.webloader import WebBaseContextTool
from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
from openagi.worker import Worker

config = AzureChatOpenAIModel.load_from_env_config()
llm = AzureChatOpenAIModel(config=config)

# Workers
researcher = Worker(
    role="Researcher",
    instructions="sample instruction.",
    actions=[
        DuckDuckGoNewsSearch,
        WebBaseContextTool,
    ],
)
writer = Worker(
    role="Writer",
    instructions="sample instruction.",
    actions=[
        DuckDuckGoNewsSearch,
        WebBaseContextTool,
    ],
)
reviewer = Worker(
    role="Reviewer",
    instructions="sample instruction.",
    actions=[
        DuckDuckGoNewsSearch,
        WebBaseContextTool,
        WriteFileAction,
    ],
)

# Admin
admin = Admin(
    planner=TaskPlanner(human_intervene=False),
    memory=Memory(),
    llm=llm,
)

# Assign sub-tasks to workers
admin.assign_workers([researcher, writer, reviewer])

res = admin.run(
    query="Write a blog post.",
    description="sample description.",
)
```
