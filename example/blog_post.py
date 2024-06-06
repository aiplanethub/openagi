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



# Output(The agent created a file with the below content):
"""
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
"""