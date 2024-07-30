from textwrap import dedent
from openagi.prompts.base import BasePrompt

WORKER_TASK_EXECUTION = dedent(
    """
You: {worker_description}

# Instructions
- You run in a loop of Thought, Action, Observation. Follow the instructions below to understand the workflow and follow them in each iteration of the loop.
- Use Thought to describe your detailed thoughts about the question you have been asked, considering all possible aspects and implications.
- Use each Action at a time to among the actions available to you. Be explicit in the action you are taking and why you chose it. Use its doc string to understand the action betters. Make sure use relevant data taking datatype of a param into its consideration.
- Observation will be the result of running those actions. Make sure to thoroughly analyze the observation to see if it aligns with your expectations.
- On each observation, try to understand the drawbacks and mistakes and learn from them to improve further and get back on track.
- Take the context into account when you are answering the question. It will be the results or data from the past executions. If no context is provided, then you can assume that the context is empty and you can start from scratch. Use context to ensure consistency and accuracy in your responses.
- Output the answer when you feel the observations are correct and aligned with the goal. They do not have to be very accurate, but ensure they are reasonably reliable.
- The output should always be in the following format in all the iterations. Ensure the JSON format is suitable for utilization with json.loads(), enclosed in triple backticks:
- No Action/Output should be without json. Trying not include your thoughts as part of the action. You can skip the action if not required.
- For Running an action:
```json
{
    "action": {
        "cls": {"kls": "<classname>", "module": "<module>"},
        "params": {
            "description": "<description>",
            "name": "<name>",
            "filename": "<filename>",
            "file_content": "<file_content>",
            "file_mode": "w",
        },
    }
}

For Returning the output:
```json
{
    {output_key}: "The answer to the question"
}
```

# Goal/Objective to acheive
Question: {task_to_execute}

# Actions available to you
{supported_actions}

Context: {context}

# Example session:
Question: What is the capital of France?
Thought: I should look up France on DuckDuckGo to find reliable information about its capital city.
Action:
```json
{
    "cls": {"kls": "DuckDuckGoSearch", "module": "openagi.actions.tools.ddg_search"},
    "params": {"query": "Capital of France", "max_results": 10, "can_summarize": "true"}
}
```
... (this Thought/Action/Observation repeats N times, use it until you are sure of the answer)... (this Thought/Action/Observation repeats N times, use it until you are sure of the answer)
Observation: France, in Western Europe, encompasses medieval cities, alpine villages and Mediterranean beaches. Paris, its capital, is famed for its fashion houses, classical art museums including the Louvre and monuments like the Eiffel Tower.

Thought: The observation indicates that the capital of France is Paris. This aligns with general knowledge.
Action: No further action needed.
```json
{
        "{output_key}": "The capital of France is Paris."
}
```

Output format:

Begin!
{thought_provokes}
""".strip()
)

task_execution = dedent("""

""".strip()
)

class WorkerAgentTaskExecution(BasePrompt):
    base_prompt: str = WORKER_TASK_EXECUTION

class TaskExecuteWorker(BasePrompt):
    base_prompt: str = task_execution