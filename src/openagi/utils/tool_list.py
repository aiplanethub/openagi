import inspect
from openagi.actions.tools import (
    ddg_search,
    document_loader,
    serp_search,
    serper_search,
    webloader,
    youtubesearch,
    exasearch,
)
from openagi.actions import files, formatter, human_input, compressor, console, obs_rag

# List of modules to inspect
modules = [
    document_loader,
    ddg_search,
    serp_search,
    serper_search,
    webloader,
    youtubesearch,
    exasearch,
    files,
    formatter,
    human_input,
    compressor,
    console,
    obs_rag
]


def get_tool_list():
    """
    Dynamically retrieves all classes from the specified modules and returns them in a list.
    Only includes classes that are subclasses of a specific base class (if needed).

    :return: List of class objects from the specified modules.
    """
    class_list = []

    for module in modules:
        # Inspect the module for classes
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Optionally, filter by a specific base class, e.g., BaseAction
            # if issubclass(obj, BaseAction) and obj is not BaseAction:
            class_list.append(obj)  # Append the class itself (not an instance)

    return class_list

"""
# Example usage
tools = get_tool_list()
for tool in tools:
    print(tool.__name__)  # Print the name of each class
"""