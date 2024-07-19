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
        instructions="""
        Analyze AI Planet (https://aiplanet.com/) to extract key information:
        - Company culture and core values
        - Main products or services in AI and ML
        - Required technical skills (Python, ReactJS, Golang, NodeJS, SQL)
        - Desired experience in Machine Learning and Deep Learning
        - Any unique selling points or benefits of working at AI Planet
        Compile findings in a structured format for the writer.
        """,
        actions=[DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )

    writer = Worker(
        role="Job Description Writer",
        instructions="""
        Create an engaging SDE 2 Full Stack Developer job posting:
        - Craft a compelling introduction highlighting AI Planet's mission
        - List key responsibilities for a Full Stack SDE 2 role
        - Detail required skills (Python, ReactJS, Golang, NodeJS, SQL)
        - Mention desired ML/DL experience as a plus
        - Include qualifications and years of experience expected
        - Highlight growth opportunities and company culture
        - Add a call-to-action for applying
        Use the researcher's insights to align with company values.
        """,
        actions=[ReadFileAction, DuckDuckGoSearch, WebBaseContextTool, WriteFileAction],
    )

    reviewer = Worker(
        role="Review and Editing Specialist",
        instructions="""
        Refine the job posting for optimal impact:
        - Ensure clarity and engaging tone throughout
        - Verify technical accuracy of required skills
        - Check for grammar, spelling, and punctuation
        - Confirm alignment with AI Planet's values and culture
        - Optimize structure for easy readability (use bullet points, short paragraphs)
        - Ensure the job title and requirements match (SDE 2 Full Stack Developer)
        Make final edits to polish the job description.
        """,
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
        description="""
        Develop a compelling job description for AI Planet (https://aiplanet.com/):
        - Position: SDE 2 Full Stack Developer
        - Required skills: Python, ReactJS, Golang, NodeJS, SQL
        - Preferred: Experience with Machine Learning and Deep Learning
        - Company focus: Technology, AI and ML
        Ensure the posting reflects AI Planet's culture and attracts qualified candidates.
        """
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
