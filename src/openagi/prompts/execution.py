from typing import Dict, List, Optional
from pydantic import Field
from openagi.prompts.base import BasePrompt

task_execution = """
You are an AI assistant tasked with processing and executing a sequence of tasks from a JSON input to achieve a specified objective. Your role involves interpreting the tasks, executing them using the provided actions, and managing the workflow to ensure the objective is met.

1. **Task Review and Initialization**: Begin by understanding the final {objective} 

2. **Review the tasks**:Review all tasks in the {all_tasks} list and. Identify the current task to be executed {current_task_name} and {current_description}.

3. **Understand Previous Task**: Understand what happened in the previous task -  {previous_task}. 

4. **Current task**: Return a json with the actions to be executed along the values for the each parameter. In the array of json you return, the value from one action will be passed to another to acheive the current task. 

Execute one step at a time, ensuring to clearly follow each step instruction, state your reasoning.
"""


class TaskExecutor(BasePrompt):
    objective: str = Field(..., description="Final objective")
    all_tasks: List[Dict] = Field(
        ..., description="List of tasks to be executed that was generated earlier"
    )
    current_task_name: str = Field(..., description="Current task name to be executed.")
    current_description: str = Field(
        ..., description="Current task name to be executed."
    )
    previous_task: Optional[str] = Field(
        ..., description="Previous task, description & result."
    )
    supported_actions: Dict = Field(
        ...,
        description="Supported Actions that can be used to acheive the current task.",
    )
    base_prompt: str = task_execution


"""
You are an AI assistant tasked with processing and giving a solution with a sequence of tasks from a JSON input to achieve a specified objective. Your role involves interpreting the tasks, specifying actions to be leveraged to acheive the task and managing the workflow to ensure the objective is met.

1. **Task Review and Initialization**: Begin by understanding the final Create a json game in pythn  

2. **Review the tasks**:Review all tasks in the [
  {
    "task_name": "Define Chess Pieces",
    "description": "Create classes or functions to define the properties and movements of each chess piece (pawn, rook, knight, bishop, queen, king)"
  },
  {
    "task_name": "Create Chess Board",
    "description": "Design a 8x8 chess board using python. The board should be able to display the current position of all pieces."
  },
  {
    "task_name": "Implement Player Turns",
    "description": "Develop a function to handle player turns. The game should alternate between two players after each move."
  },
  {
    "task_name": "Check Valid Moves",
    "description": "Create a function to validate the moves of the chess pieces according to the rules of the game."
  },
  {
    "task_name": "Checkmate and Stalemate Detection",
    "description": "Implement a function to detect checkmate or stalemate situations, to end the game when these conditions are met."
  },
  {
    "task_name": "Design User Interface",
    "description": "Develop a simple and intuitive user interface for the players to interact with the game."
  },
  {
    "task_name": "Implement Game Rules",
    "description": "Incorporate all the chess rules into the game such as castling, pawn promotion and en passant."
  },
  {
    "task_name": "Test the Game",
    "description": "Conduct extensive testing of the game to ensure all functions and rules are correctly implemented and the game runs smoothly."
  }
] list and. Identify the current task to be executedDefine Chess Pieces and Create classes or functions to define the properties and movements of each chess piece (pawn, rook, knight, bishop, queen, king).

3. **Understand Previous Task**: Understand what happened in the previous task which will be `None` if its the first task being executed - None. 

4. **Current task**: Return a json with the actions; among the ones supported; to be executed along the values for the each parameter. In the array of json you return, the value from one action will be passed to another to acheive the current task. 

supported_actions: [
                {
                    "cls": {
                        "kls": "CreateFile",
                        "module": "openagi.actions.file.create_file",
                    },
                    "params": {"filename":"<name of the file to be created>", "path": "Path where the file to should be created", "create_parents":"Create parent directories if not exist"},
                },
                {
                    "cls": {
                        "kls": "WriteFile",
                        "module": "openagi.actions.file.write_file",
                    },
                    "params": {
                        "filename": "<name of the file to be created>",
                        "path": "Path where the file to should be created",
                        "content": "Content of the file",
                        "mode": "mode of the file to opened with",
                    },
                }
                        ]
Execute one step at a time, ensuring to clearly follow each step instruction, state your reasoning.
"""
