from typing import Any, Optional
from pydantic import Field
from openagi.actions.base import ConfigurableAction
import wikipedia
import logging

class WikipediaSearch(ConfigurableAction):
	"""Use this Action to search and fetch content from Wikipedia."""

	name: str = Field(
		default_factory=str,
		description="WikipediaSearch Action to search and fetch content from Wikipedia.",
	)
	
	query: str = Field(
		default_factory=str,
		description="Search query to find relevant Wikipedia articles",
	)
	
	sentences: int = Field(
		default=5,
		description="Number of sentences to return from the Wikipedia article. Defaults to 5.",
	)

	def execute(self):
		try:
			# Set Wikipedia to English
			wikipedia.set_lang("en")
			
			# Search for the query
			search_results = wikipedia.search(self.query, results=3)
			
			if not search_results:
				return "No Wikipedia articles found for the given query."
			
			try:
				# Get the page content for the first result
				page = wikipedia.page(search_results[0])
				summary = wikipedia.summary(search_results[0], sentences=self.sentences)
				
				result = {
					"title": page.title,
					"url": page.url,
					"summary": summary
				}
				
				return result
				
			except wikipedia.DisambiguationError as e:
				# Handle disambiguation pages by taking the first option
				try:
					page = wikipedia.page(e.options[0])
					summary = wikipedia.summary(e.options[0], sentences=self.sentences)
					result = {
						"title": page.title,
						"url": page.url,
						"summary": summary
					}
					return result
				except:
					return f"Error processing disambiguation page for query: {self.query}"
					
		except Exception as e:
			logging.error(f"Error in Wikipedia search: {str(e)}")
			return f"Error searching Wikipedia: {str(e)}"