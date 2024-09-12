from textwrap import dedent
from openagi.prompts.base import BasePrompt

ltm_prompt = dedent("""
Previously asked query: {query}
Previously given description: {description}
Previously constructed plan: {plan}
Feedback on the plan by human user: {plan_feedback}
Previously generated answer: {answer}
Feedback on the answer by human user: {ans_feedback}
""".strip())


class LTMFormatPrompt(BasePrompt):
    base_prompt: str = ltm_prompt