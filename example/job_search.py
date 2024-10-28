
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.agent import Admin
from openagi.planner.task_decomposer import TaskPlanner
from rich.console import Console
from rich.markdown import Markdown
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.planner.task_decomposer import TaskPlanner
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.actions.files import WriteFileAction
from openagi.agent import Admin




import os
from getpass import getpass


config = AzureChatOpenAIModel.load_from_env_config()
llm = AzureChatOpenAIModel(config=config)

plan = TaskPlanner(autonomous=True) 

admin = Admin(
    actions = [DuckDuckGoSearch],
    planner = plan,
    llm=llm,
    
)
res = admin.run(
    query="Create a job posting for an SDE 2 Full Stack Developer at AI Planet",
    description="""
    AI Planet (https://aiplanet.com/), a cutting-edge company at the forefront of technology, artificial intelligence, 
    and machine learning, is seeking a talented SDE 2 Full Stack Developer to join our innovative team. The ideal candidate will possess strong proficiency in Python, 
    ReactJS, Golang, NodeJS, and SQL. Experience with Machine Learning and Deep Learning is highly preferred, as it aligns with our company's core focus. At AI Planet, 
    we foster a culture of innovation, collaboration, and continuous learning. We're looking for a passionate developer who can contribute to our dynamic environment and 
    help drive our mission to advance AI technology. If you're excited about pushing the boundaries of what's possible in the world of AI and want to work with a team of 
    like-minded professionals, we encourage you to apply and become part of our journey in shaping the future of technology. 
    """,
)
print(res)



# Job Posting

## Company: AI Planet

### Role: SDE 2 Full Stack Developer

# **Description:**

# AI Planet is seeking a passionate and talented SDE 2 Full Stack Developer to design, develop, and maintain web applications. The ideal candidate will collaborate with cross-functional teams, write clean and efficient code, conduct code reviews, troubleshoot issues, and optimize application performance.

# **Qualifications:**

# - Bachelor's degree in a relevant field
# - Experience with front-end technologies (HTML, CSS, JavaScript, frameworks like React)
# - Experience with back-end technologies (Node.js, Python, Java)
# - Proficiency with database systems and version control (Git)
# - Strong communication skills

# **Preferred Qualifications:**

# - Experience with cloud platforms
# - Familiarity with DevOps practices
# - Experience with containerization (Docker, Kubernetes)

# **Benefits:**

# - Competitive salary
# - Health insurance
# - Flexible work hours
# - Professional development opportunities
# - Inclusive culture

# **Company Culture:**

# AI Planet fosters a culture of innovation, collaboration, and continuous learning. We emphasize adaptability and provide a supportive environment where leveraging generative AI is encouraged.
