import importlib
import json
import logging
import re
from typing import Dict, List, Optional, Tuple

from openagi.exception import OpenAGIException
from openagi.llms.base import LLMBaseModel


def force_json_output(resp_txt: str, llm) -> str:
    """
    Forces proper JSON output format in first attempt.
    """
    prompt = """
        You are a JSON formatting expert. Your task is to process the input and provide a valid JSON output.
        
        FOLLOW THESE INSTRUCTIONS to convert:
        - Output must be ONLY a JSON object wrapped in ```json code block
        - Do not include any explanations, comments, or additional text in your response. The output needs be in JSON only. 
        
        Convert this INPUT to proper JSON:
        INPUT: {resp_txt}
        Output only the JSON:
        """.strip()

    prompt = prompt.replace("{resp_txt}", resp_txt)
    return llm.run(prompt)


def get_last_json(
    text: str, llm: Optional[LLMBaseModel] = None, max_iterations: int = 5
) -> Optional[Dict]:
    """
    Extracts valid JSON from text with improved reliability.
    """
    # More precise JSON block pattern
    pattern = r"```json\s*(\{[\s\S]*?\})\s*```"
    matches = re.findall(pattern, text, re.MULTILINE)
    
    if matches:
        try:
            last_json = matches[-1].strip()
            last_json = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', last_json)
            last_json = re.sub(r'\s+', ' ', last_json)
            return json.loads(last_json)
        except json.JSONDecodeError as e:
            logging.error(f"JSON parsing failed: {str(e)}", exc_info=True)
            if llm:
                text = force_json_output(last_json, llm)
                return get_last_json(text, None, max_iterations)
    
    if llm:
        for iteration in range(1, max_iterations + 1):
            try:
                text = force_json_output(text, llm)
                return get_last_json(text, None, max_iterations)
            except Exception as e:
                logging.error(f"Attempt {iteration} failed: {str(e)}", exc_info=True)
                if iteration == max_iterations:
                    raise OpenAGIException(
                        f"Failed to extract valid JSON after {max_iterations} attempts. Last error: {str(e)}"
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
