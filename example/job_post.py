from openagi.actions.tools.webloader import WebBaseContextTool
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.actions.files import WriteFileAction, ReadFileAction
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
        instructions="Analyze the company website and provided description to extract insights on culture, values, and specific needs. Expert in analyzing company cultures and identifying key values and needs from various sources, including websites and brief descriptions.",
        actions=[DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )
    writer = Worker(
        role="Job Description Writer",
        instructions="Use insights from the Research Analyst to create a detailed, engaging, and enticing job posting. Skilled in crafting compelling job descriptions that resonate with the company's values and attract the right candidates.",
        actions=[ReadFileAction, DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )
    reviewer = Worker(
        role="Review and Editing Specialist",
        instructions="Review the job posting for clarity, engagement, grammatical accuracy, and alignment with company values and refine it to ensure perfection. A meticulous editor with an eye for detail, ensuring every piece of content is clear, engaging, and grammatically perfect.",
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
        query="SDE 2 Full Stack Developer",
        description="Company - AI Planet(formerly DPhi), https://aiplanet.com/. Need a Full Stack SDE 2 with skills in stacks like Python, ReactJS, Golang, NodeJS, and SQL. Experience with Machine Learning and Deep Learning is a plus. Company Domain - Technology, AI and ML.",
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
