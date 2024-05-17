from typing import Any, Dict, List

from openagi.memory.base import BaseMemory


class Memory(BaseMemory):
    def save(self, query: str, planned_tasks: List[str], final_res: str) -> None:
        """Save execution details into Memory."""
        document = f"Task: {query}, Subtasks: {', '.join(planned_tasks)}, Response: {final_res}"
        metadata = {
            "task": query,
            "subtasks": planned_tasks,
            "res": final_res,
            "session_id": self.session_id,
        }
        document_id = self.session_id
        self.add_document(document, metadata, document_id)

    def search(self, query: str) -> Dict[str, Any]:
        """Search for similar tasks based on a query."""
        return self.get_documents(query, n_results=10)

    def memorize(self, task: str, information: str) -> None:
        """Store information long-term in Memory."""
        document = f"Task: {task}, Result: {information}"
        metadata = {"task": task, "information": information, "session_id": self.session_id}
        document_id = self.session_id
        self.add_document(document, metadata, document_id)

    def display_memory(self) -> Dict[str, Any]:
        """Retrieve and display the current memory state from the database."""
        result = self.get_documents(self.session_id, n_results=2)
        if result:
            return result
        return {}
