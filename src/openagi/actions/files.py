from typing import Dict, Optional, Any
from pydantic import Field
from openagi.actions.base import BaseAction

from pathlib import Path


class CreateFileAction(BaseAction):
    """Create file Action"""

    filename: str = Field(..., description="Name of the file along with the directory.")
    dir_mode: int = Field(default=0o777, description="Mode of the folder.")
    parent_mkdir: bool = Field(
        default=True, description="Create parent directories of the file if not exist."
    )
    exist_ok: bool = Field(
        default=True, description="Do not raise error if any of the parent directories exists."
    )
    file_content: str = Field(default="", description="String content of the file to insert")
    write_text_kargs: Optional[Dict] = Field(
        default=None, description="Kwargs to be passed to pathlib's write_text method"
    )

    def execute(self):
        output_file = Path(self.filename)
        output_file.parent.mkdir(
            parents=self.parent_mkdir,
            exist_ok=self.exist_ok,
            mode=self.dir_mode,
        )

        write_kwargs = {}
        if self.write_text_kargs:
            write_kwargs = {**write_kwargs}

        return output_file.write_text(data=self.file_content, **write_kwargs)


class WriteFileAction(BaseAction):
    """Create file Action"""

    filename: str = Field(..., description="Name of the file along with the directory.")
    file_content: str = Field(default="", description="String content of the file to insert")
    file_mode: str = Field(
        default="w",
        description="File mode to open the file with while using python's open() func.",
    )

    def execute(self):
        # output_file = Path(self.filename)
        # output_file.parent.mkdir(
        #     parents=self.parent_mkdir,
        #     exist_ok=self.exist_ok,
        #     mode=self.dir_mode,
        # )
        # return output_file.write_text(data=self.file_content)
        output_file = Path(self.filename)
        with open(output_file.absolute(), self.file_mode) as f:
            f.write(self.file_content)
