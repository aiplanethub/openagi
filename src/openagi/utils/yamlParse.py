import os
from pathlib import Path

import yaml

OPENAGI_CONFIG_PATH = os.environ.get("OPENAGI_CONFIG_PATH")
if not OPENAGI_CONFIG_PATH:
    raise ValueError("Environment variable not set: `OPENAGI_CONFIG_PATH`")

OPENAGI_CONFIG_PATH = Path(OPENAGI_CONFIG_PATH)
if not OPENAGI_CONFIG_PATH.is_file():
    raise FileNotFoundError(f"No such file or directory: `{OPENAGI_CONFIG_PATH.absolute()}`")


def read_yaml_config(attr_name, raise_exception=False):
    with open(OPENAGI_CONFIG_PATH, "r") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        attr_value = data.get(attr_name)
        if not attr_value and raise_exception:
            raise ValueError(f"Unable to get config {attr_name}")
        return attr_value
