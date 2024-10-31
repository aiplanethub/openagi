from openagi.actions.base import BaseAction
from pydantic import Field
from openagi.exception import OpenAGIException
from typing import ClassVar, Dict, Any

try:
    import arxiv
except ImportError:
    raise OpenAGIException("Install arxiv with cmd `pip install arxiv`")
    
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
    
class ArxivSearch(ConfigurableAction):
    """
    Arxiv Search is a tool used to search articles in Physics, Mathematics, Computer Science, Quantitative Biology, Quantitative Finance, and Statistics
    """
    query: str = Field(..., description="User query or question")
    max_results: int = Field(10, description="Total results, in int, to be executed from the search. Defaults to 10.")

    def execute(self):
        search = arxiv.Search(
        query = self.query,
        max_results = self.max_results,
                              )
        client = arxiv.Client()
        results = client.results(search)
        meta_data = ""
        for result in results:
            meta_data += f"title : {result.title}\n "
            meta_data += f"summary : {result.summary}\n "
            meta_data += f"published : {result.published}\n "
            meta_data += f"authors : {result.authors}\n "
            meta_data += f"pdf_url : {result.pdf_url}\n "
            meta_data += f"entry_id : {result.entry_id}\n\n "
        return meta_data.strip()























