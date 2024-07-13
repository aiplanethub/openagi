from pydantic import Field
from openagi.actions.base import BaseAction
from openagi.actions.data_source import DataSource
from langchain_community.document_loaders import CSVLoader
from tempfile import NamedTemporaryFile


class CSVLoader(BaseAction):
    data_source: DataSource = Field(
        default_factory=DataSource,
        description="Excel file source",
    )

    def execute(self):
        if self.data_source.url:
            loader = CSVLoader(file_path=self.data_source.url)
        else:
            with NamedTemporaryFile(suffix=".xlsx", delete=True) as temp_file:
                temp_file.write(self.data_source.content)
                temp_file.flush()
                loader = CSVLoader(file_path=temp_file.name)
                return loader.load_and_split()
        return loader.load_and_split()

    def load_csv(self):
        documents = self.execute()
        return documents
