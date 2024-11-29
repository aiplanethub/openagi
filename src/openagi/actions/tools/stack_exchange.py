# stack_exchange_tool.py

from openagi.actions.base import Tool
from stackapi import StackAPI

class StackExchangeTool(Tool):
    """
    A tool for querying Stack Exchange sites.
    """

    def __init__(self, name="StackExchange", description="A tool for querying Stack Exchange sites."):
        super().__init__(name, description)

    def _execute(self, query: str):
        # Create a StackAPI client
        SITE = StackAPI('stackoverflow')  # Replace with desired Stack Exchange site

        # Query Stack Exchange
        try:
            questions = SITE.fetch('questions', sort='votes', tagged=query)
            # Extract and return the top answer
            top_answer = questions['items'][0]['answers'][0]['body']
            return top_answer
        except Exception as e:
            return f"Error querying Stack Exchange: {e}"