import os
from openagi.actions.files import WriteFileAction
from openagi.actions.tools.ddg_search import DuckDuckGoNewsSearch
from openagi.actions.tools.webloader import WebBaseContextTool
from openagi.agent import Admin

from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
from openagi.llms.gemini import GeminiModel
from openagi.worker import Worker
from rich.console import Console
from rich.markdown import Markdown


if __name__ == "__main__":
    os.environ['GOOGLE_API_KEY'] = ""
    os.environ['Gemini_MODEL'] = "gemini-1.5-flash"
    os.environ['Gemini_TEMP'] = "0.1"

    config = GeminiModel.load_from_env_config()
    llm = GeminiModel(config=config)
    
    researcher = Worker(
        role="Research Analyst",
        instructions="""Identify and analyze current AI and data science trends. Use DuckDuckGoNewsSearch for latest news and WebBaseContextTool for deep dives. Assess impact, prioritize findings, and compile a concise report on top 3-5 trends with actionable insights.""",
        actions=[DuckDuckGoNewsSearch, WebBaseContextTool],
    )

    writer = Worker(
        role="Tech Content Strategist",
        instructions="""Craft a compelling article on tech advancements based on the research brief. Choose a unique angle, explain key points with examples, incorporate expert insights, and optimize for engagement. Deliver a complete, narrative-driven article.""",
        actions=[DuckDuckGoNewsSearch, WebBaseContextTool],
    )

    reviewer = Worker(
        role="Review and Editing Specialist",
        instructions="""Review and refine the article for clarity, engagement, and accuracy. Check grammar, facts, and SEO. Ensure alignment with company values. Write the final version using WriteFileAction. Provide file path and a summary of changes.""",
        actions=[DuckDuckGoNewsSearch, WebBaseContextTool, WriteFileAction],
    )

    # Team Manager/Admin
    admin = Admin(
        planner=TaskPlanner(human_intervene=False),
        memory=Memory(),
        llm=llm,
    )
    admin.assign_workers([researcher, writer, reviewer])

    res = admin.run(
    query="Write a blog post about the future of AI.",
    description="""Create an engaging blog post on AI's future based on 2024 advancements. Research breakthroughs, analyze impacts, and write a post highlighting 3-5 key advancements. Explain their importance, applications, and ethical considerations. Ensure the post is informative, accessible, and exciting for a tech-savvy audience. Save the final post to a file and return the file path with a brief summary."""
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