# 🧠 Memory

## What is Memory?

&#x20;Memory is one of the important components of the Agentic framework, which gives the agents their own memory to recall and remember the tasks executed and feedback received. It helps the agent make "informed decisions" by recalling previous actions and their observations. It can also store the current execution. Memory helps the agent to avoid repeating mistakes for similar tasks and improves the overall user experience by providing results based on recalled memory.

The new update introduces Long-Term Memory (LTM), a breakthrough feature that enhances the way agents interact, adapt, and grow. LTM equips AI agents with the capability to store and recall information from previous interactions over extended periods, much like human memory.

### Long Term Memory

<pre class="language-python"><code class="lang-python">from openagi.memory import Memory
<strong>
</strong># Basic memory initialization
memory = Memory()

# Long-Term Memory initialization with custom settings
ltm_memory = Memory(
    long_term=True,
    ltm_threshold=0.8,
    long_term_dir="/path/to/custom/memory/storage"
)
</code></pre>

Key Features of Long-Term Memory:

1. Seamless Integration: Enabling LTM within OpenAGI requires just a simple configuration update.
2. Customizable Memory Storage: Users have control over how and where their agent's memory is stored.
3. Smart Retrieval: LTM employs semantic similarity to retrieve and apply relevant information from past experiences.
4. Feedback-Driven Learning: Agents can incorporate user feedback to continuously enhance their performance.
5. Privacy Controls: Memory management is user-friendly, allowing easy deletion or modification of stored information.

## Parameters:

&#x20;The Memory class accepts several parameters that allow you to customize its behavior, particularly for Long-Term Memory:

| Parameter       | Type  | Default | Description                                                                                                                                                 |
| --------------- | ----- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| long\_term      | bool  | False   | Enables or disables Long-Term Memory functionality. When set to True, the agent will store and retrieve information from past interactions.                 |
| ltm\_threshold  | float | 0.7     | Sets the semantic similarity threshold for memory retrieval. Higher values make the memory more selective, only retrieving highly similar past experiences. |
| long\_term\_dir | str   | None    | Specifies the directory for storing long-term memories. If not provided, a default location will be used.                                                   |



Below we have shown how one can initiate and run using query with Long-Term Memory enabled:

```python
# imports
from openagi.agent import Admin
from openagi.llms.openai import OpenAIModel
from openagi.planner.task_decomposer import TaskPlanner
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.memory import Memory

# Define LLM
config = OpenAIModel.load_from_env_config()
llm = OpenAIModel(config=config)

# Memory Usage with Long-Term Memory enabled
admin = Admin(
    llm=llm,
    actions=[DuckDuckGoSearch],
    planner=TaskPlanner(human_intervene=False),
    memory=Memory(long_term=True),
)

# Run Admin
res = admin.run(
    query="sample query",
    description="sample description",
)
```

With LTM activated, your agent will now retain knowledge from previous interactions and use that information to provide more relevant and intelligent responses. This enhancement allows for the creation of more sophisticated AI systems that can learn and improve over time, offering a new level of continuity and context-awareness in AI-driven applications.

```
```
