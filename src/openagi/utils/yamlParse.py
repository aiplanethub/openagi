import os
from pathlib import Path


def read_from_env(attr_name, raise_exception=False):
    attr_value = os.environ.get(attr_name)
    if not attr_value and raise_exception:
        raise ValueError(f"Unable to get config {attr_name}")
    return attr_value
