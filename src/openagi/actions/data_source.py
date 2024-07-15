from pydantic import BaseModel
from typing import Optional, Dict
from openagi.actions.data_types import DataType


class DataSource(BaseModel):
    type: DataType
    url: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[Dict] = None
