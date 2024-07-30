# 🔧 Action

### What is Action?

Actions provide predefined functionalities that the Agent can invoke to accomplish various tasks. These tasks include fetching data from external sources, processing the data to extract meaningful insights, and storing the results for subsequent use.&#x20;

The Agent invokes actions during its runtime to execute specific tasks. For example, when a user queries the agent, the agent might use a search action to gather information and then a processing action to analyze it

### Attributes

The parameter attributes for Actions is dynamic and it varies based on the different use cases. One can directly pass the supported tools, files as list for defining the actions.&#x20;

### Code Snippet

```python
from openagi.actions.files import WriteFileAction
from openagi.actions.tools.ddg_search import DuckDuckGoSearch

actions = [
        DuckDuckGoSearch,
        WriteFileAction,
] 
```
