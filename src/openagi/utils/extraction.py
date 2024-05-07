import importlib
import inspect
import json
from typing import Callable, Dict, List, Optional, Tuple, Type


def extract_func_params(func: Callable):
    funcs_signature = inspect.signature(func)
    funcs_params = funcs_signature.parameters
    return {
        name: param.default != inspect.Parameter.empty
        for name, param in funcs_params.items()
        if name != "self"  # noqa: E501
    }  # {"<attr_name>":"<default_is_empty>"}


def extract_class_init_attrs(clss: Type):
    return extract_func_params(clss.__init__)


def extract_cls_method_params(clss: Type, method: Callable):
    return extract_func_params(getattr(clss, method))


def get_last_json(string):
    """
    Extracts the last JSON element from a string that might contain multiple JSON objects by iterating from the end.

    Args:
        string: The string containing potential JSON data.

    Returns:
        The last JSON element as a parsed object, or None if no valid JSON is found.
    """
    # Brute force approach: try to parse each substring from the back
    for i in range(len(string), 0, -1):
        for j in range(0, i):
            substring = string[j:i]
            try:
                # Try to parse the substring as JSON
                potential_json = json.loads(substring)
                # If parsing is successful, return the JSON object
                return potential_json
            except json.JSONDecodeError:
                continue  # If not successful, continue trying other substrings

    return None  # Return None if no valid JSON is found after all attempts


def get_classes_from_json(json_data) -> List[Tuple[str, Optional[Dict]]]:
    instances = []

    for item in json_data:
        # Extracting module and class name
        module_name = item["cls"]["module"]
        class_name = item["cls"]["kls"]

        # Dynamically import the module
        module = importlib.import_module(module_name)

        # Get the class from the module
        cls = getattr(module, class_name)

        # Extracting parameters for class initialization
        params = item["params"]

        # Storing the instance in the list
        instances.append((cls, params))

    return instances
