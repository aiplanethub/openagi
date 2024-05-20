from typing import Dict, List, Optional
from pydantic import Field
from openagi.prompts.base import BasePrompt
from openagi.prompts.constants import FAILURE_VARS

start = FAILURE_VARS["start"]
end = FAILURE_VARS["end"]

task_execution = """
You are an expert in detailed task execution. Your primary role is to clearly understand the Task Objective to provide optimal results using the supported actions. Below is a list of tasks that need to be executed:
You can code if needs be. 

All Tasks:
{all_tasks}

You are provided with the current task details from the user.

Current Task:
Name: {current_task_name}
Description: {current_description}

To execute the current task, refer to the details of the Previous Task and the All Tasks provided.

Previous Task:
{previous_task}

Supported Actions:
{supported_actions}

Your task is to understand and return a JSON array with the actions to be executed along with the values for each parameter. Use only the Supported Actions. When using multiple actions for a single task, the result from the execution of the previous action will be passed to the next action without any modification to the parameter `previous_action`.

Task Objective:
{objective}

Output Format:
```json
[
    {
        "cls": {"kls": "<action>", "module": "<module>"},
        "params": {
            "description": "<description>",
            "name": "<name>",
            "filename": "<filename>",
            "file_content": "<file_content>",
            "file_mode": "w"
        }
    }
]
```

If the task cannot be executed using the available actions, return the failure reason within the delimiters $start$ and $end$ as shown below and provide some guidance on what type of generic actions would help in acheiving it.:
$start$ Couldn't execute the `{current_task_name}` task. $end$
```

Return the actions in JSON format as per the output format mentioned above, including the delimiters "json" "", without any other content in the response.
"""


task_execution = task_execution.replace("$start$", start)
task_execution = task_execution.replace("$end$", end)


class TaskExecutor(BasePrompt):
    objective: str = Field(..., description="Final objective")
    all_tasks: List[Dict] = Field(
        ..., description="List of tasks to be executed that was generated earlier"
    )
    current_task_name: str = Field(..., description="Current task name to be executed.")
    current_description: str = Field(..., description="Current task name to be executed.")
    previous_task: Optional[str] = Field(..., description="Previous task, description & result.")
    supported_actions: List[Dict] = Field(
        ...,
        description="Supported Actions that can be used to acheive the current task.",
    )
    base_prompt: str = task_execution
