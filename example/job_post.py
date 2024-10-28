import os
from openagi.actions.tools.webloader import WebBaseContextTool
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.actions.files import WriteFileAction, ReadFileAction
from openagi.agent import Admin
from openagi.llms.gemini import GeminiModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
from openagi.worker import Worker
from rich.console import Console
from rich.markdown import Markdown



if __name__ == "__main__":
    os.environ['GOOGLE_API_KEY'] = ""
    os.environ['Gemini_MODEL'] = "gemini-1.5-flash"
    os.environ['Gemini_TEMP'] = "0.1"

    # Team Members
    researcher = Worker(
        role="Research Analyst",
        instructions="Analyze AI Planet (https://aiplanet.com/) for company culture, products/services, required skills (Python, ReactJS, Golang, NodeJS, SQL), ML/DL experience, and unique selling points. Compile findings for the writer.",
        actions=[DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )

    writer = Worker(
        role="Job Description Writer",
        instructions="Create an engaging SDE 2 Full Stack Developer job posting for AI Planet. Include company mission, responsibilities, required skills, desired ML/DL experience, qualifications, growth opportunities, and company culture. Use researcher's insights to align with company values.",
        actions=[ReadFileAction, DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )

    reviewer = Worker(
        role="Review and Editing Specialist",
        instructions="Refine the job posting for clarity, engagement, and technical accuracy. Ensure alignment with AI Planet's values, optimize readability, and polish the final description for an SDE 2 Full Stack Developer role.",
        actions=[ReadFileAction, DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )

    # Team Manager/Admin
    admin = Admin(
        actions=[DuckDuckGoSearch],
        planner=TaskPlanner(human_intervene=False),
        memory=Memory(),
        llm=llm,
    )
    admin.assign_workers([researcher, writer, reviewer])

    res = admin.run(
        query="Create a job posting for an SDE 2 Full Stack Developer at AI Planet",
        description="Develop a compelling job description for an SDE 2 Full Stack Developer at AI Planet (https://aiplanet.com/). Include required skills (Python, ReactJS, Golang, NodeJS, SQL) and preferred ML/DL experience. Reflect AI Planet's culture and focus on AI and ML technology.",
    )

    # Print the results from the OpenAGI
    print("-" * 100)  # Separator
    Console().print(Markdown(res))

"""
Job Title: SDE 2 - Full Stack Developer
Company: AI Planet

About Us:
AI Planet, formerly known as DPhi, is an organization harnessing the power of AI to tackle real-life challenges. We provide products that enable companies and institutions to develop and deploy a variety of AI models and solutions. Our unique ecosystem is designed to empower businesses and individuals to seamlessly learn, develop, and deploy AI models and solutions to address real-life problems.

Job Description:
We are seeking a seasoned Full Stack Developer to join our team. You'll be part of a cross-functional team that's responsible for the full software development life cycle, from conception to deployment. You should be comfortable with both front-end and back-end coding languages, development frameworks, and third-party libraries. You should also be a team player with a knack for visual design and utility.

Key Responsibilities:
- Developing front-end website architecture.
- Designing user interactions on web pages.
- Developing back-end website applications.
- Creating servers and databases for functionality.
- Ensuring cross-platform optimization for mobile phones.
- Ensuring responsiveness of applications.
- Working alongside graphic designers for web design features.
- Seeing through a project from conception to finished product.
- Meeting both technical and consumer needs.
- Staying abreast of developments in web applications and programming languages.

Key Qualifications:
- Degree in Computer Science.
- Strong organizational and project management skills.
- Proficiency with fundamental front-end languages such as HTML, CSS, and JavaScript.
- Familiarity with JavaScript frameworks such as Angular JS, React, and Amber.
- Proficiency with server-side languages such as Python, Ruby, Java, PHP, and .Net.
- Familiarity with database technology such as MySQL, Oracle, and MongoDB.
- Excellent verbal communication skills.
- Good problem-solving skills.
- Attention to detail.

If you're interested in creating a user-friendly environment by writing code and moving forward in your career, then this job is for you. We expect you to be a tech-savvy professional, who is curious about new digital technologies and aspires to combine usability with visual design. Ultimately, you should be able to translate our company and customer needs into functional and appealing interactive applications.
"""
