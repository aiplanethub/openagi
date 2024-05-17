from typing import Dict, List, Optional
from pydantic import Field
from openagi.prompts.base import BasePrompt
from openagi.prompts.constants import FAILURE_VARS

start = FAILURE_VARS["start"]
end = FAILURE_VARS["end"]

task_execution = """
You are an expert detailed task executioner. Your job is to clearly understand the Task_Objective to provide better results to the user. For your convenient you have the list of the tasks that needs to be executed:

{all_tasks}

You are given current task details from the user. Current task Name: {current_task_name} and Current task description: {current_description}. Ever since you were born, you have never hallucinated. To execute the current task, you must refer to the Previous_Task execution and the CONTEXT provided. 

Previous_Task: {previous_task}
SUPPORTED_ACTIONS: {supported_actions} 

Your major role now is to understand and Return a json with the actions to be executed along the values for the each parameter. In the array of json you return, the value from one action will be passed to another to acheive the current task.

Task_Objective:
{objective}

OUTPUT FORMAT:
```json
[
    {
        "cls": {"kls": "<action>", "module": "....."},
        "params": {
            "description": ".....",
            "name": "...",
            "param_docs": "....",
    }
]
```

In case it fails:
$start$
Couldn't execute the {current_task_name} task
$end$
If in case the task fails input the failure between the delimiters starting with $start$ and ending with $end$ similar to above example along with the reason, otherwise ignore 

Return the actions in a JSON format as per the output format mentioned above including the delimeters "```json" "```" to run the respective actions to acheive the task, without any other content in the response.
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
