from openagi.actions.base import BaseAction
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from pydantic import Field


class DocumentLoader(BaseAction):
    """Use this Action to extract content from documents"""

    file_path: str = Field(
        default_factory=str,
        description="File from which content is extracted",
    )

    def text_loader(self):
        loader = TextLoader(file_path=self.file_path)
        data = loader.load()
        page_content = data[0].page_content
        meta_data = data[0].metadata["source"]
        context = meta_data + " " + page_content
        return context

    def csv_loader(self):
        content = ""
        loader = CSVLoader(file_path=self.file_path)
        data = loader.load()

        for i in range(len(data)):
            row_content = data[i].page_content
            row_no = data[i].metadata["row"]
            content += "row_no" + " " + str(row_no) + ": " + str(row_content)
        return content

    def execute(self):
        if self.file_path.endswith(".txt"):
            context = self.text_loader()
        elif self.file_path.endswith(".csv"):
            context = self.csv_loader()
        return context
