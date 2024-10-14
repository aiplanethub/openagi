import logging

from pydantic import Field

from openagi.actions.base import BaseAction


class MemoryRagAction(BaseAction):
    """Action class to get all the results from the previous tasks for the current objetive.
    This action is responsible to reading and not writing. Writing is done by default for every task.
    """

    query: str = Field(
        ...,
        description="Query, a string, to run to retrieve the data from the results of previous tasks. Returns an Array of the results.",
    )
    max_results: int = Field(
        default=10,
        description="Max results to be used by querying the memory Defaults to integer 10.",
    )

    def execute(self):
        resp = self.memory.search(query=self.query, n_results=self.max_results or 10)
        logging.info(f"Retreived MEMORY DATA  -  {resp}")
        return resp
