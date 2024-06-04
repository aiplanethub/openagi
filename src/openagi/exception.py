class OpenAGIException(Exception):
    ...


class ExecutionFailureException(Exception):
    """Task Execution Failed"""


class LLMResponseError(OpenAGIException):
    """No useful Response found"""
