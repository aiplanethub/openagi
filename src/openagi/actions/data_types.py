from enum import Enum

class DataType(Enum):
    TXT = "TXT"
    PDF = "PDF"
    DOCX = "DOCX"
    PPTX = "PPTX"
    MARKDOWN = "MARKDOWN"
    CSV = "CSV"
    XLSX = "XLSX"

    def __str__(self):
        return self.value

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))