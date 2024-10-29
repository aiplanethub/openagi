import logging
from pathlib import Path
from typing import ClassVar, Dict, Any,Optional

from pydantic import Field
from openagi.actions.base import BaseAction

class ConfigurableAction(BaseAction):
    config: ClassVar[Dict[str, Any]] = {}

    @classmethod
    def set_config(cls, *args, **kwargs):
        if args:
            if len(args) == 1 and isinstance(args[0], dict):
                cls.config.update(args[0])
            else:
                raise ValueError("If using positional arguments, a single dictionary must be provided.")
        cls.config.update(kwargs)

    @classmethod
    def get_config(cls, key: str, default: Any = None) -> Any:
        return cls.config.get(key, default)
    
class CreateFileAction(ConfigurableAction):
    """
    Creates a new file with the specified content and directory structure.
    """
    exist_ok: bool = Field(
        default=True,
        description="Do not raise error if any of the parent directories exists.",
    )
    file_content: str = Field(default="", description="String content of the file to insert")
    write_text_kargs: Optional[Dict] = Field(
        default=None, description="Kwargs to be passed to pathlib's write_text method"
    )

    def execute(self):
        filename = self.get_config('filename')
        parent_mkdir = self.get_config('parent_mkdir')  
        output_file = Path(filename)
        logging.info(f"Created file - {output_file.absolute()}")
        output_file.parent.mkdir(
            parents=parent_mkdir,
            exist_ok=self.exist_ok,
        )

        write_kwargs = {}
        if self.write_text_kargs:
            write_kwargs = {**write_kwargs}

        output_file.write_text(data=self.file_content, **write_kwargs)
        return self.file_content

class WriteFileAction(ConfigurableAction):
    """
    Executes the action to write the provided content to a file at the specified path.
    """
    file_content: str = Field(default="", description="String content of the file to insert")

    def execute(self):
        filename = self.get_config('filename')  
        output_file = Path(filename)
        logging.info(f"Writing file - {output_file.absolute()}")
        with open(output_file.absolute(), "w+") as f:
            f.write(self.file_content)
        return self.file_content

class ReadFileAction(ConfigurableAction):
    """
    Reads the contents of a file specified by the `file_path` parameter.
    """ 
    def execute(self):
        filename = self.get_config('filename')  
        output_file = Path(filename)
        logging.info(f"Reading file - {output_file.absolute()}")
        with open(output_file.absolute(), "r") as f:
            return f.read()
