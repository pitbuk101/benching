"""Negotiation Factory Prompts for the util file - extract supplier name, objectives etc"""

from __future__ import annotations

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from ada.use_cases.negotiation_factory.parsers import (
    ObjectiveOutputParser,
    SupplierProfileOutputParser,
)
from ada.utils.logs.logger import get_logger

log = get_logger("Negotiation_factory_prompt")


def extract_supplier_prompt(user_query: str) -> PromptTemplate:
    """
    Generate Prompt to extract supplier name from the user query
    Args:
        user_query (str):  User query received in input payload

    Returns:
        (PromptTemplate) : prompts for supplier name
    """
    log.info(f"Extracting supplier name from user query: {user_query}")
    parser = PydanticOutputParser(pydantic_object=SupplierProfileOutputParser)
    prompt = (
        f"""
                Consider you are a Language model who can understand the user question \
                and extract the supplier/vendor name mentioned in this user query.

            USER_QUERY: {user_query}

            User want to start negotiation with a particular supplier/vendor.
            Keep in mind that in procurement, terms such as supplier, vendor, provider, seller,
            and any similar synonyms can be used interchangeably """
        + """
            Extract the supplier name and return in the JSON format
            Make sure output is in json format only with "supplier_name" key(IMPORTANT)
            {format_instructions}

            EXAMPLES:
            user Query: What is the most effective type of Negotiation I can use with Ericks BV
            Answer: {{{{
                "supplier_name" : "Ericks BV"
            }}}}
            user Query: CNC manufacturing technology Friedemann
            Answer: {{{{
                "supplier_name" : "CNC manufacturing technology Friedemann"
            }}}}

            Do not use the word json in the output. Return only a valid JSON Object.

            """
    )
    prompt = PromptTemplate.from_template(prompt).partial(
        format_instructions=parser.get_format_instructions(),
    )
    return prompt


def extract_objectives_prompt(
    user_query: str,
    probable_objectives: list[str],
) -> PromptTemplate:
    """
    Generate Prompt to extract objective list from the user query
    Args:
        user_query (str):  User query received in input payload
        probable_objectives (list[str]):  list of probable objectives

    Returns:
        (PromptTemplate) : prompt for objectives
    """
    log.info(f"Extracting objectives from user query: {user_query}")
    parser = PydanticOutputParser(pydantic_object=ObjectiveOutputParser)
    prompt = (
        f"""
            You are a procurement expert who can understand the user question and
            extract the negotiation objective mentioned in the user query.

            DEFINITION OF NEGOTIATION OBJECTIVE:
                 `Negotiation objective` is the target of the negotiations with the supplier, \
                 examples include price reduction , optimize cost saving etc.

            - List of currently available objectives are {probable_objectives}
            - USER QUERY: {user_query}
            - TASK: Given the user query, extract the negotiation objective in the user query.
            """
        + """
            NOTE:
            1. Return the extracted objective in the JSON format.
            2. Return only a valid JSON Object. NEVER have the word json in the output.
            3. Give the extracted_objectives (if found) even if it is not in the list of probable objectives.


            EXAMPLES:
            List of currently available objectives: ["spend", "payment terms", "contract duration"]
            USER QUERY: Show me insight/ objective on ABC company
            Answer: {{{{"extracted_objectives": []}}}}

            List of currently available objectives: ["price reduction", "payment terms", "contract duration"]
            USER QUERY: Negotiate with ABC company for spend
            Answer: {{{{"extracted_objectives": ["price reduction"]}}}}

            List of currently available objectives: ["price reduction", "incoterm optimization"]
            USER QUERY: give me insight/objectives on regarding security enhancement
            Answer: {{{{"extracted_objectives": ["security enhancement"]}}}}

            List of currently available objectives: ["price reduction", "incoterm optimization"]
            USER QUERY: Change negotiation objectives
            Answer: {{{{"extracted_objectives": []}}}}

            List of currently available objectives: ["spend", "incoterm optimization"]
            USER QUERY: Set objective as spend
            Answer: {{{{"extracted_objectives": ["spend"]}}}}

            """
    )
    prompt = prompt + "Format Instructions {format_instructions} \n "
    return PromptTemplate.from_template(prompt).partial(
        format_instructions=parser.get_format_instructions(),
    )


def check_email_prompt(user_query: str) -> PromptTemplate:
    """
    Generate Prompt to extract supplier name from the user query
    Args:
        user_query (str):  User query received in input payload

    Returns:
        (PromptTemplate) : prompts for supplier name
    """
    prompt = f"""
            Consider you are a Language model who can understand the user question \
            and check if it contains the contents of an AN ACTUAL email.
            Look for common elements such as greetings, body text, and signatures.

            USER_QUERY: {user_query}

            Answer "True" if the `USER_QUERY` contains the contents of an ACTUAL email (with
            the appropriate format), else "False"

            NOTE: Return only "True" or "False" in the output nothing else.

            EXAMPLES:
            USER_QUERY: "Dear Buyer,
            We hope this message finds you well. Thank you for reaching out to discuss potential cost-saving opportunities.
            We greatly appreciate your commitment to expanding our business relationship and recognize
            the significant increase in your spend with us over the past year.
            It is always our goal to provide exceptional value and quality to our valued partners.

            We understand your desire to achieve a more competitive price and improve profitability.
            Your request for an 1.7% discount on the 2 SKUs, is noted.
            As you may be aware, we have also faced increased costs in raw materials, logistics, and production.
            These factors have impacted our pricing structure. However, we are committed to exploring ways to
            optimize our operations and pass on savings to our partners where feasible.
            We would like to propose a meeting to discuss these opportunities in more detail.
            Could we schedule a meeting next week to explore these opportunities further?
            Manager,
            SKF FRANCE"
            Answer: "True"

            USER_QUERY: Supplier says "We would like to meet on the 12th
            of this month to discuss the contract, kindly confirm your availability"
            Answer: "False"
            """
    prompt = PromptTemplate.from_template(prompt)
    return prompt
