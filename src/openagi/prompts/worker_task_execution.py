from textwrap import dedent

from openagi.prompts.base import BasePrompt

WORKER_TASK_EXECUTION = dedent(
    """
You: {worker_description}
You run in a loop of Thought, Action, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.
Once you feel the observations are correct and aligned with the goal to the best, you return the Answer. It should be of the form:
```json
{
    {output_key}: "The answer to the question",
}
```
Context: {context}
Take the context into account when you are answering the question. It will be the results or data from the past executions. If no context is provided, then you can assume that the context is empty and you can start from scratch.

Example session:

Question: What is the capital of France?
Thought: I should look up France on DuckDuckGo
Action:
```json
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
```

You will be called again with this:
Observation: France is a country. The capital is Paris.

You then output:
{
        {output_key}: "The capital of France is Paris."
}

Note
  - You can use any one of supported_actions i.e., One Action at a time.
  - On each observation, try to understand the drawbacks and mistakes and learn from them to improve the thought.

Output format:
When you want to run an action, return the below json alone without anything else. Ensure the JSON format is suitable for utilization with `JSON.parse()`, enclosed in triple backticks.:
```json
{
    "action": {
        "cls": {"kls": "<action>", "module": "<module>"},
        "params": {
            "description": "<description>",
            "name": "<name>",
            "filename": "<filename>",
            "file_content": "<file_content>",
            "file_mode": "w",
        },
    }
}
```

if you have the answer, return the below json alone without anything else. Ensure the JSON format is suitable for utilization with `JSON.parse()`, enclosed in triple backticks.:
```json
{
        {output_key}: "<answer>"
}
```


Begin!

{thought_provokes}

""".strip()
)


class WorkerAgentTaskExecution(BasePrompt):
    base_prompt: str = WORKER_TASK_EXECUTION
