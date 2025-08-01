"""
RAG prompts for Negotiation
"""

import json
import numbers
import random
from typing import Any

import pandas as pd
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from numerize.numerize import numerize

from ada.use_cases.negotiation_factory.parsers import (
    ArgumentModifyParser,
    ArgumentOutputParser,
    EmailOutputParser,
)
from ada.use_cases.negotiation_factory.prompts import (
    get_common_negotiation_factory_context,
)
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger

log = get_logger("Negotiation_factory_prompt")
negotiation_conf = read_config("use-cases.yml")["negotiation_factory"]


def argument_rag_prompt(
    model_context: dict[str, Any],
    pinned_elements: dict[str, Any],
    **kwargs: Any,
) -> PromptTemplate:
    """
    Provides the prompt for argument generation.
        Args:
        model_context (dict): With the common model context for arguments, counter arguments,
            and rebuttals.
        pinned_elements (dict): dict of pinned elements if any
        **kwargs (Any): Additional data
    Returns:
        (PromptTemplate): provides prompt with all relevant information for argument generation
    """
    log.info("Additional args %d", len(kwargs))
    common_prompt = get_common_negotiation_factory_context(
        model_context,
        "arguments",
    )

    objective = model_context.get("negotiation_objective")

    arg_prompt = f"""
        Each argument should be ~50-100 words, with the specified tone,
        and aligned with the stated {objective} and goal.

        Notes:
        1. NEVER generate any arguments outside the scope of given objective-{objective}.
        2. ALWAYS Calculate and add derived metrics such as percentages,
           averages and numbers to support the arguments
          (UPTO 1 DECIMAL). Also use numbers in context only. Never make up numbers.
        3. Do not generate the instruction and only output from step 2 (with 1-3 arguments).
        4. NEVER generate arguments that weaken the buyer's position
            (e.g. NEVER MENTION price increases lower than market prices.
             price increase is 5% and market is 8%, NEVER mention it).
        5. NEVER repeat arguments and NEVER duplicate same information in multiple arguments.
        6. NEVER mention the value of price increase if its is lower than the market or the target.
        7. ALWAYS USE Incentives and Reinforcements in the arguments.
        8. Use procurement knowledge in the arguments
        (e.g. raw material cost increase can lead to price increase,
        inflation can lead to price increase).
        ).
    """
    if kwargs.get("request_type", "") == "modify":
        values = {
            f"argument{i+1}": "Modified argument to supplier"
            for i in range(len(pinned_elements.get("arguments", [])))
        }
        parser_val = ArgumentModifyParser(**values)
        parser = PydanticOutputParser(pydantic_object=parser_val)
    else:
        parser = PydanticOutputParser(pydantic_object=ArgumentOutputParser)

    arg_prompt = arg_prompt + (
        "Format Output: {format_instructions} and only produce a valid JSON"
        + "Objective & Targets of Negotiation (Focus MOST Important): {question} "
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("human", common_prompt),
            ("system", arg_prompt),
            ("human", "Past History: {chat_history}"),
            ("system", "Tone of the compelete argument must ALWAYS be {tone}"),
            (
                "system",
                "ALWAYS FACTOR target and latest offers in the argument where it makes sense",
            ),
            (
                "system",
                (
                    "ALWAYS USE `Supplier's reason for not accepting offer` in the arguments"
                    " if available"
                ),
            ),
            ("system", "ALWAYS FACTOR Carrots and Sticks in the arguments if available"),
            (
                "user",
                "Factor Relevant knowledge documents below {context}",
            ),
            ("system", "If savings are less than target, NEVER mention the savings value"),
        ],
    )
    prompt_template = prompt_template.partial(format_instructions=parser.get_format_instructions())
    print('prompt_template', prompt_template)
    return prompt_template


def counter_argument_rebuttal_rag_prompt(
    model_context: dict[str, Any],
    generation_type: str,
    **kwargs: Any,
) -> list:
    """
    Generate a prompt based on retrieved context and chat history to generate a counter-argument.
    Args:
        model_context (dict): With the common model context for arguments, counter arguments,
            and rebuttals.
        pinned_elements (dict): dict of pinned elements if any
        generation_type (str): The type of out we are generating e.g. arguments, counter argument
        selected_values (list): list of selected counter arguments or rebuttals if any
        kwargs (Any): Additional data
    Returns:
        list: A template for the generated prompt.
    """
    log.info("Additional args %d", len(kwargs))
    stakeholder = (
        f"""seller {model_context.get("supplier_name", "")}"""
        if generation_type == "counter_arguments"
        else "buyer"
    )
    stakeholder_instructions = (
        "buyers (e.g. NEVER mention things such as  no LCC supplier, being sole supplier,"
        " having few alternatives, NEVER MENTION value of inflation/ price increase being "
        "lower than market increase)"
        if generation_type == "rebuttals"
        else "sellers (e.g. having too many LCC suppliers in counter_arguments"
    )

    common_prompt = get_common_negotiation_factory_context(
        model_context,
        generation_type,
    )
    prev_step = "argument" if generation_type == "counter_arguments" else "counter argument"

    supplier_ignorance_str = ""
    if generation_type == "counter_arguments":
        supplier_ignorance_str = (
            "Also Seller is will NOT know that they are single sourced or the exact percentage"
            " of the total spend, or the percentage of category spend. NEVER MENTION THE EXACT "
            "PERCENTAGES IN COUNTER ARGUMENTS unless present in arguments. Supplier will always"
            "says that their products and services are the best."
        )

    explain_generation_type = (
        (
            f"a counter argument, which is an argument from {stakeholder} as a "
            "reply to the argument from the buyer (us)"
        )
        if generation_type == "counter_arguments"
        else "A rebuttal refers to " f"a reply to the {stakeholder}'s argument"
    )

    prompt = f"""
    {common_prompt} as a reply to the {prev_step} from the {stakeholder}'s perspective.

    NEVER mention things weaken the {stakeholder}'s position.
    ALWAYS NEGOTIATE FROM POSITION OF STRENGTH.
    KEEP EVERY {generation_type} FACTUAL ONLY Based on the provided data.

        {supplier_ignorance_str}"""

    system_prompt = (
        f"""
        ## Key information: -- Inflation is the price change of goods and services over time.
        -- If price increase is lower than market price, it is NEVER a leverage for the buyer.

        ## Task Generate {explain_generation_type}


        Generate response to user's request and separate each {generation_type} with a |.
        Generate ONLY 1 per {prev_step} in the SAME order as a DIRECT response to each.

        ## Notes:
        a. You need to generate ONLY ONE ACTUAL {generation_type} from the {stakeholder}'s
           perspective per {prev_step} or {generation_type} provided.
        b. GENERATE ONLY {generation_type} separated by |. NOTHING ELSE.
        c. ALWAYS calculate, add derived metrics like percentages, averages to aid {generation_type}
          (UPTO 1 DECIMAL).
        d. Do not put place-holders in the {generation_type}.
        e. Follow {stakeholder_instructions}
        f. NEVER GENERATION MORE {generation_type} THAN ASKED.
        g. NEVER repeat the question in the {generation_type}.
        h. Do not acknowledge everything the user tells you. They may lie to you.
        i. Use procurement knowledge in the {generation_type}
        (e.g. raw material cost increase can lead to price increase,
        inflation can lead to price increase, e.g. inflation means market increase).
    """
        + """
            Previous conversation with the Procurement Assistant (ONLY FOR REFERENCE):
            {chat_history}"""
        """
            CURRENT Selected INPUT:
            {question}
        """
        + f"ONLY GIVE THE FINAL OUTPUT FOR THE CURRENT INPUT on behalf of the {stakeholder}."
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("human", prompt),
            ("system", system_prompt),
            ("system", f"ALWAYS GIVE a POINTED reply to the {stakeholder}'s {prev_step}"),
            ("system", "Factor target and latest offers in ask ONLY if it makes sense"),
            (
                "system",
                "ALWAYS FACTOR `Supplier's reason for not accepting offer` was not accepted",
            ),
            ("system", "Use Carrots and Sticks in `reply to supplier arguments` if available"),
            (
                "user",
                "Factor Relevant knowledge documents below {context}",
            ),
        ],
    )
    return prompt_template


# def email_rag_prompt(
#     supplier: str,
#     pinned_elements: dict,
#     selected_elements: dict,
#     email_chain: list,
#     reference_data: pd.DataFrame,
#     model_context: dict[str, Any],
# ) -> PromptTemplate:
#     """
#     Generate a prompt based on retrieved context and chat history to generate an email.
#     Args:
#         supplier (str): Supplier name
#         relationship (str): Supplier relationship name
#         objective (str): The context in which the argument was generated
#         relationship_description (dict): Dictionary of relationship description
#         pinned_elements (dict): Dictionary of pinned elements
#         selected_elements (dict): Dictionary of selected elements
#         email_chain (list): List of email chains
#         objective_goal(str): Objective goal
#         reference_data (pd.DataFrame): Reference emails data
#     Returns:
#         PromptTemplate: A template for the generated prompt.
#     """

#     def extract_value(dict_element: dict[str, str]) -> tuple[str, str]:
#         """
#         Extracts available elements from the dictionay element
#         Args:
#             dict_element (dict[str, str]) The selected or pinned element
#         Returns:
#             (str) available rebuttal or counter argument or arguments
#         """
#         value = (
#             dict_element.get("rebuttals")
#             or dict_element.get("counter_arguments")
#             or dict_element.get("arguments", "")
#         )
#         key = (
#             "rebutals"
#             if dict_element.get("rebuttals")
#             else (
#                 "counter_arguments"
#                 if dict_element.get("counter_arguments")
#                 else ("arguments" if dict_element.get("arguments") else "")
#             )
#         )
#         return key, value

#     # Pinned or selected elements

#     pinned_elements_dict = {
#         key: ", ".join(
#             [
#                 item_val.get("objective") or item_val.get("details")
#                 for item_val in item
#                 if item_val.get("objective") or item_val.get("details")
#             ],
#         )
#         for key, item in pinned_elements.items()
#         if isinstance(item, list)
#     }
#     selected_elements_dict = {
#         key: ", ".join(
#             [
#                 item_val.get("objective") or item_val.get("details")
#                 for item_val in item
#                 if item_val.get("objective") or item_val.get("details")
#             ],
#         )
#         for key, item in selected_elements.items()
#         if isinstance(item, list)
#     }
#     selected_key, selected_value = extract_value(selected_elements_dict)
#     pinned_key, pinned_value = extract_value(pinned_elements_dict)
#     pinned_key = selected_key if selected_value else pinned_key
#     pinned_value = selected_value if selected_value else pinned_value

#     # Supplier profile
#     # pylint: disable=R0801
#     supplier_profile = model_context.get("supplier_profile", {})
#     supplier_profile_str = " ,".join(
#         [
#             (
#                 f"""{terms.replace("ytd", "reference/current full year")} : """
#                 f"""{numerize(value, 1) if isinstance(value, numbers.Number) else value} """
#             )
#             for terms, value in supplier_profile.items()
#             if value
#         ],
#     )
#     # pylint: enable=R0801

#     target_list = model_context.get("target_list", [])

#     objective_list = [
#         f"""{item.get("objective")} Target - {target_list[i]}"""
#         for i, item in enumerate(model_context.get("filtered_objectives", []))
#         if isinstance(item, dict) and item.get("objective")
#     ]

#     context_dict = {
#         "Supplier Profile": supplier_profile_str,
#         "Objective for negotiation": ", ".join(model_context.get("objective_type", [])),
#         "# Pinned / Selected Objectives": "\n \n ,".join(objective_list),
#         f"Pinned/ Selected {pinned_key}": pinned_value,
#         "Sourcing Approach": model_context.get("sourcing_approach", ""),
#         "Category Positioning -": model_context.get("category_positioning"),
#         model_context.get("buyer_attractiveness", {})
#         .get("question", ""): model_context.get("buyer_attractiveness", {})
#         .get("value", ""),
#         "carrots": ", ".join(model_context.get("carrots", [])),
#         "sticks": ", ".join(model_context.get("sticks", [])),
#     }
#     context_dict_str = ", ".join(
#         [f"{key}: {value}" for key, value in context_dict.items() if value],
#     )

#     log.info("emails %s", json.dumps(email_chain))

#     # Previous emails
#     email_type = "first_email" if not email_chain else "follow_up"
#     selected_reference = []
#     if reference_data is not None and len(reference_data) > 0:
#         selected_reference = reference_data.loc[
#             reference_data["archetype"] == email_type,
#             "email_content",
#         ].to_list()
#     selected_item = next(iter(random.choice(selected_reference))) if selected_reference else {} #NOSONAR
#     format_str = selected_item.get("format", "").replace("[", "").replace("]", "")

#     email_chain_data = ""
#     step = 1
#     if email_chain is not None:

#         def recurse(nodes):
#             details_list = []
#             for node in nodes:
#                 # Collect details from the current node
#                 details_list.append(node["details"])
#                 # Recursively collect details from all children
#                 details_list.extend(recurse(node["children"]))
#             return details_list

#         email_chain_data = ", ".join(recurse(email_chain))
#         email_chain_data = f"""{step + 1}. Understand previous emails, distill required information
#         Email Chain - {email_chain_data}
#         understand if its from the buyer or the the supplier {supplier}
#         by looking at the "To" field"""
#         step = step + 1
    
#     log.info("Email archetype %s", email_type)

#     human_prompt = (
#         f"""
#         You are a negotiation expert for procurement of {supplier_profile.get("category_name", "all categories")}.
#         Your task is to generate emails to the supplier {supplier_profile.get("supplier_name")}
#         and reply to emails from the supplier {supplier_profile.get("supplier_name")}.
#         Reason logically using step buy step reasoning:

#         We are the buyer from the vendor {supplier}. Any email to {supplier} must seek to maximize
#         our profit and from the supplier {supplier} will seek to maximize theirs.

#         Key Information:
#         -- Arguments: Buyer (we) makes arguments to supplier {supplier} with a requirement.
#         -- Counter-Arguments: Supplier {supplier} refutes the arguments to the buyer.
#            Products mentioned as our products in counter-arguments should be your products in email.
#         -- Rebuttals: Buyer (we) refute the counter arguments with a bigger ask
#         -- Seller {supplier} provides the products and services to the the buyers (us)
#         -- In buyer emails volunteer information which will hamper our negotiating power
#            e.g. do not mention a high single source

#         1. Understand the context below and filter out content for email generation:
#         {context_dict_str}

#         {email_chain_data} -- USE FOR CONTEXT ONLY

#         {step + 1}. Understand the content or the supplier email in the 'User provided context'
#         to formulate the current email response. Filter out necessary details.


#         {step + 2}. Understand the structure for emails and also the use example for reference only.
#         -- Every email has a structure where we generate 1-2 sentences per item, followed by '\n'.
#             {format_str}

#         -- An example {selected_item.get("tone", "")} email for this structure is
#             {selected_item.get("content", "")}

#         -- The example gives us the reference, format and the level of detail needed in the email
#         not ACTUAL FACTS/ CONTENT.
#         TYPICALLY the first email, has a less detailed analysis as compared to follow-ups.

#         {step + 3}. Generate a to the point concise logically consistent and accurate {email_type}
#         email using the content filtered out in steps 1 to  {step + 2} and its MOST IMPORTANT to
#         focus on the User provided context.

#         Do not repeat previous emails. Generate a new email response.
#     """
#         + (
#             "Format Output: {format_instructions} and only produce a valid JSON"
#             " with keys `message`, `emails` ONLY"
#         )
#         + (
#             """
#             Previous conversation with the Procurement Assistant:
#             {chat_history}

#             User Instruction (Focus MOST Important): {question}
#             """
#         )
#     )

#     system_prompt = """
#         Notes:
#         1. DO NOT GENERATE PARTS OF THE PROMPTS Or PARSERS.
#         2. Write to the point, concise and logically consistent emails and do not repeat yourself.
#         3. If any key information is not available to generate the email,
#         (For e.g. time or date of a meeting),
#         ALWAYS ADD a placeholder text `[PLACEHOLDER]`.
#         4. If user query has a supplier says followed by a statement, without a To field and body,
#         it is NOT an email.
#         5. Use only the information provided in the context and the email chain.
#         6. Add numbers and derived metrics to support the email if necessary.
#         7. Generate only single email response. Do not include parts of prompt or examples in email.
#         8. Strictly follow format for emails when generating the response and keep it to the point.
#         9. NEVER repeat previous emails in context. Always generate a new email response.
#         10. Use procurement knowledge in the emails
#         (e.g. raw material cost increase can lead to price increase,
#         inflation can lead to price increase).

#         ).
#     """

#     tone_prompt = "Tone of complete email must always be: {tone}"
#     print('tone_prompt', tone_prompt)
#     parser = PydanticOutputParser(pydantic_object=EmailOutputParser)

#     prompt_template = ChatPromptTemplate.from_messages(
#         [
#             ("human", human_prompt),
#             ("system", system_prompt),
#             ("human", "Past History: {chat_history}"),
#             ("system", tone_prompt),
#             ("human", "Relevant knowledge documents {context}"),
#             ("system", "The tone of the complete email must always be {tone}"),
#             (
#                 "system",
#                 "Factor target, and Latest offers in the ask ONLY where it makes sense",
#             ),
#             (
#                 "system",
#                 "ALWAYS factor `Supplier's reason for not accepting offer` in the email",
#             ),
#             ("system", "ALWAYS and MUST USE Carrots and Sticks in the arguments if available"),
#         ],
#     )

#     prompt_template = prompt_template.partial(format_instructions=parser.get_format_instructions())
#     return prompt_template

def email_rag_prompt(
    supplier: str,
    pinned_elements: dict,
    selected_elements: dict,
    email_chain: list,
    reference_data: pd.DataFrame,
    model_context: dict[str, Any],
) -> PromptTemplate:
    """
    Generates an optimized email prompt for GPT-4o.
    Uses a single structured prompt instead of system-human role separation.
    """

    def extract_value(dict_element: dict[str, str]) -> tuple[str, str]:
        value = (
            dict_element.get("rebuttals")
            or dict_element.get("counter_arguments")
            or dict_element.get("arguments", "")
        )
        key = "rebuttals" if dict_element.get("rebuttals") else "counter_arguments" if dict_element.get("counter_arguments") else "arguments"
        return key, value

    pinned_elements_dict = {
        key: ", ".join(
            [item_val.get("objective") or item_val.get("details") for item_val in item if item_val.get("objective") or item_val.get("details")]
        )
        for key, item in pinned_elements.items() if isinstance(item, list)
    }

    selected_elements_dict = {
        key: ", ".join(
            [item_val.get("objective") or item_val.get("details") for item_val in item if item_val.get("objective") or item_val.get("details")]
        )
        for key, item in selected_elements.items() if isinstance(item, list)
    }

    selected_key, selected_value = extract_value(selected_elements_dict)
    pinned_key, pinned_value = extract_value(pinned_elements_dict)
    pinned_key = selected_key if selected_value else pinned_key
    pinned_value = selected_value if selected_value else pinned_value

    supplier_profile = model_context.get("supplier_profile", {})
    supplier_profile_str = ", ".join(
        [f"{terms}: {value}" for terms, value in supplier_profile.items() if value]
    )

    objective_list = [
        f"{item.get('objective')} Target - {model_context.get('target_list', [])[i]}"
        for i, item in enumerate(model_context.get("filtered_objectives", []))
        if isinstance(item, dict) and item.get("objective")
    ]
    email_tone_n_tactics = model_context.get("tone", "")
    if email_tone_n_tactics:
        tactics = random.choice(email_tone_n_tactics['tactics'])

    context_dict = {
        "Supplier Profile": supplier_profile_str,
        "Negotiation Objective": ", ".join(model_context.get("objective_type", [])),
        "Pinned / Selected Objectives": "\n\n".join(objective_list),
        f"Pinned/Selected {pinned_key}": pinned_value,
        "Sourcing Approach": model_context.get("sourcing_approach", ""),
        "Category Positioning": model_context.get("category_positioning", ""),
        model_context.get("buyer_attractiveness", {}).get("question", ""): model_context.get("buyer_attractiveness", {}).get("value", ""),
        "Carrots": ", ".join(model_context.get("carrots", [])),
        "Sticks": ", ".join(model_context.get("sticks", [])),
        "Email Tone": f"{email_tone_n_tactics['title']} - {email_tone_n_tactics['description']}" if  email_tone_n_tactics else '',
        # "Prefered Negotiation Tactic": {tactics['title']:tactics['description']} if  email_tone_n_tactics else "",

    }

    context_str = "\n".join([f"- {key}: {value}" for key, value in context_dict.items() if value])

    log.info("Email Chain: %s", json.dumps(email_chain))
    email_type = "first_email" if not email_chain else "follow_up"
    
    selected_reference = []
    if reference_data is not None and len(reference_data) > 0:
        selected_reference = reference_data.loc[
            reference_data["archetype"] == email_type,
            "email_content",
        ].to_list()
    selected_item = next(iter(random.choice(selected_reference))) if selected_reference else {} #NOSONAR
    format_str = selected_item.get("format", "").replace("[", "").replace("]", "")
    email_chain_data = ", ".join([node["details"] for node in email_chain]) if email_chain else ""

    prompt = f"""
    You are an expert in procurement negotiations, responsible for writing emails to {supplier}.
    We are the buyer from the vendor {supplier}. Any email to {supplier} must seek to maximize
    our profit. The supplier {supplier} will seek to maximize theirs.
    Emails should be ready, complete in a way that it can be sent to supplier right after filling place holder values by Buyer.
    Reason logically using step buy step reasoning

    
    **Context:**
    {context_str}
    
    **Email Type:** {email_type}
    {('Previous Emails: ' + email_chain_data) if email_chain_data else ''}
    
    **Content Instructions:**
    - Start with Subject Line
    - Follow negotiation best practices.
    - Never mention things that weaken the buyer's position.
    - Always negotiate from a position of strength.
    - Keep every email factual and based on the provided data.
    - Ensure logical consistency and clarity.
    - Avoid repetition from previous emails.
    - Utilize relevant arguments, counter-arguments, and rebuttals.
    - Use numerical data when applicable.
    - If any key information is not available to generate the email,
        (For e.g. time or date of a meeting),
        ALWAYS ADD a placeholder text `[PLACEHOLDER]`.
    - Use procurement knowledge in the emails
        (e.g. raw material cost increase can lead to price increase, 
        inflation can lead to price increase).
    - Never disclose Buyer's intended savings amount or opportunity amount in any email.


    **Formatting Instructions:**
    - The email must have a proper structure, use it as formatting reference only: {format_str}
    - Tome of complete email MUST be the 'Email Tone' (if applicable)
    - Follow Tactics mentioned  (if applicable)
    
    


    **Include following in Email body but NEVER make saperate sections for it**
    - Objective of the Email
    - Buyer’s Negotiation Argument
    - Supplier’s Counter-Arguments (if applicable)
    - Rebuttals (if applicable)
    - Use Carrots & Sticks to pursuade Supplier to meet Buyer's objective (if Carrots & Sticks are present)
    - Clear Call to Action

    **General Rules**
    - Add numbers and derived metrics to support the email if necessary.
    - Generate only single email response. Do not include parts of prompt or examples in email.
    - Strictly follow format for emails when generating the response and keep it to the point.
    - NEVER repeat previous emails in context. Always generate a new email response.
    
    Generate the email now.
    """
    # prompt = f"""
    # You are an expert in procurement negotiations, responsible for writing emails to {supplier}.
    # We are the buyer from the vendor {supplier}. Any email to {supplier} must seek to maximize our profit.
    # The supplier {supplier} will seek to maximize theirs.

    # Your goal is to draft a negotiation-ready email based on insights, objectives, and context.
    # The email should be logically sound, complete, and ready to send after placeholders are filled by the buyer.

    # **⚠️ CRITICAL RULES (NEVER BREAK):**
    # - Never reveal the buyer's potential or intended savings amount, even approximately.
    # - Do not include phrases like “we will save”, “we can save”, “the savings opportunity is”, or any variant that directly states a monetary or numerical benefit to the buyer.
    # - Do not mention savings in days (e.g., "we gain 30 days") unless rephrased to be **supplier-facing**, not buyer-facing.
    # - Instead, frame insights as supplier improvement areas or expectations (e.g., "this pricing deviates from benchmarks" or "terms are not aligned with industry standards").
    # - Never include anything that reveals how much better off the buyer would be — only pressure the supplier on their side (pricing, terms, inconsistencies, benchmarks, etc.).

    # **Context:**
    # {context_str}

    # **Email Type:** {email_type}
    # {('Previous Emails: ' + email_chain_data) if email_chain_data else ''}

    # **Content Instructions:**
    # - Start with a Subject Line
    # - Follow negotiation best practices and procurement strategy
    # - Keep the buyer in a position of strength at all times
    # - Always base arguments on provided data (context + insights)
    # - Ensure logical consistency and avoid redundant statements
    # - Never repeat content from previous emails
    # - Use strong, supplier-facing language — focus on expectations, misalignments, market comparisons, etc.
    # - Include placeholders for unknowns using `[PLACEHOLDER]`
    # - Do not speculate or assume buyer intentions

    # **Formatting Instructions:**
    # - The email must be formatted as per: {format_str}
    # - Maintain the 'Email Tone' (if provided)
    # - Apply relevant Tactics (if provided)

    # **Include in the Email Body (without creating separate sections):**
    # - Objective of the Email
    # - Buyer’s Negotiation Argument
    # - Supplier’s likely Counter-Arguments (if applicable)
    # - Rebuttals to counter-arguments (if applicable)
    # - Use carrots & sticks tactically (if defined)
    # - A clear Call to Action

    # **DO NOT:**
    # - Mention potential savings (in currency, percentage, or time)
    # - Reveal buyer's financial goals or expectations
    # - Include any numeric gain or savings forecast for the buyer
    # - Use phrases like "this helps us", "this will benefit us", "our gain", "our opportunity", "improve our position", etc.

    # **General Rules:**
    # - Support arguments with factual metrics (only when helpful to strengthen pressure)
    # - Use numbers only in supplier-facing language (e.g., “this price is 18% above benchmark”)
    # - Generate a single email response — never include prompt content or meta comments
    # - Keep the email clear, confident, and focused on the supplier’s side of the negotiation

    # Generate the email now.
    # """

    return ChatPromptTemplate.from_template(prompt)
