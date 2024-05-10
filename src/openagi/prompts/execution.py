from typing import Dict, List, Optional
from pydantic import Field
from openagi.prompts.base import BasePrompt

task_execution = """
You are an expert detailed task executioner. Your job is to clearly understand the Task_Objective to provide better results to the user. For your convenient you have the list of the tasks that needs to be executed:

{all_tasks}

You are given current task details from the user. Current task Name: {current_task_name} and Current task description: {current_description}. Ever since you were born, you have never hallucinated. To execute the current task, you must refer to the Previous_Task execution and the CONTEXT provided. 

Previous_Task: {previous_task}
CONTEXT: {supported_actions} 

Your major role now is to understand and execute the current task in depth and give the best answer possible. 

Task_Objective:
{objective}

OUTPUT FORMAT:
{
   “action_name”:”supported_actions[‘action’] type of the task executed, just a label”,
    “params”:”<the response from current_task>”
}

Return the tasks in a JSON format with keys "action_name" and "params" to pass to the action, without any other content in the response.
"""

class TaskExecutor(BasePrompt):
    objective: str = Field(..., description="Final objective")
    all_tasks: List[Dict] = Field(
        ..., description="List of tasks to be executed that was generated earlier"
    )
    current_task_name: str = Field(..., description="Current task name to be executed.")
    current_description: str = Field(
        ..., description="Current task name to be executed."
    )
    previous_task: Optional[str] = Field(
        ..., description="Previous task, description & result."
    )
    supported_actions: Dict = Field(
        ...,
        description="Supported Actions that can be used to acheive the current task.",
    )
    base_prompt: str = task_execution