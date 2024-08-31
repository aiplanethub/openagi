# 🔍 JobSearch Agent

It utilize various tools for internet search and document comparison to fulfill its task. Upon finding the relevant job opportunities, The script configures the agent's role, goal, backstory, capabilities, and specific task to accomplish. Additionally, it initializes logging for debugging purposes and triggers the execution of the agent.

**Import Required Libraries**

First, we need to import the necessary modules. Each module serves a specific purpose in our script. We utilize various tools for internet search and document comparison to fulfill the agent's task. Here’s what each import does:

* `SearchApiSearch`, `GoogleSerpAPISearch` and `DuckDuckGoSearch` are tools for performing web searches.
* `Admin` manages the overall execution of tasks.
* `AzureChatOpenAIModel` is used to configure the large language model from Azure.
* `Memory` is for maintaining context during the agent's operations.
* `TaskPlanner` helps in decomposing tasks into manageable sub-tasks.
* `Worker` represents individual agents with specific roles and responsibilities.
* `Console` and `Markdown` from the `rich` library are used for printing formatted outputs.

```python
from openagi.actions.tools.serp_search import GoogleSerpAPISearch
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
from openagi.worker import Worker
from rich.console import Console
from rich.markdown import Markdown
import os
```

**Setup LLM**&#x20;

Next, we set up the environment variables and configure the Azure OpenAI model. This setup allows us to use Azure's GPT-4 model with the script. Setting up the environment variables ensures the necessary keys and endpoints are accessible during execution.

```python
os.environ["AZURE_BASE_URL"] = "https://<replace-with-your-endpoint>.openai.azure.com/"
os.environ["AZURE_DEPLOYMENT_NAME"] = "<replace-with-your-deployment-name>"
os.environ["AZURE_MODEL_NAME"] = "gpt4-32k"
os.environ["AZURE_OPENAI_API_VERSION"] = "2023-05-15"
os.environ["AZURE_OPENAI_API_KEY"] = "<replace-with-your-key>"

config = AzureChatOpenAIModel.load_from_env_config()
llm = AzureChatOpenAIModel(config=config)
```

**Define Workers**&#x20;

We define workers with specific roles and instructions. Each worker agent is equipped with the tools necessary to perform their designated tasks. The worker in this script is set up to search for job opportunities using DuckDuckGo.

```
websearcher = Worker(
    role="SW",
    instructions="""
    You are an Expert Python SW Developer with deep knowledge of job markets.
    - Focus on SDE2 (Software Development Engineer II) positions
    - Look for roles requiring 2+ years of Python experience
    - Consider various industries and company sizes
    - Pay attention to job descriptions, required skills, and company culture
    """,
    actions=[DuckDuckGoSearch],
)
```



**Define Admin**&#x20;

The `Admin` agent manages the workers and executes the tasks. It is configured to use the task planner without human intervention and maintains context using memory.

```python
admin = Admin(
    actions=[DuckDuckGoSearch],
    planner=TaskPlanner(human_intervene=False),
    memory=Memory(),
    llm=llm,
)
admin.assign_workers([websearcher])
```

**Execute Agent LLM**&#x20;

The admin runs with a specific query to find job opportunities. The query includes detailed instructions on what information to gather and how to present it.

```python
    res = admin.run(
        query="""
        Provide a list of at least 10 SDE2 job opportunities suitable for candidates with 2+ years of Python experience.
        For each job, include:
        1. Company name and location
        2. Job title
        3. Key responsibilities
        4. Required skills
        5. Any standout perks or benefits
        6. Application link or process (if available)
        """,
        description="""
        You are an expert Internet Job Searching agent. Your task is to:
        - Find the most relevant and high-quality job opportunities
        - Ensure jobs match the specified experience level and skill set
        - Provide a diverse range of companies and industries
        - Verify the credibility of job postings
        - Organize the information in a clear, easy-to-read format
        - Highlight any unique or particularly attractive aspects of each role
        """,
    )
```

**Print the Results**

Finally, the results are outputted using the `rich` library, which allows us to print the data in a nicely formatted markdown.

```python
# Print the results from the OpenAGI
print("-" * 100)  # Separator
Console().print(Markdown(res))
```

#### Sample Output

The expected output is a list of job opportunities with detailed descriptions. Each job entry includes the company name, location, job title, responsibilities, required skills, standout perks, and an application link.

```markdown
Job Opportunities and Descriptions in Finance Technology

1. **Strategic Programs Finance Tech Manager** - The Finance technology team supervises a large portfolio of ongoing transformation programs that are each operated by individual teams from Finance, CIO and more. [More details](https://www.accenture.com/in-en/careers/jobdetails?id=R354135_en)

2. **Finance Manager - FinTech** - A professional with 2+ years of experience is needed for end to end Business Finance like Strategic Planning, preparing & managing the finances. [More details](https://iimjobs.com/j/finance-manager-fintech-3-8-yrs-1194909)

3. **Working in Fintech** - Fintech is a combination of finance and technology. This combination has set high standards in the field of employment. [More details](https://imarticus.org/blog/what-is-job-description-to-work-in-fintech-and-what-are-the-skills-required/)

4. **Finance Technology Role** - Discover the typical qualifications and responsibilities for a role in Finance Technology. [More details](https://www.glassdoor.co.in/Career/technology-finance-career_KO0,18.htm)

5. **Strategic Programs Finance Tech Manager - Accenture** - Job Description for Strategic Programs Finance Tech Manager in Accenture in Gurgaon for 7 to 11 years of experience. [More details](https://www.naukri.com/job-listings-strategic-programs-finance-tech-manager-accenture-solutions-pvt-ltd-gurugram-7-to-11-years-020524909932)

6. **Financier Job** - The core responsibilities of finance professionals involve analyzing data, reconciling, providing financial advice, optimizing cash flow, and preparing. [More details](https://emeritus.org/in/learn/financier-job-roles-and-responsibilities/)

7. **12 Finance Tech Jobs** - Lucrative finance tech jobs including Compliance specialist, Cybersecurity specialist, App developer, Automation engineer, UX designer. [More details](https://www.indeed.com/career-advice/finding-a-job/finance-tech-jobs)

8. **FIN-Global Middle Office** - Ability to understand the booking structure for complex trades and raise relevant issues to Product Control management. Good Logical reasoning skills, ability. [More details](https://careers.nomura.com/Nomura/job/Mumbai-FIN-Global-Middle-Office/1128931300/)

9. **Financial Technology jobs in India** - Experience level. Internship (48). Entry level (1,708). Associate (588). Mid-Senior level (5,269). Director (402). [More details](https://in.linkedin.com/jobs/financial-technology-jobs)

10. **Senior Executive/Middle level executive - Mumbai** - The ideal candidate will be responsible for identifying, analyzing, and strategizing the resolution of non-performing assets (NPAs) acquired. [More details](https://www.naukri.com/job-listings-senior-executive-middle-level-executive-acaipl-investment-financial-services-mumbai-3-to-8-years-080524005387)
```

####
