from openagi.actions.base import BaseAction
from pydantic import Field
from typing import Any
from openagi.exception import OpenAGIException

try:
   import yt_dlp
   from youtube_search import YoutubeSearch
except ImportError:
  raise OpenAGIException("Install YouTube transcript with cmd `pip install yt-dlp` and `pip install youtube-search`")

class YouTubeSearchTool(BaseAction):
    """Youtube Search Tool"""

    query: str = Field(
        ..., description="Keyword required to search the video content on YouTube"
    )
    max_results: Any = Field(
        default=5,
        description="Total results, an integer, to be executed from the search. Defaults to 5",
    )

    def execute(self):
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'force_generic_extractor': True,
            'format': 'best'
        }
        results = YoutubeSearch(self.query, max_results=self.max_results)
        response = results.to_dict()
        context = ""
        for ids in response:
            url = "https://youtube.com/watch?v="+ids['id']
            context += f"Title: {ids['title']}"
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                description = info_dict.get('description', None)
                context += f"Description: {description} \n\n"
        return context