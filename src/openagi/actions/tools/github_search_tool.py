from openagi.actions.base import BaseAction
from pydantic import Field
import os
from langchain.document_loaders import GithubFileLoader

class GitHubFileLoad(BaseAction):
    """
    Use this Action to extract specific extension files from GitHub
    """

    repo: str = Field(
        default_factory=str,
        description="Repository name- Format: username/repo e.g., aiplanthub/openagi",
    )
    extension = Field(...,description="File extension to extract the data from")

    def execute(self):
        access_token = os.environ["GITHUB_ACCESS_TOKEN"]
        
        loader = GithubFileLoader(
             repo = self.name,  
             access_token = access_token,
             github_api_url="https://api.github.com",
             file_filter=lambda file_path: file_path.endswith(self.extension))
        
        data = loader.load()
        context = data[0].page_content
        return context