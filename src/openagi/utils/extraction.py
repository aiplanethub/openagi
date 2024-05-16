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


def get_last_json(text):
    """
    Extracts the last block of text between ```json and ``` markers from a given string.

    Args:
        text (str): The string from which to extract the JSON block.

    Returns:
        str or None: The last JSON block including the delimiters if found, otherwise None.
    """
    # Pattern to find the last occurrence of content between ```json and ```
    pattern = r"```json(.*?)```"

    # Find all matches in the text
    matches = re.findall(pattern, text, flags=re.DOTALL)

    # Return the last match if any
    try:
        if matches:
            return json.loads(matches[-1])
    except json.JSONDecodeError:
        return None
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
    '''
    Extracts question to be asked to the human and remove delimiters from orignal prompt
    '''
    start = {CLARIFIYING_VARS['start']}
    end = {CLARIFIYING_VARS['end']}
    # pattern to find question to be asked to human 
    regex = fr"{start}(.*?){end}"

    # Find all matches in the text
    matches = re.findall(regex, ques_prompt) 

    #remove <clarify from human>...</clarify from human> part from the prompt
    task = re.sub(regex , '' , ques_prompt)
  
    return task , matches[-1]


llm_response = '[\n    {"task_name": "Design the Chessboard", "description": "Create a 8x8 grid to represent the chessboard."},\n    {"task_name": "Create Chess Pieces", "description": "Define classes for each type of chess pieces including their movements."},\n    {"task_name": "Implement Chess Rules", "description": "Implement the rules for each chess piece and their valid movements."},\n    {"task_name": "Create Player Classes", "description": "Create classes for players to control the pieces and make moves."},\n    {"task_name": "Design Game Interface", "description": "Design a simple text-based user interface for players to interact with the game."},\n    {"task_name": "Implement Game Loop", "description": "Create the main game loop which will handle the game process, turns and check for game over conditions."},\n    {"task_name": "Check Mate and Stale Mate Implementation", "description": "Implement the conditions to check for Checkmate and Stalemate."},\n    {"task_name": "Pawn Promotion Rule", "description": "Implement the rule for pawn promotion when it reaches the other end of the board."},\n    {"task_name": "En Passant Rule Implementation", "description": "Implement the \'En Passant\' rule that is a special pawn capture move in chess."},\n    {"task_name": "Castling Rule Implementation", "description": "Implement the \'Castling\' rule that involves a player\'s king and one of their rooks."},\n    {"task_name": "Implement Game Saving and Loading", "description": "Add functionality to save and load game progress."},\n    {"task_name": "Test the Game", "description": "Play test the game to ensure all rules are implemented correctly and the game is working as expected."}\n]'

# print(get_last_json(llm_response))
