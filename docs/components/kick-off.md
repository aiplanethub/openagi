# Kick-Off

During this step the program gets triggered by passing the agents list and which list of agents to be started first. The dynamic agents shall be added as the  3rd  parameter. The first parameter refers to all the agent objects. The second parameter refers agents that get triggered by the user. The parallel agents execution of agents need to trigger multiple agents.

&#x20;All these 3 parameters are of list type. 4th parameter is LLM.

```python
from openagi.init_agent import kickOffAgents
kickOffAgents(agents_list, [agents_list[0]],
DynamicAgentObjectsList=[agent3], llm=llm)
```

