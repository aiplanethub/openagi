import importlib
import json
import logging
import re
from textwrap import dedent
from typing import Dict, List, Optional, Tuple

from openagi.exception import OpenAGIException
from openagi.llms.base import LLMBaseModel


def force_json_output(resp_txt: str, llm):
    """
    Forces the output once the max iterations are reached.
    """
    #prompt = dedent(
    #    """
    #    Below is a JSON block. Please try to provide the output in the format shown below only
    #    ```json
    #        {"key": "value"}
    #    ```
    #    the contents between ```json and ``` will be extracted and passed to json.loads() in python to convert it to a dictionary. Make sure that it works when passed else you will be fined. If its already in the correct format, then you can return the same output in the expected output format.
    #    Input:
    #    {resp_txt}
    #    Output:
    #    """
    #).strip()

    prompt = dedent(
        """
        Your task is to process the input JSON and provide a valid JSON output. Follow these instructions carefully:
        1. The output must be enclosed in a code block using triple backticks and the 'json' language identifier, like this:
        ```json
         {"key": "value"}
        ```
        2. The JSON inside the code block must be valid and parseable by Python's json.loads() function.
        3. Ensure there are no extra spaces, newlines, or characters outside the JSON object within the code block.
        4. If the input is already in the correct format, reproduce it exactly in the output format specified above.
        5. Do not include any explanations, comments, or additional text in your response. The output needs be in JSON only. 
        6. Verify your output carefully before submitting. Incorrect responses will result in penalties.
        
        Input: {resp_txt}
        Output:
        """
    ).strip()

    prompt = prompt.replace("{resp_txt}", resp_txt)
    return llm.run(prompt)


def get_last_json(
    text: str, llm: Optional[LLMBaseModel] = None, max_iterations: int = 5
) -> Optional[Dict]:
    """
    Extracts the last block of text between ```json and ``` markers from a given string.

    Args:
        text (str): The string from which to extract the JSON block.
        llm (Optional[LLMBaseModel]): The language model instance to use for reformatting.
        max_iterations (int): Maximum number of iterations to try reformatting.

    Returns:
        dict or None: The last JSON block as a dictionary if found and parsed, otherwise None.
    """
    pattern = r"```json(.*?)```"
    matches = re.findall(pattern, text, flags=re.DOTALL)
    if matches:
        last_json = matches[-1].strip().replace("\n", "")
        try:
            return json.loads(last_json)
        except json.JSONDecodeError:
            logging.error("JSON not extracted. Trying again.", exc_info=True)
            pass

    if llm:
        for iteration in range(1, max_iterations + 1):
            logging.info(f"Iteration {iteration} to extract JSON from LLM output.")
            try:
                text = force_json_output(text, llm)
                matches = re.findall(pattern, text, flags=re.DOTALL)
                if matches:
                    last_json = matches[-1].strip().replace("\n", "")
                    json_resp = json.loads(last_json)
                    logging.info("JSON extracted successfully.")
                    return json_resp
            except json.JSONDecodeError:
                logging.error("JSON not extracted. Trying again.", exc_info=True)
                continue
            if iteration == max_iterations:
                raise OpenAGIException(
                    "The last output is not a valid JSON. Please check the output of the last action."
                )
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
