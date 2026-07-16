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
    
    prompt_template = f"""You are an expert competitive programming mentor helping a student find problems to practice.

    You will be given a problem the student is currently working on, and a list of candidate problems retrieved from a knowledge base.

    Your task: identify which candidates are genuinely useful practice for the student, and rank them by relevance.

    Definitions:
    - "Similar" means the candidate shares a core technique, recognition pattern, or problem-solving approach with the student's problem — even if it belongs to a different named pattern.
    - A candidate is NOT similar if it is a superficial keyword match with a fundamentally different approach.

    Rules:
    1. Only recommend problems that appear in the candidate list below. Never invent a problem.
    2. For each recommended problem, give a one-sentence reason tied to a specific shared technique or idea — not a generic statement.
    3. Order recommendations from most to least relevant.
    4. If none of the candidates are meaningfully similar, respond with exactly: "No relevant problems found."

    Student's Problem:
    {query}

    Candidate Problems:
    {context}
    """
    return prompt_template.format(query=query, context=context)

def generate_recommendations(query, context):
    context_str = format_context(context["metadatas"][0])
    llm = get_llm()
    prompt = get_prompt(query, context_str)
    response = llm.invoke(prompt)
    return response
