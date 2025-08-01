"""Prompts for benchmarking component."""

from langchain_core.prompts import PromptTemplate


def factual_data_prompt() -> PromptTemplate:
    """
    Prompt to extract factual data (i.e. numerical data).
    Returns:
        (PromptTemplate): Prompt for the factual data
    """
    template = """
    System Message:
    You are an expert data extractor, your core task is to extract specific data point based on the
    rate filing information at your disposal.

    Instructions:
    1. Analyze the given question and data, and extract the numerical value as asked.
    2. double check the response and the numerical values exacted
    3. Whenever data is not present, give "NA" as the field output
    4. if the given question is "NA", create numerical factors to extract based on the information and add it to the answer

    Remember to clearly label the columns and rows with relevant entities.
    Question: {question}

    Your STRICT Response Format (response should STRICTLY be a json dictionary):
    Answer: [Generate a concise, factual, and informative response.]
    """
    prompt = PromptTemplate.from_template(template)
    return prompt


def merge_data_prompt() -> PromptTemplate:
    """
    Generate results in the form of dictionaries.
    Returns:
        (PromptTemplate): Merge data prompt template
    """
    template = """
    Information: ```{information}```

    System Message:
    You are an expert data aggregator.
    Your objective is to take in the information given and generate a structured dictionary.
    Replace any missing factor with 'NA'
    Remember to clearly label the columns and rows with relevant entities.

    Your STRICT Response Format (response should STRICTLY be a json dictionary):
    Answer:

    Here is an illustrative format for the output format:
    {output_format}

    """

    prompt = PromptTemplate.from_template(template)
    return prompt
