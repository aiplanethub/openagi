<div align="center">
<h1 align="center">OpenAGI </h1>
<h2 align="center">Making the development of autonomous human-like agents accessible to all</h2>

<a href="https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white" alt="Python 3.11"></a>
<a href="https://discord.gg/4aWV7He2QU"><img src="https://dcbadge.vercel.app/api/server/4aWV7He2QU?style=flat" alt="Discord" /></a>
<a href="https://twitter.com/aiplanethub"><img src="https://img.shields.io/twitter/follow/aiplanethub" alt="Twitter" /></a>

<p>OpenAGI aims to make human-like agents accessible to everyone, thereby paving the way towards open agents and, eventually, AGI for everyone. We strongly believe in the transformative power of AI and are confident that this initiative will significantly contribute to solving many real-life problems. Currently, OpenAGI is designed to offer developers a framework for creating autonomous human-like agents.</p>
<i><a href="https://discord.gg/4aWV7He2QU">👉 Join our Discord community!</a></i>
</div>


## Installation

1. Setup a virtual environment.

   **Note: Use python3.11**

    ```bash
    # For Mac users
    python3 -m venv venv
    source venv/bin/activate

    # For Windows users
    python -m venv venv
    venv/scripts/activate

    # to create virtual env using particular python version (in Windows)
    py -3.11 -m venv venv
    ```

2. Install the openagi

   ```bash
   pip install openagi
   ```

## To setup your crendentials

Follow this quick [installation guide](https://openagi.aiplanet.com/getting-started/installation) to complete the setup.

## Documentation

For more queries find documentation for OpenAGI at [openagi.aiplanet.com](https://openagi.aiplanet.com/)

## Understand OpenAGI

![Thumbnails](https://github.com/aiplanethub/openagi/blob/dev/assets/openagi.png)

## Example

Follow this example to create a Test Case Developer that reads code files from your github repo and creates test cases for the same.
Make sure you complete the steup of Github Tool from [here](https://openagi.aiplanet.com/components/tools#id-4.-githubsearchtool).

**Note:** Follow setup guide to configure the environment. For quick access click [here](https://openagi.aiplanet.com/getting-started/installation).

```python
from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms import OpenAIModel
from openagi.tools.integrations import GithubSearchTool

if __name__ == "__main__":
    agent_names = ["DEVELOPER", "TESTCASEDEVELOPER"]

    agent_list = [
        Agent(
            agentName=agent_names[0],
            role="DEVELOPER",
            goal="Efficiently search and retrieve relevant information regarding repository and code snippets on GitHub.",
            backstory="Developed to enhance productivity for developers, this tool integrates with the GitHub API to provide streamlined access to code resources.",
            capability="search_executor",
            task="Retrieve the code for all the files in the respository.",
            output_consumer_agent=[agent_names[1]],
            tools_list=[GithubSearchTool],
        ),
        Agent(
            agentName=agent_names[1],
            role="TESTCASEDEVELOPER",
            goal="To meticulously examine the provided Python code and provide test cases with adherence to best practices.",
            backstory="You are a seasoned software test case developer who developes unit, integration and functional test cases for the given program code",
            capability="llm_task_executor",
            task="Conduct a comprehensive test cases for the Python code, paying particular attention to functional and acceptance testing including edge cases. Also provide no of positive and edge test cases to enable the management to understand the quality of testing",
            output_consumer_agent=["HGI"],
        ),
    ]

    config = OpenAIModel.load_from_yml_config()  # Setup a file named config.yaml and set OPENAI_API_KEY variable. Follow instructions from docs in Note above.
    llm = OpenAIModel(config=config)
    kickOffAgents(agent_list, [agent_list[0]], llm=llm)
```

## Prominent Features:

- Flexible Agent Architecture: OpenAGI features a flexible agent architecture, allowing users to create sequential, parallel, and dynamic communication patterns similar to humans. This flexibility is designed to help users efficiently tackle their unique challenges.
- Streamlined Integration and Configuration: OpenAGI introduces simplified integration and configuration processes, eliminating the infinite loops commonly encountered in other tools.
- Automated & Manual Agent Configuration Generation: We provide the functionality to automatically generate the necessary configurations for building agents and their corresponding configurations. For developers preferring a hands-on approach, OpenAGI supports the manual configuration of agent solutions. This allows for detailed customization according to specific needs and preferences.

## Use Cases:

- **Education:** In education, agents can provide personalized learning experiences. They adapt and tailor learning content based on student's progress, performance and interests. It can extend to automating various other administrative tasks and assist teachers in improving their productivity.
- **Finance and Banking:** Financial services can use agents for fraud detection, risk assessment, personalized banking advice, automating trading, and customer service. They help in analyzing large volumes of transactions to identify suspicious activities and offer tailored investment advice.
- **Healthcare:** Agents can be deployed to monitor patients, provide personalized health recommendations, manage patient data, and automate administrative tasks. They can also assist in diagnosing diseases based on symptoms and medical history.

## Get in Touch

For any queries/suggestions/support connect us at [openagi@aiplanet.com](mailto:openagi@aiplanet.com)

## Contribution guidelines

OpenAGI thrives in the rapidly evolving landscape of open-source projects. We wholeheartedly welcome contributions in various capacities, be it through innovative features, enhanced infrastructure, or refined documentation.

For a comprehensive guide on the contribution process, please click [here](https://github.com/aiplanethub/openagi/blob/main/dev/Readme.md).
