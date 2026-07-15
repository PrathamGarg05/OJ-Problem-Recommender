import os
from dotenv import load_dotenv
from src.config import LLM_MODEL

import streamlit as st

load_dotenv()
@st.cache_resource
def get_llm():
    from langchain_groq import ChatGroq
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    return ChatGroq(
        model=LLM_MODEL,
        api_key=GROQ_API_KEY,
    )

def format_context(context):
    formatted_entries = []
    for entry in context:
        lines = []
        for key in ["title", "pattern", "coreIdea", "recognitionCues", "approach", "techniques", "timeComplexity", "spaceComplexity", "difficulty", "tags"]:
            if key in entry:
                value = entry[key]
                if isinstance(value, list):
                    value = ', '.join(value)
                lines.append(f"{key}: {value}")
        formatted_entries.append('\n'.join(lines))
    return '\n\n'.join(formatted_entries)

def get_prompt(query, context):
    from langchain_core.prompts import PromptTemplate
    
    prompt_template = """You are an expert competitive programming mentor.

    You are given a user's query and a list of retrieved problems.

    Your job is to rank the retrieved problems by relevance.

    Rules:
    - Recommend ONLY problems that appear in the context.
    - Never invent a new problem.
    - Explain briefly why each problem is relevant.
    - If multiple problems are similar, order them from most to least relevant.
    - If no retrieved problem is relevant, reply exactly:
    "No relevant problems found."

    Query:
    {query}

    Retrieved Problems:
    {context}
    """
    return prompt_template.format(query=query, context=context)

def generate_recommendations(query, context):
    context_str = format_context(context["metadatas"][0])
    llm = get_llm()
    prompt = get_prompt(query, context_str)
    response = llm.invoke(prompt)
    return response
