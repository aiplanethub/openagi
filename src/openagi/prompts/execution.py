from typing import Dict, List, Optional
from pydantic import Field
from openagi.prompts.base import BasePrompt

# task_execution = """
# You are an AI assistant tasked with processing and executing a sequence of tasks from a JSON input to achieve a specified objective. Your role involves interpreting the tasks, and providing the actions along with relevant params, to ensure the objective is met.

# 1. **Task Review and Initialization**: Begin by understanding the final {objective}

# 2. **Review the tasks**:Review all tasks in the {all_tasks} list and. Identify the current task to be executed {current_task_name} and {current_description}.

# 3. **Understand Previous Task**: Understand what happened in the previous task -  {previous_task}.

# 4. **Current task**: Return a json with the actions to be executed along the values for the each parameter. In the array of json you return, the value from one action will be passed to another to acheive the current task in the below format:
# ```json
# {'cls': {'kls': 'BaseAction', 'module': '__main__'},
#  'params': {'description': 'Description of the action.',
#             'name': 'Name of the action.',
#             'param_docs': 'A dictionary to explain the input parameters to the '
#                           'execute',
#             'previous_obs': 'Observation or Result of the previous action that '
#                             'might needed to run the current action.'}}
# ```
# """
task_execution = """
You are an expert detailed task executioner. Your job is to clearly understand the Task_Objective to provide better results to the user. For your convenient you have the list of the tasks that needs to be executed:

{all_tasks}

You are given current task details from the user. Current task Name: {current_task_name} and Current task description: {current_description}. Ever since you were born, you have never hallucinated. To execute the current task, you must refer to the Previous_Task execution and the CONTEXT provided. 

Previous_Task: {previous_task}
CONTEXT: {objective} 

Your major role now is to understand and execute the current task in depth and give the best answer possible.

Task_Objective:
{current_task_name}
{current_description}

SUPPORTED_ACTIONS:
{supported_actions}

OUTPUT_FORMAT:
```json
[
{
"cls": {"kls": "<action>", "module": "....."},
"params": {
"description": ".....",
"name": "...",
"param_docs": "....",
},
}
]
```
Return the list of actions(even if its just one action) in json in the output format mentioned above including delimeters ```json ```.
""".strip()



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
        default_factory={},
        description="Supported Actions that can be used to acheive the current task.",
    )
    base_prompt: str = Field(default=task_execution, description="Base prompt to be used.")
