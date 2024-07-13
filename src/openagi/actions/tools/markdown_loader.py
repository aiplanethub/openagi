from pydantic import Field
from openagi.actions.base import BaseAction
from openagi.actions.data_source import DataSource
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from tempfile import NamedTemporaryFile


class MarkdownLoader(BaseAction):
    data_source: DataSource = Field(
        default_factory=DataSource,
        description="Markdown file source",
    )

    def execute(self):
        if self.data_source.url:
            loader = UnstructuredWordDocumentLoader(file_path=self.data_source.url)
        else:
            with NamedTemporaryFile(suffix=".md", delete=True) as temp_file:
                temp_file.write(self.data_source.content)
                temp_file.flush()
                loader = UnstructuredWordDocumentLoader(file_path=temp_file.name)
                return loader.load_and_split()
        return loader.load_and_split()

    def load_markdown(self):
        documents = self.execute()
        return documents
