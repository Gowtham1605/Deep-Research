from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import (
    ChatPromptTemplate, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate, 
    MessagesPlaceholder
)
from langchain_core.messages import HumanMessage
from langgraph.types import Command, Send
from typing import Literal, Dict
from tavily import TavilyClient
from .state import ResearchState
from .configuration import Configuration
from .utils import init_llm
from .prompts import (
    SECTION_KNOWLEDGE_SYSTEM_PROMPT_TEMPLATE,
    RESULT_ACCUMULATOR_SYSTEM_PROMPT_TEMPLATE,
)
from .struct import (
    Sections,
    Queries,
    SearchResult,
    SearchResults,
)
import time
import os




def section_knowledge_node(state: ResearchState, config: RunnableConfig):
    """
    Generates initial knowledge and understanding about a section before conducting research.

    This node uses an LLM to analyze the section details and generate foundational knowledge
    that will guide the subsequent research process. It processes the section information 
    through a system prompt to establish context and requirements.

    Args:
        state (ResearchState): The current research state containing section information
        config (RunnableConfig): Configuration object containing LLM and other settings

    Returns:
        dict: A dictionary containing the generated knowledge with key:
            - knowledge (str): The LLM-generated understanding and context for the section
    """
    configurable = Configuration.from_runnable_config(config)
    llm = init_llm(
        provider=configurable.provider,
        model=configurable.model,
        temperature=configurable.temperature
    )

    section_knowledge_system_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(SECTION_KNOWLEDGE_SYSTEM_PROMPT_TEMPLATE),
        HumanMessagePromptTemplate.from_template(template="{section}"),
    ])
    section_knowledge_llm = section_knowledge_system_prompt | llm

    result = section_knowledge_llm.invoke(state)

    return {"knowledge": result.content}


def tavily_search_node(state: ResearchState, config: RunnableConfig):
    """
    Performs web searches using the Tavily search API for each generated query.

    This node takes the generated queries from the previous node and executes searches
    using the Tavily search engine. 
    Args:
        state (ResearchState): The current research state 
        config (RunnableConfig): Configuration object containing search depth and other settings

    Returns:
        dict: A dictionary containing:
            - search_results (List[SearchResults]): List of search results for each query,
              where each SearchResults object contains the original query and a list of
              SearchResult objects with URL, title and raw content
    """
    configurable = Configuration.from_runnable_config(config)

    tavily_client = TavilyClient()
    response = tavily_client.search(query=state["section"], max_results=configurable.search_depth, include_raw_content=True)

    return {"accumulated_content": response["results"]}



def result_accumulator_node(state: ResearchState, config: RunnableConfig):
    """
    Accumulates and synthesizes search results into coherent content.

    This node takes the search results from the previous node and uses an LLM to process
    and combine them into a unified, coherent piece of content. The LLM analyzes the 
    search results and extracts relevant information to build knowledge about the section topic.

    Args:
        state (ResearchState): The current research state containing search results
            and other research context
        config (RunnableConfig): Configuration object containing LLM settings and other parameters

    Returns:
        dict: A dictionary containing:
            - accumulated_content (str): The synthesized content generated from processing
              the search results
    """
    configurable = Configuration.from_runnable_config(config)
    llm = init_llm(
        provider=configurable.provider,
        model=configurable.model,
        temperature=configurable.temperature
    )

    result_accumulator_system_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(RESULT_ACCUMULATOR_SYSTEM_PROMPT_TEMPLATE),
        HumanMessagePromptTemplate.from_template(template="Internal Knowledge: {knowledge}\nSearch Result content: {accumulated_content}"),
    ])
    
    result_accumulator_llm = result_accumulator_system_prompt | llm

    result = result_accumulator_llm.invoke(state)

    return {"accumulated_content": result.content}


