from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from src.config import LLM_MODEL
from src.retriever import retrieve

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

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
    return '\n'.join(formatted_entries)

def get_prompt(query, context):
    prompt_template = """You are an expert competitive programming problem recommender. Given a query and a context, you will recommend the most relevant competitive programming problems from the context. The context contains information about various problems, including their titles, patterns, core ideas, recognition cues, approaches, techniques, time and space complexities, difficulties, and tags.

    Query: {query}

    Context: {context}

    Based on the query and the context, recommend the most relevant competitive programming problems. Provide a brief explanation for each recommendation.

    Recommendations:
    """
    prompt = PromptTemplate.from_template(prompt_template)
    return prompt.format(query=query, context=context)

def generate_recommendations(query, context):
    context = format_context(context)
    llm = ChatGroq(
        model=LLM_MODEL,
        api_key=groq_api_key,
    )
    prompt = get_prompt(query, context)
    response = llm.invoke(prompt)
    return response

query = "I want to learn about dynamic programming problems that involve optimizing a value based on constraints."
context = retrieve(query)
recommendations = generate_recommendations(query, context)
print("Recommendations:\n", recommendations.content)