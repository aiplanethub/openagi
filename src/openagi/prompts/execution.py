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

If the task fails, return the failure reason within the delimiters $start$ and $end$ as shown below:
$start$
Couldn't execute the {current_task_name} task. Reason: <add the reason here.>
$end$

The action class is designed & executed this way:

### Code Example
```python
class BaseAction(BaseModel):
    "Base Actions class to be inherited by other actions, providing basic functionality and structure."

    name: str = Field(default="BaseAction", description="Name of the action.")
    description: str = Field(
        default="Base Action class to be used by other actions that get created.",
        description="Description of the action.",
    )
    previous_action: Optional[Any] = Field(
        default=None,
        description="Observation or Result of the previous action that might needed to run the current action.",
    )

    def execute(self):
        "Executes the action"
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def cls_doc(cls):
        return {
            "cls": {
                "kls": cls.__name__,
                "module": cls.__module__,
            },
            "params": {
                field_name: field.description for field_name, field in cls.model_fields.items()
            },
        }

act = BaseAction(**params)
res = act.execute()

```
Return the actions in JSON format as per the output format mentioned above, including the delimiters "json" "", without any other content in the response.


### Debugging Steps:
1. Ensure Variables are Correctly Populated: Verify that `{current_task_name}`, `{current_description}`, `{previous_task}`, `{all_tasks}`, `{supported_actions}`, and `{objective}` are correctly populated.
2. Validate JSON Structure: Make sure the AI returns the correct JSON structure, especially the `file_content` parameter for the `WriteFileAction`.
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
