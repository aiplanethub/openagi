from typing import Dict, List, Optional
from pydantic import Field
from openagi.prompts.base import BasePrompt
from openagi.prompts.constants import FAILURE_VARS

start = FAILURE_VARS["start"]
end = FAILURE_VARS["end"]

task_execution = """
Imagine multiple different experts who knows very well to divide the task into sub-tasks for the given objective: {objective} \
As an expert, you must understand the given CURRENT_TASK by understanding PREVIOUS_TASK and make appropriate decisions \
You should now execute CURRENT_TASK by understanding CURRENT_TASK_DESCRIPTION in detail \
You must understand both PREVIOUS_TASK and CURRENT_TASK and use the relevant requirements from the ACTIONS and makes sure to pass relevant value to the action params. You can use only one action per task. You cannot use any other modules apart from the actions supported below. \
ACTIONS contains the required details on what tools must be used and how should they be used, make sure to use the mentioned supported actions only. You can ignore few params like `name`, `description` from including in the params. \
Remember you are an expert, you never lie and never hallucinate, you need to execute the task with 100 percent accuracy \

PREVIOUS_TASK: {previous_task}
CURRENT_TASK: {current_task_name}
CURRENT_TASK_DESCRIPTION: {current_description}
ACTIONS: {supported_actions} 

As an expert you must handle the possible edge cases:
1. If any task is related to storing results, you don't have to create any task for storing the results, as results returned after executing all the actions in each task will be stored \
2. In case it fails: $start$ Couldn't execute the {current_task_name} task $end$
If in case the task fails input the failure between the delimiters starting with $start$ and ending with $end$ similar to above example, otherwise ignore 

The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":

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

"""
# In order to retreive them(previous task results of the current objective) just use ```MemoryRagAction```.


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
