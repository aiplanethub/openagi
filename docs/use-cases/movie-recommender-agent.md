# 🎬 Movie Recommender Agent

This documentation provides a detailed guide on how to implement a Movie Recommendation Agent using the OpenAGI framework. The system interacts with users to gather their movie preferences and offers personalized recommendations based on their input.

### Installation

Before you begin, make sure to install the OpenAGI library. You can do this by running the following command:

```bash
pip install openagi
```

### Importing Necessary Libraries

The following libraries are required to set up the Movie Recommendation System:

```python
from openagi.actions.files import WriteFileAction, ReadFileAction
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.actions.tools.webloader import WebBaseContextTool
from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
from openagi.worker import Worker
from rich.console import Console
from rich.markdown import Markdown
```

### Environment Setup

Start by configuring the environment variables necessary for Azure OpenAI services. This setup includes specifying the base URL, deployment name, model name, API key, and API version. These variables authenticate and enable access to Azure OpenAI services.

```python
if __name__ == "__main__":
    import os

    os.environ["AZURE_BASE_URL"] = " "
    os.environ["AZURE_DEPLOYMENT_NAME"] = " "
    os.environ["AZURE_MODEL_NAME"] = " "
    os.environ["AZURE_OPENAI_API_KEY"] = " "
    os.environ["AZURE_OPENAI_API_VERSION"] = " "

    config = AzureChatOpenAIModel.load_from_env_config()
    llm = AzureChatOpenAIModel(config=config)
```

### Workers Used

#### 1. User Input Collector

The User Input Collector is tasked with gathering movie preferences from the user. It asks the user to provide 2-3 movies they enjoy and to specify the genres or themes associated with those movies. The collector confirms the gathered input with the user before moving on to the recommendation phase.

```python
user_input_collector = Worker(
    role="User Input Collector",
    instructions="""
    Your task is to gather movie preferences from the user. Follow these steps:

    1. Ask the user to name 2-3 movies they enjoy.
    2. Ensure the user specifies the genres or themes they like in these movies.
    3. Collect and prepare this information for the recommendation process.
    4. Confirm the collected preferences with the user before proceeding.

    Your output should be a list of movies and their associated genres or themes.
    """,
    actions=[
        DuckDuckGoSearch,
        WebBaseContextTool,
    ]
)
```

#### 2. Movie Recommender

The Movie Recommender uses the user’s preferences to suggest similar films. It analyzes the input from the User Input Collector, searches for related movies using the DuckDuckGo search tool, and ranks the recommendations based on similarity and popularity. The output is a structured list of recommended movies with brief descriptions.

```python
recommender = Worker(
    role="Movie Recommender",
    instructions="""
    As the Movie Recommender, your job is to suggest films based on the user's preferences. Follow these steps:

    1. Receive the list of movies and genres/themes from the User Input Collector.
    2. Use DuckDuckGoNewsSearch to find movies similar to the provided examples.
    3. Analyze the search results to find films that match the user's tastes.
    4. Rank the recommendations based on similarity and popularity.
    5. Create a summary of the recommended movies, including a brief description for each.
    6. Present the recommendations to the user in an engaging and informative way.

    Your output should be a structured list of recommended movies with descriptions.
    """,
    actions=[
        DuckDuckGoSearch,
        WebBaseContextTool,
    ]
)
```

#### 3. Recommendation Review Specialist

The Recommendation Review Specialist ensures the relevance and clarity of the movie recommendations. This worker reviews the descriptions for engagement, suggests additional movies if necessary, and finalizes the presentation format for optimal user readability.

```python
reviewer = Worker(
    role="Recommendation Review Specialist",
    instructions="""
    As the Recommendation Review Specialist, your role is to ensure the recommendations are relevant and well-presented. Follow these steps:

    1. Review the list of recommended movies provided by the Movie Recommender.
    2. Ensure each movie description is clear and engaging.
    3. Suggest any additional movies that may fit the user's preferences.
    4. Finalize the presentation to ensure it is formatted correctly for easy readability.

    Your output should be the final list of recommended movies with any suggested enhancements.
    """,
    actions=[
        DuckDuckGoSearch,
        WebBaseContextTool,
    ]
)
```

### Admin

The Admin orchestrates the workflow by assigning tasks to the various workers. It coordinates the interaction between the User Input Collector, Movie Recommender, and Recommendation Review Specialist, ensuring a smooth and efficient process.

```python
admin = Admin(
    planner=TaskPlanner(human_intervene=True),
    memory=Memory(),
    llm=llm,
)

admin.assign_workers([user_input_collector, recommender, reviewer])
```

### Execution

The script is then executed to collect user preferences and generate movie recommendations. The results are displayed in a structured format, making them easy to read and engaging for the user.

```python
res = admin.run(
    query="Recommend movies based on user preferences.",
    description="""
    The user will provide 2-3 movies they like along with their preferred genres or themes.
    Your task is to recommend similar movies based on this input.
    Ensure the user's preferences are collected first, then provide a list of recommendations.
    """
)
```

On running this code user input is collected :

<figure><img src="../.gitbook/assets/Screenshot 2024-08-22 at 15.51.33.png" alt=""><figcaption></figcaption></figure>

### Output

The output of the script is displayed using the following command:

```python
print("-" * 100)
Console().print(Markdown(res))
```

**Sample Output**

```
----------------------------------------------------------------------------------------------------
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                               Recommended Movies                                                ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Here are some movies you might enjoy:                                                                              

 1 Inception                                                                                                       
   A mind-bending thriller that explores the world of dreams and the subconscious.                                 
 2 The Shawshank Redemption                                                                                        
   A powerful story of hope and friendship set against the backdrop of a maximum-security prison.                  
 3 The Godfather                                                                                                   
   An iconic tale of family, power, and betrayal within the Italian-American mafia.                                
 4 Parasite                                                                                                        
   A darkly comedic thriller that examines class disparity through the lives of two families.                      
 5 Interstellar                                                                                                    
   A visually stunning sci-fi epic about love, sacrifice, and the survival of humanity.                            
 6 The Dark Knight                                                                                                 
   A gripping superhero film that delves into morality through the conflict between Batman and the Joker. 
```

### Conclusion

This documentation illustrates how to use the OpenAGI framework to build an interactive movie recommendation system. By effectively gathering user preferences and leveraging search tools, the system delivers personalized movie suggestions that enhance user engagement and satisfaction.
