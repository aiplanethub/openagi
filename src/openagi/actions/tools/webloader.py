from typing import Any
from openagi.actions.base import BaseAction
from pydantic import Field

from langchain_community.document_loaders import WebBaseLoader
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import nltk
nltk.download('punkt')

class WebBaseContextTool(BaseAction):
    """Use this Action to extract actual context from Web Search Tool"""
    
    link: str = Field(
        default_factory=str,
        description = "Extract context for the Agents from the Web Search",
    )

    def _get_summary(self,data):    
        parser = PlaintextParser.from_string(data, Tokenizer("english"))
        summarizer = LsaSummarizer(Stemmer("english"))
        summarizer.stop_words = get_stop_words("english")

        summary = summarizer(parser.document,6)
        summary_sentences = [str(sentence) for sentence in summary]
        return " ".join(summary_sentences)

    def execute(self):
        loader = WebBaseLoader(self.link)
        data = loader.load()
        metadata = data[0].metadata['title']
        summarize_text = self._get_summary(data[0].page_content)
        context = metadata+summarize_text
        return context
