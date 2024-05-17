import os
from github import Github
from openagi.actions.base import BaseAction
from pydantic import Field
from typing import Optional
from github.GithubException import GithubException
from dotenv import load_dotenv
load_dotenv()

class GithubTool(BaseAction):
    """Create file Action"""

    query: str = Field(..., description="action to be performed on github")
    access_token: str = Field(default=os.environ['GITHUB_ACCESS_TOKEN'], description="GitHub Personal Access Token.")
    repository: str = Field(default=os.environ['GITHUB_REPOSITORY'], description="Name of the repository.")
    github_app_id: Optional[str] = Field(default=os.environ['GITHUB_APP_ID'], description="Github App Id.")
    github_app_private_key: Optional[str] = Field(default=os.environ['GITHUB_APP_PRIVATE_KEY'], description="Github App Private Key Path.")

    def execute(self):
        try:
            access_token = self.access_token
            if not access_token:
                return {"error": "GitHub access token is missing or invalid in .env file"}

            repo_name = self.repository
            if not repo_name:
                return {"error": "Repository name is not provided in .env file"}

            if self.query == 'get_all_code_files_and_contents':
                return self.get_all_code_files_and_contents(repo_name, access_token)
            else:
                return {"error": "Unsupported query"}
        except Exception as e:
            return {"error": str(e)}

    def get_all_code_files_and_contents(self, repo_name, access_token):
        """
        Retrieves all the code files and their contents from a GitHub repository.

        Args:
        repo_name (str): Full name of the repository (e.g., 'owner/repo').
        access_token (str): GitHub Personal Access Token.

        Returns:
        A dictionary where keys are file paths and values are file contents.
        """
        try:
            g = Github(access_token)
            repo = g.get_repo(repo_name)
            contents = repo.get_contents("")
            
            file_contents = {}
            
            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))
                else:
                    if file_content.encoding == "base64":
                        try:
                            # Try to decode the file content as UTF-8
                            content = file_content.decoded_content.decode('utf-8')
                            file_contents[file_content.path] = content
                        except UnicodeDecodeError:
                            # Skip files that cannot be decoded as UTF-8
                            print(f"Skipping binary file: {file_content.path}")
                    else:
                        # Skip files with unsupported encoding
                        print(f"Skipping file with unsupported encoding: {file_content.path}")
            
            return file_contents
        except GithubException as e:
            return {"error": f"GitHub API error: {e.data['message']}" if e.data else str(e)}
        except Exception as e:
            return {"error": str(e)}