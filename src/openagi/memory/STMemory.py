from typing import Any, Dict
import uuid

class STMemory:
    def __init__(self, agent: str):
        self.agent_name = agent
        self.session_id = self._generate_session_id()
        self.memory = None

    def _save_agent_exec(
            self, 
            agent: str, 
            task: str, 
            tools: list,
            consumer: str,
            ) -> None:
        self.memory = {
            'session_id': self.session_id,
            'agent': agent,
            'task': task,
            'tools': tools,
            'consumer': consumer,
        }
    
    def _generate_session_id(self) -> str:
        session_id = str(uuid.uuid4())
        return f"{self.agent_name}_{session_id}"
    
    def search(self, query: str) -> Dict[str, Any]:
        # if self.memory['session_id'] == self.session_id:
        #     search_results = {
        #         'agent': self.memory['agent'],
        #         'task': self.memory['task'],
        #         'tools': self.memory['tools'],
        #         'consumer': self.memory['consumer'],
        #         'tools_output': []
        #     }
        #     if 'tools_output' in self.memory:
        #         search_results['tools_output'] = self.memory['tools_output']
        #     return search_results
        # else:
        #     return {}
        return NotImplementedError("Still need to make changes to search")
    
    def _save_tool_exec(
        self,
        tool_name: str,
        tool_output: Any,
        ) -> None:
        if self.memory['session_id'] == self.session_id:
            if 'tools_output' not in self.memory:
                self.memory['tools_output'] = []
            self.memory['tools_output'].append({
                'tool_name': tool_name,
                'tool_output': tool_output
            })
    
    def display_memory(self) -> Dict[str, Any]:
        return self.memory