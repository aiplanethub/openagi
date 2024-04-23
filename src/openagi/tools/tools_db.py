from openagi.tools.integrations import (
    AskDocumentTool,
    DuckDuckGoSearchTool,
    ExaSearchTool,
    GithubSearchTool,
    GmailSearchTool,
    GoogleFinanceSearchTool,
    GoogleSerperSearchTool,
    NasaSearchTool,
    OpenWeatherMapSearchTool,
    PolygonSearchTool,
    SerperIntermediateSearchTool,
    SerperSpecificSearchTool,
    SqlSearchTool,
    WikipediaTool,
    XorbitsSearchTool,
    YahooFinanceTool,
    YoutubeSearchTool,
)

TOOLS_DICT = [
    {
        "category": "Search",
        **DuckDuckGoSearchTool.get_tool_info(),
        "output": "Search results after using the tool",
    },
    {
        "category": "gmail",
        **GmailSearchTool.get_tool_info(),
        "output": "Gmail results after using the tool.",
    },
    {
        "category": "Search",
        **GithubSearchTool.get_tool_info(),
        "output": "Github results after using the tool.",
    },
    {
        "category": "Compare",
        **AskDocumentTool.get_tool_info(),
        "output": "Document comparison results after using the tool.",
    },
    {
        "category": "Search",
        **NasaSearchTool.get_tool_info(),
        "output": "Nasa results after using the tool.",
    },
    {
        "category": "Search",
        **OpenWeatherMapSearchTool.get_tool_info(),
        "output": "OpenWeatherMap results after using the tool.",
    },
    {
        "category": "Search",
        **PolygonSearchTool.get_tool_info(),
        "output": "Polygon results after using the tool.",
    },
    {
        "category": "Search",
        **SqlSearchTool.get_tool_info(),
        "output": "Sql results after using the tool.",
    },
    {
        "category": "Search",
        **XorbitsSearchTool.get_tool_info(),
        "output": "Xorbits results after using the tool.",
    },
    {
        "category": "Search",
        **GoogleSerperSearchTool.get_tool_info(),
        "output": "GoogleSerper results after using the tool.",
    },
    {
        "category": "Search",
        **YoutubeSearchTool.get_tool_info(),
        "output": "Youtube results after using the tool.",
    },
    {
        "category": "Search",
        **GoogleFinanceSearchTool.get_tool_info(),
        "output": "GoogleFinance results after using the tool.",
    },
    {
        "category": "Search",
        **WikipediaTool.get_tool_info(),
        "output": "Wikipedia results after using the tool.",
    },
    {
        "category": "Search",
        **YahooFinanceTool.get_tool_info(),
        "output": "YahooFinance results after using the tool.",
    },
    {
        "category": "Search",
        **SerperSpecificSearchTool.get_tool_info(),
        "output": "SerperSpecific results after using the tool.",
    },
    {
        "category": "Search",
        **SerperIntermediateSearchTool.get_tool_info(),
        "output": "SerperIntermediate results after using the tool.",
    },
    {
        "category": "Search",
        **ExaSearchTool.get_tool_info(),
        "output": "ExaSearch results after using the tool.",
    },
]

TOOLS_DICT_MAPPING = {
    tool["tool_name"]: tool for tool in TOOLS_DICT
}  # This is created for faster lookups when using tools in the agents
