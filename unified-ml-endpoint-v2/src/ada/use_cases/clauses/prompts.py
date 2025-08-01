"""Prompts for clauses component."""

from langchain_core.prompts import PromptTemplate


def retrieve_prompt() -> PromptTemplate:
    """
    Prompts for the LLM to retrieve and respond with clauses questions
    Returns:
        (PromptTemplate): Prompt for generating clauses
    """
    prompt_template = """
    You are an experienced lawyer who is specialized in analyzing conmmercial contracts.
    Use the following pieces of context to answer the question at the end.
    The quesion will ask for the presence of particular clause in a contract document.
    Always start your answer with either "YES" or "NO" before giving the details.

    {context}

    Question: {question}

    If the asked clause is present, cite the exact text from the document where the
    particular clause is found at the end of the response.
    """
    return PromptTemplate(template=prompt_template, input_variables=["context", "question"])
