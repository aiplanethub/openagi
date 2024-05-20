from typing import Dict, List
from openagi.prompts.base import BasePrompt
from openagi.prompts.constants import CLARIFIYING_VARS
from pydantic import Field

start = CLARIFIYING_VARS["start"]
end = CLARIFIYING_VARS["end"]

task_creation = """
You are a task-creator AI for OpenAGI. Your job is to decompose tasks into the smallest possible subtasks to ensure successful completion in an autonomous, programmatic approach using the available actions that work as a tool. Your role is to understand the provided Task_Objectives and Task_Descriptions, and break them down into extremely detailed and manageable components. Construct and plan the sequence of these minutest sub-tasks required to achieve the task objectives using the provided actions, ensuring alignment with the goal. If instructions are not followed, you and I both might be sued.

Ensure your new tasks are aligned with the overall goal and can be understood clearly when shared with another AI like similar to you to acheive the sub task. You need to understand the parameters of each of the supported actions when using them.

Task_Objectives:
{objective}

Task_Descriptions:
{task_descriptions}

SUPPORTED_ACTIONS:
{supported_actions}

OUTPUT FORMAT:
```json
[
    {
        "task_name": "...",
        "description": "..."
    }
]
```

If human input is required for any task, include the delimiters $start$ and $end$ to request human input. If not, ignore this step.

Return the tasks in JSON format with the keys "task_name" and "description". Ensure the JSON format is suitable for utilization with JSON.parse(), enclosed in triple backticks json .


### Example Usage

Given the following input:

Task_Objectives:
Create a fully functional chess game.

Task_Descriptions:
1. Set up the initial chessboard.
2. Implement piece movement rules.
3. Add special moves (castling, en passant, pawn promotion).
4. Handle game states (check, checkmate, stalemate).
5. Implement player turns.
6. Test the game.
7. Debug and refine the game.

SUPPORTED_ACTIONS:
[
    {"cls": {"kls": "CreateFileAction", "module": "openagi.actions.files"}, "params": {"name": "Name of the action.", "description": "Description of the action.", "filename": "Name of the file along with the directory.", "file_content": "String content of the file to insert", "file_mode": "File mode to open the file with while using python's open() func."}},
    {"cls": {"kls": "WriteFileAction", "module": "openagi.actions.files"}, "params": {"name": "Name of the action.", "description": "Description of the action.", "filename": "Name of the file along with the directory.", "file_content": "String content of the file to insert", "file_mode": "File mode to open the file with while using python's open() func."}}
]

OUTPUT FORMAT:
```json
[
    {
        "task_name": "...",
        "description": "..."
    }
]
```

### Example Output
```json
[
    {
        "task_name": "Create chess.py file",
        "description": "Using the 'CreateFileAction' from the 'openagi.actions.files' module, create a new Python file named chess.py. This is where we will write all the code needed for the chess game."
    },
    {
        "task_name": "Define chessboard setup",
        "description": "Using the 'WriteFileAction' from the 'openagi.actions.files' module, write the initial setup of the chessboard in the chess.py file. This will include the setup of all pieces at their initial positions as per the standard rules of chess."
    },
    {
        "task_name": "Define piece movements",
        "description": "Using the 'WriteFileAction' from the 'openagi.actions.files' module, write the rules for movement of each type of piece in the chess.py file. This will include the rules for pawn, knight, bishop, rook, queen, and king."
    },
    {
        "task_name": "Define special moves",
        "description": "Using the 'WriteFileAction' from the 'openagi.actions.files' module, write the rules for special moves in the chess.py file. This includes castling, en passant, and pawn promotion."
    },
    {
        "task_name": "Define game state conditions",
        "description": "Using the 'WriteFileAction' from the 'openagi.actions.files' module, write the conditions for various game states in the chess.py file. This includes check, checkmate, and stalemate."
    },
    {
        "task_name": "Implement player turns",
        "description": "Using the 'WriteFileAction' from the 'openagi.actions.files' module, write the code to handle player turns in the chess.py file. This includes alternating between the two players and ensuring that a player can only move their own pieces."
    },
    {
        "task_name": "Test the game",
        "description": "Manually test the game to ensure everything is working as expected. Make sure that all piece movements, special moves, and game state conditions are correctly implemented and that the game correctly alternates between the two players."
    },
    {
        "task_name": "Debug and refine the game",
        "description": "If any issues were found during testing, use the 'WriteFileAction' from the 'openagi.actions.files' module to debug and refine the game code in the chess.py file. Continue to test and refine until the game is fully functional and bug-free."
    }
]
```
"""

task_creation = task_creation.replace("$start$", start)
task_creation = task_creation.replace("$end$", end)


class TaskCreator(BasePrompt):
    objective: str = Field(..., description="The task objective that needs to be carried out")
    task_descriptions: str = Field(
        ...,
        description="The description of the task that helps AI model to further decompose the sub-tasks to achieve the objective",
    )
    supported_actions: List[Dict] = Field(
        ...,
        description="Supported Actions that can be used to acheive a task.",
    )
    base_prompt: str = task_creation
