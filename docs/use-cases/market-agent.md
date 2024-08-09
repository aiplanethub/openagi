---
description: >-
  This example uses OpenAGI to create trip itineraries by leveraging an OpenAI
  model through an Admin agent, with results displayed using Markdown via the
  rich library.
---

# 📅 Itinerary Planner

**Import Required Libraries**

First, import the necessary libraries and modules. These modules will enable the agent to perform web searches, handle task planning, write files, and display results in a readable format.

```python
from openagi.actions.files import WriteFileAction
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.agent import Admin
from openagi.llms.openai import OpenAIModel
from openagi.planner.task_decomposer import TaskPlanner
```

**Setup LLM**

Set up the environment variables required for the OpenAI configuration. These environment variables include the API key necessary for accessing the OpenAI services. This configuration is essential for the Large Language Model (LLM) to function correctly.

```python
# Set up the environment variables for OpenAI
import os
os.environ["OPENAI_API_KEY"] = "sk-proj-xxxxxxxxxxxxxxxxxx"

# Initialize the OpenAI Model
config = OpenAIModel.load_from_env_config()
llm = OpenAIModel(config=config)
```

**Define Admin**

Create an Admin instance to manage actions and execute tasks. The Admin will use the DuckDuckGoSearch tool to perform web searches, the WriteFileAction to save results, and the TaskPlanner to manage task execution without human intervention.

```python
# Set up the Admin Agent
admin = Admin(
    llm=llm,
    actions=[
        DuckDuckGoSearch,
        WriteFileAction,
    ],
    planner=TaskPlanner(
        human_intervene=False,
    ),
)
```

**Execute Agent LLM**

Run the Admin with a specific query to create an itinerary for a trip to the San Francisco Bay Area. The Admin will process this query and return a detailed itinerary based on the latest information available.

```python
# Execute the Agent to create an itinerary
travel_plan = Admin(actions=[DuckDuckGoSearch]).run(
    query="3 Days Trip to san francisco bay area",
    description="You are a knowledgeable local guide with extensive information about the city, it's attractions and customs",
)
```

**Print the Results**

Finally, use the rich library to output the results in a readable format. The Markdown class helps in rendering the itinerary content neatly in the console.

```python
# Print the results from OpenAGI using rich library
print(travel_plan)
```

By following these steps, you can set up a News Agent that helps you plan activities or trips effectively. This example uses the power of the OpenAI model and OpenAGI to perform efficient web searches and present the information in an easily digestible format, ensuring you stay informed and well-prepared.

### Output

When this code is executed, the output in the console might resemble the following itinerary:

```
# Itinerary for a 3-Day Trip to San Francisco Bay Area

## Day 1: Explore San Francisco

- **Morning**: Visit the iconic Golden Gate Bridge. Enjoy a walk or rent a bike to cross the bridge for stunning views.
  
- **Afternoon**: Head to Fisherman’s Wharf for lunch. Try the famous clam chowder in a sourdough bread bowl.

- **Evening**: Explore Pier 39, watch the sea lions, and enjoy street performances. Consider dining at one of the waterfront restaurants.

## Day 2: Culture and History

- **Morning**: Visit Alcatraz Island. Book your tickets in advance to explore the historic prison.

- **Afternoon**: Discover the San Francisco Museum of Modern Art (SFMOMA). Enjoy lunch at a nearby café.

- **Evening**: Stroll through the Mission District and enjoy the vibrant murals. Dine at a local taqueria for authentic Mexican food.

## Day 3: Nature and Surroundings

- **Morning**: Take a trip to Muir Woods National Monument. Enjoy a hike among the towering redwoods.

- **Afternoon**: Visit Sausalito for lunch and explore the charming waterfront town.

- **Evening**: Return to San Francisco and enjoy a sunset view from Twin Peaks. Consider a farewell dinner in the city.
```

This output provides a structured and detailed itinerary for a three-day trip to the San Francisco Bay Area, formatted for easy reading.
