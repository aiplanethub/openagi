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
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    config = AzureChatOpenAIModel.load_from_env_config()
    llm = AzureChatOpenAIModel(config=config)
    
    researcher = Worker(
        role="Research Analyst",
        instructions="""
        As a Research Analyst at a leading tech think tank, your task is to uncover cutting-edge developments in AI and data science. Follow these steps:

        1. Identify current hot topics: Use DuckDuckGoNewsSearch to find the latest news in AI and data science.
        2. Analyze trends: Look for patterns and recurring themes in the news results.
        3. Deep dive: For each identified trend, use WebBaseContextTool to gather more in-depth information.
        4. Evaluate impact: Assess the potential implications of each trend on the tech industry.
        5. Prioritize findings: Rank the trends based on their potential impact and novelty.
        6. Compile insights: Summarize your findings, including key statistics and expert opinions.
        7. Identify actionable takeaways: Suggest potential applications or areas for further research.
        8. Prepare a brief: Create a concise report of your findings, focusing on the top 3-5 trends.

        Your output should be a structured report that presents complex data as actionable insights.
        """,
        actions=[
            DuckDuckGoNewsSearch,
            WebBaseContextTool,
        ],
    )

    writer = Worker(
        role="Tech Content Strategist",
        instructions="""
        As a renowned Content Strategist, your task is to craft compelling content on tech advancements. Follow these steps:

        1. Review the research brief: Carefully read the report provided by the Research Analyst.
        2. Choose an angle: Decide on a unique perspective or narrative approach for the article.
        3. Outline the article: Create a structure that includes an engaging introduction, main body, and conclusion.
        4. Craft the introduction: Write a hook that captures the reader's attention and introduces the main topic.
        5. Develop the main body: For each key point:
        a. Explain the concept in simple terms.
        b. Provide relevant examples or case studies.
        c. Discuss potential implications or applications.
        6. Add expert insights: Incorporate quotes or perspectives from industry experts.
        7. Create visualizations: Suggest infographics or diagrams to illustrate complex ideas.
        8. Write the conclusion: Summarize the main points and provide a forward-looking statement.
        9. Optimize for engagement: Use subheadings, bullet points, and short paragraphs to improve readability.
        10. Review and refine: Do a final pass to ensure the article flows well and maintains reader interest throughout.

        Your output should be the complete article, transforming complex concepts into a compelling narrative.
        """,
        actions=[
            DuckDuckGoNewsSearch,
            WebBaseContextTool,
        ],
    )

    reviewer = Worker(
        role="Review and Editing Specialist",
        instructions="""
        As a meticulous editor with an eye for detail, your task is to review and refine the content to ensure perfection. Follow these steps:

        1. Initial read-through: Read the entire article without making any changes to get an overall sense of the content.
        2. Check for clarity: Identify any sections that may be unclear or confusing to the target audience.
        3. Enhance engagement: Suggest improvements to make the content more captivating and readable.
        4. Grammar and style check: 
        a. Correct any grammatical errors.
        b. Ensure consistent style and tone throughout the article.
        c. Check for proper punctuation and sentence structure.
        5. Fact-checking: Verify key facts and statistics using DuckDuckGoNewsSearch and WebBaseContextTool.
        6. Alignment with company values: Ensure the content reflects the company's stance and values.
        7. SEO optimization: Suggest improvements for search engine visibility without compromising quality.
        8. Formatting review: Check headings, subheadings, and overall structure for consistency and impact.
        9. Final polish: Make any last refinements to enhance the overall quality of the piece.
        10. Prepare for publication: 
            a. Write the final version of the blog post to a file using WriteFileAction.
            b. Generate a brief summary of the changes made and any final recommendations.

        Your output should be the path to the written file containing the perfected blog post, along with your summary of changes and recommendations.
        """,
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
    query="Write a blog post about the future of AI.",
    description="""
    Create an engaging blog post about the future of AI based on the latest advancements in 2024. Your task includes:

    1. Research recent AI breakthroughs and identify key trends.
    2. Analyze the potential impacts of these advancements on various industries and daily life.
    3. Write a blog post that:
       - Highlights 3-5 significant AI advancements
       - Explains their importance in simple, accessible terms
       - Discusses potential real-world applications
       - Addresses any relevant ethical considerations
    4. Ensure the post is:
       - Informative yet easy to understand for a tech-savvy audience
       - Engaging and exciting, conveying the wonder of AI's possibilities
       - Written in a conversational tone, avoiding complex jargon
       - Structured with a clear introduction, body, and conclusion
    5. Save the final blog post to a file and return the file path along with a brief summary.

    Feel free to use file writing for maintaining context during your research and writing process.
    """
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