import logging
from pydantic import Field
from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title

from openagi.actions.base import BaseAction


class UnstructuredPdfLoaderAction(BaseAction):
    """
    Use this Action to extract content from PDFs including metadata.
    Returns a list of dictionary with keys 'type', 'element_id', 'text', 'metadata'.
    """

    file_path: str = Field(
        default_factory=str,
        description="File or pdf file url from which content is extracted.",
    )

    def execute(self):
        logging.info(f"Reading file {self.file_path}")

        elements = partition_pdf(self.file_path, extract_images_in_pdf=True)

        chunks = chunk_by_title(elements)

        dict_elements = []
        for element in chunks:
            dict_elements.append(element.to_dict())

        with open("ele.txt", "w") as f:
            f.write(str(dict_elements))

        return str(dict_elements)
