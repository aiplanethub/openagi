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

Below is the output from the agent:

```
## Job Opportunities and Descriptions in Finance Technology

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

Below is the output from the agent:
```
The Future of AI: Key Trends and Innovations in 2024

Introduction
Artificial Intelligence (AI) continues to transform businesses, industries, and various aspects of our daily lives. As we move into 2024, the advancements in AI are set to shape the future in unprecedented ways. This blog post explores the key trends, breakthrough technologies, and potential industry impacts of AI in 2024.

Key Trends and Breakthrough Technologies
1. **AI Market Growth**: The AI market is projected to reach USD 2575.16 billion by 2032, driven by innovations in educational tools, natural language processing (NLP), and healthcare applications (MSN).
2. **Transformative AI Innovations**: AI is rapidly integrating into various sectors, transforming businesses and industries while raising potential challenges like energy consumption (Forbes).

Industry and Safety Concerns
1. **Transparency and Ethics**: Former OpenAI employees have called for increased transparency and safety measures in AI development, emphasizing the importance of ethical considerations (TechCrunch).
2. **Ethical Use in Legal and Healthcare Sectors**: The ethical use of AI is crucial, particularly in the legal and healthcare sectors, to avoid potential legal implications and ensure quality patient outcomes (Law, Forbes).

Notable Company Announcements and Market Movements
1. **Nvidia's Leadership**: Nvidia's announcements at Computex 2024 highlighted significant AI advancements and partnerships, showcasing their leadership in AI technology (SiliconANGLE).
2. **Market Performance**: Nvidia surpassed Apple in market cap, with both companies reaching a $3 trillion valuation, underscoring Nvidia's dominance in the AI market (MSN).

Sector-Specific Impacts
1. **AI in Finance**: AI is revolutionizing banking and financial software development, enhancing financial services and customer experiences (TechBullion).
2. **AI in Healthcare**: AI holds great potential in healthcare for improving patient outcomes but requires careful implementation and ethical guidelines (Forbes).
3. **AI/ML-Enabled Medical Devices**: Innovators like Tejesh Marsale are leading advancements in AI/ML-enabled medical devices, pushing the boundaries of healthcare technology (TechBullion).

Conclusion
The future of AI in 2024 is marked by rapid advancements, significant market growth, and transformative impacts across various sectors. However, ethical considerations and transparency are paramount to ensure responsible AI development. By balancing innovation with ethical practices, we can harness the full potential of AI to create a better future for all.
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
