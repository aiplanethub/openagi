import uuid
from typing import Any, Dict
import chromadb

class LTMemory:
    def __init__(self, agent_name: str) -> None:
        self.agent_name = agent_name
        self.session_id = self._generate_session_id()
        self.long_term_memory = chromadb.Client()

    def _generate_session_id(self) -> str:
        session_id = str(uuid.uuid4())
        return f"{self.agent_name}_{session_id}"

    def memorize(self, information: Dict[str, Any]) -> None:
        self.long_term_memory.add(information)

    def get(self, task: str) -> Dict[str, Any]:
        relevant_results: Dict[str, Any] = {}
        relevant_results = self.long_term_memory.query(task, n_results=2)
        return relevant_results

    def display_memory(self) -> Dict[str, Any]:
        return self.long_term_memory

