import requests
from typing import List, Optional
from pydantic import Field
from openagi.actions.base import ConfigurableAction
import logging

class HackerNewsTopStories(ConfigurableAction):
	"""Use this Action to fetch top stories from Hacker News."""

	name: str = Field(
		default_factory=str,
		description="HackerNewsTopStories Action to fetch top stories from Hacker News.",
	)
	
	num_stories: int = Field(
		default=5,
		description="Number of top stories to fetch. Defaults to 5.",
	)

	def _fetch_item_details(self, item_id: int) -> Optional[dict]:
		"""Fetch details for a specific item ID"""
		try:
			response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json")
			return response.json() if response.status_code == 200 else None
		except Exception as e:
			logging.error(f"Error fetching item {item_id}: {str(e)}")
			return None

	def execute(self):
		try:
			# Fetch top stories IDs
			response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
			if response.status_code != 200:
				return "Failed to fetch top stories from Hacker News"

			story_ids = response.json()[:self.num_stories]
			
			# Fetch details for each story
			stories = []
			for story_id in story_ids:
				story = self._fetch_item_details(story_id)
				if story and 'dead' not in story and 'deleted' not in story:
					stories.append({
						'title': story.get('title'),
						'url': story.get('url'),
						'score': story.get('score'),
						'author': story.get('by'),
						'comments_count': story.get('descendants', 0)
					})

			return stories

		except Exception as e:
			logging.error(f"Error fetching Hacker News stories: {str(e)}")
			return f"Error fetching Hacker News stories: {str(e)}"