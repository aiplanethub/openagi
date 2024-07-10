from enum import Enum

class DataType(Enum):
    TXT = "TXT"
    PDF = "PDF"
    DOCX = "DOCX"
    PPTX = "PPTX"
    GOOGLE_DOC = "GOOGLE_DOC"
    MARKDOWN = "MARKDOWN"
    GITHUB_REPOSITORY = "GITHUB_REPOSITORY"
    WEBPAGE = "WEBPAGE"
    NOTION = "NOTION"
    URL = "URL"
    YOUTUBE = "YOUTUBE"
    CSV = "CSV"
    XLSX = "XLSX"

    def __str__(self):
        return self.value

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))