import logging
import os

from langchain.agents import (
    AgentType,
    Tool,
    initialize_agent,
)
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from pydantic import BaseModel, Field

from openagi.tools.base import BaseTool, tool
from openagi.utils.yamlParse import read_yaml_config


def DocuCompare(searchString, llm):
    os.environ["AZURE_OPENAI_ENDPOINT"] = read_yaml_config("BASE_URL")
    deployment_name = read_yaml_config("EMBEDDING_DEPLOYMENT")
    tools = []
    directory = read_yaml_config("pdfFile")  # Specify the directory path here
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            file_info = {"name": os.path.splitext(filename)[0], "path": file_path}
            files.append(file_info)
    for file in files:
        loader = PyPDFLoader(file["path"])
        pages = loader.load_and_split()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(pages)
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment=deployment_name,
            openai_api_version=read_yaml_config("OPENAI_API_VERSION"),
        )
        retriever = FAISS.from_documents(docs, embeddings).as_retriever()
        tools.append(
            Tool(
                name=file["name"],
                description=f"useful when you want to answer questions about {file['name']}",
                func=RetrievalQA.from_chain_type(llm=llm, retriever=retriever),
            )
        )
    agent = initialize_agent(
        agent=AgentType.OPENAI_FUNCTIONS,
        tools=tools,
        llm=llm,
        verbose=True,
    )
    result = agent({"input": searchString})
    logging.debug(result)
    return result


class DocumentCompareInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class DocumentCompareOutputSchema(BaseModel):
    response: str = Field(
        description="Response from the agent regarding action performed by DocumentCompare."
    )


class DocumentCompareSearchTool(BaseTool):
    name: str = "DocumentCompareSearch Tool"
    description: str = (
        "A tool which can be used to by the agent to question uploaded files by the user."
    )

    @tool(args_schema=DocumentCompareInputSchema, output_schema=DocumentCompareOutputSchema)
    def _run(self, search_str: str = None):
        return DocuCompare(searchString=search_str, llm=self.llm.llm)
