from pydantic import Field
from openagi.actions.base import BaseAction
from openagi.actions.data_source import DataSource
from langchain_community.document_loaders import TextLoader
from tempfile import NamedTemporaryFile

class TxtLoader(BaseAction):
    data_source: DataSource = Field(
        default_factory=DataSource,
        description="Text file source",
    )
    def execute(self):
        with NamedTemporaryFile(suffix=".txt", delete=True) as temp_file:
            if self.data_source.url:
                file_response = TextLoader(self.data_source.url).text
            else:
                file_response = self.data_source.content
            temp_file.write(file_response.encode())
            temp_file.flush()
            loader = TextLoader(file_path=temp_file.name)
            return loader.load_and_split()

    def load_txt(self):
        documents = self.execute()
        return documents
