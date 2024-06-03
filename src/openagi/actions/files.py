import logging
from pathlib import Path
from typing import Dict, Optional

from pydantic import Field

from openagi.actions.base import BaseAction


class CreateFileAction(BaseAction):
    """
    Creates a new file with the specified content and directory structure.
    """

    filename: str = Field(..., description="Name of the file along with the directory.")
    parent_mkdir: bool = Field(
        default=True, description="Create parent directories of the file if not exist."
    )
    exist_ok: bool = Field(
        default=True,
        description="Do not raise error if any of the parent directories exists.",
    )
    file_content: str = Field(default="", description="String content of the file to insert")
    write_text_kargs: Optional[Dict] = Field(
        default=None, description="Kwargs to be passed to pathlib's write_text method"
    )

    def execute(self):
        output_file = Path(self.filename)
        print(f"Created file - {output_file.absolute()}")
        output_file.parent.mkdir(
            parents=self.parent_mkdir,
            exist_ok=self.exist_ok,
        )

        write_kwargs = {}
        if self.write_text_kargs:
            write_kwargs = {**write_kwargs}

        output_file.write_text(data=self.file_content, **write_kwargs)
        return self.file_content


class WriteFileAction(BaseAction):
    """
    Executes the action to write the provided content to a file at the specified path.
    """

    filename: str = Field(..., description="Name of the file along with the directory.")
    file_content: str = Field(default="", description="String content of the file to insert")
    file_mode: str = Field(
        default="w",
        description="File mode to open the file with while using python's open() func. Defaults to 'w'",
    )

    def execute(self):
        logging.debug(f"Running Action {self.__class__.__name__}")
        output_file = Path(self.filename)
        logging.info(f"Writing file - {output_file.absolute()}")
        with open(output_file.absolute(), self.file_mode) as f:
            f.write(self.file_content)
        return self.file_content


class ReadFileAction(BaseAction):
    """
    Reads the contents of a file specified by the `file_path` parameter.
    """

    file_path: str = Field(..., description="Name of the file along with the directory.")

    def execute(self):
        logging.debug(f"Running Action {self.__class__.__name__}")
        output_file = Path(self.file_path)
        logging.info(f"Reading file - {output_file.absolute()}")
        with open(output_file.absolute(), "r") as f:
            return f.read()
