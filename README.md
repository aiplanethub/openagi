<div align="center">
<h1 align="center">OpenAGI </h1>
<h2 align="center">Making the development of autonomous human-like agents accessible to all</h2>

<a href="https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11-3776AB.svg?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11-3776AB.svg?style=flat&logo=python&logoColor=white" alt="Python Versions"></a>
<a href="https://discord.gg/4aWV7He2QU"><img src="https://dcbadge.vercel.app/api/server/4aWV7He2QU?style=flat" alt="Discord" /></a>
<a href="https://twitter.com/aiplanethub"><img src="https://img.shields.io/twitter/follow/aiplanethub" alt="Twitter" /></a>

<p>OpenAGI aims to make human-like agents accessible to everyone, thereby paving the way towards open agents and, eventually, AGI for everyone. We strongly believe in the transformative power of AI and are confident that this initiative will significantly contribute to solving many real-life problems. Currently, OpenAGI is designed to offer developers a framework for creating autonomous human-like agents.</p>
<i><a href="https://discord.gg/4aWV7He2QU">👉 Join our Discord community!</a></i>
</div>

## Installation

1. Setup a virtual environment.

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

## To setup your credentials

Follow this quick [installation guide](https://openagi.aiplanet.com/getting-started/installation) to complete the setup.

## Documentation

For more queries find documentation for OpenAGI at [openagi.aiplanet.com](https://openagi.aiplanet.com/)

## Understand OpenAGI

![Thumbnails](https://github.com/aiplanethub/openagi/blob/dev/assets/openagi.png)

## Example (Single Agent)

Follow this example to create a **Job Search Agent** that helps you to search available job posting for a given category.
Here in the example we are using `AzureChatOpenAIModel` along with `GoogleSerpAPISearch` to search the internet for various job posting on the particular role.

**Note:** Follow setup guide to configure the environment. For quick access click [here](https://openagi.aiplanet.com/getting-started/installation).

```python
from openagi.actions.tools.serp_search import GoogleSerpAPISearch
from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
from rich.console import Console
from rich.markdown import Markdown

if __name__ == "__main__":
    config = AzureChatOpenAIModel.load_from_env_config()
    llm = AzureChatOpenAIModel(config=config)

    company_domain = input("What is the company domain?\n")
    job_domain = input("What is the job domain?\n")
    job_level = input("What level job are you looking for?\n")
    job_location = input("In what location are you for the job?\n")

    query = f"""
Need help finding a job description based on the following criteria:

Company Domain: {company_domain}
Job Domain: {job_domain}
Job Level: {job_level}
Job Location: {job_location}

Please provide a list of suitable job descriptions, including the key responsibilities, requirements, and any other relevant details.
"""

    admin = Admin(
        llm=llm,
        actions=[GoogleSerpAPISearch],
        planner=TaskPlanner(human_intervene=False),
        memory=Memory(),
    )

    res = admin.run(
        query=query,
        description="You are an expert Internet searching agent , who gives best possible response.",
    )

    # Print the results from the OpenAGI
    print("-" * 100)  # Separator
    Console().print(Markdown(res))
```

## Example (Workers)
Workers are used to create a Multi-Agent architecture.

Follow this example to create a **Blog post Agent** that helps you research and write blog posts. A number of workers (agents) are working together to achieve this task. 

```python
from openagi.actions.files import WriteFileAction
from openagi.actions.tools.ddg_search import DuckDuckGoNewsSearch
from openagi.actions.tools.webloader import WebBaseContextTool
from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
from openagi.worker import Worker
from rich.console import Console
from rich.markdown import Markdown

if __name__ == "__main__":
    config = AzureChatOpenAIModel.load_from_env_config()
    llm = AzureChatOpenAIModel(config=config)

    # Team Members
    researcher = Worker(
        role="Research Analyst",
        instructions="Uncover cutting-edge developments in AI and data science. You work at a leading tech think tank. Your expertise lies in identifying emerging trends. You have a knack for dissecting complex data and presenting actionable insights.",
        actions=[
            DuckDuckGoNewsSearch,
            WebBaseContextTool,
        ],
    )
    writer = Worker(
        role="Tech Content Strategist",
        instructions="Craft compelling content on tech advancements. You are a renowned Content Strategist, known for your insightful and engaging articles.You transform complex concepts into compelling narratives. Finally return the entire article as output.",
        actions=[
            DuckDuckGoNewsSearch,
            WebBaseContextTool,
        ],
    )
    reviewer = Worker(
        role="Review and Editing Specialist",
        instructions="Review the content for clarity, engagement, grammatical accuracy, and alignment with company values and refine it to ensure perfection. A meticulous editor with an eye for detail, ensuring every piece of content is clear, engaging, and grammatically perfect. Finally write the blog post to a file and return the same as output.",
        actions=[
            DuckDuckGoNewsSearch,
            WebBaseContextTool,
            WriteFileAction,
        ],
    )

    # Team Manager/Admin
    admin = Admin(
        # actions=[DuckDuckGoSearch],
        planner=TaskPlanner(human_intervene=False),
        memory=Memory(),
        llm=llm,
    )
    admin.assign_workers([researcher, writer, reviewer])

    res = admin.run(
        query="Write a blog post about future of AI. Feel free to write files to maintain the context.",
        description="Conduct a comprehensive analysis of the latest advancements in AI in 2024. Identify key trends, breakthrough technologies, and potential industry impacts. Using the insights provided, develop an engaging blog post that highlights the most significant AI advancements. Your post should be informative yet accessible, catering to a tech-savvy audience. Make it sound cool, avoid complex words so it doesn't sound like AI.",
    )

    # Print the results from the OpenAGI
    print("-" * 100)  # Separator
    Console().print(Markdown(res))
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
