from typing import Any
from openagi.actions.tools import (
    TxtLoader,
    PDFLoader,
    CSVLoader,
    PPTXLoader,
    ExcelLoader,
    MarkdownLoader,
    DOCXLoader,
)
from openagi.actions.data_types import DataType
from openagi.actions.data_source import DataSource


class DataLoader:
    def __init__(self, data_source: DataSource):
        self.data_source = data_source

    def load(self) -> Any:
        loader_methods = {
            DataType.TXT: self.load_txt,
            DataType.PDF: self.load_pdf,
            DataType.PPTX: self.load_pptx,
            DataType.DOCX: self.load_docx,
            DataType.MARKDOWN: self.load_markdown,
            DataType.CSV: self.load_csv,
            DataType.XLSX: self.load_excel,
        }

        loader = loader_methods.get(self.data_source.type)
        if loader:
            return loader()
        else:
            raise ValueError(f"Loader not implemented for type: {self.data_source.type}")

    def load_txt(self):
        return TxtLoader(data_source=self.data_source).load_txt()

    def load_pdf(self):
        return PDFLoader(data_source=self.data_source).load_pdf()

    def load_pptx(self):
        return PPTXLoader(data_source=self.data_source).load_pptx()

    def load_docx(self):
        return DOCXLoader(data_source=self.data_source).load_pptx()

    def load_markdown(self):
        return MarkdownLoader(data_source=self.data_source).load_markdown()

    def load_csv(self):
        return CSVLoader(data_source=self.data_source).load_csv()

    def load_excel(self):
        return ExcelLoader(data_source=self.data_source).load_excel()
