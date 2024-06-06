from textwrap import dedent

from openagi.prompts.base import BasePrompt

summarizer_prompt = dedent(
    """AI, your task is to generate a concise summary of the previous interactions if the assisstant.
The interactions are as follows:

{past_messages}

This summary should encapsulate the main points of all the Thoughts, Actions and Observations, highlighting the key issues discussed, decisions made, and any actions assigned.
It should serve as a recap of the past interaction, providing a clear understanding of the conversation's context and outcomes.
Do not return anything else other than the summary. Ensure to include all the important points from the Observations.
{instructions}
""".strip()
)


class SummarizerPrompt(BasePrompt):
    base_prompt: str = summarizer_prompt
