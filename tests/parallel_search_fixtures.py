"""Deterministic LLM and in-memory storage for the native Admin execution loop."""

import json
import re
from urllib.parse import urlparse

from pydantic import Field

from openagi.actions.tools.parallel_search import ParallelSearch
from openagi.agent import Admin, OutputFormat
from openagi.llms.base import LLMBaseModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
from openagi.storage.base import BaseStorage


class InMemoryStorage(BaseStorage):
    documents: list = Field(default_factory=list)

    def save_document(self, id, document, metadata):
        self.documents.append(document)

    def update_document(self, id, document, metadata):
        self.documents.append(document)

    def query_documents(self, **kwargs):
        return {"documents": self.documents}


class EvidenceLLM(LLMBaseModel):
    query: str
    calls: int = 0
    observation: str = ""

    def load(self):
        return self

    @staticmethod
    def load_from_env_config():
        return {}

    def run(self, input_data):
        self.calls += 1
        if self.calls == 1:
            assert "openagi.actions.tools.parallel_search" in input_data
            answer = {
                "action": {
                    "cls": ParallelSearch.cls_doc()["cls"],
                    "params": {"query": self.query, "timeout": 30},
                }
            }
        else:
            # Produce the final answer from the actual observation, not a canned answer.
            self.observation = input_data.rsplit("Observation: ", 1)[1]
            results, _ = json.JSONDecoder().raw_decode(self.observation)
            source = next(
                r
                for r in results["results"]
                if urlparse(r["url"]).hostname in ("python.org", "www.python.org")
            )
            excerpt = "\n".join(source["excerpts"])
            sentence = re.search(r"Python is a programming language[^.]*\.", excerpt).group()
            answer = {"final_output": f"{sentence} Source: {source['url']}"}
        return "```json\n" + json.dumps(answer) + "\n```"


def run_agent_search(query):
    storage = InMemoryStorage(name="test-memory")
    # Avoid saved Chroma settings, persistence and embedding model downloads.
    memory = Memory.model_construct(storage=storage, ltm_storage=storage, long_term=False)
    llm = EvidenceLLM(config={}, query=query)
    admin = Admin(
        actions=[ParallelSearch],
        llm=llm,
        memory=memory,
        planner=TaskPlanner(autonomous=False, human_intervene=False),
        output_format=OutputFormat.raw_text,
        summarize_task_context=False,
    )
    result = admin.run(
        query=query,
        description="Answer with a source URL.",
        planned_tasks=[{"task_name": "Search", "description": query}],
    )
    return result, llm, memory
