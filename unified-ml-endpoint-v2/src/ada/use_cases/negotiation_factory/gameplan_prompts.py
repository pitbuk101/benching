"""Negotiation Factory Game plan Prompts - Negotiation Approach, Strategy Prompt"""

from __future__ import annotations

import numbers
from typing import Any

import pandas as pd
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from numerize.numerize import numerize

from ada.use_cases.negotiation_factory.parsers import (
    NegotiationApproachOutputParser,
    NegotiationChangeOutputParser,
    NegotiationStrategyOutputParser,
)
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger

log = get_logger("Negotiation_factory_argument_model")
negotiation_conf = read_config("use-cases.yml")["negotiation_factory"]


def common_strategy_prompt(
    category_positioning: str,
    supplier_positioning: str,
    market_approach: str,
    pricing_methodology: str,
    contract_methodology: str,
    supplier_profile: dict[str, Any],
) -> str:
    """Common prompt for negotiation strategy and negpotiation approach.
    Args:
        category_positioning (str): Selected category position from DB
        supplier_positioning (str): Selected supplier position from DB
        market_approach (str): Selected market approach from DB
        pricing_methodology (str): Selected pricing method from DB
        contract_methodology (str): Selected contract method from DB
        supplier_profile (dict) : extracted supplier profile from DB
    Returns:
        (str): common prompt with the extracted context for the NF strategy and
        sourcing approach models"""
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
    supplier_name = supplier_profile.get("supplier_name", "this company")
    strategy_prompt = f"""
            You are a procurement expert for {supplier_profile.get("category_name")}.
            Your job is to advise Buyer to negotiatiate with Supplier {supplier_name}.

            UNDERSTAND SELECTED PARAMETERS:
            '''
            {
                ""
                if(category_positioning == "")
                else
                "Category positioning (reflects supplier's position in a category) - "
            }{category_positioning}
            {
                ""
                if(supplier_positioning == "")
                else
                "Supplier positioning (reflects strategy to handle supply chain) - "
            }{supplier_positioning}
            Market approach - {market_approach}
            Pricing methodology - {pricing_methodology}
            Contract methodology - {contract_methodology}

            NUMERICAL PARAMETERS TO SUPPORT YOUR RESPONSE (MUST USE):
            {supplier_profile_str}

            KEY TERMS EXPLANATION:
            LCC: Low cost country, where procurement costs are low. Several LCC suppliers
                is a leverage for negotiating and not having any is a big risk
            Single Source Spend: {numerize(supplier_profile.get("single_source_spend_ytd", 0), 1)} of spending
                    (total {numerize(supplier_profile.get("spend_ytd", 0), 1)})
                    for the SKUs of {supplier_name} that does not have another vendor.
            Percentage Single Source Spend: {numerize(supplier_profile.get("percentage_spend_which_is_single_sourced", 0), 1)}
                    percentage of the total {supplier_name}'s spending which does not have any other vendors identified.
                    High values of this is a risk.
            The percentage single source spend is only {supplier_name}'s spend not the entire
            {supplier_profile.get("category_name", "category")} spend. For e.g. 100% single source spend means there are no
            alternative suppliers for the SKUs which {supplier_name} supplies.
            It does NOT mean its 100% of {supplier_profile.get("category_name", "category")}'s single source spend.
            '''
            NOTE:
            1. ALWAYS SUBSTANTIATE your answer with ONLY RELEVANT percentages and the numbers
            for your recommendation (e.g. category spend, supplier spend, number of suppliers etc.).
            2. Generate ONLY A VALID JSON output NOTHING ELSE.
            3. ALL CTA buttons should be in suggested_prompts.
            4. Do not have an opening sentence before the output.
            5. Do not include roles such as "AI" or describe who gave the output.
            6. If you advise against the user selected option do it within the headings only.
            7. Please return the output as **raw JSON** without any markdown, code blocks, or
            formatting (such as ```json).Make sure it is a valid JSON response.
            '''
            Take a step by step approach for the MAIN task below.\n
        """
    return strategy_prompt


def negotiation_strategy_prompt(
    category_positioning: str,
    supplier_positioning: str,
    market_approach: str,
    pricing_methodology: str,
    contract_methodology: str,
    market_map: pd.DataFrame,
    supplier_profile: dict[str, Any],
) -> PromptTemplate:
    """Prompts to generate negotiation strategy on top of the common strategy prompts.
    Args:
        category_positioning (str): Selected category position from DB
        supplier_positioning (str): Selected supplier position from DB
        market_approach (str): Selected market approach from DB
        pricing_methodology (str): Selected pricing method from DB
        contract_methodology (str): Selected contract method from DB
        market_map (pd.DataFrame): Market approach mapping from DB
        supplier_profile (dict[str, Any]): extracted supplier profile from DB
    Returns:
        (PromptTemplate): prompt template to give negotiation strategy to user and
        answer follow-up questions
    """

    common_prompt = common_strategy_prompt(
        category_positioning,
        supplier_positioning,
        market_approach,
        pricing_methodology,
        contract_methodology,
        supplier_profile,
    )
    strategy_prompt = f"""
    {common_prompt}
    When user is first asking for negotiation strategy, based on {market_map}, generate \
    FINAL negotiation strategy  containing **Market approach**, **Pricing methodology**,\
        and **Contracting methodology**. Each component should have an explanation and rationale
        (with supporting facts).
        -- Heading are **Market approach** , **Pricing methodology** and **Contracting methodology**.
        -- ALWAYS keep CTAs as "Change market approach", "Change pricing methodology" \
           and "Change contracting methodology".
    """
    parser = PydanticOutputParser(pydantic_object=NegotiationStrategyOutputParser)
    prompt_template = PromptTemplate.from_template(
        strategy_prompt
        + "Format Output: {format_instructions} and only produce a valid JSON \n"
        + """
        Previous conversation with the Procurement Assistant:
        {history}
        Current Conversation-
        Procurement Negotiator: {input}
        """,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    return prompt_template


def negotiation_set_positioning_prompt(
    category_positioning: str,
    supplier_positioning: str,
    market_approach: str,
    pricing_methodology: str,
    contract_methodology: str,
    supplier_profile: dict[str, Any],
) -> PromptTemplate:
    """Generate a prompt to give proper response for negotiation strategy questions.
    Args:
        category_positioning (str): Selected category position
        supplier_positioning (str): Selected supplier position
        market_approach (str): Selected market approach
        pricing_methodology (str): Selected pricing method
        contract_methodology (str): Selected contract method
        supplier_profile (dict) : extracted supplier profile
    Returns:
        prompt template to give negotiation strategy to user and answer follow-up questions"""
    common_prompt = common_strategy_prompt(
        category_positioning,
        supplier_positioning,
        market_approach,
        pricing_methodology,
        contract_methodology,
        supplier_profile,
    )

    category_positioning_map = negotiation_conf["category_positioning_map"]
    category_name = supplier_profile.get("category_name", "")
    category_vals = category_positioning_map.get(category_positioning, ["low", "low"])

    sourcing_str = "not" if category_vals[0] == "high" else ""
    supplier_name = supplier_profile.get("supplier_name", "Supplier")
    sourcing_str = (
        f"""The material or service is provided by {supplier_name} is {sourcing_str} commoditized"""
    )

    strategy_prompt = ""
    if category_positioning == "":
        strategy_prompt = f"""
                {common_prompt}
                TASK AT HAND
                When the user initially inquires about the negotiation approach, provide a concise 3-line explanation outlining the rationale for the classification of the supplier or category. This explanation should cover:
                1. The business impact and supply market complexity of the supplier/category.
                2. The supplier's position determined by their spend and market standing.
                3. The recommended strategy based on the classification (Core, Grow, Nuisance).
                Additionally, provide the definition for the selected category:
                - **Core**: Suppliers with high business Spend and high supply market complexity. A long-term, strategic partnership is crucial.
                - **Grow**: Suppliers with low business Spend but high supply market complexity. Focus on improvement and development.
                - **Nuisance**: Suppliers with low business Spend and low supply market complexity. Focus on streamlining processes and reducing transaction costs.
                - **Ramp Down (Exploitable Suppliers)**:  High business impact, low supply market complexity
                Request confirmation from the user following the presentation of the classification and rationale.\
                --  Headings are **Supplier Positioning**.
                --  CTAs are ALWAYS "Change supplier positioning" and "Set category positioning"
            """
    elif supplier_positioning == "":
        strategy_prompt = f"""
                {common_prompt}
                MOST IMPORTANT INFORMATION
                {category_name} is positioned as {category_positioning} since it has {category_vals[1]}
                business criticality. {sourcing_str} in the {category_name} category.

                CATEGORY POSITIONING EXPLANATION LOGIC  
                **IMPORTANT**: Please ensure that your explanation does not reference suppliers or supplier-specific details. Focus solely on the category and its characteristics.  

                Please use the following framework to explain and justify the category positioning:

                - **Strategic**: Categories with high business spend concentration (≥ 80%) and high supply market complexity. These are critical to operations and require long-term, strategic management and active risk mitigation strategies.
                - **Leverage**: Categories with high business spend concentration (≥ 80%) but low supply market complexity. These offer strong negotiating power and should be optimized for cost, quality, and efficiency.
                - **Bottleneck**: Categories with low business spend concentration (< 80%) but high supply market complexity. These pose a risk due to supply constraints or dependency, requiring careful category management and risk mitigation.
                - **Shop (Non-Critical)**: Categories with low business spend concentration (< 80%) and low supply market complexity. These are low-impact, transactional purchases that should be streamlined through automation or aggregation."""

    else:
        strategy_prompt = f"""
                {common_prompt}
                MOST IMPORTANT INFORMATION
                {category_name} is positioned as {category_positioning} since it has {category_vals[1]}
                business criticality. {sourcing_str} in the {category_name} category.

                TASK AT HAND
                When user is first asking for negotiation approach - give an explanation and \
                        rationale (with supporting facts) for "**Category Positioning**" and "**Supplier positioning**"
                        and ask user for confirmation.\
                        --  Headings are **Category Positioning** and **Supplier Positioning**.
                        --  CTAs are ALWAYS "Change category positioning" and "Change supplier positioning"
            """
    parser = PydanticOutputParser(pydantic_object=NegotiationApproachOutputParser)
    prompt_template = PromptTemplate.from_template(
        strategy_prompt
        + "Formating Instructions: {format_instructions} and only produce a valid JSON \n"
        + """
        Previous conversation with the Procurement Assistant:
        {history}
        Current Conversation-
        Procurement Negotiator: {input}
        """,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    return prompt_template


def negotiation_change_positioning_prompt(**kwargs) -> PromptTemplate:
    """Generate a prompt to give proper response for negotiation strategy questions.
    Args:
        all_category_positioning (list): Other category positions applicable
        all_supplier_positioning (list): Other supplier positions applicable
        positioning (str): category/supplier
    Returns:
        prompt template to give negotiation strategy to user and answer follow-up questions"""

    all_category_str = ", ".join(kwargs["all_category_positioning"])
    all_supplier_str = ", ".join(kwargs["all_supplier_positioning"])

    strategy_prompt = f"""
        Take a step by step approach

        Whenever the user changes options, provide all the alternatives as follows:
            -- If user asks to change `Category positioning`
            Headings are {all_category_str}.
            CTA is ALWAYS {
                "Set supplier positioning"
                if(kwargs["pinned_elements"].get("supplier_positioning", {}).get("value", "") == "")
                else
                "Change supplier positioning"
            }
            -- If user asks to change `Supplier positioning`
            Headings are {all_supplier_str}.
            CTA is ALWAYS {
                "Set category positioning"
                if(kwargs["pinned_elements"].get("category_positioning", {}).get("value", "") == "")
                else
                "Change category positioning"
            }

        If the user asks to change the `Category positioning`
        return {
            "negotiation_approach_sp"
            if(kwargs["pinned_elements"].get("supplier_positioning", {}).get("value", "") == "")
            else
            "negotiation_strategy_change"
        } as the `request_type`
            If the user asks to change the `Supplier positioning`
            return {
                'negotiation_approach_cp'
                if(kwargs["pinned_elements"].get("category_positioning", {}).get("value", "") == "")
                else
                'negotiation_strategy_change'
        } as the `request_type`

        Instructions:
        1. Always substantiate your answer with relevant percentages, numbers for your recommendation.
        2. Do not add number or extra words, like `Option 1`,`1. ` to Headings.
        3. Do not repeat the Headings.
        4. Each Heading must be ALWAYS surrounded by ** on both sides and start with uppercase.
        5. Except First Heading, each heading MUST ALWAYS START with newline.
        6. ALWAYS RETURN A VALID JSON output. NEVER add the word json in the output.
    """

    parser = PydanticOutputParser(pydantic_object=NegotiationChangeOutputParser)
    prompt_template = PromptTemplate.from_template(
        strategy_prompt
        + "STRICT Format Instructions: {format_instructions} and only produce a valid JSON \n"
        + """
        Previous conversation with the Procurement Assistant
        (MUST USE TO UNDERSTAND CURRENT OPTION & DETAILS FOR RATIONALE):
        {history}
        Current Conversation-
        Procurement Negotiator: {input}
        """,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    return prompt_template


def change_prompt(
    all_category_positioning: list[str],
    all_supplier_positioning: list[str],
    all_market_approach: list[str],
    all_pricing_methodology: list[str],
    all_contract_methodology: list[str],
) -> PromptTemplate:
    """Generate a prompt to give proper response for negotiation strategy questions.
    Args:
        all_category_positioning (list): Other category positions applicable
        all_supplier_positioning (list): Other supplier positions applicable
        all_market_approach (list): Other market approach applicable
        all_pricing_methodology (list): Other pricing methods applicable
        all_contract_methodlogy (list): Other contract methods applicable
    Returns:
        prompt template to give negotiation strategy to user and answer follow-up questions"""

    all_market_approach = list(set(all_market_approach))
    all_pricing_methodology = list(set(all_pricing_methodology))
    all_contract_methodology = list(set(all_contract_methodology))
    all_category_positioning = list(set(all_category_positioning))
    all_supplier_positioning = list(set(all_supplier_positioning))

    all_market_str = ", ".join(all_market_approach)
    all_pricing_str = ", ".join(all_pricing_methodology)
    all_contract_str = ", ".join(all_contract_methodology)
    all_category_str = ", ".join(all_category_positioning)
    all_supplier_str = ", ".join(all_supplier_positioning)

    log.info("All Market Approach: %s", all_market_str)

    strategy_prompt = f"""
            Key Understanding:
            -- Category positioning reflects supplier's position in a category
            -- Supplier positioning reflects strategy to handle supply chain

            MAIN TASK
            Instructions for change in Sourcing strategy or the Negotiation Approach:
            Take a step by step approach

            Whenever user changes options, provide all the alternatives as follows:
                -- If user asks to change `Go to market approach`.
                Headings are {all_market_str}.
                The CTA buttons are {all_market_str} only.
                -- If user asks to change `Pricing methodology`.
                Headings are {all_pricing_str}.
                CTA buttons are {all_pricing_str} only.
                -- If user asks to change `Contracting methodology`.
                Headings are {all_contract_str}.
                CTA buttons are {all_contract_str} only.
                -- If user asks to change `Category positioning`
                Headings are {all_category_str}.
                CTA buttons are {all_category_str} only.
                -- If user asks to change `Supplier positioning`
                Headings are {all_supplier_str}.
                CTA buttons are {all_supplier_str} only.

            If the user asks to change the `Category positioning`
            return `negotiation_approach_cp` as the `request_type`
            If the user asks to change the `Supplier positioning`
            return `negotiation_approach_sp` as the `request_type`
            if the user asks to change the `Market approach` or `Pricing methodology`or `Contracting methodology`
            return `negotiation_strategy` as the `request_type`

            Instructions:
            1. Always substantiate you answer with relevant percentages, numbers for your recommendation.
            2. Always include the specific selected option (with its name) in the Headings at the first place.
            3. NEVER REPEAT the same option twice.
            4. Do not attach number or extra words, like `Option 1`,`1. ` to Headings.
            5. Do not repeat the Headings, text or add extra CTAs.
            6. Do not include the word `Current Option` in the Headings.
            7. ALWAYS RETURN A VALID JSON output. NEVER add the word json in the output.
            8. Each heading must be ALWAYS surrounded by ** on both sides.
            9. Always add `Change to ` as a prefix to CTA buttons.
            10. Except the first Heading, each heading must always start with newline and have a description.
        """
    parser = PydanticOutputParser(pydantic_object=NegotiationChangeOutputParser)
    prompt_template = PromptTemplate.from_template(
        strategy_prompt
        + "STRICT Format Instructions: {format_instructions} and only produce a valid JSON. \n"
        + """
        Previous conversation with the Procurement Assistant
        (MUST USE TO UNDERSTAND CURRENT OPTION & DETAILS FOR RATIONALE):
        {history}
        Current Conversation-
        Procurement Negotiator: {input}
        """,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    return prompt_template
