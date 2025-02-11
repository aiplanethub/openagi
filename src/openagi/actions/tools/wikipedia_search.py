import json
from typing import Any
from openagi.actions.base import ConfigurableAction
from pydantic import Field
import wikipedia
import logging

class WikipediaSearch(ConfigurableAction):
	"""Use this Action to search Wikipedia for a query."""

	name: str = Field(
		default_factory=str,
		description="WikipediaSearch Action to search Wikipedia using the query.",
	)
	description: str = Field(
		default_factory=str,
		description="This action is used to search and retrieve information from Wikipedia articles.",
	)

	query: str = Field(
		...,
		description="User query to fetch information from Wikipedia",
	)

	max_results: int = Field(
		default=3,
		description="Maximum number of sentences to return from the Wikipedia article. Defaults to 3.",
	)

	def execute(self):
		try:
			# Search Wikipedia
			search_results = wikipedia.search(self.query)
			
			if not search_results:
				return json.dumps({"error": "No results found"})
			
			# Get the first (most relevant) page
			try:
				page = wikipedia.page(search_results[0])
				summary = wikipedia.summary(search_results[0], sentences=self.max_results)
				
				result = {
					"title": page.title,
					"summary": summary,
					"url": page.url
				}
				
				return json.dumps(result)
			
			except wikipedia.DisambiguationError as e:
				# Handle disambiguation pages
				return json.dumps({
					"error": "Disambiguation error",
					"options": e.options[:5]  # Return first 5 options
				})
				
		except Exception as e:
			logging.error(f"Error in Wikipedia search: {str(e)}")
			return json.dumps({"error": str(e)})
