from openagi.actions.tools.ddg_search import DuckDuckGoNewsSearch
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
    actions=[
        DuckDuckGoNewsSearch
    ],  # Actions that the Agent can use to acheive the given objective
    planner=TaskPlanner(human_intervene=False),
)

# Run the Agent with a query and description of the query.
res = admin.run(
    query="Recent AI News from Microsoft",
    description="",
)

# Print the results from the OpenAGI
print("-" * 100)  # Separator
print(res)
print("-" * 100)  # Separator
Console().print(Markdown(res))


# The Agent did some research using the given actions and share the itinerary.
"""
## Microsoft's Week of AI Starts With News About PCs

![Image](https://img-s-msn-com.akamaized.net/tenant/amp/entityid/BB1mJB6C.img?w=1280&h=826&m=4&q=67)

*Date: 2024-05-21T17:46:00+00:00*

Microsoft's stock idled last week, trading in line with the market, while Google lifted shares of its parent, Alphabet, with demos of its artificial intelligence might. Expect a fusillade of news showing that Microsoft has as much AI as Google.

**Source:** [Barron's on MSN.com](https://www.msn.com/en-us/news/technology/microsoft-s-week-of-ai-starts-with-news-about-pcs/ar-BB1mJDev)

---

## Microsoft Unveils AI Strategy Updates, Touts 'Fit-To-Purpose' Models, Plans To Expand Azure Footprint

![Image](https://cdn.benzinga.com/files/imagecache/1024x768xUP/images/story/2024/05/21/Microsoft-Azure.jpeg)

*Date: 2024-05-21T21:28:00+00:00*

Microsoft embedded AI at every level of the Microsoft Cloud and first-party assets like GitHub, Power Platform, and Security Services.

**Source:** [Business Insider](https://markets.businessinsider.com/news/stocks/microsoft-unveils-ai-strategy-updates-touts-fit-to-purpose-models-plans-to-expand-azure-footprint-1033409032)

---

## Microsoft Build 2024: The Biggest News In AI, Copilots, Data, Security

![Image](https://www.crn.com/news/ai/2024/media_14070b9c216e3fcae8fdeb440d6e4d7b8fd66d593.jpeg?width=1200&format=pjpg&optimize=medium)

*Date: 2024-05-21T13:14:00+00:00*

News around Microsoft Copilot in Azure, Team Copilot and Defender for Cloud are some of the most exciting updates to come out of Build 2024.

**Source:** [CRN](https://www.crn.com/news/ai/2024/microsoft-build-2024-the-biggest-news-in-ai-copilots-data-security)

---

## Watch the Microsoft Build 2024 keynote live here: More on Copilot+ and AI-enhanced PCs

![Image](https://s.yimg.com/ny/api/res/1.2/pz8afy8PRMVhmHAtZS03jw--/YXBwaWQ9aGlnaGxhbmRlcjt3PTEyMDA7aD02NzA-/https://s.yimg.com/os/creatr-uploaded-images/2024-05/c1f32200-16d0-11ef-bff7-037a785b4e97)

*Date: 2024-05-21T14:41:00+00:00*

Microsoft is streaming its Build 2024 keynote on Tuesday. Here's how to watch -- and what to know about the lower-profile event the day before.

**Source:** [Yahoo](https://www.yahoo.com/news/watch-microsoft-build-2024-keynote-live-here-more-on-copilot-and-ai-enhanced-pcs-003204775.html)

---

## Microsoft introduces Phi-Silica, a 3.3B parameter model made for Copilot+ PC NPUs

![Image](https://venturebeat.com/wp-content/uploads/2024/05/DSC06049.jpg?w=1200&strip=all)

*Date: 2024-05-22T00:14:00+00:00*

Phi-Silica is the fifth variation of Microsoft's Phi-3 model, joining Phi-3-mini with 3.8 billion parameters, Phi-3-small with 7 billion parameters, Phi-3-medium with 14 billion parameters, and Phi-3-vision with 4.2 billion parameters.

**Source:** [VentureBeat](https://venturebeat.com/ai/microsoft-introduces-phi-silica-a-3-3b-parameter-model-made-for-copilot-pc-npus/)

---

## Microsoft Build 2024: news and announcements from the developer conference

*Date: 2024-05-22T00:45:00+00:00*

Microsoft is kicking off its three-day Build developer conference on Tuesday, May 21st, with a livestream starting at 11:30AM ET / 8:30AM PT. It'll lead into an in-person keynote led by CEO Satya Nadella, which commences at 12PM ET / 9AM PT, followed by developer sessions that will come available to check out online.

**Source:** [The Verge](https://www.theverge.com/2024/5/21/24161221/microsoft-build-2024-news-ai-copilot-plus/archives/2)

---

## Microsoft's Copilot+ PCs, New Surface Laptops and More Pre-Build 2024 Announcements

![Image](https://assets.techrepublic.com/uploads/2024/05/tr_20240522-microsoft-copilot-pcs-surface-laptops.jpg)

*Date: 2024-05-22T01:14:00+00:00*

During a keynote event before its Build 2024 conference, Microsoft announced Copilot+ PCs, Surface Pro 11, Surface Laptop 7 and more.

**Source:** [TechRepublic](https://www.techrepublic.com/article/microsoft-copilot-pcs-surface-laptops/)

---

## Microsoft's Team Copilot is a virtual team member that can run meetings and projects

![Image](https://venturebeat.com/wp-content/uploads/2024/05/adobe-firefly-robot-helping-human-in-office.jpg?w=1200&strip=all)

*Date: 2024-05-21T22:29:00+00:00*

Microsoft introduces Team Copilot, a virtual team member to run meetings, take notes, and handle project management, coming later in 2024.

**Source:** [VentureBeat](https://venturebeat.com/ai/microsoft-introduces-team-copilot-to-run-meetings-and-projects/)

---

## Microsoft's AI will be inside Minecraft, and other Xbox, PC games: new Copilot features will search your inventories, offer tips and guides

![Image](https://cdn.mos.cms.futurecdn.net/QK8cAuTq6XEmrbeQyQJjvB-1200-80.jpg)

*Date: 2024-05-20T21:46:00+00:00*

Microsoft Copilot is a suite of tools based on OpenAI's ChatGPT and Dalle-3 language models to help users with every day queries. Microsoft demonstrated Copilot AI gaming features at today's Surface and AI event, detailing how Copilot will help gamers find information more easily.

**Source:** [Windows Central on MSN.com](https://www.msn.com/en-us/news/technology/microsofts-ai-will-be-inside-minecraft-and-other-xbox-pc-games-new-copilot-features-will-search-your-inventories-offer-tips-and-guides/ar-BB1mJyzz)

---

## Microsoft's Build Conference This Week To Showcase AI Push, New Products And More: Here's What Investors Should Know

![Image](https://cdn.benzinga.com/files/imagecache/1024x768xUP/images/story/2024/05/20/Microsoft-Copilot.jpeg)

*Date: 2024-05-20T15:25:00+00:00*

Microsoft is set to kick off its annual Build developer conference, where the company will highlight its AI initiatives and new product launches.

**Source:** [Business Insider](https://markets.businessinsider.com/news/stocks/microsoft-s-build-conference-this-week-to-showcase-ai-push-new-products-and-more-here-s-what-investors-should-know-1033403395)
"""
