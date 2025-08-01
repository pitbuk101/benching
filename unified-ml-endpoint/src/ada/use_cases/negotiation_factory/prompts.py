"""Negotiation Factory Prompts - Arguments, Counter-arguments,
     Rebuttals, and Chat prompts"""

from __future__ import annotations

import json
import numbers
import random
from typing import Any

import numpy as np
import pandas as pd
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from numerize.numerize import numerize
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from ada.use_cases.negotiation_factory.parsers import (
    EmailOutputParser,
    ExtractedOpportunityList,
)
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger
from ada.utils.metrics.similarity import get_best_match_from_list

log = get_logger("Negotiation_factory_prompt")
negotiation_conf = read_config("use-cases.yml")["negotiation_factory"]


def get_common_negotiation_factory_context(
    model_context: dict,
    generation_type: str,
) -> str:
    """
    Generate common context for argument, counter-argument, rebuttals
    and user actions on the feature page

    Args:
        model_context (dict): The context needed for models to function,
        pinned_elements (dict): The pinned elements from the UI,
        generation_type (str): Type: of response generated ,
    Returns:
        str: Common prompt with extracted context structured in a step-by-step approach.

    """
    # Gettting Objective
    objective_types = model_context.get("objective_types", [])

    # Getting supplier details
    supplier_profile = model_context.get("supplier_profile", {})
    if "percentage_spend_which_is_single_sourced" in supplier_profile:
        supplier_profile["percentage_spend_which_is_single_sourced"] = (
            100 * (supplier_profile["percentage_spend_which_is_single_sourced"] or 0)
        )
    if "percentage_spend_without_po" in supplier_profile:
        supplier_profile["percentage_spend_without_po"] = (
            100 * (supplier_profile["percentage_spend_without_po"] or 0)
        )
    if generation_type == "counter_arguments":
        for element in negotiation_conf["counter_argument_remove_list"]:
            if element in supplier_profile:
                supplier_profile.pop(element)

    supplier_profile_str = " ,".join(
        [
            (
                f"""{terms.replace("ytd", "reference/current full year")} : """
                f"""{numerize(value, 1) if isinstance(value, numbers.Number) else value} """
            )
            for terms, value in supplier_profile.items()
            if value and terms in negotiation_conf["argument_data_list"]
        ],
    )
    savings_val = {
        key: value
        for key, value in supplier_profile.items()
        if (
            (key in negotiation_conf["savings_list"])
            and (
                (
                    isinstance(value, numbers.Number)
                    and value > negotiation_conf["idp"]["spend_threshold"]
                )
                or isinstance(value, str)
            )
        )
    }
    savings_str = " ,".join(
        [
            (
                f"""Savings from {terms}: """
                f"""{numerize(value, 1) if isinstance(value, numbers.Number) else value} """
            )
            for terms, value in savings_val.items()
            if value
        ],
    )
    # insights_str = "\n ".join(
    #     [insight for insight in model_context.get("filtered_insights", [])],
    # )
    # Modify the construction of insights_str based on filtered_insights being a dictionary
    insights_str = "\n".join(
        [f"**Relevant Insights for {objective_type.capitalize()}:**\n" + "\n".join(
            [f"- {insight}" for insight in insights]
        ) for objective_type, insights in model_context.get('filtered_insights', {}).items()]
    )


    negotiation_strategy = model_context.get("sourcing_approach", "")
    log.info("Negotiation strategy %s", ", ".join(negotiation_strategy))
    # goals = [f"{i}. {obj}" for i, obj in enumerate(objective_types)]
    goals = [f"{obj_type}. {objective.get('objective','')}"for obj_type, objective in zip(objective_types, model_context.get("filtered_objectives", []))]
    
    obj_count = len(objective_types)

    carrot_priority_str = (
        f""" ({model_context.get("priority", {}).get("carrots", "")} priority)"""
        if model_context.get("priority", {}).get("carrots")
        else ""
    )
    sticks_priority_str = (
        f""" ({model_context.get("priority", {}).get("sticks", "")} priority)"""
        if model_context.get("priority", {}).get("sticks")
        else ""
    )

    argument_tone_n_tactics = model_context.get("tone", "")
    if argument_tone_n_tactics:
        tactics = random.choice(argument_tone_n_tactics['tactics'])

    log.info("Carrot in prompt %s", model_context.get("carrots", []))
    context_dict = {
        f"Objectives for Negotiation (Goals) - ": f"{', '.join(goals)}",
        f"Supplier Information (Numerical Values for Generation) - ": f"{supplier_profile_str}",
        f"Sourcing Approach - ": f"{', '.join(negotiation_strategy)}",
        f"Category Positioning - ": f"{model_context.get('category_positioning')}",
        f"{model_context.get('buyer_attractiveness', {}).get('question', '')}": f"{model_context.get('buyer_attractiveness', {}).get('value', '')}",
        f"Savings from Supplier - ": f"{savings_str}",
        f"Negotiation Insights - ": f"{insights_str}",
        f"Negotiation Targets - ": '\n'.join(map(str, model_context.get('target_list', []))),
        f"(IMPORTANT) Carrots {carrot_priority_str} - ": f"{', '.join(model_context.get('carrots', []))}",
        f"(IMPORTANT) Sticks {sticks_priority_str} - ": f"{', '.join(model_context.get('sticks', []))}",
        f"Argument Tone": f"{argument_tone_n_tactics['title']} - {argument_tone_n_tactics['description']}" if argument_tone_n_tactics else "",
        # f"Past examples for REFERENCE - ": f"{model_context.get('past_examples', '')}",
    }
    if generation_type != "arguments":
        context_dict.pop("Sourcing Approach - ")

    context_dict_str = " ".join(
        [f"""{key} {value} \n""" for key, value in context_dict.items() if value],
    )
    log.info("Context dict %s", json.dumps(context_dict, indent=4))
    obj_literal = "objectives" if (obj_count > 1) else "objective"
    key_action = {
        "arguments": f"""You are the buyer, generate arguments to extract as much profit from
                  {supplier_profile.get("supplier_name")}""",
        "counter_arguments": (
            f"""You are representing {supplier_profile.get("supplier_name")} """
            """and are refuting the buyer's argument without giving any profit to the buyer"""
        ),
        "rebuttals": (
            f"""You are the buyer,counter rebuttal to extract as much profit from"""
            f""" {supplier_profile.get("supplier_name")}"""
        ),
    }

    return f"""
        Act as a procurement expert for {supplier_profile.get("category_name")}.
        {key_action[generation_type]}. Use a step by step chain of thoughts approach to generate
        a LOGICALLY CONSISTENT {generation_type} for negotiation.

        Step 1: Understand supplier context and filter out useful information to generate
            {generation_type}
            {context_dict_str}
            [NOTE: Use appropriate numbers from the context above only. Do not make up numbers]

        Step 2: Using the data generate precise and compelling negotiation {generation_type}
            (with supporting numbers & leverage) to meet {obj_count} {obj_literal},
            which {obj_count} {"are" if (obj_count > 0) else "is"} listed below -
            {context_dict["Objectives for Negotiation (Goals) - "]}.
    """

def argument_prompt(
    model_context: dict,
    argument_history,
    **kwargs: Any,
) -> ChatPromptTemplate:
    """
    Provides the prompt for argument generation.
    Args:
        model_context (dict): With the common model context for arguments, counter arguments,
            and rebuttals.
        pinned_elements (dict): dict of pinned elements if any
        **kwargs (Any): Additional data
    Returns:
        ChatPromptTemplate: Provides prompt with all relevant information to be used for argument generation.
    """
    log.info("Additional args %d", len(kwargs))
    common_prompt = get_common_negotiation_factory_context(
        model_context,
        "arguments",
    )

    key_terminology = f"""KEY TERMINOLOGY
        - LCC: A Low-Cost Country (LCC) or High-Cost Country (HCC) refers to the geographical location where
            the buyer is procuring a good from. LCC countries are considered lower in cost and hence would be
            recommended to consider procuring from in order to capitalize on the lower pricing. It is important
            to consider the quality of the product between LCC and HCC countries in parallel, as well as
            after-sales services. Having several suppliers (e.g.50+) from low-cost countries is a leverage for
            buyers and not having any is a big risk for buyers.
        - Single source supplier: Not having competitors. It is a risk for buyers (who cannot ask for discounts)
            and a leverage for suppliers (who can refuse discounts).
        - Parametric cost modelling: Savings opportunity which can be realized through better pricing.
        - Price arbitrage: Savings which can be immediately realized by switching suppliers.
            For eg. Price Arbitrage analysis shows EUR xm opportunity (x% on EUR xm spend base) for
            {model_context.get("supplier_profile", {}).get("supplier_name")}. So, buyer can request {model_context.get("supplier_profile", {}).get("supplier_name")}
            to either give discounts or the buyer can switch SKUs A and B to supplier Y.
        - Price Variation: Savings when there are price differences over time or across locations for the same SKU and
            same supplier. For e.g. “Our analysis suggests EUR xm opportunity (x% on EUR xm spend base)
            for {model_context.get("supplier_profile", {}).get("supplier_name")} by lowering prices to x
            (lowest price identified after that month) for SKUs A and B.”
            A spend decrease driven by price NEVER gives a buyer leverage AND IT DOES NOT MEAN A SHIFT TO OTHER SUPPLIERS.
        - Payment Terms Standardization: Savings achieved by negotiating improved payment conditions. By securing longer payment periods or favorable early payment discounts, buyers can optimize cash flow, lower financing expenses, and enhance supplier relationships.
        - Price Reduction: A negotiated decrease from the original or listed price achieved by leveraging analytical insights such as cost modeling, early payment discounts, and supplier rate adjustments. This reduction improves profit margins and optimizes the overall procurement spend.
    """
    common_prompt = key_terminology + common_prompt
    objective_types = model_context.get("objective_types", [])
    value_list = negotiation_conf["idp"]["savings"] + negotiation_conf["idp"]["payment"]

    objective_match_dict: dict[str, Any] = {}
    ask_str = ""
    for objective_type in objective_types:
        objective_match = get_best_match_from_list(
            value_list,
            objective_type,
            negotiation_conf["model"]["similarity_model"],
            negotiation_conf["idp_similarity_threshold"],
        )
        log.info("Objective match %s", objective_match)
        supplier_profile = model_context.get("supplier_profile", {})

        if objective_match in negotiation_conf["idp"]["savings"]:
            spend_denom = supplier_profile.get("spend_ytd", 0) or 1
            savings_dict = {
                key: supplier_profile.get(key)
                for key in negotiation_conf["savings_list"]
                if supplier_profile.get(key)
            }
            top_keys: list = sorted(
                savings_dict,
                key=savings_dict.get,  # type: ignore
                reverse=True,
            )[: negotiation_conf["idp"]["top_n"]]

            total_str = (
                (
                    f"""The total possible savings are {numerize(supplier_profile.get("total_savings", 0), 1)}.\n"""
                )
                if supplier_profile.get("total_savings")
                else ""
            )
            discount_str = "\n".join(
                [
                    (
                        f"""The discount for {key.replace("_", " ")} is {round(100 * savings_dict.get(key, 0) / spend_denom, 1)}%"""
                    )
                    for key in top_keys
                    if savings_dict.get(key, 0) > negotiation_conf["idp"]["spend_threshold"]
                ],
            )
            dis_ask_str = (
                f"""{total_str} with a discount of {round(supplier_profile.get("total_savings", 0), 1) / spend_denom} on the total spend base. Its breakdown is: {discount_str}"""
            )
            ask_str = f"""ALWAYS USE {dis_ask_str} to HAVE a CONCRETE ASK and RATIONALE"""

        elif objective_match in negotiation_conf["idp"]["payment"]:
            early_payments_loss = (
                f"""Early payment loss on paying earlier than contract demands is {numerize(supplier_profile.get("early_payment", 0), 1)}\n"""
                if supplier_profile.get("early_payment", 0)
                > negotiation_conf["idp"]["spend_threshold"]
                else ""
            )
            terms_standardization = (
                f"""Savings on standardizing contract is {numerize(supplier_profile.get("payment_terms_standardization", 0), 1)}\n"""
                if supplier_profile.get("payment_terms_standardization", 0)
                > negotiation_conf["idp"]["spend_threshold"]
                else ""
            )

            payment_ask_str = (
                f"""Current days for payterm are up to {supplier_profile.get("payment_term_avg", "lower than best")}. We should ask for best payment terms.\n {terms_standardization} {early_payments_loss}"""
            )
            total_payment_savings = np.nansum(
                [
                    supplier_profile.get("early_payment", np.nan),
                    supplier_profile.get("payment_terms_standardization", np.nan),
                ],
            )
            ask_str = (
                f"""ALWAYS USE {payment_ask_str} to HAVE a CONCRETE ASK and RATIONALE (match payment terms to get savings of {numerize(total_payment_savings, 1)})"""
            )
        elif objective_match in negotiation_conf["idp"]["delivery"]:
            ask_str = ""

        log.info("ASK ARGUMENTS %s", ask_str + objective_match)

        objective_match_dict[objective_type] = ask_str

        if kwargs.get("arguments"):
            objective_match_dict = {
                key: value
                for key, value in objective_match_dict.items()
                if key in kwargs.get("arguments")
            }
    objective_list = ", ".join(
        str(item.get("objective"))
        for item in model_context.get("filtered_objectives", [])
        if isinstance(item, dict) and item.get("objective")
    )
        
    user_query_section = f"""
        **User Query:** {kwargs.get("user_query")}
        - Ensure the arguments explicitly addresses the user's query and aligns with the negotiation objectives while maintaining the sensible parts of previous arguments.
        """ if kwargs.get("user_query") else ""

    history_json = json.dumps(argument_history, indent=4)


    
    arg_prompt = f"""
    {common_prompt}

    From the buyer’s perspective, propose a set of negotiation arguments (≈50 words each),
    using the specified supplier relationship tone, aligned with these objectives: {objective_types}.
   

    **User Query**
    
    {user_query_section}
    This is the user query to be addressed in the argument.

    SUPPLIER CONTEXT:
    - Name: {model_context.get("supplier_profile", {}).get("supplier_name")}.
    - Objectives: {objective_types}

    **Conditional Data**
    Below is the original negotiaiton target which user set to negotiatiate the SKUs purchases, 
    {model_context['target_list']}
    but at any time during the edits user may have asked to update the target which can be seen in previous arguments or user requests,
    so based on all of these do reason and select the latest target value asked by user for SKU negotiations in arguments(important).

    ***SKU Information***
    From the below objectives take the SKU details, which user is interested to negotiatiate,
    This data is primarily for SKU info and not for negotiation target,
    Do Include Interest SKU in the arguments, but do not include the target value in arguments unless explicitly asked by the user..
    {objective_list}

    PREVIOUS ARGUMENT ROUNDS (rightmost = most recent):

    {history_json}

      Note: history is sorted right→left; the rightmost entry is the latest. Generate new arguments on top of that most recent round.

    **Instructions:**
    1. **Position of strength**  
        Always negotiate from strength. Do **not** mention limited alternatives, sole‑supplier status, low LCC suppliers, or that any price increase is lower than market.
    2. **Reinforcement**  
        Each argument must include either a positive incentive or a negative consequence as reinforcement.
    3. **Data consistency**  
        When requesting discounts, match **exactly** the opportunity numbers provided in context (e.g. parametric cost modelling figures).
    4. **Relevance**  
        Include target reductions, reasons, and current offers only where they make sense.
    5. **Output format**  
        Follow this JSON schema *exactly*, including both "message" and "arguments" keys—even if values are empty:
        - The objective of the arguments
        - Rebuttals, if applicable
        - Must utilize Carrots & Sticks to persuade the supplier (if available)
        - A clear call to action

    ```json
    {{
        "message": "Your summary message here",
        "arguments": [
            {{
            "id": "argument_1",
            "title":"title based on the argument details"
            "details": "Your first argument (≈50 words)"
            }},
            {{
            "id": "argument_2",
            "title":"title based on the argument details"
            "details": "Your second argument (≈50 words)"
            }}
        ]
    }}
    '''
    """
    arg_prompt = arg_prompt.replace("{", "{{").replace("}", "}}")

    return ChatPromptTemplate([SystemMessage(content=arg_prompt)])


def counter_argument_rebuttal_prompt(
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
    request_type = kwargs.get("request_type", "")
    # pylint: disable=R0801
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
    # pylint: enable=R0801

    prompt = f"""
        {common_prompt} as a reply to the {prev_step} from the {stakeholder}'s perspective.

        NEVER mention things weaken the {stakeholder}'s position. ALWAYS NEGOTIATE FROM a POSITION OF STRENGTH.
        KEEP EVERY {generation_type} FACTUAL Based on the provided data.

        {supplier_ignorance_str}

        ## Task
        Generate response to each {prev_step} and separate each {generation_type} with a |.
        Always generate 1 per {prev_step} in the SAME order as a DIRECT response to each.

        ## Notes:
        a. GENERATE ONLY {generation_type} separated by |. NOTHING ELSE.
        b. Do not hamper negotiations for the {stakeholder_instructions}.
        c. Do NOT repeat the prompt and a {generation_type} is not an e-mail
        d. Output SHOULD have details on {generation_type} and support in ~50 words.
        f. Only answer the provided {prev_step} do not digress excessively.
        g. A rebuttal is not the same as an argument and the rebuttal tone is always assertive.
           The user will provide the supplier argument in the input when generating rebuttal.
           Keep in mind the use query though provided by user, but is actually from supplier.
        h. Do not reiterate the same facts again in {generation_type} unless absolutely necessary.
        i. Do NOT acknowledge anything you have received, they might lie to you.
           Think twice about what is presented to you. Always make sure your statement is logically consistent.
        j. DO NOT OUTPUT WHO ANSWERED.
        k. All needed information is provided in the prompt. Do not ask for additional information.
        l. f. Never repeat the {prev_step} in the {generation_type}. Only generate a reply to the {prev_step}.
        """

    prompt_template = PromptTemplate.from_template(
        prompt
        + """
            Previous conversation with the Procurement Assistant (ONLY FOR REFERENCE):
            {history}

            """
        + f""" CURRENT Selected
        {prev_step if not "modify" in request_type else generation_type}:"""  # noqa: E713
        """
            {input}

            ONLY GIVE THE FINAL OUTPUT FOR THE CURRENT INPUT.

            Factor target, reason and current offers in the ask ONLY where it makes sense
            """,
    )
    return prompt_template


def email_prompt(
    supplier: str,
    pinned_elements: dict,
    selected_elements: dict,
    email_chain: list,
    objective_goals: list[str],
    reference_data: pd.DataFrame,
) -> PromptTemplate:
    """
    Generate a prompt based on retrieved context and chat history to generate an email.
    Args:
        supplier (str): Supplier name
        pinned_elements (dict): Dictionary of pinned elements
        selected_elements (dict): Dictionary of selected elements
        email_chain (list): List of email chains
        objective_goals (list[str]): Selected Objective goals
        reference_data (pd.DataFrame): Reference emails data
    Returns:
        PromptTemplate: A template for the generated prompt.
    """

    def extract_value(dict_element: dict[str, str]) -> str:
        """
        Extracts available elements from the dictionay element
        Args:
            dict_element (dict[str, str]) The selected or pinned element
        Returns:
            (str) available rebuttal or counter argument or arguments
        """
        return (
            dict_element.get("rebuttals")
            or dict_element.get("counter_arguments")
            or dict_element.get("arguments", "")
        )

    # Objectives for negotiation
    objective_goal_str = ", ".join([f"{i}. {obj}\n" for i, obj in enumerate(objective_goals)])

    # Pinned or selected elements
    pinned_elements_dict = {
        key: ", ".join(
            [
                item_val.get("objectives") or item_val.get("details")
                for item_val in item
                if item_val.get("objectives") or item_val.get("details")
            ],
        )
        for key, item in pinned_elements.items()
        if isinstance(item, list)
    }
    selected_elements_dict = {
        key: ", ".join(
            [
                item_val.get("objectives") or item_val.get("details")
                for item_val in item
                if item_val.get("objectives") or item_val.get("details")
            ],
        )
        for key, item in selected_elements.items()
        if isinstance(item, list)
    }
    pinned_value = extract_value(selected_elements_dict) or extract_value(pinned_elements_dict)

    # Supplier profile
    supplier_profile = pinned_elements.get("supplier_profile", {})
    supplier_profile_str = " ,".join(
        [
            (
                f"""{terms.replace("ytd", "reference/current full year")} : """
                f"""{numerize(value, 1) if isinstance(value, numbers.Number) else value} """
            )
            for terms, value in supplier_profile.items()
            if value
        ],
    )

    context_dict = {
        "# Supplier Profile": supplier_profile_str,
        "# Pinned/ Selected Objectives": selected_elements_dict.get("objectives") or pinned_elements_dict.get("objectives"),
        "# Objectives for negotiation": objective_goal_str,
        "# Pinned/ Selected Values": pinned_value,
        "# Negotiation strategy": selected_elements.get("negotiation_strategy", {}).get("message") or pinned_elements.get("negotiation_strategy", {}).get("message"),
        "# Negotiation approach": selected_elements.get("negotiation_approach", {}).get("message") or pinned_elements.get("negotiation_approach", {}).get("message"),
    }
    # pylint: disable=R0801
    context_dict_str = ", ".join(
        [f"{key}: {value}" for key, value in context_dict.items() if value],
    )

    # Previous emails
    email_type = "first_email" if not email_chain else "follow_up"
    selected_reference = reference_data.loc[
        reference_data["archetype"] == email_type,
        "email_content",
    ].to_list()
    selected_item = next(iter(random.choice(selected_reference))) if selected_reference else {} #NOSONAR
    format_str = selected_item.get("format", "").replace("[", "").replace("]", "")

    email_chain_data = ""
    step = 1
    if email_chain is not None:

        def recurse(nodes):
            details_list = []
            for node in nodes:
                # Collect details from the current node
                details_list.append(node["details"])
                # Recursively collect details from all children
                details_list.extend(recurse(node["children"]))
            return details_list

        email_chain_data = ", ".join(recurse(email_chain))
        email_chain_data = f"""{step + 1}. Understand previous emails, distill required information
        Email Chain - {email_chain_data}
        understand if its from the buyer or the the supplier {supplier}
        by looking at the "To" field"""

    prompt = f"""
        You are a procurement expert for {supplier_profile.get("category_name", "all categories")}.
        Your task is to generate emails to the supplier {supplier_profile.get("supplier_name")}
        and reply to emails from the supplier {supplier_profile.get("supplier_name")}.
        Reason logically using step buy step reasoning:

        We are the buyer from the vendor {supplier}. Any email to {supplier} must seek to maximize our profit and from
        the supplier {supplier} will seek to maximize theirs.

        Key Information:
        -- Arguments: Buyer (we) makes arguments to supplier {supplier} with a requirement.
        -- Counter-Arguments: Supplier {supplier} refutes the arguments to the buyer.
           Products mentioned as our products in counter-arguments should be made your products in email.
        -- Rebuttals: Buyer (we) refute the counter arguments with a bigger ask
        -- Seller {supplier} provides the products and services to the the buyers (us)
        -- In buyer emails volunteer information which will hamper our negotiating power
           e.g. do not mention a high single source

        1. Understand the context below and filter out content for email generation:
        {context_dict_str}

        {email_chain_data} -- USE FOR CONTEXT ONLY

        {step + 1}. Understand the content or the supplier email in the 'User provided context'
        to formulate the current email response. Filter out necessary details.


        {step + 2}. Understand the structure for emails and also the use the example for reference only.
        -- Every email has a structure where we generate 1-2 sentences per item below, followed by '\n'.
            {format_str}

        -- An example {selected_item.get("tone", "")} email for this structure is
            {selected_item.get("content", "")}

        -- The example gives us the reference, format and the level of detail needed in the email not ACTUAL FACTS/ CONTENT.
        TYPICALLY the first email, has a less detailed analysis as compared to follow-ups.

        {step + 3}. Generate a to the point concise logically consistent and accurate {email_type} email using the content
           filtered out in steps 1, - {step + 2} and its MOST IMPORTANT to focus on the User provided context.
           Do not repeat previous emails. Generate a new email response.


        Notes:
        1. DO NOT GENERATE PARTS OF THE PROMPTS Or PARSERS.
        2. Write to the point, concise and logically consistent emails and do not repeat yourself.
        3. If any key information is not available to generate the email,(For e.g. time or date of a meeting),
        ALWAYS ADD a placeholder text `[PLACEHOLDER]`.
        4. If user query has a supplier says followed by a statement, without a To field and body, it is NOT an email.
        5. Use only the information provided in the context and the email chain.
        6. Add numbers and derived metrics to support the email if necessary.
        7. Generate only a single email response. Do not imclude parts of the prompt or examples in the email.
        8. Strictly follow a format for emails when generating the response and keep it to the point.
        9. NEVER repeat previous emails in context. Always generate a new email response.
        10. Factor target, reason and current offers in the ask ONLY where it makes sense
    """
    parser = PydanticOutputParser(pydantic_object=EmailOutputParser)

    prompt_template = PromptTemplate.from_template(
        prompt
        + (
            "Format Output: {format_instructions} and only produce a valid JSON"
            " with keys `message`, `emails`, `supplier_email` ONLY"
            " NEVER include the word json or ` in emails \n."
        )
        + """
            Previous conversation with the Procurement Assistant:
            {history}
            Current Conversation-
            User Instruction (Focus MOST Important): {input}
            """,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    # pylint: enable=R0801

    return prompt_template


def user_query_prompt(
    category_name: str,
    category_qna: str,
    supplier_profile: dict,
    supplier_qna: str,
    sku_qna: str,
    negotiation_objective: str,
    negotiation_factory_help: str,
    selected_elements: dict,
) -> PromptTemplate:
    """
    Generate a prompt based on retrieved context and chat history answer user questions.
    Args:
        category_name (str): Name of the category selected
        category_qna (str): String containing the category qna
        supplier_profile (dict): Dictionary of supplier profile information
        supplier_qna (str): String of the supplier qna
        sku_qna (str): String of the sku qna
        negotiation_objective (str): The context in which the argument was generated
        negotiation_factory_help (str): Help ttext for negotiation factory
        selected_elements (dict): Dictionary of selected elements
    Returns:
        (PromptTemplate): A template for the generated prompt.
    """
    # pylint: disable=R0801

    supplier_profile_str = " ,".join(
        [
            (
                f"""{terms.replace("ytd", "reference/current full year")} : """
                f"""{numerize(value, 1) if isinstance(value, numbers.Number) else value} """
            )
            for terms, value in supplier_profile.items()
            if value
        ],
    )
    # pylint: enable=R0801

    selected_elements = {
        key: " ,".join([entry["details"] for entry in item])
        for key, item in selected_elements.items()
        if item
    }

    selected_elements_str = ", ".join(
        [f"""Selected {key}: {item}""" for key, item in selected_elements.items()],
    )
    log.info("selected_elements, %s", selected_elements_str)
    context_dict = {
        "Category specific questions": category_qna,
        "Supplier profile information": supplier_profile_str,
        "Supplier specific questions": supplier_qna,
        "SKU specific questions": sku_qna,
        "Negotiation objective": negotiation_objective,
        "Negotiation factory help": negotiation_factory_help,
        "Selected/ Pinned elements": selected_elements_str,
    }
    context_str = " \n".join(
        [
            f"""{i + 1}. {key} : {context_dict[key]}"""
            for i, key in enumerate(context_dict.keys())
            if context_dict[key]
        ],
    )
    query_prompt = f"""
    You are an expert procurement negotiator for the {category_name} category.

    Take a step by step approach using chain of thoughts

    Step 1: Understand the available context and data
    {context_str}

    Step 2: Based on the context and data in Step 1 generate the response (50-150 words)
      for {category_name} only the it is possible to generate an ACCURATE answer from
      context and knowledge.
    """
    prompt_template = PromptTemplate.from_template(
        query_prompt
        + "\n"
        + """
        Previous conversation with Negotiator :
        {history}

        Current Conversation -
        Procurement Negotiator: {input}
        AI Assistant :

        NOTE:
        1. If you cannot generate an ACCURATE answer from context or your knowledge respond "NO"
        2. Do not respond "NO" unless you are missing knowledge and context to completely answer.
        3. For general questions which you can answer with knowledge respond with the answer.
        4. Do NOT describe who responded in the answer (DO NOT MENTION AI Assistant)
        5. Be concise in your response and do not repeat the prompt or the context.

        For example:
        User question asks for 17 suppliers, you have only 5 then respond "NO"
        """,
    )
    return prompt_template


def summary_email_prompt(
    supplier: str,
    pinned_elements: dict,
    objective_goals: list[str],
) -> PromptTemplate:
    """
    Generate a prompt based on retrieved context to generate a summary email.
    Args:
        supplier (str): Supplier name
        pinned_elements (dict): Dictionary of selected elements
        objective_goals (list[str]): selected objective descriptions by users
    Returns:
        PromptTemplate: A template for the generated prompt.
    """
    pinned_objectives = []
    objectives = pinned_elements.get("objectives", [])
    for objective in objectives:
        if "target" in objective.keys() and objective.get("target", "") != "":
            pinned_objectives.append(objective)
    pinned_elements["objectives"] = pinned_objectives
    pinned_objectives_dict = {
        key: ", ".join(
            [
                value.get("objective") or value.get("details")
                for value in values
                if value.get("objective") or value.get("details")
            ],
        )
        for key, values in pinned_elements.items()
        if isinstance(values, list)
    }
    supplier_profile = pinned_elements.get("supplier_profile", {})
    supplier_profile_str = " ,".join(
        [
            (
                f"""{terms.replace("ytd", "reference/current full year")} : """
                f"""{numerize(value, 1) if isinstance(value, numbers.Number) else value} """
            )
            for terms, value in supplier_profile.items()
            if value
        ],
    )

    objective_goal_str = ", ".join([f"{i}. {obj}\n" for i, obj in enumerate(objective_goals)])
    context_dict = {
        "Supplier Profile": supplier_profile_str,
        "# Objectives for negotiation": objective_goal_str,
        "# Pinned/ Selected Objectives": pinned_objectives_dict.get("objectives"),
    }
    context_dict_str = ", ".join(
        [f"{key}: {value}" for key, value in context_dict.items() if value],
    )
    prompt = f"""
        Task:
        You are a procurement expert for category {supplier_profile.get("category_name", "all categories")}.
        Your task is to generate generate summary email to the supplier - {supplier_profile.get("supplier_name")}
        by understanding negotiation objective and insights generated for that objective.

        A summary emails is always from the buyer to the supplier {supplier}.

        Key Information:
        -- Seller {supplier}: provides the products and services to the the buyers (us)
        -- Negotiation Objective or Objective: Buyer (we) set goals or objective and whole negotiation happens with
           supplier {supplier} on that  objectives.For example - Price Reduction, Increasing Payment Terms etc
        -- Insights: As a Buyer (we), we have facts and figures available to negotiate with supplier {supplier}
        -- current: current value of selected negotiation objective
        -- currentUnit: Unit used for current value of selected negotiation objective
        -- target: target value that buyer (we) want to achieve
        -- targetUnit: Unit used for target value of selected negotiation objective
        -- latestOffer: latest offer value received from supplier against the negotiation objective

        Reason logically using step by step reasoning:
        1. Understand the context below and filter out content for summary email generation:
        {context_dict_str}

        2. Summary email must consist of 6 parts (IMPORTANT):
           3.1: Use the exact subject information i.e. `Subject: Acceptance of Offer`, do not remove the colon(:) after Subject.
           3.2: Greet the supplier {supplier}.
           3.3: In 20-25 words, we should inform to the supplier {supplier} about the acceptance of offer,
                we must include category {supplier_profile.get("category_name", "all categories")} and
                {objective_goal_str} in short.
           3.4: Complete this part of the email in 50-75 words only in single paragraph.Describe the opprtunity
                from insights {context_dict.get("# Pinned/ Selected Insights")} in short,
                then make use of values of `current`, `currentUnit`, `target`, `targetUnit` and `latestOffer`
                from context against respective objective goals - {objective_goal_str} in short. Finally use the
                sentense like `strengthen our business relationship` to finish this part of the email.
           3.5: Use the exact information i.e. Thank you for your continued partnership. We look forward to your confirmation.
           3.6: Use the exact information i.e. Best Regards, then add {supplier}.

        Notes:
        1. AFTER EVERY PART OF THE EMAIL, ADD A NEW LINE.(IMPORTANT)
        2. DO NOT GENERATE PARTS OF THE PROMPTS Or PARSERS.
        3. Write to the point, concise and logically consistent emails and do not repeat yourself.
        4. If any key information is not available to generate the email,(For e.g. time or date of a meeting),
        5. ALWAYS ADD a placeholder text `[PLACEHOLDER]`.
        6. Use only the information provided in the context.
        7. Add numbers and derived metrics to support the email if necessary.
        8. Do not generate a garbled version of multiple emails.
        9. Strictly follow a format for emails when generating the response and keep it to the point.
        10. Please return the output as **raw JSON** without any markdown, code blocks, or formatting
            (such as ```json).Make sure it is a valid JSON response.
        11. Use procurement knowledge in the response (e.g. raw material cost increase can
        lead to price increase, inflation can lead to price increase).
    """
    parser = PydanticOutputParser(pydantic_object=EmailOutputParser)
    prompt_template = PromptTemplate.from_template(
        prompt
        + (
            "Format Output: {format_instructions} and only produce a valid JSON"
            " with keys `message`, `emails` ONLY"
            " NEVER include the word json or ` in emails \n."
        )
        + """
            Previous conversation with the Procurement Assistant:
            {history}
            Current Conversation-
            User provided context: {input}
            """,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    return prompt_template


def get_opportunity_extraction_prompt(insights: list[dict[str, Any]]) -> PromptTemplate:
    """
    Prompt for extracting opportunity values from insights.
    args:
        insights (list[dict[str, Any]]): List of insights to extract opportunity values from
        returns:
        (PromptTemplate): Prompt for extracting opportunity values from insights.
    """
    parser = PydanticOutputParser(pydantic_object=ExtractedOpportunityList)

    prompt = f"""
    You are a helpful assistant extracting the opportunity value from the following insights.
    For each insight, return a JSON object containing the id, opportunity_value and opportunity_unit mentioned in the input.
    If no opportunity value is found, return null for that id. Ensure that length of input insights and output should match.
    Do not skip any insight in the output.
    Do not use the word json in the output. Return only a valid JSON Object.
    E.g. {{"id":1245, "insight": "Total opportunity is 32.1M USD"}} should be converted to
     {{"id":1245, "opportunity_value": 32.1, "opportunity_scale": "M", "opportunity_currency": "USD"}}

    Insights:
    {insights}

    """
    # Escape curly braces in the f-string to avoid unintended variable interpretation
    escaped_prompt = prompt.replace("{", "{{").replace("}", "}}")

    prompt_template = PromptTemplate.from_template(template=escaped_prompt).partial(
        format_instructions=parser.get_format_instructions(),
    )
    return prompt_template



def generate_objective_summary_prompt(context_dict: dict[str, Any]) -> ChatPromptTemplate:
    """
    Generates a prompt template for summarizing actionable insights for negotiation.

    Args:
        input_insights_dict (dict[str, Any]): A dictionary containing insights and related information.
            - label (list): List of insights.
            - reinforcements (list): List of reinforcement types corresponding to each insight.
            - objective (str): The main objective of the negotiation.
            - category_name (str, optional): The category name for procurement.
            - supplier_name (str, optional): The supplier name.

    Returns:
        ChatPromptTemplate: A template for generating negotiation summaries.
    """
    
    context_dict = {key: value for key, value in context_dict.items() if value}
    data = context_dict.get("data", {})
    examples = {
        "incoterms": [
            "Analysis shows 2 SKUs have been purchased with multiple incoterms since the beginning of the year, "
            "covering a combined spend of EUR 8.25M. The two SKUs are (i) UPPER BEARING FY 2.15/16 TF/GHYVZ6A7 and "
            "(ii) UPPER BEARING UCF 215 WITH GUARD with respective spend of 5.14M, 3.11M EUR",
        ],
        "price reduction": [
            "a. There is a total price reduction opportunity of xM EUR (xM spend-base) on 'n' SKUs from the supplier SKF FRANCE."
            " The price reduction opportunity is driven by (i) price arbitrage analysis showing xK EUR opportunity "
            "(ii) parametric cost modelling showing xK EUR opportunity (iii) rates harmonization showing xK EUR opportunity"
            "b. There is a x% increase in spend with supplier SKF FRANCE with respect to the previous year (EUR xm 2022 to EUR ym 2023)."
            "  Driven primarily by [(i) price increases in SKUs A and B (ii) volume increase in SKUs A + B (iii) volume and price "
            "  increases in SKUs A and B"
            "c. There is EUR xm opportunity on x SKUs from Parametric Cost Modelling. According to our analysis, there is a gap between"
            "   actual price and should cost of x% for SKUs A and B. We would request you to reduce prices by x% ",
            "d. Top SKUs with the higest price arbitrage opportunity are (i) UPPER BEARING FY 2.15/16 TF/GHYVZ6A7 with xK EUR"
            "   (ii) UPPER BEARING UCF 215 WITH GUARD with yK EUR",
        ],
        "payment terms standardization": '''
            "a. Our analysis suggests that over the past year y EUR was paid earlier than contractually agreed."
            "Aligning payments with contractual payment terms represents an opportunity to increase working capital by x%."
            "b. As per our analysis, the best in class payment term days in the region is y Days."
            "We would like you to move our future purchases to this payment term."
            NOTE: Always give Avg Payment Term Days alone with Potential Cost Savings for a given time period''',

        "early payments": '''"c. Our analysis of early payment trends indicates that payments were made on average x days earlier than agreed, resulting in a discounted price and representing a potential savings opportunity of y EUR. Leveraging early payment discounts strategically can reduce procurement costs and optimize cash flow."
        NOTE: ALWAYS mention Early Payment Opportunityg and Avg Early Payment Days to achieve it for a given time period ''',

        "parametric cost modeling": [
            "Our analysis suggests 5 occurrences of the in-month price variation for the material PDR SKF BEARING ROLLER."
            " We ask you reduce the prices of this material to 13.80 EUR. (32.9%)",
        ],
        "unused discount":"a. Our analysis indicates that supplier discounts negotiated in contracts have not been fully utilized, leading to a missed savings opportunity of xK EUR. "
    "We request that future invoices reflect the agreed discount rates to maximize cost savings. "
    }



    example_str = "\n".join([str(key)+":"+str(examples[key]) for key in data.keys() if key in examples])
    example_str = "Example summaries FOR REFERENCE ONLY:" + example_str if example_str else ""
    




    prompt_template = f"""
You are a procurement domain expert for {context_dict.get("category")}.
Your task is to summarize actionable insights (from your perspective) to negotiate with the supplier
{context_dict.get("supplier", "")}. Never weaken your position to the supplier.

Insights available are of three types:
1. General or demand insights: Which need to be summarized and actions extracted.
2. Positive reinforcement while negotiating.
3. Negative reinforcement while negotiating.

KEY UNDERSTANDING:
1. Generate logically consistent summaries:
    - If there is a price decrease, despite volume increase, it's not a negotiating lever.
    - If there are price increases but unit price decreases, it's not a negotiating lever.
    - If there is a negative gap mentioned, do not use it in the summary.
    - If the price increase is lower than the inflation rate, it is not a negotiating lever.
2. For the **price reduction** objective:
    - Focus **only** on the following analytics:
        - Unused Discount Opportunities
        - Parametric Cost Modeling
        - Price Arbitrage Query
        - Early Payment Opportunities
    - **Do not include** payment term standardization-related insights.
        - Early Payment Opportunities
    - **Do not include** payment term standardization-related insights.
3. For the **payment terms** objective:
    - Focus only on payment behavior such as standard term optimization or early payment trends.
    - **Do not include** "Unused Discount Opportunities" in the summary.
    - Focus only on payment behavior such as standard term optimization or early payment trends.
    - **Do not include** "Unused Discount Opportunities" in the summary.
4. Never show negative values in days. Round up any day values and rephrase accordingly (e.g., "-8 days" becomes "payment made 8 days earlier").
5. Do not include any placeholder text like "no data available" or "data not present." Simply omit any missing data from the summary.

Strict Constraints:
- Do not include any statement or suggestion about a metric unless its data is present.
- Do not include placeholders or generic phrases for metrics with missing data.
- Never use coding-style terms like "unused_discount" or "parametric_cost_modeling" in the output. Convert all such keys into readable, human-like phrases (e.g., "Unused Discount Opportunities").

Take a step-by-step approach:
Step 1: Understand the main intent of the negotiation.
{context_dict.get("insight_objective")}

Step 2: Understand the data provided below, where each key represents an analytic type and the value is a multi-year dataframe containing relevant data for that key. A summary can be a combination of multiple analytic types, so capture each one completely.
{context_dict.get("data")}

Step 3: Based on the understanding gathered and domain knowledge, generate a detailed, **natural language summary** for each material (SKU) broken down as follows:

For each SKU:
    a. Year-level insights:
        - Include insights only for available analytics.
        - For **price reduction**, only include:
            - Unused Discount Opportunities
            - Parametric Cost Modeling
            - Price Comparison Analysis (Arbitrage)
            - Early Payment Opportunities
            - Early Payment Opportunities
        - Provide derived insights (e.g., % change, savings amount, pricing variance) for each analytic.
        - If multiple components exist for a single year and analytic type, list them as **bullet points**.
        - Each bullet must be descriptive — include the opportunity value, gap, and negotiation relevance.
        - Do **not** repeat the year header for each component.

    b. Quarter-level insights:
        - Include only if quarter-level data is available.
        - Follow the same formatting: show quarter once, then bullet points for each component within that analytic, with descriptive insights.

Format:

Summary:
- Start with an overall savings opportunity across all SKUs (sum of discount, arbitrage, and modeling savings).
- Follow with a natural language breakdown per SKU, **ordered by descending total savings opportunity**.
- Maintain a confident, consultative tone.
- Do not use bullet points in this section.

Details:
- List SKUs in **decreasing order of total savings**, structured like this:

    SKU: <Material Name or ID>
        Year: <YYYY>
            <Analytic Name>:
            - <Descriptive insight in natural language with amount, % gap, and leverage for negotiation>.
            <Analytic Name>:
            - <Descriptive insight in natural language with amount, % gap, and leverage for negotiation>.
            - <Component>: ...
        Quarter: <QX YYYY> (only if quarter-level data is present)
            <Analytic Name>:
            <Analytic Name>:
            - <Component>: <Descriptive insight>.
            - ...

Actions:
- Recommend **precise and data-backed negotiation levers**, such as specific price differences, gaps, or modeling insights.
- **For payment terms optimization**, always recommend negotiating for 90 days payment term to maximize working capital benefit.
- Avoid generic recommendations. Link each action to real data (e.g., "Negotiate for 90 days with <Supplier> for <SKU> to unlock a working capital benefit of €Y").
- **For payment terms optimization**, always recommend negotiating for 90 days payment term to maximize working capital benefit.
- Avoid generic recommendations. Link each action to real data (e.g., "Negotiate for 90 days with <Supplier> for <SKU> to unlock a working capital benefit of €Y").

Notes:
1. Always include derived metrics to support insights.
2. Do not use bullet points in the summary.
3. Use bullet points only within the **Details** section (for component-level breakdowns).
4. Avoid assumptions or speculative language—only use available data.
5. Maintain negotiating strength and a clear, cohesive narrative.
6. Use bullet points only in the "Actions" section and within grouped insights under each year/quarter in Details.
7. For **price reduction**, only include relevant analytics like unused discounts and early payments, avoiding any mention of payment terms actions.
8. Ensure the details are descriptive, with clear statements about potential savings or savings opportunities tied to each action.
7. For **price reduction**, only include relevant analytics like unused discounts and early payments, avoiding any mention of payment terms actions.
8. Ensure the details are descriptive, with clear statements about potential savings or savings opportunities tied to each action.
"""


    return ChatPromptTemplate([SystemMessage(prompt_template)])

# def generate_payment_terms_prompt(context_dict, supplier_profile) -> ChatPromptTemplate:
#     """
#     Generates a ChatPromptTemplate specifically for the Payment Terms negotiation objective.
#     Focused solely on aligning to a 90-day standard.
#     """
#     context_dict = {key: value for key, value in context_dict.items() if value}
#     data = context_dict.get("data", {})
#     log.info("supplier_profile, %s", supplier_profile)
#     log.info("data getting passed in payment terms %s", data)
# #     prompt_template = f"""
# # You are a procurement domain expert for {context_dict.get("category")}.
# # Your task is to generate a clean, structured, and aligned summary of payment term optimization opportunities with the supplier {context_dict.get("supplier", "")}.

# # This prompt is exclusively focused on the Payment Terms negotiation objective.

# # Strict Guidelines:
# # 1. Only include insights that appear in the provided data. Do not invent or generalize.
# # 2. If a SKU appears only in Q2 and Q4, do not mention Q1 or Q3 in that section.
# # 3. Never reuse quarters or savings across SKUs.
# # 4. Always use the exact 'Avg Payment Term Days' and 'Potential Cost Savings' values provided.
# # 5. Use the phrase “working capital benefit” consistently instead of “potential savings.”
# # 6. Do not include any generic recommendations or general improvement statements.

# # Step 1: Understand the input data:
# # {data}

# # Step 2: Generate the following structured output:

# # Summary:
# # - Start with a high-level, natural language overview of the working capital opportunity due to below-standard payment terms.
# # - Mention the supplier by name.
# # - Do not include any numeric values or SKUs in this section.

# # Details:
# # - Organize the information by Year → SKU.
# # - For each SKU:
# #     - Include only the years and quarters present in the data.
# #     - Start with a “Yearly Summary” that sums the working capital benefit across all quarters in that year for that SKU.
# #     - Follow with a breakdown per quarter (only if that quarter is present in the data).
# #     - Use the exact numeric values for “Avg Payment Term Days” and “Potential Cost Savings.”
# #     - Example:

# # Year: 2025  
# #     PDR SKF BEARING ROLLER  
# #         - Yearly Summary: The average payment terms are below the 90 day standard, with a total working capital benefit of approximately €4,080.  
# #         - In Q4, the average payment term is 66 days. Aligning this to 90 days could unlock a working capital benefit of €4,080.

# #     UPPER BEARING UCF 215 WITH GUARD  
# #         - Yearly Summary: Quarterly data suggests a total working capital benefit of €17,048.  
# #         - In Q3, the average payment term is 74 days. Adjustment to 90 days could yield €14,654 in working capital benefit.  
# #         - In Q2, the average payment term is 73 days. This offers a further benefit of €2,394.

# # Actions:
# # - For each SKU, generate **one actionable statement** based on the total working capital benefit across the year.
# # - Mention SKU name, supplier, and euro amount.
# # - Do not include generic or group-level action lines.
# # - Example:
# #     - "Extend payment terms to 90 days for PDR SKF BEARING ROLLER at SKF FRANCE to secure a working capital benefit of €4,080."
# #     - "Negotiate 90-day terms for UPPER BEARING UCF 215 WITH GUARD with SKF FRANCE to unlock a working capital benefit of €17,048."

# # Final Style Guidelines:
# # - Use clear, natural business language.
# # - Never make up quarters or values.
# # - Be consistent with terminology.
# # - Output must strictly follow the structure and logic of the data above.
# # - Always round up the days to the nearest whole number.
# # - Use the phrase “working capital benefit” consistently instead of “potential savings.”
# # - Never mention analytics where saving 

# # """
#     prompt_template = f"""
# You are a procurement domain expert for {context_dict.get("category")}.
# Your task is to generate a clean, structured, and aligned summary of payment term optimization opportunities with the supplier {context_dict.get("supplier", "")}.

# This prompt is exclusively focused on the Payment Terms negotiation objective.

# Definition:
# Payment term standardization refers to aligning all supplier payment terms to a common industry benchmark (typically 90 days).
# This allows the buyer to optimize cash flow and unlock working capital by delaying cash outflows in a standardized and efficient manner.

# Strict Guidelines:
# 1. Only include insights that appear in the provided data. Do not invent or generalize.
# 2. If a SKU appears only in Q2 and Q4, do not mention Q1 or Q3 in that section.
# 3. Never reuse quarters or savings across SKUs.
# 4. Always use the exact 'Avg Payment Term Days' and 'Potential Cost Savings' values provided.
# 5. Use the phrase “working capital benefit” consistently instead of “potential savings.”
# 6. Do not include any generic recommendations or general improvement statements.

# Step 1: Understand the input data:
# {data}

# Step 2: Generate the following structured output:

# Summary:
# - Start the summary with:
#   “The current average payment term days for {context_dict.get("supplier", "")} is {int(round(supplier_profile.get('payment_term_avg'), 0))}.”.
# - Then follow with a high-level, natural language overview of the working capital opportunity due to below-standard payment terms.
# - Mention the supplier by name.
# - Do not include any numeric values or SKUs beyond the initial average payment term sentence.

# Details:
# - Organize the information by Year → SKU.
# - For each SKU:
#     - Include only the years and quarters present in the data.
#     - Start with a “Yearly Summary” that sums the working capital benefit across all quarters in that year for that SKU.
#     - Follow with a breakdown per quarter (only if that quarter is present in the data).
#     - Use the exact numeric values for “Avg Payment Term Days” and “Potential Cost Savings.”
#     - Example:

# Year: 2025  
#     PDR SKF BEARING ROLLER  
#         - Yearly Summary: The average payment terms are below the 90 day standard, with a total working capital benefit of approximately €4,080.  
#         - In Q4, the average payment term is 66 days. Aligning this to 90 days could unlock a working capital benefit of €4,080.

#     UPPER BEARING UCF 215 WITH GUARD  
#         - Yearly Summary: Quarterly data suggests a total working capital benefit of €17,048.  
#         - In Q3, the average payment term is 74 days. Adjustment to 90 days could yield €14,654 in working capital benefit.  
#         - In Q2, the average payment term is 73 days. This offers a further benefit of €2,394.

# Actions:
# - For each SKU, generate **one actionable statement** based on the total working capital benefit across the year.
# - Mention SKU name, supplier, and euro amount.
# - Do not include generic or group-level action lines.
# - Example:
#     - "Extend payment terms to 90 days for PDR SKF BEARING ROLLER at SKF FRANCE to secure a working capital benefit of €4,080."
#     - "Negotiate 90-day terms for UPPER BEARING UCF 215 WITH GUARD with SKF FRANCE to unlock a working capital benefit of €17,048."

# Final Style Guidelines:
# - Use clear, natural business language.
# - Never make up quarters or values.
# - Be consistent with terminology.
# - Output must strictly follow the structure and logic of the data above.
# - Always round up the days to the nearest whole number.
# - Use the phrase “working capital benefit” consistently instead of “potential savings.”
# - Never mention analytics where saving is not available or zero.
# """

#     return ChatPromptTemplate([SystemMessage(prompt_template)])

# def generate_payment_terms_prompt(context_dict, supplier_profile) -> ChatPromptTemplate:
#     """
#     Generates a ChatPromptTemplate to enhance the natural language of a pre-generated
#     payment terms summary without altering its structure or numeric values.
#     """
#     context_dict = {key: value for key, value in context_dict.items() if value}
#     summary = context_dict.get("summary", "")
#     supplier_name = context_dict.get("supplier", "")
#     category = context_dict.get("category", "")
#     payment_term_avg = int(round(float(supplier_profile.get("payment_term_avg", 0))))

#     # prompt_template = f"""
#     # You are a procurement domain expert for the category: {category}.
#     # Your task is to enhance the **language** of the following pre-generated summary related to payment term standardization for the supplier {supplier_name}.

#     # This summary was generated based on precise calculations and must **not** be altered structurally or numerically.

#     # Definition:
#     # Payment term standardization refers to aligning all payment terms to a 90-day benchmark to improve working capital efficiency.

#     # Guidelines:
#     # 1. Your sole task is to **improve the natural language tone and clarity** of the summary.
#     # 2. **Do not modify or rephrase** any of the following:
#     # - Supplier name
#     # - Average payment term days or euros
#     # - Order of SKUs, quarters, or years
#     # 3. Do not add or remove any SKUs, quarters, or values.
#     # 4. Use business-appropriate language that sounds natural, varied, and human-like.
#     # 5. Maintain all facts and structure exactly as provided.
#     # 6. Preserve the three sections: Summary, Saving Opportunities (Details), and Actions.

#     # Current Average Payment Term for Supplier:
#     # - The current average payment term days for {supplier_name} is {payment_term_avg}.

#     # Enhance the following summary without altering any facts:
#     # {summary}
#     # """
    
#     # prompt_template = f"""
#     # You are a procurement strategy expert specializing in supplier engagement and working capital optimization for the category: {category}.

#     # Your objective is to refine the language of the following summary report, which outlines payment term standardization opportunities for the supplier **{supplier_name}**.

#     # Please note:
#     # - The report is based on verified data analytics and financial modeling.
#     # - **You must not alter the numeric values, data structure, or sequence**.

#     # ---

#     # **Definition:**  
#     # Payment term standardization involves aligning all SKU-level payment terms to a benchmark of **90 days**, with the goal of unlocking working capital and improving cash flow discipline.

#     # ---

#     # **Instructions for Enhancement:**
#     # 1. Your sole task is to enhance the **clarity, tone, and business professionalism** of the language used in the summary.
#     # 2. **Do not modify, reorder, or exclude**:
#     # - Supplier name (**{supplier_name}**)
#     # - Any average payment term figures or euro amounts
#     # - The order of SKUs, quarters, or years
#     # 3. **Do not introduce or remove** any SKUs, years, quarters, or numeric entries.
#     # 4. Use precise, boardroom-ready phrasing that is natural, human-like, and reflective of executive-level reporting.
#     # 5. Preserve the existing structure and content under the following three headings:
#     # - **Summary**
#     # - **Saving Opportunities**
#     # - **Actions**

#     # ---

#     # **Current Baseline Metric:**  
#     # - The current average payment term across all transactions with {supplier_name} is **{payment_term_avg} days**.

#     # ---

#     # Please elevate the writing quality of the following summary without introducing any changes to data or structure:

#     # {summary}
#     # """

#     prompt_template = f"""
#     You are a procurement expert working on the category: {category}.

#     Your task is to improve the **language and tone** of the following summary related to payment term standardization for the supplier {supplier_name}.

#     Consider yourself as prcrutment bussiness expert. now rewrite the response.

#     Please follow these rules:

#     1. Do not change any numbers, dates, or SKUs.
#     2. Keep the order of SKUs, years, and quarters exactly the same.
#     3. Keep the three main sections: Summary, Saving Opportunities, and Actions.
#     4. Do not add or remove any content.
#     5. Just make the writing more clear, natural, and professional.

#     Definition:
#     Payment term standardization means aligning all payment terms to 90 days to improve working capital.

#     Current average payment term for {supplier_name}: {payment_term_avg} days.

#     Now, improve the language of this summary without changing any facts:

#     {summary}
#     """

#     return ChatPromptTemplate([SystemMessage(prompt_template)])

def generate_payment_terms_prompt(context_dict, supplier_profile) -> ChatPromptTemplate:
    """
    Generates a ChatPromptTemplate to enhance the natural language of a pre-generated
    payment terms summary without altering its structure or numeric values.
    """
    context_dict = {key: value for key, value in context_dict.items() if value}
    log.info("context_dict, %s", context_dict)
    summary = context_dict.get("summary", "")
    supplier_name = context_dict.get("supplier", "")
    category = context_dict.get("category", "")
    payment_term_avg = int(round(float(supplier_profile.get("payment_term_avg", 0))))

    # Updated prompt template for language refinement with YTD instructions
    prompt_template = f"""
    You are a procurement expert specializing in supplier engagement and working capital optimization for the category: {category}.

    Your task is to improve the **language and tone** of the following summary related to payment term standardization for the supplier {supplier_name}. The goal is to make the language clearer, more professional, and varied, while keeping the data, structure, and facts unchanged.

    Please follow these guidelines:

    1. **Do not alter any numbers, dates, or SKUs**.
    2. **Keep the order** of SKUs, years, and quarters exactly as they are.
    3. Ensure that the summary includes the three main sections: **Summary**, **Details**, and **Actions**.
    4. **Do not introduce or remove any content**. The facts and structure must remain exactly the same.
    5. Make sure to **vary the language**: improve tone and readability with natural, engaging, and varied phrasing, avoiding overly repetitive language.
    6. Use a **business-professional tone**, suitable for executive-level reporting. The writing should be polished and crisp, conveying the information clearly and effectively.
    7. In the **Details** section, ensure that 2025 figures are referenced with **YTD** where applicable. For example, use natural variations such as:
    - "In 2025 YTD, the average payment term is..."
    - "As of 2025 YTD, the average payment term is..."
    - "So far in 2025, the average payment term is..."
    - "Through 2025 YTD, the average payment term stands at..."
    - "As of 2025 YTD, the average payment term for this SKU is..."
    - "Through 2025 YTD, the average payment term is 60 days, which could have resulted in an unrealized working capital benefit of approximately €10,000."
    - "In 2025 YTD, the average payment term is 72 days, leading to an unrealized working capital benefit of €13,570."
    8. Focus on **clarity** and **natural flow**, while maintaining the formality and professionalism expected in procurement reporting.

    **Definition:**  
    Payment term standardization refers to aligning all payment terms to a 90-day benchmark to improve working capital and optimize cash flow.

    **Current baseline metric:**  
    The current average payment term for {supplier_name} is **{payment_term_avg} days**.

    Now, please rewrite the following summary in a more polished, natural, and professional manner, without changing any factual details:

    Make sure the language is getting updated every time and not the data.

    {summary}
    """

    return ChatPromptTemplate([SystemMessage(prompt_template)])


def generate_price_reduction_prompt(context_dict) -> ChatPromptTemplate:
    """
    Generates a ChatPromptTemplate specifically for the Price Reduction negotiation objective.
    Consolidates all insights per SKU, but explicitly labels each analytic in natural language sentences.
    """
    log.info(f'data recived for price reduction objective, {context_dict.get("data", {})}')
    
    context_dict = {key: value for key, value in context_dict.items() if value}
    data = context_dict.get("data", {})
    log.info("data getting passed in price reduction, %s", data)

#     prompt_template = f"""
# You are a senior procurement strategist preparing a price reduction negotiation brief for the category {context_dict.get("category")} with supplier {context_dict.get("supplier", "")}.

# Use only the data provided—do not fabricate or infer missing values:
# {data}

# Return your output in up to three clearly titled sections, in this exact order:
# Summary
# Details
# Actions

# Summary
# - Begin with: "After performing various analyses, we found that we can save approximately €X—corresponding to a gap range of A–B%—by addressing pricing inefficiencies across components."
# - Follow with a sentence identifying where the biggest savings are, e.g.:
#   "The largest opportunities lie in stainless steel scrap, R&D, energy, and machine costs across key SKUs."
# - Ensure the €X value represents the **aggregated total savings across all valid opportunities from the following analytics**:
#   - Cleansheet: `CLEANSHEET_OPPORTUNITY` (from "Total Saving Achieved")
#   - Early Payments: `EARLY_PAYMENT_OPPORTUNITY` (from "early payments")
#   - Unused Discounts: `DISCOUNT_NOT_USED` (from "unused discount")
#   - Price Arbitrage: `PRICE_ARBITRAGE_PERCENTAGE` (from "price arbitrage query") — apply percentage to related spend if required
# - A–B% should reflect the **lowest and highest non-zero percentage gaps** observed across all applicable analytics, based on the available data.

# Details
# - Include only if there is at least one positive savings amount (> €0) or gap (> 0%).
# - For each SKU, show a header followed by all valid savings insights (sorted by savings amount, descending):
#   `<SKU name> (<Year>)`
#     - `The <Component> cost shows a gap of <percent>% with a savings opportunity of €<amount>.`
#     - `Early payment: paid <X> days earlier, saved €<Y>` (if applicable)
# - Do not include components with 0% gap or €0 savings
# - Use natural, professional business language without repeating labels

# Actions
# - Include only if Details are present.
# - Each action must summarize **overall savings for that SKU**, aggregating all valid opportunities across the following analytics. The savings must be computed independently for each SKU, based on the data provided. This applies regardless of how many SKUs are present—dynamically identify each distinct SKU (each SKU is identified by the 'MATERIAL' field), and calculate its total savings by summing all valid Cleansheet, Early Payment, Unused Discount, and Price Arbitrage values associated with it.

#   Automatically compute per-SKU totals by summing all analytics values specific to that SKU from:
#     - `Engage {context_dict.get("supplier", "")} to align cost drivers for SKU <SKU>, targeting savings of up to €<aggregated_savings_for_SKU>.`
#     - `Accelerate payments for SKU <SKU> by <X> days to unlock €<Y> savings.`
# - Ensure that savings shown in actions are **specific to each SKU**, computed as the sum of Cleansheet, Early Payment, Unused Discount, and Price Arbitrage values for that SKU only. Do not reuse or replicate the overall summary value.
# - Do not include early payment actions unless valid early payment data is present in the dataset.

# Strict Rules
# - Always include Summary
# - Include Details and Actions only when valid
# - Include all components with savings > €0 and gap > 0%
# - Aggregate savings across all four analytics: Cleansheet, Early Payments, Unused Discounts, Price Arbitrage
# - Never include zero/negative savings or technical analytic terms
# - No placeholder values like x or y in final output
# """

#     prompt_template = f"""
# You are a senior procurement strategist preparing a price reduction negotiation brief for the category {context_dict.get("category")} with supplier {context_dict.get("supplier", "")}.

# Use only the data provided—do not fabricate or infer missing values:
# {data}

# Return your output in up to three clearly titled sections, in this exact order:
# Summary
# Details
# Actions

# Summary
# - Begin with: "After performing various analyses, we found that we can save approximately €X—corresponding to a gap of A%—by addressing pricing inefficiencies across components."
# - Follow with a sentence identifying where the savings are, e.g.:
#   "The opportunity lies in the <component> component." (If only one SKU is available, remove "largest opportunities lie in" and simply state where the savings come from.)
# - If multiple SKUs are present, follow with a sentence identifying where the biggest savings are, e.g.:
#   "The largest opportunities lie in stainless steel scrap, R&D, energy, and machine costs across key SKUs."
# - Ensure the €X value represents the **aggregated total savings across all valid opportunities from the following analytics**:
#   - Cleansheet: `CLEANSHEET_OPPORTUNITY` (from "Total Saving Achieved")
#   - Early Payments: `EARLY_PAYMENT_OPPORTUNITY` (from "early payments")
#   - Unused Discounts: `DISCOUNT_NOT_USED` (from "unused discount")
#   - Price Arbitrage: `PRICE_ARBITRAGE_PERCENTAGE` (from "price arbitrage query") — apply percentage to related spend if required
# - A% should reflect the **gap percentage** for a single SKU when only one SKU is available or the **lowest and highest non-zero percentage gaps** observed across all SKUs.
# - **All savings and gaps are based on the current year (2025) YTD data**.

# Details
# - Include only if there is at least one positive savings amount (> €0) or gap (> 0%).
# - For each SKU, show a header followed by all valid savings insights (sorted by savings amount, descending):
#   `<SKU name> (<Year>)`
#     - `The <Component> cost shows a gap of <percent>% with a savings opportunity of €<amount> based on 2025 YTD data.`
#     - `Early payment: paid <X> days earlier, saved €<Y> (based on 2025 YTD data)` (if applicable)
# - Do not include components with 0% gap or €0 savings.
# - Use natural, professional business language without repeating labels.

# Actions
# - Include only if Details are present.
# - Each action must summarize **overall savings for that SKU**, aggregating all valid opportunities across the following analytics. The savings must be computed independently for each SKU, based on the data provided. This applies regardless of how many SKUs are present—dynamically identify each distinct SKU (each SKU is identified by the 'MATERIAL' field), and calculate its total savings by summing all valid Cleansheet, Early Payment, Unused Discount, and Price Arbitrage values associated with it.

#   Automatically compute per-SKU totals by summing all analytics values specific to that SKU from:
#     - `Engage {context_dict.get("supplier", "")} to align cost drivers for SKU <SKU>, targeting savings of up to €<aggregated_savings_for_SKU> based on 2025 YTD data.`
#     - `Accelerate payments for SKU <SKU> by <X> days to unlock €<Y> savings.`
# - Ensure that savings shown in actions are **specific to each SKU**, computed as the sum of Cleansheet, Early Payment, Unused Discount, and Price Arbitrage values for that SKU only, based on **2025 YTD data**.
# - Do not include early payment actions unless valid early payment data is present in the dataset.

# Strict Rules
# - Always include Summary.
# - Include Details and Actions only when valid.
# - Include all components with savings > €0 and gap > 0%.
# - Aggregate savings across all four analytics: Cleansheet, Early Payments, Unused Discounts, Price Arbitrage.
# - Never include zero/negative savings or technical analytic terms.
# - No placeholder values like x or y in final output.
# """

#     prompt_template = f"""
# You are a senior procurement strategist preparing a price reduction negotiation brief for the category {context_dict.get("category")} with supplier {context_dict.get("supplier", "")}.

# Use only the data provided—do not fabricate or infer missing values:
# {data}

# Return your output in three clearly titled sections, in this exact order:
# Summary  
# Details  
# Actions  

# Summary  
# - Always begin with: "After performing various analyses, we found that significant savings opportunities exist by addressing pricing inefficiencies."
# - If **only one SKU** presents a valid opportunity:
#     - Mention the SKU name directly and state the specific gap and potential savings, e.g.:
#       "There is a cost gap of 28.25% for UPPER BEARING FY 2.15/16 TF/GHYVZ6A7 with a savings potential of €574,764.37."
# - If **multiple SKUs** present valid opportunities:
#     - Mention the gap range across SKUs and reference cost drivers more generally, e.g.:
#       "There are cost gaps ranging from 12% to 28.25% across selected items, representing pricing inefficiencies across components."
# - All savings and gaps should be based on 2025 YTD data.
# - Total savings (aggregated across SKUs and components) should be included at the end of the summary, e.g.:
#   "The total potential saving amounts to approximately €X based on 2025 YTD data."

# Details  
# - Include only if at least one SKU shows savings > €0 or gap > 0%.
# - For each SKU, include the year and insights, sorted by savings amount (descending):
#   <SKU name> (2025)
#     - The <Component> cost shows a gap of <percent>% with a savings opportunity of €<amount>.
#     - Early payment: paid <X> days earlier, saved €<Y> (if applicable)
# - Avoid repetition and technical terminology.
# - Do not include components with 0% gap or €0 savings.

# Actions  
# - Include only if Details are present.
# - For each SKU, sum all valid savings values from:
#   - CLEANSHEET_OPPORTUNITY
#   - EARLY_PAYMENT_OPPORTUNITY
#   - DISCOUNT_NOT_USED
#   - PRICE_ARBITRAGE_PERCENTAGE (apply to relevant spend if needed)
# - Show:
#   - "Engage {context_dict.get("supplier", "")} to align cost drivers for SKU <SKU>, targeting savings of up to €<aggregated_savings> based on 2025 YTD data."
#   - If valid early payment data is present:  
#     - "Accelerate payments for SKU <SKU> by <X> days to unlock €<Y> savings."
# - If multiple SKUs present savings, include a general action:
#   - "Engage {context_dict.get("supplier", "")} to align cost drivers for SKUs listed above, targeting total savings of up to €<total_aggregated_savings> based on 2025 YTD data."

# Strict Rules  
# - Always include Summary.
# - Include Details and Actions only when applicable.
# - Never include placeholder values.
# - Use business-natural language.
# - Aggregate savings strictly by SKU using only 2025 YTD data.
# """

#     prompt_template = f"""
# You are a senior procurement strategist preparing a price reduction negotiation brief for the category {context_dict.get("category")} with supplier {context_dict.get("supplier", "")}.

# Use only the data provided—do not fabricate or infer missing values:
# {data}

# Return your output in three clearly titled sections, in this exact order:
# Summary  
# Details  
# Actions  

# Summary  
# - Always begin with: "After performing various analyses, we found that significant savings opportunities exist by addressing pricing inefficiencies."
# - If **only one SKU** presents a valid opportunity:
#     - Mention the SKU name directly and state the specific gap and potential savings, e.g.:
#       "There is a cost gap of 28.25% for UPPER BEARING FY 2.15/16 TF/GHYVZ6A7 with a savings potential of €574,764.37."
# - If **multiple SKUs** present valid opportunities:
#     - Mention the gap range across SKUs and reference cost drivers more generally, e.g.:
#       "There are cost gaps ranging from 12% to 28.25% across selected items, representing pricing inefficiencies across components."
# - Do **not** mention the total savings value in the Summary.
# - All references should be based on 2025 YTD data.

# Details  
# - Include only if at least one SKU shows savings > €0 or gap > 0%.
# - For each SKU, display the insights in a single line as follows:
#   "<SKU name>: The cost shows a gap of <percent>% with a savings opportunity of €<amount> based on 2025 YTD data."
# - If valid early payment data exists, append:  
#   " Paid <X> days earlier, saved €<Y>."
# - Avoid repetition and technical terminology.
# - Do not include components with 0% gap or €0 savings.

# Actions  
# - Include only if Details are present.
# - For each SKU, sum all valid savings values from:
#   - CLEANSHEET_OPPORTUNITY
#   - EARLY_PAYMENT_OPPORTUNITY
#   - DISCOUNT_NOT_USED
#   - PRICE_ARBITRAGE_PERCENTAGE (apply to relevant spend if needed)
# - Show:
#   - "Engage {context_dict.get("supplier", "")} to align cost drivers for SKU <SKU>, targeting savings of up to €<aggregated_savings> based on 2025 YTD data."
#   - If valid early payment data is present:  
#     - "Accelerate payments for SKU <SKU> by <X> days to unlock €<Y> savings."
# - If multiple SKUs present savings, include a general action:
#   - "Engage {context_dict.get("supplier", "")} to align cost drivers for SKUs listed above, targeting total savings of up to €<total_aggregated_savings> based on 2025 YTD data."

# Strict Rules  
# - Always include Summary.
# - Include Details and Actions only when applicable.
# - Never include placeholder values.
# - Use business-natural language.
# - Aggregate savings strictly by SKU using only 2025 YTD data.
# """
#     prompt_template = f"""
# You are a senior procurement strategist preparing a price reduction negotiation brief for the category {context_dict.get("category")} with supplier {context_dict.get("supplier", "")}.

# Use only the data provided—do not fabricate or infer missing values:
# {data}

# Return your output in three clearly titled sections, in this exact order:
# Summary  
# Details  
# Actions  

# Summary  
# - Always begin with: "After performing various analyses, we found that significant savings opportunities exist by addressing pricing inefficiencies."
# - If **only one SKU** presents a valid opportunity (with savings ≥ €1,000):
#     - Mention the SKU name and its cost gap, but **do not** mention the savings value.
#     - Example format (for structure, not fixed numbers):  
#       "The SKU <SKU> presents a cost gap of <percent>% based on 2025 YTD data."
# - If **multiple SKUs** present valid opportunities:
#     - Mention the range of cost gaps observed and refer to inefficiencies across selected components.
# - Do **not** include the total savings value in the Summary.
# - All references must be based strictly on 2025 YTD data.
# - Exclude any SKU with total savings < €1,000.

# Details  
# - Include only if at least one SKU (with total savings ≥ €1,000) shows savings > €0 or gap > 0%.
# - For each qualifying SKU, present a single-line insight:
#   "<SKU name>: The cost shows a gap of <percent>% with a savings opportunity of €<amount> based on 2025 YTD data."
# - If valid early payment data exists for that SKU and savings from it are ≥ €1,000, append:
#   " Paid <X> days earlier, saved €<Y>."
# - Exclude components with gap = 0% or savings = €0.
# - Exclude SKUs where total savings (from all analytics combined) is < €1,000.

# Actions  
# - Include only if Details are present.
# - For each SKU with total savings ≥ €1,000, sum all valid savings from:
#   - CLEANSHEET_OPPORTUNITY
#   - EARLY_PAYMENT_OPPORTUNITY
#   - DISCOUNT_NOT_USED
#   - PRICE_ARBITRAGE (apply to relevant spend if needed)
# - Show:
#   - "Engage {context_dict.get("supplier", "")} to align cost drivers for SKU <SKU>, targeting savings of up to €<aggregated_savings> based on 2025 YTD data."
#   - If valid early payment data is present and ≥ €1,000:
#     - "Accelerate payments for SKU <SKU> by <X> days to unlock €<Y> savings."
# - If multiple SKUs qualify, you may include a general action:
#   - "Engage {context_dict.get("supplier", "")} to align cost drivers for SKUs listed above, targeting total savings of up to €<total_aggregated_savings> based on 2025 YTD data."

# Strict Rules  
# - Always include Summary.
# - Include Details and Actions only when applicable.
# - Never use placeholder values or static examples.
# - Exclude SKUs with < €1,000 in total savings.
# - Do not include savings values in the Summary (even for a single SKU).
# - Use professional, natural business language.
# - Aggregate savings strictly per SKU using only 2025 YTD data.
# """
    prompt_template = f"""
You are a senior procurement strategist preparing a price reduction negotiation brief for the category {context_dict.get("category")} with supplier {context_dict.get("supplier", "")}.

Use only the data provided—do not fabricate or infer missing values:
{data}

When analyzing savings opportunities, **consider only these saving columns**:  
- EARLY_PAYMENT_OPPORTUNITY  
- DISCOUNT_NOT_USED  
- CLEANSHEET_OPPORTUNITY  
- PRICE_ARBITRAGE  

Return your output in three clearly titled sections, in this exact order:  
Summary  
Details  
Actions  

Summary  
- Always begin with: "After performing various analyses, we found that significant savings opportunities exist by addressing pricing inefficiencies."  
- If **only one SKU** presents a valid opportunity with total savings (sum of the above four columns) ≥ €1,000:  
    - Mention the SKU name and its cost gap, but **do not** mention the savings value.  
    - Example: "The SKU <SKU> presents a cost gap of <percent>% based on 2025 YTD data."  
- If **multiple SKUs** present valid opportunities (each with total savings ≥ €1,000):  
    - Mention the range of cost gaps observed and refer to inefficiencies across selected components.  
- Do **not** include total savings in the Summary.  
- All references must be based strictly on 2025 YTD data.  
- Exclude SKUs with total savings (sum of the four columns) less than €1,000.

Details  
- Include only SKUs where total savings (sum of the four columns) ≥ €1,000 and where savings > €0 or gap > 0%.  
- For each qualifying SKU, present a single-line insight:  
  "<SKU name>: The cost shows a gap of <percent>% with a savings opportunity of €<amount> based on 2025 YTD data."  
- If valid early payment data exists for that SKU with EARLY_PAYMENT_OPPORTUNITY savings ≥ €1,000, append:  
  " Paid <X> days earlier, saved €<Y>."  
- Exclude components with gap = 0% or savings = €0.  
- Include SKUs named '#', '$', or any special characters without exception.

Actions  
- Include only if Details are present.  
- For each SKU with total savings ≥ €1,000, sum valid savings from only these columns:  
  - EARLY_PAYMENT_OPPORTUNITY  
  - DISCOUNT_NOT_USED  
  - CLEANSHEET_OPPORTUNITY  
  - PRICE_ARBITRAGE (apply to relevant spend if needed)  
- Show:  
  - "Engage {context_dict.get("supplier", "")} to align cost drivers for SKU <SKU>, targeting savings of up to €<aggregated_savings> based on 2025 YTD data."  
  - If valid early payment data is present and EARLY_PAYMENT_OPPORTUNITY savings ≥ €1,000:  
    - "Accelerate payments for SKU <SKU> by <X> days to unlock €<Y> savings."  
- If multiple SKUs qualify, you may include a general action:  
  - "Engage {context_dict.get("supplier", "")} to align cost drivers for SKUs listed above, targeting total savings of up to €<total_aggregated_savings> based on 2025 YTD data."

Strict Rules  
- Always include Summary.  
- Include Details and Actions only when applicable.  
- Never use placeholder values or static examples.  
- Exclude SKUs with total savings (sum of EARLY_PAYMENT_OPPORTUNITY, DISCOUNT_NOT_USED, CLEANSHEET_OPPORTUNITY, PRICE_ARBITRAGE) < €1,000.  
- Do not exclude or ignore SKUs based on name format or special characters.  
- Do not include savings values in the Summary (even for a single SKU).  
- Use professional, natural business language.  
- Aggregate savings strictly per SKU using only 2025 YTD data and only the four specified saving columns.
"""

    return ChatPromptTemplate([SystemMessage(prompt_template)])


def create_chatbot_prompt(user_query: str, supplier_name: str, category: str) -> str:
    """
    Generates a structured prompt for the key fact chatbot based on user input.

    Parameters:
        user_query (str): The user's query about the supplier.
        supplier_name (str): The name of the supplier.
        category (str): The category under which the query falls.

    Returns:
        str: A well-structured prompt for the chatbot.
    """
    
    prompt_template = f"""
    You are an intelligent procurement assistant. Given a user’s query, a supplier name, and a category, generate a precise and well-structured question to ask the key fact chatbot.
    The question should be direct, clear, and relevant to obtaining key factual information.

    ### Inputs:
    - **User Query:** {user_query}
    - **Supplier Name:** {supplier_name}
    - **Category:** {category}

    ### Instructions:
    1. Reframe the user query into a clear and fact-seeking question.
    2. Ensure the question is specific to the supplier and category.
    3. Avoid vague or open-ended phrasing—ensure the question prompts a direct factual response.
    4. Use formal and professional language.

    Given user's query convert and fix user's query to a standard format.
    User's query can be anything and it may not be in the standard format.

    ### MANDATORY INSTRUCTIONS ###
    1. ALWAYS OUTPUT THE FIXED QUERY
    2. ALWAYS KEEP THE PREFIX AS "Calculate the"
    3. Make Sure that LLM can understand this question.
    5. FIX THE SPELLING MISTAKES
    6. ALWAYS PUT CURRENT YEAR IN CONDITION IF NOT TIME IS MENTIONED
    7. IF YOU FIND A PROPER NOUN OR A NAME OR AN ID PUT IT IN '' OR "".
    8. KEYWORDS LIKE MATERIAL, SUPPLIER, COMPANY IS A BUSINESS ENTITY AND SHOULD BE PUT IN '' OR "".
    8. IF NO TIME IS MENTIONED THEN PUT THE CURRENT YEAR IN THE CONDITION.
    9. UPDATE THE METRIC NAME TO THE STANDARD METRIC NAME
        1. PCM OPPORTUNITY: Parameteric Cost Modeling Opportunity OR PCM GAP Opportunity OR Cleansheet Opportunity
        2. PRICE ARBITRAGE: PRICE ARBITRAGE or RATE HARMONIZATION
        3. Savings Opportunity: Total Savings Opportunity
        4. HCC LCC Opportunity: HCC LCC Opportunity or HCC to LCC Opportunity
        5. OEM NON OEM: OEM vs NON OEM or OEM TO NON OEM
        6. UNUSED DISCOUNT: UNUSED DISCOUNT OPPORTUNITY
        7. EARLY PAYMENT: EARLY PAYMENT OPPORTUNITY
        8. POTENTIALS SAVINGS BY STANDARDIZATION: POTENTIAL SAVINGS BY STANDARDIZATION
        9. RAW MATERIALS: COMPONENTS
    
    ### STANDARD FORMAT ###
    The standard format consists of three parts:
    1. **Prefix**: The leading phrase that sets up the query (e.g., "What are the", "Calculate the", "How many", "What is my").
    2. **Metric**: The key measurement or subject of the query (e.g., "PCM Opportunity", "Price Arbitrage").
    3. **Condition**: The contextual filters or constraints (e.g., "in current year and in category bearings").

    Query: {{ user_query }}

    ### Examples ###
    Here are few examples:
    1.  query: "what is the price of tin in asia for year 2024 in category bearings"
        ### STANDARD FORMAT ###
        prefix: "what is the"
        metric: "price of tin"
        condition: "in asia for year 2024"
        
        ### OUTPUT ###
        
            "Calculate the price of tin in asia for year 2024 in category bearings"
        

    2. query: "calculate the PCM Opportunity in current year in category bearings"
        ### STANDARD FORMAT ###
        prefix: "calculate the"
        metric: "PCM Opportunity"
        condition: "in current year in category bearings" 

        ### OUTPUT ###
        
            "Calculate the PCM Opportunity in current year in category 'bearings'"
        
    
    3. calculate the rate harmonization for each supplier in year 2023 in category bearings
        ### STANDARD FORMAT ###
        prefix: "calculate the"
        metric: "PCM Opportunity"
        condition: "in current year in category bearings"

        ### OUTPUT ###
        
            "Calculate the rate harmonization for each supplier in year 2023 in category 'bearings'"
        

    4. How many suppliers are there in category bearings
        ### STANDARD FORMAT ###
        prefix: "how many"
        metric: "Suppliers"
        condition: "in category bearings"

        ### OUTPUT ###
        
            "Calculate the count of suppliers in category 'bearings' in current year"
        

    5. Is the market price for this category predicted to go up or down in the next 3 months?
        ### STANDARD FORMAT ###
        prefix: "is the"
        metric: "market price to go up or down"
        condition: "in the next 3 months in category bearings"

        ### OUTPUT ###
        
           "Calculate the marktet price to go up or down in the next 3 months in category 'bearings'"
        

    6. What is the total spend for the company Complex Assembly Safety GmbH?
        ### STANDARD FORMAT ###
        prefix: "What is the"
        metric: "total spend"
        condition: "for the company 'Complex Assembly Safety GmbH'"

        ### OUTPUT ###
        
            "Calculate the total spend for the company 'Complex Assembly Safety GmbH' in current year"
        
    7. savings oppurtunity for material in category bearings
        ### STANDARD FORMAT ###
        prefix: "calculate the"
        metric: "total savings opportunity"
        condition: "for material in category 'bearings'"

        ### OUTPUT ###
        
            "calculate the total savings opportunity for material in category 'bearings' in current year"
        

        Output Format:
        
            "..."
        

    """

    return ChatPromptTemplate([SystemMessage(prompt_template)])

def str_match_prompt(user_query):

    prompt_template = f'''You are a text classifier that maps procurement-related queries to predefined pattern keys. 
    Given a user query, return the appropriate pattern key and numeric value (if present). 

    Available Patterns Key and Values:
    - "top_suppliers_tail_spend": Matches queries like "10 tail suppliers", "top tail vendors", "tail suppliers".
    - "largest_gap": Matches queries like "5 suppliers with largest YOY spend evolution", "suppliers with highest YoY spend increase".
    - "spend_without_po": Matches queries like "suppliers with missing PO spend".
    - "highest_single_spend": Matches queries like "single source vendors", "single-source suppliers".
    - "top_supplier": Matches queries like "top 20 suppliers by spend", "top spend suppliers".
    - "top_supplier_by_opportunity": Matches queries like "top suppliers by opportunity", "top suppliers by savings", "top opportunity suppliers"

    Extract the **pattern key** and **value** from the given query. If no number is present, default to "10".
    if **pattern** is about top_suppliers_tail_spend and if no number is present, default to "5".

    ### Example Outputs:
    Input: "top 20 suppliers by spend"
    Output:  "pattern_key": "top_supplier", "value": "20"

    Input: "suppliers with largest YOY spend evolution"
    Output:  "pattern_key": "largest_gap", "value": "5"

    Now classify this query:
    {user_query}

    '''
    return ChatPromptTemplate([SystemMessage(prompt_template)])

def create_objectives_prompt_v2(supplier,category,analytics_data,supplier_profile,insights_data):

    # prompt_template = f"""
    # You are a procurement strategy expert for category {category}, advising on negotiations with {supplier}. 
    # Based on the data provided, generate clear and concise negotiation objectives that focus on optimizing commercial terms such as payment terms,
    # pricing, volume discounts etc.
    # prompt_template = f"""
    # You are a procurement strategy expert for category {category}, advising on negotiations with {supplier}. 
    # Based on the data provided, generate clear and concise negotiation objectives that focus on optimizing commercial terms such as payment terms,
    # pricing, volume discounts etc.

    # The output should be structured with the following sections for each objective:
  
    # Summary:  
    # Start with the current state for the supplier and the selected SKUs. Mention any benchmarks or targets that present a negotiation opportunity.
    # Use simple, actionable language.  

    # Saving opportunities:  
    # List SKUs or spend categories. For each, specify the current status (e.g. average payment term), what the target could be 
    # (e.g. aligning to 90 days), and quantify the potential benefit (e.g. working capital unlocked or cost savings).  

    # Actions:  
    # End with 1-2 specific recommendations. Focus on what should be changed and why — keep it results-focused.

    # Use a professional but straightforward tone, just like in internal procurement strategy documents. 
    # Avoid generic advice and make the output data-driven and measurable wherever possible.

    # Return the final output strictly in the following JSON format. The "objectives" list may contain multiple non-overlapping objectives. 
    # Do not include any extra text, explanations, or formatting.

    # {{{{
    # "objectives": [
    #     {{{{
    #     "id": 0,
    #     "objective": "Summary:\\n[Start with a concise overview of current state and opportunity. Include specific data points: payment terms, prices, volumes, benchmarks. Keep it factual.]\\n\\nSaving opportunities:\\n[List 2-3 key SKUs or categories. For each, provide supporting data: current term/price, target term/price, and estimated opportunity in € where applicable.]\\n\\nActions:\\n[Recommend specific actions—e.g., extend payment terms, renegotiate price, align to benchmark. Quantify benefits if possible.]",
    #     "objective_type": "[e.g., Payment Terms, Price Reduction, Volume Leverage, etc.]",
    #     "objective_reinforcements": [],
    #     "list_of_skus": [
    #         "[SKU 1]",
    #         "[SKU 2]",
    #         "[...]"
    #     ]
    #     }}}},
    #     {{{{
    #     "id": 1,
    #     "objective": "Summary:\\n[...]\n\\nSaving opportunities:\\n[...]\n\\nActions:\\n[...]",
    #     "objective_type": "[...]",
    #     "objective_reinforcements": [],
    #     "list_of_skus": [
    #         "[SKU 1]",
    #         "[SKU 2]",
    #         "[...]"
    #     ]
    #     }}}}
    # ]
    # }}}}

    # Only return a valid, parsable JSON object as the output. Do not include any explanations, markdown, or surrounding text. 
    # Focus on clear, measurable, and structured insights in professional procurement language.

    # == Available Analytics ==
    
    # Data: {{{additional_data}}}

    # """
    
    # prompt_template = f"""
    # You are a procurement domain expert for {category}, advising on negotiations strategy with {supplier} with facts as per the input data.
    # Maintain maximum leverage—never weaken your position.

    # == Available Data==
    # Analytics_Data: {analytics_data}
    # Insights_Data : {insights_data}
    # Supplier_Profile: {supplier_profile}
    # Currency_Symbol: {supplier_profile.get('currency_symbol', '€')}

    # == Important Update ==
    # Only consider analytics that represent negotiation levers with the current supplier.  
    # Exclude any analytics that imply switching suppliers or relocating spend (e.g., HCC-LCC country moves or supplier-consideration opportunities),
    # as these are not actionable negotiation objectives with {supplier}.
    # Use the currency_symbol key value provided in the Supplier Profile data (e.g., €, $) for all monetary values.
    # as these are not actionable negotiation objectives with {supplier}.
    # **When referencing monetary values, **always use the currency symbol from the `currency_symbol` field in the Supplier_Profile data.**  
    # **Do not assume or invent any other currency symbols**
    # **Always use the currency symbol from the `currency_symbol` field in the Supplier_Profile data whenever referring to any figures or savings.**

    
    # == Step 1: Infer Objectives ==
    # 1. Get negotiation objectives from available analytics (example: "Price Reduction," "Payment Terms," "Service Levels," etc.)
    #     based solely on their names and typical procurement use-cases. Also, leverage the provided insights and supplier profile data.
    # - **Only** include analytics that can be used to negotiate with the current supplier
    # - **Include** market benchmarks or targets that present a negotiation opportunity. 
    # - **Exclude** analytics that require changing supplier or shifting spend geography.
    #     (e.g. do not include  HCC-LCC country moves or supplier-consideration opportunities as they try to achieve saving by changing the supplier).  
    # - If there are no valid objectives, return an empty list.
    # 2. For each objective, explicitly list:
    # - **Included analytics** (only those that directly impact this objective)  
    # - **Excluded analytics** (the rest)

    # == Step 2: Data Integrity Rules ==
    # - **Do not alter any numbers, dates, or SKUs**.
    # - Mention a metric only if its data exists.  
    # - Convert all internal keys to clear, human-readable phrases.  
    # - Never use placeholders or show negative days (e.g., "–8 days" → "8 days earlier").

    # ** Step 3: Logical Constraints **
    # - Discard price "levers" where volume rises even as price falls, or where unit-price drops accompany list-price hikes.  
    # - Ignore any gap below inflation or negative gaps—they aren't negotiation levers.

    # ** Step 4: Structure Your Response **
    # The output should be structured with the following sections for each objective:
  
    # Summary:  
    # - Start with the current state for the supplier and the selected SKUs by summarizing information that have relevant data values present in `Supplier_Profile` data. 
    # - Mention any benchmarks or targets that present a negotiation opportunity.
    # - Use simple, actionable language. 
    # - If **only one SKU** presents a valid opportunity (with savings ≥ 0) as per `Insights_Data` and `Analytics_Data`:
    #     - Mention the SKU name and its cost gap, but **do not** mention the savings value.
    #     - Example format (for structure, not fixed numbers):  
    #       "The SKU <SKU> presents a cost gap of <percent>% "
    # - If **multiple SKUs** present valid opportunities:
    #     - Mention the range of cost gaps observed and refer to inefficiencies across selected components.
    # - Do **not** include the total savings value in the Summary.
    
    # Details:  
    # - For every objective list the SKUs or spend categories.
    # - - For each qualifying SKU, present a single-line insight as per the `Insights_Data`:
    #     "<SKU name>: The cost shows a gap of <percent>% with a savings opportunity of {supplier_profile.get('currency_symbol', '€')}<amount> based on 2025 YTD data."
    # - Specify the current status (e.g. average payment term), what the target could be 
    # (e.g. aligning to Y days), and always quantify the potential benefit which can be achieved (e.g. working capital unlocked of (value from available data) amount or cost savings of (value from available data) amount).  

    # ** Actions **
    # End with 1-2 specific recommendations. Focus on what should be changed and why — keep it results-focused.

    # Use a professional but straightforward tone, just like in internal procurement strategy documents. 
    # Avoid generic advice and make the output data-driven and measurable wherever possible.

    # Return the final output strictly in the following JSON format. The "objectives" list may contain multiple non-overlapping objectives. 
    # Do not include any extra text, explanations, or formatting.
    # == Step 5: Deliver ==
    # Based only on the data in `analytics_data` or `insights_data`, produce a cohesive, assertive, data-driven objectives report.
    # Use a professional but straightforward tone—like internal procurement strategy documents.
    # Avoid generic or speculative language.

    # Return the final output strictly in the following JSON format. The "objectives" list may contain multiple non-overlapping objectives. 
    # Do not include any extra text, explanations, or formatting. Ensure all newlines and bold markers are **real**, not escaped:

    # Generate five high value objectives for the supplier {supplier} in category {category} based on the data provided. The objectives should be actionable, measurable, and focused on optimizing commercial terms such as payment terms, pricing, volume discounts etc. Cover the market insights and other relevant insights from the supplier profile data to make objectives more actionable and relevant. Ensure the objectives are data-driven and measurable wherever possible.

    # {{{{
    # "objectives": [
    #     {{{{
    #     "id": 0,
    #     "objective": "**Summary**\\n\\n-[Start with a concise overview of current state and opportunity. Include specific data points: payment terms, prices, volumes, benchmarks. Keep it factual.]\\n\\n**Details:**\\n[List 2-3 key SKUs or categories. For each, provide supporting data: current term/price, target term/price, and estimated opportunity where applicable.]\\n\\n**Actions:**\\n\\n[Recommend specific actions—e.g., extend payment terms, renegotiate price, align to benchmark. Quantify benefits if possible.]",
    #     "objective_type": "[e.g., Payment Terms, Price Reduction, Volume Leverage,]",
    #     "objective_reinforcements": [],
    #     "list_of_skus": [
    #         "[<SKU name>]",
    #         "[SKU 2]",
    #         "[...]"
    #     ]
    #     }}}},
    #     {{{{
    #     "id": 1,
    #     "objective": "**Summary:**\\n[...]\\n\\n**Details:**\\n[...]\\n\\n**Actions:**\\n[...]",
    #     "objective_type": "[...]",
    #     "objective_reinforcements": [],
    #     "list_of_skus": [
    #         "[SKU 1]",
    #         "[SKU 2]",
    #         "[...]"
    #     ]
    #     }}}}
    # ]
    # }}}}

    # Only return a valid, parsable JSON object as the output. Do not include any explanations, markdown, or surrounding text. 
    # Focus on clear, measurable, and structured insights in professional procurement language.

    # NOTE: DO NOT REPEAT ANY OBJECTIVE_TYPE, KEEP IT UNIQUE AND APPROPRIATE FOR THE SPECIFIC OBJECTIVE. TREAT OBJECTIVE_TYPE AS A HEADING FOR THE OBJECTIVE.
    # NOTE: DO NOT CONSIDER SUPPLIER_RELATIONSHIP, IT IS NOT RELEVANT FOR THE OBJECTIVE.

    # """

    prompt_template = f"""
    You are a senior procurement negotiator specializing in {category}, tasked with developing a sharp, data-backed negotiation strategy with {supplier}. You must focus exclusively on value capture **with the current supplier**. Maintain a strong negotiation stance at all times.

    == Input Data ==
    Analytics_Data: {analytics_data}  
    Insights_Data: {insights_data}  
    Supplier_Profile: {supplier_profile}  
    Currency_Symbol: {supplier_profile.get('currency_symbol', '€')}

    == Core Directives ==
    - Extract **only** those levers which are actionable with the current supplier.
    - Disregard analytics that imply a switch of supplier, relocation of spend (e.g., HCC-LCC shifts), or OEM to non-OEM substitutions.
    - You must have consistent information across objectives, there MUST not be data or information mismatch or contradicting data. Example if payment terms are mentioned in an objective, you must not mentioned different values in different objectives. You must be consistent.
    - All monetary values **must use the supplier's currency symbol**: {supplier_profile.get('currency_symbol', '€')}
    - **Do not fabricate** any price, volume, cost driver, or payment term value. Use only what’s provided.

    == Step 1: Filter and Classify Objectives ==
    From the data, derive distinct, high-impact negotiation objectives**. Classify each using one of the following **approved objective types** (no repetition allowed):
    
    - Negotiate Price Reduction
    - Negotiate Payment Terms
    - Discuss Compliance Enforcement
    - Discuss Category and SKU Cost Models
    - Negotiate Volume Discounts
    - Optimise Contractual Terms

    NOTE: You don't have to include all objective types, only those which have high impact.

    For each objective:
    - Include only **analytics and insights relevant to that specific objective**.
    - Exclude those unrelated, or that imply switching suppliers/geographies.

    == Step 2: Data Use Rules ==
    - Do not alter, guess, or invent any metric.  
    - Do not reference benchmarks unless the data includes a market price, cost driver, or target explicitly.
    - Avoid negative days (e.g., "–8 days" becomes "8 days earlier").

    == Step 3: Logical Constraints ==
    - Discard price levers where price dropped despite volume increase.
    - Ignore gaps below inflation or negative price deltas.
    - Disregard list price variance if unit price trend is favorable.

    == Step 4: Structure of Each Objective ==
    Each objective must include:

    **Summary:**  
    - Open with a commercial context derived from the Supplier Profile. Mention key metrics: payment terms, contract status, PO usage, financial risk, price/cost variances.
    - Highlight a clear value gap using facts from analytics/insights.
    - If only one SKU is affected, name it and reference percentage variance (no savings amount).  
    - If multiple SKUs are impacted, provide the % range and flag inefficiencies across the group.

    **Details:**  
    - List key SKUs or categories that support the objective.
    - For each, show:  
    "<SKU>: Cost gap of <percent>%, savings potential of {supplier_profile.get('currency_symbol', '€')}<amount> based on 2025 YTD data."

    **Actions:**  
    - Recommend specific negotiation steps, measurable outcomes, and leverage points.
    - Where applicable, quantify the working capital unlocked, savings realized, or process improvements achieved.

    == Output Requirements ==
    - Output only valid, parsable JSON.
    - Use professional, no-fluff procurement language. Avoid vague suggestions.
    - Do not repeat any `objective_type`.
    - Include fields:
    - `id`: Index number
    - `objective`: Full formatted text block
    - `objective_type`: One of the allowed unique types
    - `objective_reinforcements`: Leave as an empty list
    - `list_of_skus`: Include all SKUs used in the objective

    == Final Deliverable Format ==
    Output exactly as a JSON object, without markdown, preamble, or extra explanation. Format:

    {{
    "objectives": [
        {{
        "id": 0,
        "objective": "**Summary**\\n\\n[summary]\\n\\n**Details:**\\n[details]\\n\\n**Actions:**\\n[actions]",
        "objective_type": "[Unique from list above]",
        "objective_reinforcements": [],
        "list_of_skus": ["SKU1", "SKU2", "..."]
        }},
        ...
    ]
    }}

    == Special Triggers ==
    - If high spend without PO, Contract, or Material Reference: trigger “Compliance Enforcement”
    - If cost driver (e.g., aluminum, energy) changed significantly: trigger “Price Formula/Cost Model Alignment”
    - If financial risk or profit/revenue drop is detected: trigger “Risk-Driven Terms Reassessment”
    - If unused discounts or short payment terms exist: trigger “Discount Utilization” or “Payment Terms”
    - If pricing or terms vary widely across BUs: trigger “Standardization or Harmonization”

    Now, based on the data available, generate **strong negotiation objectives** tailored for supplier {supplier} and category {category}.
    """

    return ChatPromptTemplate([SystemMessage(prompt_template)])

def classify_prompt(df_sample: pd.DataFrame) -> str:
    """
    Builds a prompt for the LLM that embeds a 2-row sample of the DataFrame,
    so it can infer for each column whether to use .sum() or .mean() when
    rolling up month-level data to year-level.
    """
    # Take exactly two rows (or fewer if df has <2)
    sample = df_sample
    # Convert to a JSON-serializable list of records
    sample_records = sample.to_dict(orient="records")
    
    prompt_template = f"""
        You are a data engineer. You need to decide, for each column in a monthly DataFrame sample, whether the correct pandas aggregation to roll up to yearly is `.sum()` or `.mean()`.

        Here is a 2-row snapshot of the data:

        {json.dumps(sample_records, indent=2)}

        Based on the values and common usage (for example, monetary/spend/savings fields should be summed, while rate or duration fields like days should be averaged), classify **each** column.

        **Output:** Return **only** a Python dict literal mapping column names to `"sum"` or `"mean"`, 
        
        for example:

        ```python
        {{
        "SPEND": "sum",
        "NUM_DAYS": "mean",
        "POTENTIALSAVINGS": "sum",
        "PAYMENT_COUNT": "sum",
        "PAYMENT_DAYS": "mean",
        "PRICE_ARBITRAGE": "sum"
        }}
        
        Do not include any other text or explanation.
        

        """
    return ChatPromptTemplate([SystemMessage(prompt_template)])