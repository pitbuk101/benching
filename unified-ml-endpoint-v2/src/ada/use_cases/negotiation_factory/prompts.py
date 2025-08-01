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
            100 * supplier_profile["percentage_spend_which_is_single_sourced"]
        )
    if "percentage_spend_without_po" in supplier_profile:
        supplier_profile["percentage_spend_without_po"] = (
            100 * supplier_profile["percentage_spend_without_po"]
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
    insights_str = "\n ".join(
        [insight["insight"] for insight in model_context.get("filtered_insights", [])],
    )

    negotiation_strategy = model_context.get("sourcing_approach", "")
    log.info("Negotiation strategy %s", ", ".join(negotiation_strategy))
    goals = [f"{i}. {obj}" for i, obj in enumerate(objective_types)]
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
    log.info("Carrot in prompt %s", model_context.get("carrots", []))
    context_dict = {
        "Objectives for Negotiation (Goals) - ": ", ".join(goals),
        "Supplier Information (Numerical Values for Generation) - ": supplier_profile_str,
        "Sourcing Approach - ": ", ".join(negotiation_strategy),
        "Category Positioning - ": model_context.get("category_positioning"),
        model_context.get("buyer_attractiveness", {})
        .get("question", ""): model_context.get("buyer_attractiveness", {})
        .get("value", ""),
        "Savings from Supplier - ": savings_str,
        "Negotiation Insights - ": insights_str,
        "Negotiation Targets - ": "\n".join(model_context.get("target_list", [])),
        f"(IMPORTANT) Carrots {carrot_priority_str} - ": ", ".join(
            model_context.get("carrots", []),
        ),
        f"(IMPORTANT) Sticks {sticks_priority_str} - ": ", ".join(model_context.get("sticks", [])),
        # "Past examples for REFERENCE - ": model_context.get("past_examples", ""),
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
    **kwargs: Any,
) -> list:
    """
    Provides the prompt for argument generation.
        Args:
        model_context (dict): With the common model context for arguments, counter arguments,
            and rebuttals.
        pinned_elements (dict): dict of pinned elements if any
        **kwargs (Any): Additional data
    Returns:
        (list): provides prompt with all relevant information to be used for argument generation
    """
    log.info("Additional args %d", len(kwargs))
    common_prompt = get_common_negotiation_factory_context(
        model_context,
        "arguments",
    )

    key_terminology = """KEY TERMINOLOGY
        - LCC: A Low-Cost Country (LCC) or High-Cost Country (HCC) refers to the geographical location where
          the buyer is procuring a good from. LCC countries are considered lower in cost and hence would be
          recommended to consider procuring from in order to capitalize on the lower pricing. It is important
          to consider the quality of the product between LCC and HCC countries in parallel, as well as
          after-sales services. Having several suppliers (e.g.50+) from low-cost countries is a leverage for
          buyers and not having any is a big risk for buyers
        - Single source supplier: Not having competitors. It is a risk for buyers (who cannot ask for discounts)
          and a leverage for suppliers (who can refuse discounts).
        - Parametric cost modelling are savings are opportunity which can be realized through better pricing.
        - Price arbitrage are savings which can be immediately realized by switching suppliers.
          For eg. Price Arbitrage analysis shows EUR xm opportunity (x% on EUR xm spend base) for
          {supplier_profile.get("supplier_name")}. So, buyer can request {supplier_profile.get("supplier_name")}
            to either give discounts or the buyer can switch SKUs A and B to supplier Y
        - Payment terms standardization are savings which can be realized by using best terms for payments.
        - Price Variation are savings when there are price differences over time or across locations for the same SKU and
          same supplier. For e.g. “Our analysis suggests EUR xm opportunity (x% on EUR xm spend base)
          for {supplier_profile.get("supplier_name")} by lowering prices to x
          (lowest price identified after that month) for SKUs A and B”
          A Spend decrease driven by price NEVER gives a buyer leverage AND IT DOES NOT MEAN A SHIFT TO OTHER SUPPLIERS.
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
                    f"""The total possible savings are "
                "{numerize(supplier_profile.get("total_savings", 0), 1)}. \n"""
                )
                if supplier_profile.get("total_savings")
                else ""
            )
            discount_str = "\n".join(
                [
                    (
                        f"""The discount for {key.replace("_", " ")} is """
                        f"""{round(100 * savings_dict.get(key, 0) / spend_denom, 1)}%"""
                    )
                    for key in top_keys
                    if savings_dict.get(key, 0) > negotiation_conf["idp"]["spend_threshold"]
                ],
            )
            dis_ask_str = (
                f"""{total_str} with a discount of "{
                    round(
                        supplier_profile.get("total_savings", 0),
                        1
                    ) / spend_denom
                }.\n"""
                f"""on the total spend base. Its breakdown is:  {discount_str}"""
            )
            ask_str = f"""ALWAYS USE {dis_ask_str} to HAVE a CONCRETE ASK and RATIONALE"""

        elif objective_match in negotiation_conf["idp"]["payment"]:
            early_payments_loss = (
                f"""Early payment loss on paying earlier than contract demands is """
                f"""{numerize(supplier_profile.get("early_payment", 0), 1)}\n"""
                if supplier_profile.get("early_payment", 0)
                > negotiation_conf["idp"]["spend_threshold"]
                else ""
            )
            terms_standardization = (
                f"""Savings on standardizing contract is """
                f"""{numerize(supplier_profile.get("payment_terms_standardization", 0), 1)}\n"""
                if supplier_profile.get("payment_terms_standardization", 0)
                > negotiation_conf["idp"]["spend_threshold"]
                else ""
            )

            payment_ask_str = (
                f"""Curent days for payterm are upto """
                f"""{supplier_profile.get("payment_term_avg", "lower than best")}."""
                f"""We should ask for best payment terms."""
                f""" \n {terms_standardization} {early_payments_loss}"""
            )
            total_payment_savings = np.nansum(
                [
                    supplier_profile.get("early_payment", np.nan),
                    supplier_profile.get("payment_terms_standardization", np.nan),
                ],
            )
            ask_str = (
                f"""ALWAYS USE {payment_ask_str} to HAVE a CONCRETE ASK and RATIONALE """
                f"""(match payment terms to get savings of {numerize(total_payment_savings, 1)})"""
            )
        # MI:07102024: Separated the incoterms objective. Right now it is empty as we do not have
        # any relevant data on incoterms.
        elif objective_match in negotiation_conf["idp"]["delivery"]:
            ask_str = ""

        log.info("ASK ARGUMENTS %s", ask_str + objective_match)

        objective_match_dict[objective_type] = ask_str

    arg_prompt = f"""{common_prompt} from the buyer's perspective. {objective_match_dict}

        Each argument should be ~50 words, with the specified supplier relationship tone,
        and aligned with the stated {objective_types} and goal.
        ALWAYS NEGOTIATE FROM a POSITION OF STRENGTH ( DO NOT MENTION things such as no LCC supplier,
        being sole supplier, or having no or less alternatives,
        DO NOT MENTION price increase is lower than the market)
        ALWAYS have a reinforcement (positive or negative) as the reason for the argument.
        An argument is also a way to work with the supplier. so a negative reinforcement is to be
        used as a threat unless the supplier meets the demand and not a suggestion.

        For example & REFERENCE ONLY:
            -If spend increase driven by volume growth: “Our spend with you has grown by x%
            over the past year, driven primarily by volume growth. To reward and incentivize
            this growth, we ask that you price-in volume effect and reduce prices over the
            overall portfolio by y%”

            -If spend increase driven by price increase: “We have identified that over the
            past year, our spend with you has increased by x%, driven primarily by higher
            prices of SKU A and B. This exceeds price evolution on the market for these SKUs.
            We ask you reduce prices by x% to be in line with market prices“

            - When asking discounts:
            “We have identified a total price arbitrage opportunity of 307.9K EUR  on
            SKUs UPPER BEARING FY2.15/16 TF/GHYVZ6A7, PDR SKF BEARING ROLLER,
            LOWER BEARING 443 276 BEARING+SLEEVE, representing a 2.2% of our total spend
            with SKF FRANCE. We request price reductions on these SKUs to align pricing with market prices:
                i.	X% on UPPER BEARING FY2.15/16 TF/GHYVZ6A7
                ii.	Y% on PDR SKF BEARING ROLLER
                iii. Z% on LOWER BEARING 443 276 BEARING+SLEEVE”

        Notes:
        1. DO NOT generate any arguments outside the scope of given negotiation objectives - {objective_types}.
        2. DO "NOT REPEAT" any of the arguments and "AVOID duplication" of same information in multiple arguments.
        3. ALWAYS Calculate and add derived metrics such as percentages, averages and numbers to support the arguments
          (UPTO 1 DECIMAL).
        4. Do not generate the instruction and only output from step 2 (with 1-3 arguments).
        5. When asking for DISCOUNTS, USE ONLY THE NUMBERS PROVIDED IN CONTEXT BY MATCHING IT \
            WITH THE OPPORTUNITY (e.g. discount for parametric cost modelling should match \
            with the opportunity paramteric cost modeling
        6. ALWAYS follow the output format in EACH response including "```json" and "```". \
            You can leave "message" or "arguments" key values empty, but they have to present in your output.
        7. Factor target, reason and current offers in the ask ONLY where it makes sense

        Please ALWAYS strictly use the following output format when reply to user:
        {{{{
            "message": "Your message here",
            "arguments":[
                {{
                    "id": "argument_1",
                    "details": "Your first argument"
                }},
                {{
                    "id": "argument_2",
                    "details": "Your second argument"
                }},
                ...
            ]
        }}}}

    """

    # don't use Langchain's parser, will mess up in prompt
    # use OpenAI chat completion
    return [{"role": "system", "content": arg_prompt}]


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
        "Supplier Profile": supplier_profile_str,
        "# Pinned/ Selected Objectives": selected_elements_dict.get("objectives")
        or pinned_elements_dict.get("objectives"),
        "# Objectives for negotiation": objective_goal_str,
        "# Pinned/ Selected Values": pinned_value,
        "# Negotiation strategy": selected_elements.get("negotiation_strategy", {}).get("message")
        or pinned_elements.get("negotiation_strategy", {}).get("message"),
        "# Negotiation approach": selected_elements.get("negotiation_approach", {}).get("message")
        or pinned_elements.get("negotiation_approach", {}).get("message"),
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
            "   actual price and should cost of x% for SKUs A and B. We would request you to reduce prices by x% ",
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

def generate_payment_terms_prompt(context_dict) -> ChatPromptTemplate:
    """
    Generates a ChatPromptTemplate specifically for the Payment Terms negotiation objective.
    Focused solely on aligning to a 90-day standard.
    """
    context_dict = {key: value for key, value in context_dict.items() if value}
    data = context_dict.get("data", {})

    prompt_template = f"""
You are a procurement domain expert for {context_dict.get("category")}.
Your task is to generate a clean, structured, and aligned summary of payment term optimization opportunities with the supplier {context_dict.get("supplier", "")}.

This prompt is exclusively focused on the Payment Terms negotiation objective.

Strict Guidelines:
1. Only include insights that appear in the provided data. Do not invent or generalize.
2. If a SKU appears only in Q2 and Q4, do not mention Q1 or Q3 in that section.
3. Never reuse quarters or savings across SKUs.
4. Always use the exact 'Avg Payment Term Days' and 'Potential Cost Savings' values provided.
5. Use the phrase “working capital benefit” consistently instead of “potential savings.”
6. Do not include any generic recommendations or general improvement statements.

Step 1: Understand the input data:
{data}

Step 2: Generate the following structured output:

Summary:
- Start with a high-level, natural language overview of the working capital opportunity due to below-standard payment terms.
- Mention the supplier by name.
- Do not include any numeric values or SKUs in this section.

Details:
- Organize the information by Year → SKU.
- For each SKU:
    - Include only the years and quarters present in the data.
    - Start with a “Yearly Summary” that sums the working capital benefit across all quarters in that year for that SKU.
    - Follow with a breakdown per quarter (only if that quarter is present in the data).
    - Use the exact numeric values for “Avg Payment Term Days” and “Potential Cost Savings.”
    - Example:

Year: 2025  
    PDR SKF BEARING ROLLER  
        - Yearly Summary: The average payment terms are below the 90-day standard, with a total working capital benefit of approximately €4,080.  
        - In Q4, the average payment term is 66.6 days. Aligning this to 90 days could unlock a working capital benefit of €4,080.

    UPPER BEARING UCF 215 WITH GUARD  
        - Yearly Summary: Quarterly data suggests a total working capital benefit of €17,048.  
        - In Q3, the average payment term is 74.5 days. Adjustment to 90 days could yield €14,654 in working capital benefit.  
        - In Q2, the average payment term is 73 days. This offers a further benefit of €2,394.

Actions:
- For each SKU, generate **one actionable statement** based on the total working capital benefit across the year.
- Mention SKU name, supplier, and euro amount.
- Do not include generic or group-level action lines.
- Example:
    - "Extend payment terms to 90 days for PDR SKF BEARING ROLLER at SKF FRANCE to secure a working capital benefit of €4,080."
    - "Negotiate 90-day terms for UPPER BEARING UCF 215 WITH GUARD with SKF FRANCE to unlock a working capital benefit of €17,048."

Final Style Guidelines:
- Use clear, natural business language.
- Never make up quarters or values.
- Be consistent with terminology.
- Output must strictly follow the structure and logic of the data above.
"""
    return ChatPromptTemplate([SystemMessage(prompt_template)])


def generate_price_reduction_prompt(context_dict) -> ChatPromptTemplate:
    """
    Generates a ChatPromptTemplate specifically for the Price Reduction negotiation objective.
    Consolidates all insights per SKU, but explicitly labels each analytic in natural language sentences.
    """
    context_dict = {key: value for key, value in context_dict.items() if value}
    data = context_dict.get("data", {})

    prompt_template = f"""
You are a senior procurement strategist preparing a price reduction negotiation brief for the category {context_dict.get("category")} with supplier {context_dict.get("supplier", "")}.

This analysis focuses strictly on **Price Reduction opportunities**, derived from component-level cost gaps, early payment behavior, and pricing misalignments. Your goal is to generate a structured, negotiation-ready summary using only the data provided.

Input Data  
Use the structured data exactly as provided. Do not fabricate or infer missing values:
{data}

Formatting Instructions

You must return the output in **three clearly titled sections**, exactly in this order:  
**Summary**  
**Details**  
**Actions**

Summary  
- Write exactly two paragraphs:
  1. A high-level overview describing the savings potential across all SKUs with this supplier. Do not include numbers or SKUs.
  2. Describe the key savings components for each SKU, using actual values (€ and %) in narrative form. Include early payment savings with the approved template:
     “Our analysis of early payment trends indicates that payments were made on average X days earlier than agreed, resulting in a discounted price and representing a potential savings opportunity of €Y.”

- Use natural language, not bullet points or action verbs like "negotiate" or "request".
- Do not use analytic names (e.g., "Early Payment Opportunity" or "Parametric Cost Modeling").

Details  
- Structure like this: 
    Year: <YYYY>  
    <SKU NAME>

- For each SKU:
    - Do not include generic phrases like “Significant opportunities were identified…”
    - Use one bullet per insight:
        - For components: clearly mention the component name, savings amount (€), and gap (%)
        - If quarter is available, start with: “In Q<quarter>, …”
        - For early payments, always use:
          “Our analysis of early payment trends indicates that payments were made on average X days earlier than agreed, resulting in a discounted price and representing a potential savings opportunity of €Y.”

- Skip all zero or missing values.
- Avoid all analytic names.
- Use natural, professional business language.

Actions  
- Each bullet should address one savings opportunity.
- Include supplier name, SKU, component (if applicable), savings amount, and a strong verb like:
    - “Negotiate for a pricing correction with…”
    - “Request supplier adjustment for…”
    - “Realign pricing for…”
    - “Accelerate payments for…”

- For early payments, always use:
    “Accelerate payments for SKU <X> to secure a benefit of €<Y> by paying <Z> days earlier.”

Strict Rules  
- Always generate all three section headers: Summary, Details, Actions  
- Never combine savings across SKUs or components  
- Never mention analytics or technical labels  
- Never include negative days — express them as “X days earlier”  
- Do not include insights with €0 value or 0% gap  
- Use varied, business-appropriate phrasing
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
    - "top_suppliers_tail_spend": Matches queries like "10 tail suppliers", "top tail vendors".
    - "largest_gap": Matches queries like "5 suppliers with largest YOY spend evolution".
    - "spend_without_po": Matches queries like "suppliers with missing PO spend".
    - "highest_single_spend": Matches queries like "single source vendors".
    - "top_supplier": Matches queries like "top 20 suppliers by spend", "top suppliers by spend".

    Extract the **pattern key** and **value** from the given query. If no number is present, default to "5".

    ### Example Outputs:
    Input: "top 20 suppliers by spend"
    Output:  "pattern_key": "top_supplier", "value": "20"

    Input: "suppliers with largest YOY spend evolution"
    Output:  "pattern_key": "largest_gap", "value": "5" 

    Now classify this query:
    {user_query}

    '''
    return ChatPromptTemplate([SystemMessage(prompt_template)])