from openagi.actions.base import BaseAction
from pydantic import Field
from typing import Any, ClassVar, Dict
from openagi.exception import OpenAGIException

try:
    import yt_dlp
    from youtube_search import YoutubeSearch
except ImportError:
    raise OpenAGIException("Install YouTube transcript with cmd `pip install yt-dlp` and `pip install youtube-search`")

class ConfigurableAction(BaseAction):
    config: ClassVar[Dict[str, Any]] = {}

    @classmethod
    def set_config(cls, *args, **kwargs):
        if args:
            if len(args) == 1 and isinstance(args[0], dict):
                cls.config.update(args[0])
            else:
                raise ValueError("If using positional arguments, a single dictionary must be provided.")
        cls.config.update(kwargs)

    @classmethod
    def get_config(cls, key: str, default: Any = None) -> Any:
        return cls.config.get(key, default)

class YouTubeSearchTool(ConfigurableAction):
    """Youtube Search Tool"""

    query: str = Field(
        ..., description="Keyword required to search the video content on YouTube"
    )
    max_results: Any = Field(
        default=5,
        description="Total results, an integer, to be executed from the search. Defaults to 5",
    )

    def execute(self):
        ydl_opts = self.get_config('ydl_opts', {
            'quiet': True,
            'skip_download': True,
            'force_generic_extractor': True,
            'format': 'best'
        })

        results = YoutubeSearch(self.query, max_results=self.max_results)
        response = results.to_dict()
        context = ""
        for ids in response:
            url = f"https://youtube.com/watch?v={ids['id']}"
            context += f"Title: {ids['title']}\n"
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                description = info_dict.get('description', 'No description available')
                context += f"Description: {description}\n\n"
        return context.strip()