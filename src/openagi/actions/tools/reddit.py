from typing import Optional, List
import warnings
import os
from pydantic import Field
from openagi.actions.base import ConfigurableAction
from openagi.exception import OpenAGIException

try:
    import praw
except ImportError:
    raise OpenAGIException("Install PRAW with cmd `pip install praw`")

class RedditSearch(ConfigurableAction):
    """
    Reddit Search Tool to search and retrieve posts/comments from Reddit using PRAW
    """
    query: str = Field(..., description="User query to search Reddit")
    subreddit: Optional[str] = Field(
        default=None,
        description="Specific subreddit to search in. If None, searches across all subreddits"
    )
    sort: str = Field(
        default="relevance",
        description="Sort method for results: 'relevance', 'hot', 'top', 'new', or 'comments'"
    )
    limit: int = Field(
        default=10,
        description="Maximum number of results to return (1-25)"
    )
    include_comments: bool = Field(
        default=False,
        description="Whether to include top comments in the results"
    )

    def __init__(self, **data):
        super().__init__(**data)
        self._check_deprecated_usage()
    
    def _check_deprecated_usage(self):
        required_keys = ['client_id', 'client_secret', 'user_agent']
        env_keys = {
            'REDDIT_CLIENT_ID': 'client_id',
            'REDDIT_CLIENT_SECRET': 'client_secret',
            'REDDIT_USER_AGENT': 'user_agent'
        }
        
        config_missing = any(not self.get_config(key) for key in required_keys)
        env_vars_present = any(key in os.environ for key in env_keys)
        
        if config_missing and env_vars_present:
            warnings.warn(
                "Using environment variables for Reddit credentials is deprecated and will be removed in a future version. "
                "Please use RedditSearch.set_config() instead of setting environment variables.",
                DeprecationWarning,
                stacklevel=2
            )
            self.set_config(**{
                conf_key: os.environ.get(env_key)
                for env_key, conf_key in env_keys.items()
                if env_key in os.environ
            })

    def _init_reddit_client(self) -> praw.Reddit:
        """Initialize and return PRAW Reddit client"""
        client_id = self.get_config('client_id')
        client_secret = self.get_config('client_secret')
        user_agent = self.get_config('user_agent')
        
        if not all([client_id, client_secret, user_agent]):
            raise OpenAGIException(
                "Reddit credentials not found. Use RedditSearch.set_config() to set:"
                "\n- client_id: Your Reddit API client ID"
                "\n- client_secret: Your Reddit API client secret"
                "\n- user_agent: A unique identifier for your application"
            )
        
        return praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    def _format_submission(self, submission: praw.models.Submission, include_comments: bool) -> str:
        """Format a submission into a string with optional comments"""
        result = (
            f"TITLE: {submission.title}\n"
            f"SUBREDDIT: r/{submission.subreddit.display_name}\n"
            f"CONTENT: {submission.selftext if submission.is_self else '[External Link]'}\n"
            f"SCORE: {submission.score}\n"
            f"URL: https://reddit.com{submission.permalink}\n"
        )
        
        if include_comments:
            submission.comments.replace_more(limit=0)
            top_comments = submission.comments[:3]  # Get top 3 comments
            if top_comments:
                result += "TOP COMMENTS:\n"
                for comment in top_comments:
                    result += f"- {comment.body[:200]}... (Score: {comment.score})\n"
        
        return result + "\n"

    def execute(self) -> str:
        # Validate limit
        self.limit = max(1, min(25, self.limit))
        
        # Initialize Reddit client
        reddit = self._init_reddit_client()
        
        # Perform search
        if self.subreddit:
            search_results = reddit.subreddit(self.subreddit).search(
                self.query,
                sort=self.sort,
                limit=self.limit
            )
        else:
            search_results = reddit.subreddit("all").search(
                self.query,
                sort=self.sort,
                limit=self.limit
            )

        # Format results
        formatted_results = []
        for submission in search_results:
            formatted_results.append(
                self._format_submission(submission, self.include_comments)
            )

        if not formatted_results:
            return "No results found."
            
        return "\n".join(formatted_results).strip()
