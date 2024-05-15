from .base import BaseMemory
import uuid
from typing import Any, Dict, List

class STMemory(BaseMemory):
    def __init__(self):
        super().__init__('ST')
        # self.agent_name = agent
        self.session_id = self._generate_session_id()

    def _generate_session_id(self) -> str:
        """Generate a unique session ID incorporating the agent's name."""
        session_id = str(uuid.uuid4())
        return f"{self.agent_name}_{session_id}"

    def save_admin_exec(self, query: str, planned_tasks: List[str], final_res: str) -> None:
        """Save execution details into ChromaDB."""
        document = f"Task: {query}, Subtasks: {', '.join(planned_tasks)}, Response: {final_res}"
        metadata = {
            'task': query,
            'subtasks': planned_tasks,
            'res': final_res,
            'session_id': self.session_id
        }
        document_id = self.session_id
        self.add_document(document, metadata, document_id)

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search for similar tasks based on a query."""
        return self.get_documents(query, n_results=10)

    def save_tool_exec(self, tool_name: str, tool_output: Any) -> None:
        """Update the existing session data with tool execution details."""
        from .storage import update_document
        updated_document = f"Updated tool execution: {tool_name}, Output: {tool_output}"
        update_document([self.session_id], [updated_document], [{'tool_name': tool_name, 'tool_output': tool_output}])

    def display_memory(self) -> Dict[str, Any]:
        """Retrieve and display the current memory state from the database."""
        result = self.get_documents(self.session_id, n_results=2)
        if result:
            return result
        return {}