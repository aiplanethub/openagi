# xml_tool.py

from openagi.actions.base import Tool
import xml.etree.ElementTree as ET

class XMLTool(Tool):
    """
    A tool for interacting with XML data.
    """

    def __init__(self, name="XMLTool", description="A tool for interacting with XML data."):
        super().__init__(name, description)

    def _execute(self, query: str):
        try:
            # Parse the XML data from the query
            root = ET.fromstring(query)

            # Example: Extract information from the XML
            # You can use various methods like find, findall, iter, etc.
            # to navigate and extract data from the XML tree
            # For instance, to get the text of the first 'title' element:
            title = root.find('title').text

            return title  # Or any other processed data from the XML

        except ET.ParseError as e:
            return f"Error parsing XML: {e}"
        except Exception as e:
            return f"Error processing XML: {e}"