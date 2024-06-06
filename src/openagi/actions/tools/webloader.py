import nltk
from langchain_community.document_loaders import WebBaseLoader
from pydantic import Field
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from sumy.utils import get_stop_words

from openagi.actions.base import BaseAction

nltk.download("punkt")


class WebBaseContextTool(BaseAction):
    """
    Use this Action to extract actual context from a Webpage. The WebBaseContextTool class provides a way to load and optionally summarize the content of a webpage, returning the metadata and page content as a context string.
    """

    link: str = Field(
        default_factory=str,
        description="Extract context for the Agents from the Web Search",
    )
    can_summarize: bool = Field(
        default=True,
        description="Indicates whether the action can summarize the content before returning. Uses ntlk & sumy.summarizers.lsa.LsaSummarizer. Defaults to true.",
    )

    def _get_summary(self, data):
        parser = PlaintextParser.from_string(data, Tokenizer("english"))
        summarizer = LsaSummarizer(Stemmer("english"))
        summarizer.stop_words = get_stop_words("english")

        summary = summarizer(parser.document, 6)
        summary_sentences = [str(sentence) for sentence in summary]
        return " ".join(summary_sentences)

    def execute(self):
        loader = WebBaseLoader(self.link)
        data = loader.load()
        metadata = data[0].metadata["title"]
        page_content = data[0].page_content
        if page_content:
            page_content = page_content.strip()
        if self.can_summarize:
            page_content = self._get_summary(page_content)
        context = metadata + page_content
        return context
