from openagi.data_extractors.data_types import DataType
class DataSource:
    def __init__(self, type: DataType, url: str = None, content: str = None, metadata: dict = None):
        self.type = type
        self.url = url
        self.content = content
        self.metadata = metadata