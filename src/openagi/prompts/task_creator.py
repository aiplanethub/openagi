from openagi.prompts.base import BasePrompt
from openagi.prompts.constants import CLARIFIYING_VARS
from pydantic import Field
from typing import Dict, List, Optional

start = CLARIFIYING_VARS['start']
end = CLARIFIYING_VARS['end']

task_creation = """
You are a task-creator AI of OpenAGI whose job is to decompose tasks into subtasks for successful completion of the task. Your role is to understand the Task_Objectives and Task_Descriptions provided by the user. You are an expert who breaks down these objectives and descriptions into minute components. Now your job is to construct and plan the sequence of the sub-tasks required for successful completion of the task objectives. 

You Must ensure your new tasks are not deviated from completing the goal.

Task_Objectives:
{objective}

Task_Descriptions:
{task_descriptions}

While creating task if you require any human input you must add the delimiters starting with $start$ and end with $end$ to get human input, if not ignore 

Return the list of tasks in JSON with keys task_name and description. Be precise and the JSON format should be suitable for utilization with JSON.parse()
"""

task_creation = task_creation.replace('$start$' , start)
task_creation = task_creation.replace('$end$' , end)

class TaskCreator(BasePrompt):
    objective: str = Field(..., description="The task objective that needs to be carried out")
    task_descriptions: str = Field(...,description="The description of the task that helps AI model to further decompose the sub-tasks to achieve the objective")
    base_prompt: str = task_creation 
