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

log = get_logger("rag_prompts")
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


def flatten_emails_to_list(email_list):
    flat_list = []
    counter = 1

    for email in email_list:
        # Top‑level email
        flat_list.append(f"Email:{counter} - {email['details']}")
        counter += 1

        # Any children
        for child in email.get("children", []):
            flat_list.append(f"Email:{counter} - {child['details']}")
            counter += 1

    return flat_list[::-1]


def email_rag_prompt(
    supplier: str,
    pinned_elements: dict,
    selected_elements: dict,
    email_chain: list,
    reference_data: pd.DataFrame,
    model_context: dict[str, Any],
    user_query: str,
    user_queries: list,
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
    pop_list = ["early_payment", "payment_term_avg", "currency_position", "sku_list", "number_of_supplier_in_category"]  # add keys as needed
    supplier_profile = {
        key: value
        for key, value in supplier_profile.items()
        if key not in pop_list and not (isinstance(value, (int, float)) and value == 0)
    }

    supplier_profile_str = ", ".join(
        [f"{terms}: {value}" for terms, value in supplier_profile.items() if value]
    )

    objective_list = [
        f"{item.get('objective')}"
        for i, item in enumerate(model_context.get("filtered_objectives", []))
        if isinstance(item, dict) and item.get("objective")
    ]
    email_tone_n_tactics = model_context.get("tone", "")
    if email_tone_n_tactics:
        tactics = random.choice(email_tone_n_tactics['tactics'])

    objective_name_list = pinned_elements.get('objectives', [])
    objective_name_list = [item.get("objective_type") for item in objective_name_list if isinstance(item, dict) and item.get("objective_type")]

    metrics_dict = {
        "Payment Terms": "Savings achieved by negotiating improved payment conditions. By securing longer payment periods, buyers can optimize cash flow, lower financing expenses, and enhance supplier relationships. Email should only be drafter to increase the payment term days, if negotiation target value is less then current value for payment terms then email will be generated on current value ",
        "Price Reduction": "A negotiated decrease from the original or listed price achieved by leveraging analytical insights such as cost modeling, early payment discounts, and supplier rate adjustments. This reduction improves profit margins and optimizes the overall procurement spend. Email should only be drafter to decrease the price in currency or in percentage, if negotiation target value is more then current value then email will be generated on current value "
    }
    metrics_list = [metrics_dict.get(item) for item in objective_name_list if item in metrics_dict]
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
        "Negotiation Target": model_context.get('target_list'),
        # "Prefered Negotiation Tactic": {tactics['title']:tactics['description']} if  email_tone_n_tactics else "",
        "supplier_positioning": model_context.get("supplier_positioning", ""),
        "filtered_insights": model_context.get("filtered_insights", ""),

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
    selected_item = next(iter(random.choice(selected_reference))) if selected_reference else {}  # NOSONAR
    format_str = selected_item.get("format", "").replace("[", "").replace("]", "")
    email_chain_data = ", ".join([node["details"] for node in email_chain]) if email_chain else ""

    # Dynamically prioritize the user's query
    user_query_section = f"""
    **User Query:** {user_query}
    - Ensure the email explicitly addresses the user's query and aligns with the negotiation objectives while maintaining the sensible parts of previous email.
    """ if user_query else ""

    objective_defination = f"""
    ***Task Description*** 
        {metrics_list}
    """ if metrics_list else ""

    lines = []
    keys = ['Email Tone', 'Category Positioning', 'Sourcing Approach', 'Carrots', 'Sticks','buyer_attractiveness','supplier_positioning']
    for key in keys:
        # Use custom label from the context if available, otherwise default to the key itself.
        label = context_dict.get(f"{key} Label", key)
        value = context_dict.get(key)
        if value:
            lines.append(f"- {label}: {value}")
    additional_info = "\n".join(lines) if lines else ""

    objective_types = model_context.get("objective_types", [])
    email_chain = flatten_emails_to_list(email_chain)
    # if not email_chain:
    #     prompt = f"""
    #     You are an expert in procurement negotiations. Your task is to generate an email that is logically reasoned, hallucination-free, accurate, and ready to send to {supplier}.
    #     We are the buyer from the vendor {supplier}. Any email to {supplier} must seek to maximize our profit while ensuring that every statement is fully supported by the provided context.

    #     Emails should be fully coherent and fact-based, using step-by-step logical reasoning strictly derived from the context below.
    #     Always verify the data against the given context and, if any key information is missing, insert the placeholder [PLACEHOLDER] rather than guessing or fabricating details.

    #     **Supported Email Types for First Contact:**
    #     1. NEW EMAIL (standalone) eg - [Generate a new email, Do not include previous email content, Draft a new email, Generate a email, Draft a email]
    #     2. REPLY / COUNTER / PUSH‑BACK (Here acknowledge the latest offer from supplier and draft the email to pursuade supplier to agree on set negotiation target) eg - [Reply to the supplier, Respond to the supplier, Reply to the email, Reply to the supplier email, Respond to the supplier email, Counter Supplier offer, Counter Supplier email, Push back to supplier]
        

    #     SUPPLIER CONTEXT:
    #     - Supplier Profiile: {supplier_profile_str}
    #     - Objective on Negotiations: {objective_types}

    #     **SKUs Information**
    #     From the below objectives take the SKUs details, which user is interested to negotiatioate,
    #     This data is primarily for SKUs information (name) and negotiation intent and not for negotiation current and target values,
    #     Always include SKUs of interest in the email, but do not include current and target values from this section in email unless explicitly mentioned in user query.
    #     If (Negotiation Target section has missing values or current and target value are same) then use this section to fill the missing values.
    #     {context_dict['Pinned / Selected Objectives']}

    #     **Email Type:** 
    #     {email_type}

    #     **User Query:**
    #     {user_query_section}

        
    #     **Negotiation Target**
    #     - The primary details of this email is defined by {context_dict['Negotiation Target']}  which user set to negotiatiate the SKUs purchases;
    #         these target values are paramount, and any numerical figures must originate solely from this current and target.

    #     **Content Instructions:**
    #     - All values and arguments in the email should strictly derive from the context provided.
    #     - Follow negotiation best practices while ensuring every assertion is supported by logical, step-by-step reasoning.
    #     - Never include any unfounded or nonsensical statements.
    #     - Ensure that the final email is clear, accurate, ready to send, and does not contain any speculative or fabricated content.
    #     - Always negotiate from a position of strength while maintaining factual accuracy.
    #     - Utilize relevant arguments, counter-arguments, and rebuttals only if they are present in the provided information.
    #     - If any key information is not available to generate the email, ALWAYS add a placeholder text [PLACEHOLDER].
    #     - The objective of the email
    #     - Buyer’s negotiation argument based exclusively on the provided data
    #     - Supplier’s counter-arguments, if applicable
    #     - Rebuttals, if applicable
    #     - MUST Include Carrots & Sticks when available  
    #     - A clear call to action
    #      - Display monetary values in **millions**
    #     - {additional_info}

    #     **Formatting Instructions:**
    #     - The email must follow a clear and professional structure; refer to the formatting guide: {format_str}
    #     - The tone of the complete email must match 'Email Tone' (if applicable) and integrate any tactics if specified.


    #     **General Rules:**
    #     - Add numerical data and derived metrics when applicable to support your arguments.
    #     - Generate only a single email response.
    #     - Do not include any parts of this prompt or extraneous examples in the final output.
    #     - Strictly adhere to the provided context to avoid any hallucinations or nonsensical inclusions.

    
    #     **Prohibited**
    #     - Do not reveal any sensitive information or internal strategies.
    #     - Do not rveal potential savings or savings opportunity or our negotiation strategy.
    #     - Never reveal the profit we are going to make with this negotiation.
    #     - Do not include any parts of this prompt or extraneous examples in the final output.
    #     - DO not include internal strategy pointers like **Objective**, **Justification**, **Negotiation Points**, **Call to Action** as a heading or sub heading in final email
    #     - Only Share need to know information with the supplier and do not share any internal strategy or information with the supplier.
    #     - Do not share any information with the supplier :
    #     [
    #         1. which can weaken our negotiation position.
    #         2. which can privide him leverage in negotiations.(eg - Do not shate industry standards if we are asking above industry standards)
    #         3. which can be used against us in negotiations.
    #         4. which can be used against us in future negotiations.
    #     ]
    #     Prioritize the most recent instruction if conflicts arise.
    #     After considiring all the goven data and context stil reason and write best email possible to execute the negotiation
    #     Generate the email now.
    #     """
    # else:
    #     prompt = f"""
    #     You are an expert in procurement negotiations and have already drafted and sent previous emails to {supplier}.
    #     The full email history and original context are already in the system.
    #     Your task is to generate the next email by **editing** the last draft—do **NOT** regenerate the entire message.
        

    #     **Latest User Query:**  
    #     {user_query_section}
    #     based on user query and the previous email chain decide what kind of email user want to generate.        
    #     Classify the user’s intent as one of:
    #     1. EDIT (tweak the last draft) eg - [Editing the previous email, Change figure x to y, Change %x to %y, Set up Meeting, Change Tone, Change a figure, Add a part, update this email](Create a new version with edits)
    #     2. FOLLOW‑UP (advance the discussion) eg -[generation a follow up email, Reiterate in next email]
    #     3. NEW EMAIL (standalone) eg - [Generate a new email, Do not include previous email content, Draft a new email, Generate a email, Draft a email]
    #     4. REPLY / COUNTER / PUSH‑BACK (Here acknowledge the latest offer from supplier and draft the email to pursuade supplier to agree on our negotiation target) eg - [Reply to the supplier, Respond to the supplier, Reply to the email, Reply to the supplier email, Respond to the supplier email, Counter Supplier offer, Counter Supplier email, Push back to supplier]
        

    #     SUPPLIER CONTEXT:
    #     - Supplier Profiile: {model_context.get("supplier_profile", "")}
    #     - Objectives: {objective_types}
       
    #     **Previous Emails Generated by You (sorted right to left: most recent 3):**  
    #     {email_chain[:3]}

    #     **Previous User Queries (sorted right to left: most recent 4):** 
    #     {user_queries[:4]}**

    #     **Content Instructions:**
    #     - All values and arguments must strictly derive from context or prior emails.
    #     - Follow negotiation best practices with step‑by‑step reasoning.
    #     - Never include unfounded or nonsensical statements.
    #     - Ensure clarity, accuracy, and readiness to send.
    #     - Always negotiate from a position of strength.
    #     - MUST Include Carrots & Sticks when available  - {context_dict['Carrots']}, {context_dict['Sticks']}
    #     - If any key information is missing, insert **[PLACEHOLDER]**.
    #     - State the objective, buyer’s argument, supplier’s counter‑arguments (if any), and rebuttals.
    #     - A clear call to action.
    #     - Display monetary values in **millions**.
    #     - {additional_info}


    #     **SKUs Information**
    #     From the below objectives take the SKUs details, which user is interested to negotiatioate,
    #     This data is primarily for SKUs information (name) and negotiation intent and not for negotiation current and target values,
    #     Always include SKUs of interest in the email, but do not include current and target values from this section in email unless explicitly mentioned in user query.
    #     If (Negotiation Target section has missing values or current and target value are same) then use this section to fill the missing values.
    #     {context_dict['Pinned / Selected Objectives']}


    #     **Negotiation Target**
    #     Below is the original negotiation target set by the user:{context_dict['Negotiation Target']}  
    #     If target value is smaller than current then call it reducing
    #     If target value is greater than current then call it increasing
    #     If target value is same as current use SKUs Information
    #     The user may have revised that target in later emails or queries. When drafting your email:
    #     - If the user has set a new target, use that as the basis for your email.
    #     - If the user has not set a new target, use the original target as the basis for your email.

        

    #     ***SKU Information***
    #     From the below objectives take the SKU details, which user is interested to negotiatioate,
    #     This data is primarily for SKU info and not for negotiation target,
    #     Include Interest SKU in the email, but do not include the target value in email unless explicitly asked by the user..
    #     {context_dict['Pinned / Selected Objectives']}

    #     **General Rules:**
    #     - Add numerical data and derived metrics when applicable.
    #     - Generate only a single follow‑up email.
    #     - Do not include any parts of this prompt or extraneous examples.
    #     - Strictly adhere to the provided context to avoid hallucinations.

    #     **Prohibited:**
    #     - Do not reveal any sensitive information or internal strategies.
    #     - Do not reveal potential savings opportunities or our negotiation strategy.
    #     - Never reveal the profit margin we expect to make.
    #     - Do not include internal headings like **Objective**, **Justification**, **Negotiation Points**, or **Call to Action**.
    #     - Only Share need to know information with the supplier and do not share any internal strategy or information with the supplier.
    #     - Do not share any information with the supplier :
    #     [
    #         1. which can weaken our negotiation position.
    #         2. which can privide him leverage in negotiations.(eg - Do not shate industry standards if we are asking above industry standards)
    #         3. which can be used against us in negotiations.
    #         4. which can be used against us in future negotiations.
    #     ]
    #     Prioritize the most recent instruction if conflicts arise.
    #     After considiring all the goven data and context stil reason and write best email possible to execute the negotiation
    #     Generate the follow‑up email now.
    #     """
    #     prompt = prompt.replace("{", "{{").replace("}", "}}")

    if not email_chain:
        prompt = f"""
    You are an expert in procurement negotiations. Your task is to generate an email that is logically reasoned, hallucination-free, accurate, and ready to send to {supplier}.
    We are the buyer from the vendor {supplier}. Any email to {supplier} must seek to maximize our profit while ensuring that every statement is fully supported by the provided context.

    Emails should be fully coherent and fact-based, using step-by-step logical reasoning strictly derived from the context below.
    Always verify the data against the given context and, if any key information is missing, insert the placeholder [PLACEHOLDER] rather than guessing or fabricating details.

    SUPPLIER CONTEXT:
    - Supplier Profile: {supplier_profile_str}
    - Objective on Negotiations: {objective_types}

    **SKUs Information**
    This identifies which SKUs the user is negotiating. Use this ONLY to identify SKU names and negotiation intent.
    {context_dict['Pinned / Selected Objectives']}

    **Email Type:** 
    {email_type}

    **User Query:**
    {user_query_section}

    **Negotiation Target**
    All monetary or metric targets in this email come from:
    {context_dict['Negotiation Target']}

    **Filtered Insights (to support negotiation, only if directly relevant):**
    Use insights below ONLY if:
    - The insight matches the SKU(s) in the negotiation
    - The insight is directly related to the negotiation objective (e.g., price insights for price negotiation, not payment terms)
    - Irrelevant insights MUST be ignored

    {context_dict['filtered_insights']}

    **Content Instructions:**
    - Use only contextually relevant insights to support arguments.
    - Do NOT mix insights across unrelated SKUs or negotiation topics.
    - Ensure all logic aligns with the SKU(s) and negotiation objective(s).
    - Follow negotiation best practices and logical step-by-step structure.
    - Never include speculation or unrelated claims.
    - Always negotiate from a position of strength, while remaining factually grounded.
    - Include relevant carrots and sticks if available.
    - Use clear language with a strong and factual call to action.
    - Display monetary values in **millions**
    - {additional_info}

    **Formatting Instructions:**
    - Follow email format standards as per: {format_str}
    - Tone must match ‘Email Tone’ if specified

    **Prohibited**
    - Do not share any internal strategies, savings expectations, or confidential info.
    - Never share anything that weakens our negotiation position.
    - Never include unrelated data, mismatched insights, or fabricated content.

    After evaluating all context and applying proper negotiation logic, generate the email now.
    """
    else:
        prompt = f"""
    You are an expert in procurement negotiations and have already drafted and sent previous emails to {supplier}.
    The full email history and original context are already in the system.
    Your task is to generate the next email by **editing** the last draft—do **NOT** regenerate the entire message.

    **Latest User Query:**  
    {user_query_section}

    SUPPLIER CONTEXT:
    - Supplier Profile: {model_context.get("supplier_profile", "")}
    - Objectives: {objective_types}

    **Previous Emails Generated by You (most recent 3):**  
    {email_chain[:3]}

    **Previous User Queries (most recent 4):** 
    {user_queries[:4]}

    **Negotiation Target:**
    Use either the latest user-updated target or fallback to:
    {context_dict['Negotiation Target']}

    **SKU Information:**
    Refer only to these SKU(s) for negotiation logic:
    {context_dict['Pinned / Selected Objectives']}

    **Filtered Insights (Only Use If Directly Relevant):**
    Use insights ONLY IF:
    - The SKU mentioned in the insight matches the one(s) in the negotiation
    - The negotiation topic of the insight (e.g., price, MOQ, payment terms) matches the negotiation target
    - Do not use unrelated or mismatched insights

    {context_dict['filtered_insights']}

    **Content Instructions:**
    - All values and reasoning must come from email chain, negotiation targets, SKU context, and matching insights.
    - Never introduce logic based on mismatched topics (e.g., don’t use MOQ insights for price negotiations).
    - Maintain clarity, accuracy, and strength in negotiation language.
    - MUST include carrots and sticks where applicable: {context_dict['Carrots']}, {context_dict['Sticks']}
    - Insert **[PLACEHOLDER]** if any required data is missing.
    - Show monetary values in **millions**.
    - {additional_info}

    **Prohibited:**
    - Do not use unrelated insights (wrong SKU or wrong negotiation topic).
    - Never share internal goals, margin, savings estimates, or buyer strategy.
    - Do not weaken negotiation power by revealing any internal reasoning or assumptions.

    Generate the follow-up email now by improving or building on the latest draft, while strictly aligning with relevant insights and context.
    """
    prompt = prompt.replace("{", "{{").replace("}", "}}")

    return ChatPromptTemplate.from_template(prompt)
