import logging
from openagi.actions.base import BaseAction


def run_action(action_cls: str, memory, llm, **kwargs):
    """
    Runs the specified action with the provided keyword arguments.

    Args:
        action_cls (str): The class name of the action to be executed.
        **kwargs: Keyword arguments to be passed to the action class constructor.

    Returns:
        The result of executing the action.
    """
    logging.info(f"Running Action - {str(action_cls)}")
    kwargs["memory"] = memory
    kwargs["llm"] = llm
    action: BaseAction = action_cls(**kwargs)  # Create an instance with provided kwargs
    res = action.execute()
    return res
