import base64
import os
from typing import Dict, List

import requests
from langchain_community.document_loaders.github import GithubFileLoader
from pydantic import Field

from openagi.actions.base import BaseAction


class OpenAGIGithubFileLoader(GithubFileLoader):
    def get_file_paths(self) -> List[Dict]:
        base_url = (
            f"{self.github_api_url}/repos/{self.repo}/git/trees/" f"{self.branch}?recursive=1"
        )
        response = requests.get(base_url, headers=self.headers)
        response.raise_for_status()
        all_files = response.json()["tree"]
        """ one element in all_files
        {
            'path': '.github', 
            'mode': '040000', 
            'type': 'tree', 
            'sha': '89a2ae046e8b59eb96531f123c0c6d4913885df1', 
            'url': 'https://github.com/api/v3/repos/shufanhao/langchain/git/trees/89a2ae046e8b59eb96531f123c0c6d4913885dxxx'
        }
        """
        required_files = [
            f for f in all_files if not (self.file_filter and not self.file_filter(f["path"]))
        ]
        return required_files

    def get_file_content_by_path(self, path: str) -> str:
        base_url = f"{self.github_api_url}/repos/{self.repo}/contents/{path}"
        response = requests.get(base_url, headers=self.headers)
        response.raise_for_status()

        content_encoded = response.json()["content"]
        return base64.b64decode(content_encoded).decode("utf-8")


class GitHubFileLoadAction(BaseAction):
    """
    Use this Action to extract specific extension files from GitHub.
    """

    repo: str = Field(
        default_factory=str,
        description="Repository name- Format: username/repo e.g., aiplanthub/openagi",
    )
    extension: str = Field(
        ...,
        description="File extension to extract the data from. eg: `.py`, `.md`",
    )

    def execute(self):
        access_token = os.environ.get("GITHUB_ACCESS_TOKEN")

        loader = OpenAGIGithubFileLoader(
            repo="Shreeharivaasishta/openagi",
            access_token=access_token,
            github_api_url="https://api.github.com",
            branch="main",
            file_filter=lambda files: files.endswith(self.extension),
        )

        data = loader.load()
        response = []
        for doc in data:
            response.append(f"{doc.page_content}\nMetadata")

        return "\n\n".join(response)
