import importlib
import json
import logging
from typing import Dict, List
import os

from langchain.chains import LLMChain
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from openagi.llms.base import LLMBaseModel
from openai import OpenAI


def extract_json_from_string(text_block):
    # Load JSON string into Python object
    try:
        json_extracted = text_block.replace("```json", "").replace("```", "")
        logging.debug(f" the extracted string:: {json_extracted}")
        ret = json.loads(json_extracted)
        return ret
    except Exception as e:
        print(f"Error - please make one more attempt to run the usecase {e}")
        logging.error(f" the extracted string:: has non json {json_extracted} ::{e}")
        os._exit(1)
        # to be implemented


def tools_handler(
    tools: List,
    task_input: Dict,
    llm: LLMBaseModel,
):
    model_prefix = """You are a smart assistant which is capable of smartly answering about how to solve a given problem in sequential tasks using the available tools.
                    The available tools are provided to you and you are supposed to answer What all tools are required to solve the problem and in which order with all of their parameters.
            """

    tool_prefix = """
        Tool describing format:
        [
            {
                "category" : "The category of the tool, defines what the tool can do in a basic manner.",
                "tool_name" : "The tool name",
                "description": "Description of the tool",
                "args": {"arg1": "arg1"},
                "cls": {
                    "kls": "Class name",
                    "module": "module name"
                },
                "output": "Output schema"
            }
        ]


        """

    tools_db = f"""
            The available tools:
            {tools}
            """
    task_desc = """
                    Task Statement:
            The Task statement has 5 parameters, and you must pay attention to all of them and give the best output.
            The 5 parameters are:
            "role" : This describes the role of the Language Model. This role tells you about your interest while looking for answers. For example if you are a private investment investor, then you will look for stock related information of different companies in recent timeframe using a search engine to properly answer the given task problem.
            "goal" : This is the goal which the final answer should achieve.
            "backstory" : This describes your role in a more detailed manner.
            "task" : The real task objective which needs to be solved. You are supposed to solve this problem by giving out sequential steps to solve the entire problem. 
            "instructions" : These are additional instructions which you have to follow while solving the task. It may be given or may not be given.
            "Tools_List" : These are the list of tools which you need to use. You are supposed to tell how to use these tools with all their paramters to solve the original problem.
            "OrderOfExecution" : This parameter tells you, whether you have to follow exact and strict order as given in the tools list or not while solving the main problem at hand. If the value is True we use the tools list in a strict manner, other wise a versatile manner.
            """

    task_input_str = ""

    for k, v in task_input.items():
        task_desc += f"\n{k}: {v}"

    example = (
        """
        Refer to some examples with the input information and the output information, you are supposed to answer the answer in this very format
        [
            {
                "role" : "Intelligent Question-answering Assistant",
                "goal" : "Answer the question with Best and very high accuracy with no mistake.",
                "backstory" : "You are an question-answering Assistant which has access to all the tools mentioned, like search and calculate, you are supposed to use thos to get the final answer.",
                "task" : "Where does the singer Arijit Singh belong to?",
                "instructions" : "",
                "Tools_list" : ["ScrapeAndSearchWebsite, SearchInternetGoogle, SearchInternetDuckDuck, getYoutubeSearchResults"],
                "OrderOfExecution" : true,
            }

            Tools:
            """
        + str(tools_db)
        + """
            Answer:
            ```json
                [
                    {
                        "category": "Search",
                        "tool_name": "DuckDuckGoSearch Tool",
                        "args": {"search_str": "trends in 2H 2023 onwards"},
                        "cls": {
                            "kls": "DuckDuckGoSearhTool",
                            "module": "openagi.tools.integrations.duckducksearch",
                        },
                        "output": "",
                    },
                    {
                        "category": "Search",
                        "tool_name": "Youtube Tool",
                        "args": {"search_str": "Trending in 2H 2023 onwards"},
                        "cls": {
                            "kls": "YoutubeSearchTool",
                            "module": "openagi.tools.integrations.youtubesearch",
                        },
                        "output": "",
                    },

                ]

            ```
        ]"""
    )

    suffix = "Provide a JSON-formatted response with the correct tool names and parameter values, without explanations, to solve the given problem accurately. Ensure the JSON format is error-free and follows the specified structure. Do not give any explanation paragraph, just give the required json answer. I want to use the final output in my code, so make sure it is in such a manner."

    final_prompt = f"""
    {model_prefix}
    {tool_prefix}
    {tools_db}
    {task_desc}
    "Task Input: {task_input_str}\n"
    {example}
    {suffix}
    """

    resp = llm.run(final_prompt)
    json_resp_tool = extract_json_from_string(resp)

    tools_resp = []
    for tool in json_resp_tool:
        cls_name = tool["cls"]["kls"]
        mod_name = tool["cls"]["module"]
        tool_cls = getattr(importlib.import_module(mod_name), cls_name)
        params = tool["args"]
        tool_cls = tool_cls()
        setattr(tool_cls, "llm", llm)
        tool_obj = tool_cls._run(**params)
        tool_resp = {
            "tool_name": tool["tool_name"],
            "output": tool_obj,
        }
        tools_resp.append(tool_resp)

    # Concatenate tools_resp into a string
    # TODO: Make it return any kind of datatypes. Right now it supports strings only.
    tool_resp_str = ""
    for tool in tools_resp:
        logging.info("getting tool output for: {tool['tool_name']}")
        tool_resp_str += f"{tool['tool_name']}: {tool['output']}\n"

    return tool_resp_str


def getEmail(inputString, role, backstory, goal, task, llm):
    template = "As a {role}, your primary objective is to {goal}. Your assigned task involves composing an email based on the provided summary. Here's some background information to guide you: {backstory}. Your challenge is to craft a detailed email within the given context. Please ensure that your email remains focused on the following context: {context}. Keep the email concise and relevant to the provided information."
    prompt = PromptTemplate(
        input_variables=["goal", "role", "task", "backstory", "context"],
        template=template,
    )
    prompt.format(context=inputString, role=role, backstory=backstory, goal=goal, task=task)
    chain = LLMChain(llm=llm, prompt=prompt)
    inputs = {
        "role": role,
        "backstory": backstory,
        "task": task,
        "goal": goal,
        "context": inputString,  # Assuming the inputString is the context
    }
    blog = chain.run(inputs)
    print(f"the blog is  {blog}")
    return blog


def getSummary(inputString, role, backstory, goal, task, llm):
    template = "As a {role}, your primary objective is to {goal}. Your assigned task involves performing the following {task}. Here's some background information to guide you: {backstory}. Your challenge is to craft a detailed summary within the given context. Please ensure that your summary remains focused on the following context:{context}. Keep the summary concise and relevant to the provided information.\n"
    prompt = PromptTemplate(
        input_variables=["goal", "role", "task", "backstory", "context"],
        template=template,
    )
    prompt.format(context=inputString, role=role, backstory=backstory, goal=goal, task=task)
    chain = LLMChain(llm=llm, prompt=prompt)
    inputs = {
        "role": role,
        "backstory": backstory,
        "task": task,
        "goal": goal,
        "context": inputString,  # Assuming the inputString is the context
    }
    blog = chain.run(inputs)
    print(f"output of getSummary {blog}")
    return blog


def llm_chain(role, backstory, goal, task, llm: LLMBaseModel, input_string):
    template = "As a {role}, your primary objective is to {goal}. Your assigned task involves performing the following {task} to the best of your ability. Here's some background information to guide you: {backstory}. Also use context: {context} to provide answer for the given task. Keep the answer concise and relevant to the provided information."
    prompt = PromptTemplate(
        input_variables=["goal", "role", "task", "backstory", "context"], template=template
    )
    prompt.format(role=role, backstory=backstory, goal=goal, task=task, context=input_string)
    chain = LLMChain(llm=llm.llm, prompt=prompt)
    inputs = {
        "role": role,
        "backstory": backstory,
        "task": task,
        "goal": goal,
        "context": input_string,
    }
    code = chain.run(inputs)
    return code


# function to generate a review
def getReview(inputString, role, backstory, goal, task, llm):
    template = "As a {role}, your primary objective is to {goal}. Your assigned task involves performing the following {task}. Here's some background information to guide you: {backstory}. Your challenge is to perform the task within the given context:{context}. Keep the answer relevant to the provided information.\n"
    prompt = PromptTemplate(
        input_variables=["goal", "role", "task", "backstory", "context"],
        template=template,
    )
    prompt.format(context=inputString, role=role, backstory=backstory, goal=goal, task=task)
    chain = LLMChain(llm=llm, prompt=prompt)
    inputs = {
        "role": role,
        "backstory": backstory,
        "task": task,
        "goal": goal,
        "context": inputString,  # Assuming the inputString is the context
    }
    review = chain.run(inputs)
    return review


def handleLocalLLMTask(inputString, role, backstory, goal, task, llm):
    sysMsg = role + " " + backstory + " " + goal + " " + task
    # Point to the local server
    client = OpenAI(base_url="http://localhost:1236/v1", api_key="not-needed")

    completion = client.chat.completions.create(
        model="local-model",  # this field is currently unused
        messages=[
            {"role": "system", "content": sysMsg},
            {"role": "user", "content": inputString},
        ],
        temperature=0.7,
    )

    return completion.choices[0].message.content


def getfromLocalLLM(inputString, role, backstory, goal, task, llm):
    llm_1 = Ollama(model="llama2")
    template = "As a {role}, your primary objective is to {goal}. Your assigned task involves performing the following {task}. Here's some background information to guide you: {backstory}. Your challenge is to perform the task within the given context:{context}. Keep the answer relevant to the provided information.\n"
    prompt = PromptTemplate(
        input_variables=["goal", "role", "task", "backstory", "context"], template=template
    )
    prompt.format(context=inputString, role=role, backstory=backstory, goal=goal, task=task)
    chain = LLMChain(llm=llm_1, prompt=prompt)
    inputs = {
        "role": role,
        "backstory": backstory,
        "task": task,
        "goal": goal,
        "context": inputString,  # Assuming the inputString is the context
    }  # inputstring with localllm
    review = chain.run(inputs)
    return review


def handleLLMTask(inputString, role, backstory, goal, task, llm):
    logging.info(f"Running handleLLMTask:: {llm}")
    return llm_chain(
        role=role,
        backstory=backstory,
        goal=goal,
        task=task,
        llm=llm,
        input_string=inputString,
    )


# Example Usage:
if __name__ == "__main__":
    backstory = "You are a software developer working on a platform that provides code snippets for various programming tasks."
    role = "Coder"
    goal = "To generate Python code for calculating the factorial of a number in a way that it can be easily copied and pasted by users for execution.Do not use any python libraries for it, hardcode it completely"
    task = " Develop a Python script that calculates the factorial of a given number, presenting the code in a line-by-line format to ensure clarity and ease of use for users."
    inputString = "write program with given instructions"
    llm = "abc"
    # ret= getfromLocalLLM(inputString,role,backstory,goal,task,llm)
    ret = handleLocalLLMTask(inputString, role, backstory, goal, task, llm)
    print(ret)
