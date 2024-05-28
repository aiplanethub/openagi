import importlib
import json
import re
from typing import Dict, List, Optional, Tuple

from openagi.prompts.constants import CLARIFIYING_VARS


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


def get_act_classes_from_json(json_data) -> List[Tuple[str, Optional[Dict]]]:
    """
    Extracts the Action class names and parameters from a JSON block.

    Args:
        json_data (List[Dict]): A list of dictionaries containing the class and parameter information.

    Returns:
        List[Tuple[type, Optional[Dict]]]: A list of tuples containing the Action class and its initialization parameters.
    """
    actions = []

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
        actions.append((cls, params))

    return actions


def extract_ques_and_task(ques_prompt):
    """
    Extracts the question and task from a given prompt.

    Args:
        ques_prompt (str): The prompt containing the question and task.

    Returns:
        Tuple[str, str]: The task and question extracted from the prompt.
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
    """
    Finds the content of the last <r_failure> tag in the given text.

    Args:
        text (str): The text to search for the <r_failure> tag.

    Returns:
        str or None: The content of the last <r_failure> tag, or None if no matches are found.
    """
    pattern = r"<r_failure>(.*?)</r_failure>"
    matches = list(re.finditer(pattern, text, re.DOTALL))
    if matches:
        last_match = matches[-1]
        return last_match.group(1)
    else:
        return None


def extract_str_variables(template):
    """
    Extracts all variable names from a given template string.

    The function uses a regular expression to find all placeholders within curly braces in the template string, and returns a list of the extracted variable names.

    Args:
        template (str): The template string to extract variables from.

    Returns:
        list[str]: A list of variable names extracted from the template.
    """
    # This regular expression will find all placeholders within curly braces
    pattern = r"\{(\w+)\}"
    matches = re.findall(pattern, template)
    return matches
