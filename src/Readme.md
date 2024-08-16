## Run Agentic workflow without using OpenAI API keys

### Installation

```bash
!pip install openagi
!pip install langchain_groq
```

### Import Statements

```py
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.agent import Admin
from openagi.llms.groq import GroqModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
```

### Setup Groq LLM and save variables in environment

```py
import os

os.environ['GROQ_API_KEY'] = ""
os.environ['GROQ_MODEL'] = "mixtral-8x7b-32768"
os.environ['GROQ_TEMP'] = "0.1"

config = GroqModel.load_from_env_config()
llm = GroqModel(config=config)
```

### Define Task Planner and Action

```py
planner = TaskPlanner(human_intervene=False)
action = DuckDuckGoSearch
```

### Define Admin

```py
admin = Admin(
    actions= [action],
    planner = planner,
    memory=Memory(),
    llm = llm,
    max_iterations = 5
)

res = admin.run(
    query="3 Days Trip to San francisco Bay area",
    description="You are a knowledgeable local guide with extensive information about the city, it's attractions and customs",
)
print(res)
```

### Output

Here is the requested 3-day itinerary for San Francisco in markdown format:

```markdown
Here is a 3-day itinerary for San Francisco that takes into account local customs and etiquette:

## Day 1
- Morning: Visit the Golden Gate Bridge and Park. Remember to respect the natural surroundings and other visitors.
- Afternoon: Explore Fisherman's Wharf and Pier 39. Be mindful of the sea lions and their space.
- Evening: Have dinner in Chinatown. Follow local dining etiquette and be respectful of the culture.

## Day 2
- Morning: Take a stroll through the Presidio and visit the Walt Disney Family Museum. Dress appropriately for the weather and be respectful of the museum's rules.
- Afternoon: Visit the Exploratorium or California Academy of Sciences. Follow the institutions' guidelines and be considerate of other visitors.
- Evening: Enjoy a meal in the Mission District. Familiarize yourself with local customs and try some authentic Mexican cuisine.

## Day 3
- Morning: Ride a cable car and visit Lombard Street. Follow traffic rules and be respectful of residents and other tourists.
- Afternoon: Explore the Haight-Ashbury neighborhood and the Golden Gate Park. Respect the local culture and the environment.
- Evening: Have dinner in North Beach, also known as Little Italy. Be aware of local dining etiquette and try some Italian-American dishes.

I hope you find this itinerary helpful and enjoy your trip to San Francisco!
```
