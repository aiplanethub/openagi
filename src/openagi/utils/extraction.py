import importlib
import json
import logging
import re
from textwrap import dedent
from typing import Dict, List, Optional, Tuple

from openagi.exception import OpenAGIException
from openagi.llms.base import LLMBaseModel


def force_json_output(resp_txt: str, llm: LLMBaseModel):
    """
    Forces the output once the max iterations are reached.
    """
    prompt: str = dedent(
        f"""
                        Below is a JSON block. Please try to provide the output in the format shown below.
                        ```json
                            {"key": "value"}
                        ```
                        the contents between ```json and ``` will be extracted and passed to json.loads() in python to convert it to a dictionary. Make sure that it works when passed else you will be fined.

                        Input:
                        {resp_txt}

                        Output:

    """.strip()
    )
    return llm.run(prompt)


def get_last_json(
    text,
    llm: Optional[LLMBaseModel] = None,
    max_iterations: int = 5,
) -> Optional[Dict]:
    """
    Extracts the last block of text between ```json and ``` markers from a given string.

    Args:
        text (str): The string from which to extract the JSON block.

    Returns:
        dict or None: The last JSON block as a dictionary if found and parsed, otherwise None.
    """
    parsing_failed = False
    if not llm:
        pattern = r"```json(.*?)```"
        matches = re.findall(pattern, text, flags=re.DOTALL)
        try:
            if matches:
                last_json = matches[-1].strip().replace("\n", "")
                return json.loads(last_json)
            else:
                raise OpenAGIException(
                    "The last output is not a valid JSON. Please check the output of the last action."
                )
        except json.JSONDecodeError:
            parsing_failed = True
    if parsing_failed and llm:
        iters = 1
        while iters <= max_iterations:
            logging.info(f"Iteration {iters} to extract JSON from LLM output.")
            try:
                return get_last_json(force_json_output(text, llm), llm, max_iterations)
            except json.JSONDecodeError:
                if iters == max_iterations:
                    raise OpenAGIException(
                        "The last output is not a valid JSON. Please check the output of the last action."
                    )
            iters += 1
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
