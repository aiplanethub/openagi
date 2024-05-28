import importlib
import inspect
import json
import re
from typing import Callable, Dict, List, Optional, Tuple, Type
from openagi.prompts.constants import CLARIFIYING_VARS


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


def get_last_json(text, max_retry=2):
    """
    Extracts the last block of text between ```json and ``` markers from a given string,
    with retries if extraction or parsing fails.

    Args:
        text (str): The string from which to extract the JSON block.
        max_retry (int): The maximum number of retries if extraction or parsing fails.

    Returns:
        dict or None: The last JSON block as a dictionary if found and parsed, otherwise None.
    """
    pattern = r"```json(.*?)```"

    for _ in range(max_retry + 1):
        # Find all matches in the text
        matches = re.findall(pattern, text, flags=re.DOTALL)

        if matches:
            try:
                # Attempt to load the last match as JSON
                json_resp = json.loads(matches[-1].strip())
                if not json_resp:
                    continue
                else:
                    return json_resp
            except json.JSONDecodeError:
                # If JSON decoding fails, continue to the next attempt
                continue

    return None


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


def extract_ques_and_task(ques_prompt):
    """
    Extracts question to be asked to the human and remove delimiters from orignal prompt
    """
    start = CLARIFIYING_VARS["start"]
    end = CLARIFIYING_VARS["end"]
    # pattern to find question to be asked to human
    regex = rf"{start}(.*?){end}"

    # Find all matches in the text
    matches = re.findall(regex, ques_prompt)

    # remove <clarify from human>...</clarify from human> part from the prompt
    task = re.sub(regex, "", ques_prompt)
    if not matches:
        return None, None

    question = matches[-1]
    if question and question.strip():
        f"OpenAGI: {question}\nYou: "
    return task, question


def find_last_r_failure_content(text):
    pattern = r"<r_failure>(.*?)</r_failure>"
    matches = list(re.finditer(pattern, text, re.DOTALL))
    if matches:
        last_match = matches[-1]
        return last_match.group(1)
    else:
        return None
