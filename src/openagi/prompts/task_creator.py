from typing import Dict, List
from openagi.prompts.base import BasePrompt
from openagi.prompts.constants import CLARIFIYING_VARS
from pydantic import Field

start = CLARIFIYING_VARS["start"]
end = CLARIFIYING_VARS["end"]

task_creation = """
You are a task-creator AI for OpenAGI. Your job is to decompose tasks into the smallest possible subtasks to ensure successful completion in an autonomous, programmatic approach using the available actions that work as a tool. Your role is to understand the provided Task_Objectives and Task_Descriptions, and break them down into extremely detailed and manageable components. Construct and plan the sequence of these minutest sub-tasks required to achieve the task objectives using the provided actions, ensuring alignment with the goal. If instructions are not followed, you and I both might be sued.

Ensure your new tasks are aligned with the overall goal and can be understood clearly when shared with another AI like similar to you to acheive the sub task. You need to understand the parameters of each of the supported actions when using them.

Task_Objectives:
{objective}

Task_Descriptions:
{task_descriptions}

SUPPORTED_ACTIONS:
{supported_actions}

OUTPUT FORMAT:
```json
[
    {
        "task_name": "...",
        "description": "..."
    }
]
```

Return the tasks in JSON format with the keys "task_name" and "description". Ensure the JSON format is suitable for utilization with JSON.parse(), enclosed in triple backticks ```json ```.
Results returned after executing all the actions in each task will be stored, so you dont have to create any task for storing the results. You can retreive them(previous task results of the current objective) using `MemoryRagAction`.
"""
# If human input is required to curate the task, include the delimiters $start$ and $end$ to request human input. If not, ignore this step.

task_creation = task_creation.replace("$start$", start)
task_creation = task_creation.replace("$end$", end)


class TaskCreator(BasePrompt):
    objective: str = Field(..., description="The task objective that needs to be carried out")
    task_descriptions: str = Field(
        ...,
        description="The description of the task that helps AI model to further decompose the sub-tasks to achieve the objective",
    )
    supported_actions: List[Dict] = Field(
        ...,
        description="Supported Actions that can be used to acheive a task.",
    )
    base_prompt: str = task_creation
