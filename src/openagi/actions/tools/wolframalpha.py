# wolframalpha_tool.py

from openagi.actions.base import Tool
from openagi.config import get_config
import wolframalpha

class WolframAlphaTool(Tool):
    """
    A tool for querying Wolfram Alpha.
    """

    def __init__(self, name="WolframAlpha", description="A tool for querying Wolfram Alpha."):
        super().__init__(name, description)

    def _execute(self, query: str):
        # Get Wolfram Alpha API key from user input
        config = get_config()
        app_id = config.get("wolframalpha", "app_id")

        # Create a Wolfram Alpha client
        client = wolframalpha.Client(app_id)

        # Query Wolfram Alpha
        try:
            res = client.query(query)
            # Extract and return the result
            return next(res.results).text
        except Exception as e:
            return f"Error querying Wolfram Alpha: {e}"