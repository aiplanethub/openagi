from .base import BaseMemory
import uuid
from typing import Any, Dict, List

class LTMemory(BaseMemory):
    def __init__(self, agent_name: str):
        super().__init__('LT')
        # self.agent_name = agent_name
        self.session_id = self._generate_session_id()

    def _generate_session_id(self) -> str:
        """Generate a unique session ID incorporating the agent's name."""
        session_id = str(uuid.uuid4())
        return f"{session_id}"                      #TODO: after implementation use worker_id

    def memorize(self, task: str, information: str) -> None:
        """Store information long-term in ChromaDB."""
        document = f"Task: {task}, Result: {information}"
        metadata = {
            'task': task,
            'information': information,
            'session_id': self.session_id
        }
        document_id = self.session_id
        self.add_document(document, metadata, document_id)

    def get(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve long-term memory based on a query."""
        return self.get_documents(query, n_results=2)

    def display_memory(self) -> Dict[str, Any]:
        """Retrieve and display the current memory state from the database."""
        result = self.get_documents(self.session_id, n_results=2)
        if result:
            return result
        return {}