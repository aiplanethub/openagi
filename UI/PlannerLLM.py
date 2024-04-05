import logging

from openagi.llms import AzureChatOpenAIModel, OpenAIModel
from openagi.utils.yamlParse import read_yaml_config


def executor_llm(llm_choice):
    print(f"{llm_choice=}")
    if llm_choice == "azure-openai":
        config = AzureChatOpenAIModel.load_from_yml_config()
        llm_1 = AzureChatOpenAIModel(config=config)
    elif llm_choice == "openai":
        config = OpenAIModel.load_from_yml_config()
        llm_1 = OpenAIModel(config=config)
    else:
        raise ValueError("Invalid LLM choice. Please provide a valid LLM choice.")
    return llm_1


def generateDAG(objective, tool_list, llm_choice):
    # Prompts to get response
    objective_prefix = """Now you will be provided with an Objective as input and you have to return the Division of tasks to perform the objective flawlessly as shown in the example with the help of relevant tools.
The User can also provide you with additional tools. The additional tools will be given in JSON format.
This is the Objective:"""

    question = (
        """{
    "OBJECTIVE" : """
        + objective
        + """,
    "llm_api":"""
        + llm_choice
        + """,
    "tool_list" : """
        + str(tool_list)
        + """
}"""
    )

    model_prefix = """You are an intelligent and smart assistant which is capable of smartly answering about how to solve a given objective in sequential tasks using the available tools."""

    what_to_accomplish = """You are provided with with an Objective/Aim Task, the `llm` we will use and the list of tools. You have to tell the division of the task in small subtasks which can be individually handled by an `Agent` individually."""

    explanation = f"""Explanation of some terms is given below:
`llm` : A Large language model which is capable of giving high quality text output. The possible values for this are ["azure", "gemini", "local"]
`Agent` : A tool which can solve a given task using a set of tools and a `llm`

How you will approach the given problem will be explained using some examples.

{objective_prefix}
{question}"""

    output_prefix = (
        """You have to generate Division of work in proper JSON format:
[
    {
        "agentName" : "Name of the Agent", // Name of the Agent based on the type of task it will handle, for example `RESEARCHER`, `WRITER`
        "role" : "The role of the Agent", // A small and concise sentence describing the role of the Agent
        "goal" : "The goal of the Agent", // The goal which the agent has to achieve after completion of the task assigned to it
        "backstory" : "The backstory or the system prompt", // A concise sentence which gives a brief description about the things which the agent can handle
        "capability" : "llm_task_executor", // This parameter tells what kind of capability the Agent has. This parameter can have 3 possible values ["search_executor", "llm_task_executor", "tool_executor"]
        "task" : "The task of the agent", // The task which has to be handled by the Agent.
        "output_consumer_agent" : ["The agentName of the agent which will recieve the output of this agent as the input"], // The output of the current agent will be given to the output_consumer_agent as an input, so sequential tasks can be executed. The value of this parameter will be "HGI" for the last agent in the sequence.
        "llm_api": """
        + '"'
        + llm_choice
        + '"'
        + """,
        "tools_list" : ["List of required tools"] // The list of tools required by this Agent to execute its task. The list of available tools is given in the input. IF a tool is required which does not exist in the tools_list in the input then a description of the required tool has to be extended in the tools_list. A possible example of the tool_list is ["SearchInternetGoogle", "A tool capable of parsing strings in JSON format"]
    }
]"""
    )

    example = """Example:

The Input provided Data
{
    "OBJECTIVE" : "create separate emails to doctors and general public after summarizating recent trends in covid treatment and precautions after mid 2023 using azure",
    "llm" : "azure", // The llm which will be used by an individual Agent to solve a particular task
    "tool_list" : [
        "DuckDuckGoSearchTool", // A tool that can be used to search for words, documents, images, videos, news, maps and text translation using the DuckDuckGo.com search engine. Downloading files and images to a local hard drive.
        "exaSearchTool", // A tool which can be used to do a Exa Search and provide sources for the same.
        "WikipediaTool", // A tool designed to Tool that searches the Wikipedia API for a specific query
        "GoogleSerperSearchTool", // Tool used to perform a search online using a Google SERP (Search Engine Results Page) scraping API wrapper.
        "DocumentCompareSearchTool", // A tool which can be used to by the agent to question uploaded files by the user.
        "GithubSearchTool", // A tool which can be used to retrieve information regarding respective repository like code changes, commits, active PRs, issues, etc by using natural language.
        "GmailSearchTool", // A tool which can be used to perform actions on gmail by using natural language
        "NasaSearchTool", // A tool which can be used to retrieve information from NASA database like images, videos, documents, etc by using natural language
        "OpenWeatherMapSearchTool", // A tool which can be used to retrieve information about weather of any place in the world.
        "XorbitsSearchTool", // A tool which can be used to retrieve information from files by performing pandas or numpy code by using natural language.
        "YoutubeSearchTool", // A tool that can be used to search for videos on YouTube based on specific queries.
        "SerperSpecificSearchTool", // A tool which can be used to scrape information from the search engine for a specific type and period using natural language
        "SerperIntermediateSearchTool", // Searches for information on the internet
    ]
}"""

    expected_output_format = (
        """The Expected output in JSON format:

[
    {
        "agentName" : "RESEARCHER",
        "role" : "Searches about relevant information from various sources", 
        "goal" : "search for latest trends in Corona and Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
        "backstory" : "Has the capability to execute internet search tool", 
        "capability" : "search_executor",
        "task" : "search internet for the goal for the trends after first half of 2023", 
        "output_consumer_agent" : ["SUMMARIZER"],
        "llm_api":"""
        + '"'
        + llm_choice
        + '"'
        + """,
        "tools_list" : ["SearchInternetGoogle", "SearchInternetDuckDuck"] 
    },
    {
        "agentName" : "SUMMARIZER",
        "role" : "SUMMARIZER", 
        "goal" : "summarize input into presentable points",
        "backstory" : "Expert in summarising the given text", 
        "capability" : "llm_task_executor",
        "task" : "summarize points to present to health care professionals and general public separately", 
        "output_consumer_agent" : ["EMAILER"],
        "llm_api":"""
        + '"'
        + llm_choice
        + '"'
        + """,
        "tools_list" : []
    },
    {
        "agentName" : "Name of the Agent" ,
        "role" : "EMAILER" ,
        "goal" : "composes the email based on the content", 
        "backstory" : "Good in composing precise emails", 
        "capability" : "llm_task_executor",
        "task" : "composes email based on summary to doctors and general public separately into a file with subject-summary and details", 
        "output_consumer_agent" : ["HGI"],
        "llm_api":"""
        + '"'
        + llm_choice
        + '"'
        + """,
        "tools_list" : []
    },
]


End of the example."""
    )

    final_prompt = f"""{model_prefix}\n{what_to_accomplish}\n\n{explanation}\n\n{output_prefix}\n\n{example}\n{expected_output_format}\n"""
    llm = executor_llm(read_yaml_config("PLANNER_LLM"))
    resp = llm.run(final_prompt)
    logging.debug(f"LLM generated content {resp}")
    return resp


if __name__ == "__main__":
    obj = "Write a Newspaper Article on the recent event of the pre-marriage of the son of the famous millionaire Mukesh Ambani."
    obj = "Pros and cons of buying Reliance  stock. Provide your recommendations."
    tool_list = [
        {
            "MyCalculator": "Calculated the values of mathematical expressions with the help of python."
        }
    ]
    reply = generateDAG(obj, tool_list)
