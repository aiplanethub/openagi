from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.agent import Admin
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.planner.task_decomposer import TaskPlanner
from rich.console import Console
from rich.markdown import Markdown

# Set the AZURE_BASE_URL, AZURE_DEPLOYMENT_NAME, AZURE_MODEL_NAME, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_API_KEY as environment variables
config = AzureChatOpenAIModel.load_from_env_config()
llm = AzureChatOpenAIModel(config=config)


# Setup an Admin Agent
admin = Admin(
    llm=llm,
    actions=[DuckDuckGoSearch],  # Actions that the Agent can use to acheive the given objective
    planner=TaskPlanner(human_intervene=False),
)

# Run the Agent with a query and description of the query.
res = admin.run(
    query="Recent AI News Microsoft",
    description="",
)

# Print the results from the OpenAGI
print("-" * 100)  # Separator
Console().print(Markdown(res))


# The Agent did some research using the given actions and share the itinerary.
"""
## Microsoft AI Blogs | Artificial Intelligence News and Updates
Realize business value with AI. Optimize your organization at every level and uncover valuable new opportunities with Microsoft AI solutions. Microsoft AI Blog keeps you up-to-date about the latest advancements in artificial intelligence and their integration into our products and platforms. [Read more](https://www.microsoft.com/en-us/ai/blog/)

## Microsoft wants to make Windows an AI operating system, launches ...
The latest Surface Laptop — available with a 13.8- or 15-inch display — has been redesigned with "modern lines" and thinner screen bezels. [Read more](https://techcrunch.com/2024/05/20/microsoft-build-2024-windows-ai-operating-system-copilot-plus-pcs/)

## Accelerating innovation: A new era of AI at work begins
At Microsoft, we continue to innovate across platforms to unlock everyone's full potential, with AI giving time back in the day to be more creative, more strategic and more innovative. Yusuf Mehdi, Executive Vice President, at Microsoft, announced today how we are revolutionizing the PC for the AI era with Copilot+ PCs. [Read more](https://blogs.windows.com/windowsexperience/2024/05/20/accelerating-innovation-a-new-era-of-ai-at-work-begins/)

## Introducing GPT-4o: OpenAI's new flagship ... - azure.microsoft.com
Exciting future developments: GPT-4o at Microsoft Build 2024 . We are eager to share more about GPT-4o and other Azure AI updates at Microsoft Build 2024, to help developers further unlock the power of generative AI. [Read more](https://azure.microsoft.com/en-us/blog/introducing-gpt-4o-openais-new-flagship-multimodal-model-now-in-preview-on-azure/)

## Microsoft debuts 'Copilot+' PCs with AI features | Reuters
Microsoft on Monday debuted a new category of personal computers with AI features as it rushes to build the emerging technology into products across its business and compete with Alphabet and Apple. [Read more](https://www.reuters.com/technology/microsoft-unveil-ai-devices-features-ahead-developer-conference-2024-05-20/)

## Microsoft Unveils Advanced AI-Powered Innovations
Microsoft's new Surface devices provide the perfect platform to showcase the amazing AI capabilities of the latest Windows update. [Read more](https://news.microsoft.com/en-cee/2023/09/21/microsoft-unveils-advanced-ai-powered-innovations/)

## Microsoft Unveils New AI Software, Devices as It Battles Apple, Google
Microsoft Corp. introduced new software and computers infused with artificial intelligence features — stepping up its efforts to out-compete Alphabet Inc.'s Google and Apple Inc. [Read more](https://www.bloomberg.com/news/articles/2024-05-20/microsoft-unveils-new-ai-software-devices-as-it-battles-apple-google)

## Microsoft will build AI into new laptops, firing shot at Apple
Microsoft said OpenAI's latest AI models — GPT4o — will also be included on its new computers. Microsoft signed a multibillion-dollar deal with OpenAI in early 2023, gaining access to its ... [Read more](https://www.washingtonpost.com/technology/2024/05/20/microsoft-build-surface-ai-event-copilot/)

## Announcing Microsoft's AI Customer Commitments
That's why today we are announcing three AI Customer Commitments to assist our customers on their responsible AI journey. [Read more](https://blogs.microsoft.com/blog/2023/06/08/announcing-microsofts-ai-customer-commitments/)

## Microsoft and LinkedIn release the 2024 Work Trend Index on the state ...
For employees, AI raises the bar and breaks the career ceiling. We also see AI beginning to impact the job market. While AI and job loss are top of mind for some, our data shows more people are eyeing a career change, there are jobs available, and employees with AI skills will get first pick. [Read more](https://blogs.microsoft.com/blog/2024/05/08/microsoft-and-linkedin-release-the-2024-work-trend-index-on-the-state-of-ai-at-work/)
"""
