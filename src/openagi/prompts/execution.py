from typing import Dict, List, Optional
from pydantic import Field
from openagi.prompts.base import BasePrompt

task_execution = """
You are an AI assistant tasked with processing and executing a sequence of tasks from a JSON input to achieve a specified objective. Your role involves interpreting the tasks, executing them using the provided actions, and managing the workflow to ensure the objective is met.

1. **Task Review and Initialization**: Begin by understanding the final {objective} 

2. **Review the tasks**:Review all tasks in the {all_tasks} list and. Identify the current task to be executed {current_task_name} and {current_description}.

3. **Understand Previous Task**: Understand what happened in the previous task -  {previous_task}. 

4. **Current task**: Return a json with the actions to be executed along the values for the each parameter. In the array of json you return, the value from one action will be passed to another to acheive the current task. 

Execute one step at a time, ensuring to clearly follow each step instruction, state your reasoning.
"""


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
