from openagi.prompts.base import BasePrompt

task_creation = """
You are a task creation AI that uses the result of an execution agent
to create new tasks with the following objective: {objective}
Based on the result, create new tasks to be completed
by the AI system that do not overlap with incomplete tasks.
Task must be answered in english.
Consider the ultimate objective of your team.
Return the tasks in a json with keys "task_name" and "description", without any other content in the response;
"""


class TaskCreator(BasePrompt):
    param_docs: dict = {
        "objective": "The objective to be achieved.",
        "result": "",
        "incomplete_tasks": "",
        "previous_tasks": "...",
    }
    base_prompt: str = task_creation