# 👨‍💼 Admin

## What is an Admin?

Imagine Admin as the master task executor who is responsible for all the major configurations for the execution. From planning of tasks to execution, and defining the brain which is what LLM to use and whether or not to use memory.&#x20;

Admin is the decision-maker that understand the specifications of tasks and execute them in a more human-like manner.&#x20;

## Attributes

The `Admin` class in the `openagi` library is a central component designed to manage and orchestrate various functionalities within the framework. Below is a detailed explanation of its components, attributes, and usage.

The `Admin` class in the OpenAGI framework can be considered an Agent.&#x20;



<table><thead><tr><th width="179">Attribute</th><th width="179">Optional Parameter</th><th>Description</th></tr></thead><tbody><tr><td><strong>planner</strong></td><td></td><td>Help us define the type of planner we can use to decompose the given task into sub tasks.</td></tr><tr><td><strong>llm</strong></td><td></td><td>Users can provide an LLM of their choosing, or use the default one.</td></tr><tr><td><strong>memory</strong></td><td>Yes</td><td>Users can initiate Admin memory, to recall and remember the task and it's response</td></tr><tr><td><strong>actions</strong></td><td></td><td>Admin can be given access to various actions to perform it's task, such as SearchAction, Github Action, etc.</td></tr><tr><td><strong>output_format</strong></td><td>Yes</td><td>Users can define the output format as either "markdown" or "raw_text"  </td></tr><tr><td><strong>max_steps</strong></td><td>Yes</td><td>The number of iterations admin can perform to obtain appropriate output.</td></tr></tbody></table>

### Code Snippet

<pre class="language-python"><code class="lang-python">from openagi.agent import Admin

<strong>admin = Admin(
</strong>    llm=llm,
    actions=actions,
    planner=planner,
)
</code></pre>

Below we have shown how one can initiate and run a simple admin query.

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

# declare the Admin
admin = Admin(
    llm=llm,
    actions=[DuckDuckGoSearch],
    planner=TaskPlanner(human_intervene=False),
    memory=Memory(),
    output_type=OutputFormat.markdown, # Defaults to markdown
)

# execute the task
res = admin.run(
            query="sample query",
            description="sample description",
            )
```
