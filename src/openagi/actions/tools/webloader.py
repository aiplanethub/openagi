import re
from collections import Counter
from langchain_community.document_loaders import WebBaseLoader
from pydantic import Field
from openagi.actions.base import ConfigurableAction
import logging

class WebBaseContextTool(ConfigurableAction):
	"""
	Use this Action to extract actual context from a Webpage. The WebBaseContextTool class provides a way to load and optionally summarize the content of a webpage, returning the metadata and page content as a context string.
    If a url seems to be failing for more than once, ignore it and move forward.
	"""

	link: str = Field(
		default_factory=str,
		description="Extract context for the Agents from the Web Search through web page",
	)
	can_summarize: bool = Field(
		default=True,
		description="Indicates whether the action can summarize the content before returning. Uses lightweight summarization. Defaults to true.",
	)

	def _split_into_sentences(self, text):
		"""Split text into sentences using simple regex"""
		text = re.sub(r'\s+', ' ', text)
		sentences = re.split(r'[.!?]+', text)
		return [s.strip() for s in sentences if len(s.strip()) > 10]

	def _calculate_word_freq(self, sentences):
		"""Calculate word frequency across all sentences"""
		words = ' '.join(sentences).lower().split()
		return Counter(words)

	def _score_sentence(self, sentence, word_freq):
		"""Score a sentence based on word frequency and length"""
		words = sentence.lower().split()
		score = sum(word_freq[word] for word in words)
		return score / (len(words) + 1)

	def _get_summary(self, text, num_sentences=6):
		"""Create a simple summary by selecting top scoring sentences"""
		sentences = self._split_into_sentences(text)
		if not sentences:
			return text
			
		word_freq = self._calculate_word_freq(sentences)
		
		scored_sentences = [
			(self._score_sentence(sentence, word_freq), i, sentence)
			for i, sentence in enumerate(sentences)
		]
		
		top_sentences = sorted(scored_sentences, reverse=True)[:num_sentences]
		ordered_sentences = sorted(top_sentences, key=lambda x: x[1])
		
		return ' '.join(sentence for _, _, sentence in ordered_sentences)

	def execute(self):
		loader = WebBaseLoader(self.link)
		data = loader.load()
		metadata = data[0].metadata["title"]
		page_content = data[0].page_content
		if page_content:
			page_content = page_content.strip()
		if self.can_summarize:
			logging.info(f"Summarizing the page {self.link}...")
			page_content = self._get_summary(page_content)
		context = metadata + page_content
		return context
