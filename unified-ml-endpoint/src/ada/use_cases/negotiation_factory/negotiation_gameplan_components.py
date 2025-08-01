"""Module to generate insight , set negotiation target """

from __future__ import annotations

import ast
import json
import re
from typing import Any, Dict
import pandas as pd
import ast
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache


from ada.components.db.pg_connector import PGConnector
from ada.components.db.sf_connector import SnowflakeClient
from ada.components.llm_models.generic_calls import (
    generate_chat_response_with_chain,
    run_conversation_chat,
)
from ada.use_cases.negotiation_factory.analytics_queries import get_early_payments_query, get_parametric_cost_modeling_query, get_payment_terms_query, get_unused_discount_query, get_price_arbitrage_query
from ada.use_cases.negotiation_factory.prompts import create_objectives_prompt_v2, classify_prompt #, generate_objective_summary_prompt, generate_price_reduction_prompt, generate_payment_terms_prompt
from ada.use_cases.negotiation_factory.exception import NegotiationFactoryException
from ada.use_cases.negotiation_factory.gameplan_prompts import (
    change_prompt,
    negotiation_change_positioning_prompt,
    negotiation_set_positioning_prompt,
    negotiation_strategy_prompt,
)
from ada.use_cases.negotiation_factory.negotiation_factory_utils import (
    convert_insights_to_objectives,
    convert_to_response_format,
    get_airesponse_as_dict,
    get_distinct_suggested_prompts,
    get_negotiation_strategy_data,
    get_prompts_to_be_removed,
    get_section_suggested_prompts,
    get_supplier_profile,
    get_supplier_profile_insights_objectives,
    get_workflow_suggested_prompts,
    json_regex,
    process_approach_response_key_content,
    process_strategy_response_key_content,
)

from ada.use_cases.negotiation_factory.negotiation_objective_prompts import generate_payment_terms_objective, generate_price_reduction_objective
from ada.use_cases.negotiation_factory.util_prompts import extract_objectives_prompt
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time
from datetime import datetime

log = get_logger("Negotiation_gameplan_components")
negotiation_conf = read_config("use-cases.yml")["negotiation_factory"]
model_conf = read_config("models.yml")
negotiation_tables = negotiation_conf["tables"]

def get_category_positioning(sf_client,category_name):
    """
    Set category positioning data
    Returns:
        (dict[str, Any]): Return category positioning data
    """
    query = f'''
    SELECT
        YEAR,
        CATEGORY,
        SPEND_YTD AS TOTAL_SPEND
    FROM
        {negotiation_tables["supplier_details"]}
    WHERE
        YEAR = (select max(YEAR) from  {negotiation_tables["supplier_details"]})
        AND CATEGORY = '{category_name}'
  '''
    log.info("Fetching category positioning data")
    df = sf_client.fetch_dataframe(query)
    # breakpoint()

    
    # 2) compute grand total
    grand_total = df['TOTAL_SPEND'].sum()
    if grand_total == 0:
        raise ValueError("No spend found for current year.")

    # 3) lookup the requested category
    category_spend = df.loc[df['CATEGORY'].str.lower() == category_name.lower(), 'TOTAL_SPEND']
    if category_spend.empty:
        raise ValueError(f"Category '{category_name}' not found in this year's data.")
    amount = float(category_spend.iloc[0])

    # 4) compute percentage
    pct = round((amount / grand_total) * 100, 2)
    # breakpoint()
    category_market_complexity_df = pd.read_csv("src/ada/use_cases/negotiation_factory/category_market_complexity.csv")
    category_market_complexity = category_market_complexity_df.loc[category_market_complexity_df['TXT_CATEGORY_LEVEL_3'].str.lower() == category_name.lower(), 'Supplier market complexity']
    if category_market_complexity.empty:
        category_market_complexity = pd.Series(['High'])

    category_market_complexity = category_market_complexity.iloc[0]

    if pct >= 80: # laverage or strategic
        if category_market_complexity == 'High': 
            return "strategic partnership",pct
        elif category_market_complexity == 'Low':
            return "leverage",pct
    elif pct < 80: # shop or bottleneck
        if category_market_complexity == 'High':
            return "bottleneck",pct
        elif category_market_complexity == 'Low':
            return "shop",pct
    

def get_positioning_data(
    sf_client: Any,
    profile: dict[str, Any],
    category: str,
    reference_data: dict[str, Any],
    user_query: str,
) -> dict[str, Any]:
    """
    Get data related to positioning in the market
    Args:
        profile (dict[str, Any]): supplier profile data
        category (str): Category name user is operating in
        reference_data (dict[str, Any]): tenant specific negotiation factory reference data
        user_query (str) : received user query
    Returns:
        (dict[str, Any]: Return positioning data related to supplier and category
    Raises:
        NegotiationFactoryUserException: If supplier name not present in user query
                                         or supplier data is not present for the category
    """
    log.info("Starting positioning data generation for category: %s, user query: %s", category, user_query)
    positioning: dict[str, Any] = {}

    strategy_data = get_negotiation_strategy_data(reference_data, category)
    log.debug("Fetched strategy data: %s", strategy_data)

    incumbency = int(profile.get("number_of_supplier_in_category", "0"))
    log.debug("Incumbency determined as: %s", incumbency)

    positioning["supplier_relationship"] = profile.get("supplier_relationship", "").lower()
    positioning["all_supplier_relationships"] = negotiation_conf["supplier_positioning"]
    positioning["category_positioning"] = strategy_data.get(
        negotiation_conf["category_positioning_column"],
        "",
    )
    positioning["category_positioning"],pct = get_category_positioning(sf_client,category)
    positioning["all_category_positioning"] = negotiation_conf["category_positioning"]
    positioning["all_pricing_methodology"] = strategy_data.get(
        negotiation_conf["pricing_methodology"],
        [],
    )
    positioning["all_contracting_methodology"] = strategy_data.get(
        negotiation_conf["contracting_methodology"],
        [],
    )

    pm_child_index = 0
    cm_child_index = 0
    all_pm = positioning["all_pricing_methodology"]
    all_cm = positioning["all_contracting_methodology"]

    log.debug("All pricing methodologies: %s", all_pm)
    log.debug("All contracting methodologies: %s", all_cm)

    for child in all_pm:
        if user_query.replace("Change to ", "").lower().strip() == child.lower().strip():
            pm_child_index = all_pm.index(child)
            break
    for child in all_cm:
        if user_query.replace("Change to ", "").lower().strip() == child.lower().strip():
            cm_child_index = all_cm.index(child)
            break

    positioning["pricing_methodology"] = all_pm[pm_child_index]
    positioning["contracting_methodology"] = all_cm[cm_child_index]

    positioning["market_map_df"] = reference_data[
        negotiation_conf["reference_tables"]["common"]["negotiation_market_approach"]
    ]
    log.info("Market map data (head):\n%s", positioning["market_map_df"].head(5))

    positioning["filtered_market"] = positioning["market_map_df"][
        (positioning["market_map_df"]["incumbency"] <= incumbency)
        & (
            positioning["market_map_df"]["category_positioning"].apply(
                lambda x: positioning["category_positioning"] in x,
            )
        )
        & (
            positioning["market_map_df"]["supplier_relationship"].apply(
                lambda x: positioning["supplier_relationship"] in x,
            )
        )
    ]

    log.info("Filtered market data shape: %s", positioning["filtered_market"].shape)
    log.debug("Filtered market data:\n%s", positioning["filtered_market"])

    if len(positioning["filtered_market"]) == 0:
        error_msg = """Market approach not found based on the selected parameters. Please
            change the parameters to get a relevant market approach for strategy."""
        log.error(error_msg)
        raise NegotiationFactoryException(error_msg)

    all_market_alternatives = positioning["market_map_df"][
        (
            positioning["market_map_df"][negotiation_conf["category_auction_map"]]
            == strategy_data.get(negotiation_conf["category_auction_map"], "")
        )
        & (positioning["market_map_df"]["incumbency"] <= incumbency)
    ]
    positioning["alternatives_market_approach"] = (
        all_market_alternatives["market_approach"].unique().tolist()
    )

    log.info("Alternatives market approaches: %s", positioning["alternatives_market_approach"])
    log.info("Final positioning data generated: %s", positioning)
    return positioning,pct

@log_time
def generate_strategy(
    reference_data: dict[str, Any],
    pg_db_conn: PGConnector,
    sf_client: Any,
    category: str,
    user_query: str,
    pinned_elements: dict[str, Any],
    chat_history: list[dict[str, Any]],
    generation_type: str,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Create negotiation strategy for the supplier
    Args:
        reference_data (dict[str, Any]): tenant specific negotiation factory reference data
        pg_db_conn (PGConnector) : Connection object to postgres database
        category (str): user selected category
        user_query (str) : received user query
        pinned_elements (dict[str, Any]): elements pinned by the user
        chat_history (list[dict[str, Any]]) : chat history list
        generation_type (str): type of request
        kwargs (Any): Any additional arguments
    Returns:
        (dict[str, Any]: Return Negotiation strategy for the suppliers
    Raises:
        NegotiationFactoryUserException: If supplier name not present in user query
                                         or supplier data is not present for the category
    """
    log.info("Initiating Negotiation Strategy with generation_type: %s", generation_type)
    log.debug("Incoming pinned elements: %s", pinned_elements)

    _, supplier_profile = get_supplier_profile(
        pg_db_conn,
        sf_client,
        category,
        user_query,
        pinned_elements,
    )

    postitioning, pct = get_positioning_data(
        sf_client=sf_client,
        profile=supplier_profile,
        category=category,
        reference_data=reference_data,
        user_query=user_query,
    )
    log.debug("Resolved positioning data: %s", postitioning)

    params = {
        "category_positioning": postitioning["category_positioning"],
        "supplier_positioning": postitioning["supplier_relationship"],
        "market_approach": postitioning["filtered_market"].head(1)["market_approach"].values,
        "pricing_methodology": postitioning["pricing_methodology"],
        "contract_methodology": postitioning["contracting_methodology"],
        "supplier_profile": supplier_profile,
    }

    prompt, response_keys, init_message, action = get_strategy_prompts(
        params,
        generation_type,
        market_map=postitioning["market_map_df"],
        all_category_positioning=postitioning["all_category_positioning"],
        all_supplier_relationships=postitioning["all_supplier_relationships"],
        all_pricing_methodology=postitioning["all_pricing_methodology"],
        alternatives_market_approach=postitioning["alternatives_market_approach"],
        all_contracting_methodology=postitioning["all_contracting_methodology"],
        pinned_elements=pinned_elements,
        user_query=user_query,
    )

    log.info("Prompt prepared for strategy generation.")

    response = run_conversation_chat(
        chat_history,
        prompt,
        user_query,
        model=negotiation_conf["model"]["model_name"],
        window_size=negotiation_conf["model"]["conversation_buffer_window"],
    )
    response = response.replace("json", "").replace("`", "")
    log.info("Strategy model raw response: %s", response)

    ai_response = get_airesponse_as_dict(response=response, response_keys=response_keys)
    params = process_strategy_response_key_content(
        supplier_profile=supplier_profile,
        ai_response=ai_response,
        init_message=init_message,
        generation_type=generation_type,
        pinned_elements=pinned_elements,
        user_query=user_query,
    )

    if (
        all(ai_response.get(key) for key in negotiation_conf[f"{generation_type}_keys"])
        and negotiation_conf[f"{generation_type}_keys"]
    ):
        if generation_type == "negotiation_strategy":
            params[generation_type] = {
                key: {
                    "value": ai_response.get(key),
                    "details": ai_response.get(f"{key}_detail", ""),
                }
                for key in negotiation_conf[f"{generation_type}_keys"]
            }

    elif (generation_type == "negotiation_strategy_change") and (
        ("category" in user_query.lower()) or ("supplier" in user_query.lower())
    ):
        pattern = r"\*\*(.*?)\*\*\s*(.*?)(?=\*\*|$)"
        colon_with_space = ": "
        space_with_colon = " :"
        len_colon_with_space = len(colon_with_space)
        matches = re.findall(pattern, ai_response.get("message", "").replace("\n", ""))
        types = []
        for heading, description in matches:
            types.append(heading.strip())
            types.append(description.strip())

        params[
            ("category_positions" if ("category" in user_query.lower()) else "supplier_positions")
        ] = [
            {
                "value": types[index],
                "details": (
                    (
                        types[index + 1][len_colon_with_space:]
                        if types[index + 1].startswith(colon_with_space)
                        else types[index + 1]
                    ).rstrip(space_with_colon)
                ),
            }
            for index in range(0, len(types), 2)
        ]

        params["suggested_prompts"] = [
            prompt
            for prompt in params["suggested_prompts"]
            if prompt["prompt"]
            not in [
                (
                    "Change category positioning"
                    if "category" in user_query.lower()
                    else "Change supplier positioning"
                ),
            ]
        ]
        params["message"] = ""

    elif (
        generation_type == "negotiation_strategy_change"
        and action == "negotiation_change_sourcing_approach"
    ):
        lst_prompt: list[dict[str, Any]] = []
        for key in ai_response.get("suggested_prompts", []):
            holder = str(key).lower().replace("all options in", "").replace("  ", " ").capitalize()
            lst_prompt.append(
                {
                    "prompt": holder,
                    "intent": "negotiation_strategy",
                },
            )
        params["suggested_prompts"] = lst_prompt + [
            {
                "prompt": (
                    f"{'Change' if ('tone_and_tactics' in pinned_elements.keys()) else 'Set'}"
                    " tone & tactics"
                ),
                "intent": (
                    "negotiation_approach_tnt"
                    f"{'_change' if ('tone_and_tactics' in pinned_elements.keys()) else ''}"
                ),
            },
        ]

    params["suggested_prompts"] = get_distinct_suggested_prompts(
        prompts=params["suggested_prompts"],
    )

    log.info("Returning final strategy response.")
    return convert_to_response_format(**params)


@log_time
def generate_insights(
    pg_db_conn: PGConnector,
    sf_client: Any,
    category: str,
    user_query: str,
    pinned_elements: dict[str, Any] = {},
    generation_type: str = "",
    before_update_request_type: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Extract Insights related to supplier from database
    Args:
        pg_db_conn (PGConnector) : Connection object to postgres database
        category (str): user selected category
        user_query (str) : received user query
        pinned_elements (dict[str, Any]): Pinned elements including supplier profile
        before_update_request_type (str): request_type from frontend
        generation_type (str): identified intent of the user query
        call_directly (bool) : False if its getting call from other model \
                                    like arguments, counter-arguments else True
        *kwargs: Additional arguments if any
    Returns:
        (dict[str, Any]: Return insights for the supplier in proper response format
    """
    log.info("Starting insight generation. Total kwargs received: %d", len(kwargs))
    log.debug("Pinned elements received: %s", pinned_elements)
    log.debug("User query received: %s", user_query)

    (
        supplier_name,
        supplier_profile,
        insights,
        objectives,
    ) = get_supplier_profile_insights_objectives(
        pg_db_conn,
        sf_client,
        category,
        user_query,
        pinned_elements,
    )
    all_keys = pinned_elements.keys()
    if before_update_request_type == "" or generation_type == "negotiation_begin":
        log.info("Request originated from chat. Preparing response to guide user to SKU selection.")

        ctas = {
            "prompt": negotiation_conf["cta_button_map"]["select_skus"],
            "intent": "negotiation_select_skus",
        }

        suggested_prompts = get_section_suggested_prompts(section_name="Select Supplier")
        remove_list = [
            f"{'Set' if 'insights' in pinned_elements.keys() else 'Change'} negotiation objectives"
        ]
        suggested_prompts = [
            prompt for prompt in suggested_prompts if prompt["prompt"] not in remove_list
        ]


        params = {
            "response_type": "supplier_details",
            "message": (
                f"Thank you for selecting {supplier_name}."
            ),
            "additional_data": {
                "suppliers_data": [{
                    "supplier_name": supplier_profile['supplier_name'],
                    "spend": supplier_profile['spend_ytd'],
                    "currency_symbol": supplier_profile['currency_symbol'],
                    "percentage_spend_contribution": supplier_profile['percentage_spend_across_category_ytd'],
                    "currency_position": supplier_profile['currency_position']
                }],
                "follow_up_prompt": ctas,
                "welcome_message": "Thank you for selecting SUPPLIER_NAME. Here are few probable next steps:",
            },
            "suppliers_profiles": [supplier_profile],
        }

        log.debug("Returning navigation redirection response: %s", params)
        return convert_to_response_format(**params)

    log.info("Request type identified as: %s", generation_type)
    display_val = insights if generation_type == "negotiation_insights" else objectives
    log.debug("Display values being processed: %s", display_val)

    if len(display_val) == 0:
        log.warning("No data found for %s", generation_type)
        return convert_to_response_format(
            response_type=generation_type.replace("negotiation_", ""),
            message=(
                "Apologies, but at the moment, "
                f"""we don't have any {generation_type.replace("negotiation_", "")} for"""
                f" supplier {supplier_name}"
            ),
            supplier_profile=supplier_profile,
        )

    probable_objectives = list({insight["insight_objective"] for insight in display_val})
    log.info("Probable objectives identified: %s", probable_objectives)

    if user_query.lower() in [
        negotiation_conf["cta_button_map"]["objective"].lower(),
        "change negotiation objectives",
        negotiation_conf["cta_button_map"]["insights"].lower(),
    ]:
        matched_objectives = probable_objectives
    else:
        objective_prompt = extract_objectives_prompt(
            user_query=user_query,
            probable_objectives=probable_objectives,
        )
        ai_response = generate_chat_response_with_chain(
            objective_prompt,
            model=negotiation_conf["model"]["model_name"],
        )
        ai_response = ai_response.replace("json", "").replace("`", "").strip()
        log.info("Raw LLM response: %s", ai_response)

        try:
            extracted_objectives = json.loads(ai_response)
        except json.decoder.JSONDecodeError as json_error:
            log.error("Error in decoding JSON: %s", json_error)
            extracted_objectives = json_regex(ai_response, ["extracted_objectives"])
            if not extracted_objectives:
                extracted_objectives["extracted_objectives"] = []

        matched_objectives = (
            extracted_objectives.get("extracted_objectives", []) or probable_objectives
        )

    matched_objectives = [objective_val.lower() for objective_val in matched_objectives]
    log.info("Matched objectives after processing: %s", matched_objectives)

    insights_objectives = [
        insight
        for insight in display_val
        if insight["insight_objective"].lower() in matched_objectives
    ]

    log.info("Final number of insights/objectives: %d", len(insights_objectives))

    if not insights_objectives:
        return convert_to_response_format(
            response_type=generation_type.replace("negotiation_", ""),
            message=(
                "I'm sorry, but I couldn't find any "
                f"""{generation_type.replace("negotiation_", "")}"""
                " matching with specified goal [ i.e. "
                f"{', '.join(matched_objectives)} ]"
                f" for supplier {supplier_name}. Is there anything else I can assist you with?"
            ),
            supplier_profile=supplier_profile,
        )

    if generation_type == "negotiation_insights":
        suggested_prompts = get_section_suggested_prompts(section_name="Select Supplier")
        remove_list = [
            f"{'Set' if 'objectives' in all_keys else 'Change'} negotiation objectives"
        ]
        suggested_prompts = [
            prompt for prompt in suggested_prompts if prompt["prompt"] not in remove_list
        ]
    else:
        suggested_prompts = get_workflow_suggested_prompts(
            pinned_elements,
            need_supplier_profile_check=False,
            include_insights=generation_type != "negotiation_insights",
            starts_with="objective",
        )

    log.debug("Suggested prompts: %s", suggested_prompts)

    params = {
        "response_type": generation_type.replace("negotiation_", ""),
        "message": (
            f"""Please see below important {generation_type.replace("negotiation_", "")}"""
            f""" for supplier {supplier_name}."""
        ),
        "insights": insights_objectives,
        "supplier_profile": supplier_profile,
        "suggested_prompts": suggested_prompts,
    }

    log.info("Returning final insight response.")
    return convert_to_response_format(**params)


@log_time
def generate_objectives(
    pg_db_conn: PGConnector,
    sf_client: Any,
    category: str,
    user_query: str,
    pinned_elements: dict[str, Any],
    generation_type: str = "",
    skus: Any = None,
    **kwargs: Any,
) -> dict[str, Any]:
    log.info("Starting objective generation. Total kwargs received: %d", len(kwargs))
    log.info("Request type: %s", generation_type)
    log.info("SKU list passed in: %s", skus)

    sku_names = [item['name'] for item in skus] if skus else None
    supplier_name = pinned_elements.get("supplier_profile", {}).get("supplier_name")

    with ThreadPoolExecutor(max_workers=5) as executor:
        supplier_future = executor.submit(
            get_supplier_profile_insights_objectives,
            pg_db_conn, sf_client, category, user_query, pinned_elements
        )
        analytics_future = executor.submit(
            extract_category_analytic_data,
            supplier_name, sku_names, category, sf_client
        )

        supplier_name, supplier_profile, insights_fr_db, objectives_fr_db = supplier_future.result()
        analytics_data = analytics_future.result()

    nego_insights = pinned_elements.get("nego_insights", {})
    if not isinstance(nego_insights, dict):
        nego_insights = {}

    log.info("Analytics data extracted: %s", analytics_data)
    log.info("Nego insights data extracted: %s", nego_insights)

    if not analytics_data and not nego_insights:
        return convert_to_response_format(
            response_type=generation_type.replace("negotiation_", ""),
            message=(
                f"I'm sorry, but I couldn't find any {generation_type.replace('negotiation_', '')} matching with specified goal "
                f"for supplier {supplier_name}. Is there anything else I can assist you with?"
            ),
            supplier_profile=supplier_profile,
            suggested_prompts=[{'prompt': 'Change SKUs', 'intent': 'negotiation_select_skus'}],
        )

    objective_prompt = create_objectives_prompt_v2(
        supplier_name, category, analytics_data, supplier_profile, nego_insights
    )
    objectives = generate_chat_response_with_chain(prompt=objective_prompt, model='gpt-4o', temperature=0.3)

    # Cleaning of objectives
    objectives = objectives.replace("```json", "").replace("```", "").strip()
    objectives = json.loads(objectives)

    if not objectives['objectives']:
        log.warning("No objectives could be generated for supplier: %s", supplier_name)
        return convert_to_response_format(
            response_type=generation_type.replace("negotiation_", ""),
            message=(
                "I'm sorry, but I couldn't find any "
                f"{generation_type.replace('negotiation_', '')} matching with specified goal "
                f"for supplier {supplier_name}. Is there anything else I can assist you with?"
            ),
            supplier_profile=supplier_profile,
            suggested_prompts=[{'prompt': 'Change SKUs','intent':'negotiation_select_skus'}],
        )

    suggested_prompts = get_objectives_ctas(pinned_elements=pinned_elements, user_query=user_query)
    log.debug("Suggested prompts prepared: %s", suggested_prompts)

    return convert_to_response_format(
        response_type=generation_type.replace("negotiation_", ""),
        message=f"Please see below important {generation_type.replace('negotiation_', '')} for supplier {supplier_name}.",
        objectives=objectives['objectives'],
        supplier_profile=supplier_profile,
        suggested_prompts=suggested_prompts,
    )


# @log_time
# def generate_objectives(
#     pg_db_conn: PGConnector,
#     sf_client: Any,
#     category: str,
#     user_query: str,
#     pinned_elements: dict[str, Any],
#     generation_type: str = "",
#     skus: Any = None,
#     **kwargs: Any,
# ) -> dict[str, Any]:
#     """
#     Extract objectives related to supplier from database
#     """
#     log.info("Starting objective generation. Total kwargs received: %d", len(kwargs))
#     log.info("Request type: %s", generation_type)
#     log.info("SKU list passed in: %s", skus)

#     supplier_name, supplier_profile, insights_fr_db, objectives_fr_db = get_supplier_profile_insights_objectives(
#         pg_db_conn,
#         sf_client,
#         category,
#         user_query,
#         pinned_elements,
#     )
#     log.info("Supplier extracted: %s", supplier_name)

#     sku_names = [item['name'] for item in skus] if skus else None
#     formatted_sku = "('{}')".format("', '".join(sku_names)) if sku_names else None
#     log.debug("SKU Names: %s", sku_names)

#     objective_analytic_config = {
#         "Payment Terms": {
#             "analytic_name": ["payment terms standardization"],
#             "queries": [get_payment_terms_query],
#             "rename": [
#                 {
#                     "SPEND": "Total Spend",
#                     "SELECTED_PAYMENT_TERM_DAYS": "Avg Payment Term Days",
#                     "POTENTIAL_SAVINGS": "Potential Cost Savings"
#                 }
#             ],
#             "aggregation": [
#                 {
#                     'SPEND': 'sum',
#                     'SELECTED_PAYMENT_TERM_DAYS': 'mean',
#                     'POTENTIAL_SAVINGS': 'sum'
#                 }
#             ],
#             "groupby_cols": [
#                 {
#                     "current_year": ['YEAR', 'QUARTER', 'MATERIAL'],
#                     "last_year": ['YEAR', 'MATERIAL']
#                 }
#             ],
#             "sorting_cols": [["POTENTIAL_SAVINGS"]],
#         },
#         "Price Reduction": {
#             "analytic_name": ["early payments", "unused discount", "Total Saving Achieved", "price arbitrage query"],
#             "queries": [get_early_payments_query, get_unused_discount_query, get_parametric_cost_modeling_query, get_price_arbitrage_query],
#             "rename": [
#                 {
#                     "TOTAL_SPENDS": "Total Spends",
#                     "DIFF_EARLY_PAYMENT": "Avg Early Payment Days",
#                     "EARLY_PAYMENT_OPPORTUNITY": "Early Payment Opportunity"
#                 },
#                 {"DISCOUNT": "DISCOUNT USED"},
#                 {
#                     "COMPONENT": "COMPONENT",
#                     "CLEANSHEET_OPPORTUNITY": "Cleansheet Opportunity",
#                     "PCM_GAP_PERCENTAGE_PER_UNIT": "PCM Gap %"
#                 },
#                 {
#                     "MINIMUM_AVERAGE_PRICE": "Min Avg Price",
#                     "PRICE_AVERAGE": "Price Avg",
#                     "PRICE_ARBITRAGE": "Price Arbitrage",
#                     "PRICE_ARBITRAGE_PERCENTAGE": "Arbitrage %"
#                 }
#             ],
#             "aggregation": [
#                 {
#                     'TOTAL_SPENDS': 'sum',
#                     'DIFF_EARLY_PAYMENT': 'mean',
#                     'EARLY_PAYMENT_OPPORTUNITY': 'sum'
#                 },
#                 {
#                     'DISCOUNT': 'mean',
#                     'DISCOUNT_POSSIBLE': 'mean',
#                     'DISCOUNT_NOT_USED': 'mean'
#                 },
#                 {
#                     'CLEANSHEET_OPPORTUNITY': 'sum',
#                     'PCM_GAP_PERCENTAGE_PER_UNIT': 'mean'
#                 },
#                 {
#                     'MINIMUM_AVERAGE_PRICE': 'mean',
#                     'PRICE_AVERAGE': 'mean',
#                     'PRICE_ARBITRAGE': 'mean',
#                     'PRICE_ARBITRAGE_PERCENTAGE': 'mean'
#                 }
#             ],
#             "groupby_cols": [
#                 {
#                     "current_year": ['YEAR', 'QUARTER', 'MATERIAL'],
#                     "last_year": ['YEAR', 'MATERIAL']
#                 },
#                 {
#                     "current_year": ['YEAR', 'QUARTER', 'MATERIAL'],
#                     "last_year": ['YEAR', 'MATERIAL']
#                 },
#                 {
#                     "current_year": ['YEAR', 'QUARTER', 'MATERIAL', 'COMPONENT'],
#                     "last_year": ['YEAR', 'MATERIAL', 'COMPONENT']
#                 },
#                 {
#                     "current_year": ['YEAR', 'QUARTER', 'MATERIAL'],
#                     "last_year": ['YEAR', 'MATERIAL']
#                 }
#             ],
#             "sorting_cols": [["EARLY_PAYMENT_OPPORTUNITY"],["DISCOUNT_NOT_USED"],["CLEANSHEET_OPPORTUNITY"],["PRICE_ARBITRAGE_PERCENTAGE"]]
#         }
#     }

#     objectives = []

#     for objective_name, config in objective_analytic_config.items():
#         log.info("Generating data for objective: %s", objective_name)
#         context_dict = {
#             "objective": objective_name,
#             "supplier": supplier_name,
#             "category": category,
#             "supplier_profile": supplier_profile,
#             "data": {}
#         }
#         analytics_names = []

#         for query_func, agg, analytic_name, rename_cols, groupby_cols, sorting_col in zip(
#             config["queries"],
#             config["aggregation"],
#             config["analytic_name"],
#             config["rename"],
#             config["groupby_cols"],
#             config["sorting_cols"]
#         ):
#             query = query_func(supplier_name=supplier_name, sku_names=formatted_sku)
#             log.debug("Executing query for analytic: %s", analytic_name)
#             log.info("Query %s for analytic: %s", query, analytic_name)
#             df = sf_client.fetch_dataframe(query)

#             if df.empty:
#                 log.warning("No data returned for analytic: %s", analytic_name)
#                 continue
#             # columns_to_check = [
#             #     "EARLY_PAYMENT_OPPORTUNITY",
#             #     "DISCOUNT_NOT_USED",
#             #     "CLEANSHEET_OPPORTUNITY",
#             #     "PRICE_ARBITRAGE_PERCENTAGE"
#             # ]

#             # for col in columns_to_check:
#             #     if col in df.columns:
#             #         if df[col].sum() == 0:
#             #             log.info("No data for column: %s for analytics %s", col, analytic_name)
#             #             continue
#             #         print(f"{col} total: {df[col].sum()}")
#             current_year = datetime.now().year
#             df_current = df[df['YEAR'] == current_year].groupby(groupby_cols['current_year']).agg(agg).reset_index()
#             df_past = df[df['YEAR'] < current_year].groupby(groupby_cols['last_year']).agg(agg).reset_index()

#             if len(sorting_col) > 1:
#                 final_df = pd.concat([df_current, df_past], ignore_index=True).sort_values(['YEAR', 'QUARTER'] + sorting_col, ascending=[False, False, False])
#             else:
#                 final_df = pd.concat([df_current, df_past], ignore_index=True).sort_values(['YEAR', 'QUARTER'], ascending=[False, False])
#             final_df.reset_index(drop=True, inplace=True)
#             if not sku_names:
#                 top_5_materials = final_df.dropna(subset=['MATERIAL', 'QUARTER']).sort_values(sorting_col)['MATERIAL'].unique()[:5]
#                 final_df = final_df[final_df['MATERIAL'].isin(top_5_materials)]

#             days_cols = ['DIFF_EARLY_PAYMENT', 'SELECTED_PAYMENT_TERM_DAYS']
#             for col in days_cols:
#                 if col in final_df.columns:
#                     final_df[col] = final_df[col].apply(lambda x: f"{int(x)}" if pd.notnull(x) else x)
#             final_df.rename(columns=rename_cols, inplace=True)
#             context_dict["data"][analytic_name] = final_df.to_dict(orient="records")
#             analytics_names.append(analytic_name)
#         if context_dict["data"]:
#             log.info("Non-empty objective context generated for: %s", objective_name)
#             if objective_name == 'Payment Terms':
#                 objective_generation_prompt = generate_payment_terms_prompt(context_dict, supplier_profile)
#             else:

#                 objective_generation_prompt = generate_price_reduction_prompt(context_dict)
#                 # if (objective_generation_prompt) == False or str(objective_generation_prompt).lower() == 'False':
#                 #     log.warning("No data found for objective: %s", objective_name)
#                 #     continue
#             summary = generate_chat_response_with_chain(prompt=objective_generation_prompt, temperature=0.3)
#             summary = summary.replace('*', '')
#             objectives.append({
#                 "id": len(objectives),
#                 "objective": summary,
#                 "objective_type": objective_name,
#                 "objective_reinforcements": [],
#                 "list_of_skus": sku_names,
#                 "analytics_names": analytics_names
#             })
#         # breakpoint()             
#     if len(objectives) == 0:
#         log.warning("No objectives could be generated for supplier: %s", supplier_name)
#         return convert_to_response_format(
#             response_type=generation_type.replace("negotiation_", ""),
#             message=(
#                 "I'm sorry, but I couldn't find any "
#                 f"{generation_type.replace('negotiation_', '')}"
#                 " matching with specified goal "
#                 f"for supplier {supplier_name}. Is there anything else I can assist you with?"
#             ),
#             supplier_profile=supplier_profile,
#         )

#     suggested_prompts = get_objectives_ctas(pinned_elements=pinned_elements, user_query=user_query)
#     log.debug("Suggested prompts prepared: %s", suggested_prompts)

#     params = {
#         "response_type": generation_type.replace("negotiation_", ""),
#         "message": (
#             f"""Please see below important {generation_type.replace('negotiation_', '')}"""
#             f""" for supplier {supplier_name}."""
#         ),
#         "objectives": objectives,
#         "supplier_profile": supplier_profile,
#         "suggested_prompts": suggested_prompts,
#     }
#     log.info("Returning final objective response with %d objectives", len(objectives))
#     return convert_to_response_format(**params)


def filter_valid_kpi_tables(analytic_map_df: pd.DataFrame, sf_client) -> pd.DataFrame:
    """
    Removes entries whose KPI table (with _FRONTEND stripped) doesn't exist in the schema.
    """
    # Strip `_FRONTEND` from table names
    analytic_map_df['KPI_TABLE_NAME'] = analytic_map_df['KPI_TABLE_NAME'].str.replace("_FRONTEND", "", regex=False)

    # Get all actual table names in DATA schema
    existing_tables_df = sf_client.fetch_dataframe("""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = 'DATA'
    """)

    existing_tables = set(existing_tables_df['TABLE_NAME'].str.upper())

    # Keep only rows where KPI_TABLE_NAME exists in schema
    analytic_map_df['KPI_TABLE_NAME'] = analytic_map_df['KPI_TABLE_NAME'].str.upper()
    filtered_df = analytic_map_df[analytic_map_df['KPI_TABLE_NAME'].isin(existing_tables)].copy()

    dropped = len(analytic_map_df) - len(filtered_df)
    log.info("Filtered out %d non-existent tables from KPI mapping.", dropped)

    return filtered_df


# def extract_category_analytic_data(supplier_name:str, skus, category_name: str, sf_client):
#     """
#     Extracts category analytic data from the dataframe.
#     """

#     analytic_map = f"""
#         SELECT * FROM DATA.T_C_KPI_TABLE_MAPPING_FRONTEND
#         WHERE LOWER(CATEGORY) = LOWER('{category_name}')

#     """
#     analytic_map_df = sf_client.fetch_dataframe(analytic_map)
#     log.info("Analytic map data: %s", analytic_map_df)
#     if analytic_map_df.empty:
#         log.error("No data found for category: %s", category_name)
#         return None
#     # breakpoint()
#     # analytic_map['KPI_TABLE_NAME'] = analytic_map_df['KPI_TABLE_NAME'].str.replace("_FRONTEND", "")
#     analytic_map_df['KPI_TABLE_NAME'] = analytic_map_df['KPI_TABLE_NAME'].str.replace("_FRONTEND", "", regex=False)
#     analytic_map_df = filter_valid_kpi_tables(analytic_map_df, sf_client)
#     data_dict = {}
#     for row in analytic_map_df.itertuples():

#         if row.KPI_TABLE_NAME == None:
#             continue
        
#         # column_query = f'''SELECT COLUMN_NAME
#         # FROM information_schema.columns
#         # WHERE TABLE_SCHEMA = 'DATA'
#         # AND TABLE_NAME   = '{row.KPI_TABLE_NAME}'
#         # ORDER BY ORDINAL_POSITION;'''

#         # column_names = sf_client.fetch_dataframe(column_query)['COLUMN_NAME'].tolist()
#         # log.debug("Column names for table %s: %s", row.KPI_TABLE_NAME, column_names)
#         # Dynamically construct SKU filter if applicable
#         try:
#             sku_query = ""
#             if skus:
#                 formatted_skus = "', '".join(skus)
#                 sku_query = f"AND MATERIAL IN ('{formatted_skus}')"
            
#             analytic_data = pd.DataFrame(
#                 sf_client.select_records_with_filter(
#                     table_name='DATA.'+row.KPI_TABLE_NAME,

#                     filter_condition=(
#                         f"""
#                         SUPPLIER = '{supplier_name}'
#                         AND
#                         LOWER(category) = LOWER('{category_name}')
#                         AND 
#                         YEAR = (SELECT MAX(YEAR) FROM {'DATA.'+row.KPI_TABLE_NAME})""" 
#                         + sku_query
                        
#                     ),

#                 ),
#             )
#             if not analytic_data.empty:
#                 # Filter out columns with object dtype to avoid incorrect aggregation
#                 obj_cols = analytic_data.select_dtypes(include="object").columns
#                 if "MATERIAL" in obj_cols:
#                     obj_cols = obj_cols.drop("MATERIAL")
#                 obj_map = { col: "first" for col in obj_cols }

                
#                 # Generate the prompt for classification
#                 numeric_cols = [col for col in analytic_data.select_dtypes(include='number').columns if col != 'YEAR']
#                 prompt = classify_prompt(analytic_data[numeric_cols].head(2))

#                 agg_map = generate_chat_response_with_chain(prompt=prompt, model='gpt-4o')
#                 agg_map = re.sub(r"(?:python)?\s*", "", agg_map).strip("`\n ")

#                 agg_map = ast.literal_eval(agg_map)
                
#                 # group & aggregate
#                 groupby_cols = ["YEAR"]
#                 if "MATERIAL" in analytic_data.columns:
#                     groupby_cols.append("MATERIAL")
#                 # breakpoint()
#                 # Clean obj_map to remove keys that are also in groupby_cols
#                 clean_obj_map = {k: v for k, v in obj_map.items() if k not in groupby_cols}

#                 # Aggregate using combined agg_map and cleaned obj_map
#                 year_df = analytic_data.groupby(groupby_cols).agg(agg_map | clean_obj_map).reset_index()

#                 log.info("Executing query for analytic: %s", row.KPI_NAME)
        

#                 data_dict[row.KPI_NAME] = year_df #column_names #analytic_data
#         except:
#             log.error("Error processing table %s for supplier %s in category %s", row.KPI_TABLE_NAME, supplier_name, category_name)
#             continue
#     if data_dict:
#         return data_dict
#     else:
#         log.error("No data found for category: %s", category_name)
#         return None
    
@log_time
def extract_category_analytic_data(supplier_name: str, skus, category_name: str, sf_client):
    """
    Extracts category analytic data for a supplier and category from the KPI tables.
    """

    analytic_map_query = f"""
        SELECT * FROM DATA.T_C_KPI_TABLE_MAPPING_FRONTEND
        WHERE LOWER(CATEGORY) = LOWER('{category_name}')
    """
    analytic_map_df = sf_client.fetch_dataframe(analytic_map_query)

    if analytic_map_df.empty:
        log.warning("No KPI table mapping found for category: %s", category_name)
        return None

    # Clean table names
    analytic_map_df['KPI_TABLE_NAME'] = analytic_map_df['KPI_TABLE_NAME'].str.replace("_FRONTEND", "", regex=False)

    # Filter valid KPI tables (single threaded function assumed)
    analytic_map_df = filter_valid_kpi_tables(analytic_map_df, sf_client)

    data_dict = {}

    def fetch_column_names(table_name):
        column_query = f"""
            SELECT COLUMN_NAME
            FROM information_schema.columns
            WHERE TABLE_SCHEMA = 'DATA'
            AND TABLE_NAME = '{table_name}'
            AND COLUMN_NAME IN ('MATERIAL', 'SUPPLIER')
        """
        try:
            return table_name, sf_client.fetch_dataframe(column_query)['COLUMN_NAME'].str.upper().tolist()
        except Exception as e:
            log.error("Failed fetching column names for table %s. Error: %s", table_name, str(e))
            return table_name, []

    # Step 1: Pre-fetch column names in parallel
    table_name_map = {}
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(fetch_column_names, row.KPI_TABLE_NAME) for row in analytic_map_df.itertuples()]
        for future in as_completed(futures):
            table, cols = future.result()
            table_name_map[table] = cols

    def process_row(row):
        try:
            table_name = row.KPI_TABLE_NAME
            if not table_name:
                return None

            column_names = table_name_map.get(table_name, [])
            has_material_column = "MATERIAL" in column_names
            has_supplier_column = "SUPPLIER" in column_names

            log.debug("Does table %s have 'MATERIAL'? %s | 'SUPPLIER'? %s", table_name, has_material_column, has_supplier_column)

            if not has_supplier_column:
                return None

            sku_query = ""
            if skus and has_material_column:
                safe_skus = [sku.replace("'", "''") for sku in skus]
                formatted_skus = "', '".join(safe_skus)
                sku_query = f"AND MATERIAL IN ('{formatted_skus}')"

            filter_condition = f"""
                SUPPLIER = '{supplier_name.replace("'", "''")}'
                AND LOWER(category) = LOWER('{category_name}')
                AND YEAR = (SELECT MAX(YEAR) FROM DATA.{table_name})
                {sku_query}
            """

            analytic_data = pd.DataFrame(
                sf_client.select_records_with_filter(
                    table_name=f'DATA.{table_name}',
                    filter_condition=filter_condition,
                )
            )

            if analytic_data.empty:
                return None

            obj_cols = analytic_data.select_dtypes(include="object").columns
            if "MATERIAL" in obj_cols:
                obj_cols = obj_cols.drop("MATERIAL")

            obj_map = {col: "first" for col in obj_cols}

            numeric_cols = [col for col in analytic_data.select_dtypes(include='number').columns if col != 'YEAR']
            prompt = classify_prompt(analytic_data[numeric_cols].head(2))

            agg_map_raw = generate_chat_response_with_chain(prompt=prompt, model='gpt-4o')
            agg_map_raw = re.sub(r"(?:python)?\s*", "", agg_map_raw).strip("`\n ")
            agg_map = ast.literal_eval(agg_map_raw)

            groupby_cols = ["YEAR"]
            if "MATERIAL" in analytic_data.columns:
                groupby_cols.append("MATERIAL")

            clean_obj_map = {k: v for k, v in obj_map.items() if k not in groupby_cols}
            year_df = analytic_data.groupby(groupby_cols).agg(agg_map | clean_obj_map).reset_index()

            log.info("Query executed for KPI: %s", row.KPI_NAME)
            return (row.KPI_NAME, [year_df, row.KPI_OPPORTUNITY_COLUMN_NAME])

        except Exception as e:
            log.error("Failed processing table %s for supplier %s in category %s. Error: %s",
                         row.KPI_TABLE_NAME, supplier_name, category_name, str(e))
            return None

    # Step 2: Process analytic rows in parallel
    with ThreadPoolExecutor(max_workers=1000) as executor:
        futures = [executor.submit(process_row, row) for row in analytic_map_df.itertuples()]
        for future in as_completed(futures):
            result = future.result()
            if result:
                kpi_name, kpi_data = result
                data_dict[kpi_name] = kpi_data

    if not data_dict:
        log.warning("No analytic data extracted for category: %s", category_name)
        return None

    return data_dict


@log_time
def get_strategy_prompts(
    params: dict[str, Any],
    generation_type: str,
    **kwargs: Any,
) -> tuple[list, list, str, str]:
    """
    Gets the prompts and data for NF strategy based on the request type
    Args:
        params (dict): common arguments for the prompts
        generation_type (str): type of request
        kwargs (Any): Additional request specific data
    Returns
        tuple[list, list, str]: prompt, keys for the prompt, init message, current action
    """
    log.info("Generating strategy prompt for generation_type: %s", generation_type)
    market_map_df = kwargs["market_map"]
    action = ""

    if generation_type == "negotiation_strategy":
        log.debug("Processing default negotiation strategy.")
        params["market_map"] = market_map_df
        prompt = negotiation_strategy_prompt(**params)
        response_keys = [
            "market_approach",
            "market_approach_detail",
            "pricing_methodology",
            "pricing_methodology_detail",
            "contracting_methodology",
            "contracting_methodology_detail",
            "message",
            "suggested_prompts",
        ]
        init_message = (
            f"""Great! Based on our expertise, here is the best"""
            f"""{negotiation_conf["cta_button_map"]["strategy"].replace("Set", "")} to adopt:\n"""
        )
        action = "negotiation_strategy"
        log.info("Prompt and keys prepared for default strategy generation.")

    elif (generation_type == "negotiation_strategy_change") and (
        ("category" in kwargs["user_query"].lower()) or ("supplier" in kwargs["user_query"].lower())
    ):
        log.debug("Processing positioning change strategy for category/supplier.")
        args = {
            "all_category_positioning": kwargs["all_category_positioning"],
            "all_supplier_positioning": kwargs["all_supplier_relationships"],
            "category_positioning": params["category_positioning"],
            "supplier_positioning": params["supplier_positioning"],
            "market_approach": params["market_approach"],
            "pricing_methodology": params["pricing_methodology"],
            "contract_methodology": params["contract_methodology"],
            "supplier_profile": params["supplier_profile"],
            "pinned_elements": kwargs["pinned_elements"],
        }
        prompt = negotiation_change_positioning_prompt(**args)
        response_keys = ["message", "suggested_prompts", "request_type"]
        init_message = ""
        action = "negotiation_change_positioning"
        log.info("Prompt and keys prepared for positioning change.")

    else:
        log.debug("Processing change sourcing approach scenario.")
        params = {
            "all_category_positioning": kwargs["all_category_positioning"],
            "all_supplier_positioning": kwargs["all_supplier_relationships"],
            "all_market_approach": kwargs["alternatives_market_approach"],
            "all_pricing_methodology": kwargs["all_pricing_methodology"],
            "all_contract_methodology": kwargs["all_contracting_methodology"],
        }
        prompt = change_prompt(**params)
        response_keys = ["message", "suggested_prompts", "request_type"]
        init_message = ""
        action = "negotiation_change_sourcing_approach"
        log.info("Prompt and keys prepared for sourcing approach change.")

    log.info("Strategy prompt generation completed for action: %s", action)
    return prompt, response_keys, init_message, action

@log_time
def generate_tones_n_tactics(  # pylint: disable=too-many-statements
    reference_data: dict[str, Any],
    pinned_elements: dict[str, Any],
    generation_type: str,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Handle `Set/Change tone & tactics` functionality
    Args:
        reference_data (dict[str, Any]): tenant specific negotiation factory reference data
        pinned_elements (dict[str, Any]): elements pinned by the user
        generation_type (str): type of request
        kwargs (Any): Any additional arguments
    Returns:
        (dict[str, Any]: Return Negotiation strategy for the suppliers
    Raises:
        NegotiationFactoryUserException: If supplier name not present in user query
                                         or supplier data is not present for the category
    """
    log.info("Initiating Negotiation Approach for Tone & Tactics with %d kwargs", len(kwargs))
    params: dict[str, Any] = {}
    all_pinned_keys = pinned_elements.keys()
    flag_bp = "buyer_attractiveness" not in all_pinned_keys
    flag_sp = "supplier_positioning" not in all_pinned_keys
    log.debug("Missing buyer_positioning: %s, Missing supplier_positioning: %s", flag_bp, flag_sp)

    if flag_bp or flag_sp:
        log.warning("Buyer/Supplier positioning missing. Redirecting to setup steps.")
        holder_str = ""
        holder_list = []
        if flag_bp and flag_sp:
            holder_str = "buyer positioning & supplier postioning"
            holder_list.append({"prompt": "Set buyer positioning", "intent": "negotiation_approach_bp"})
            holder_list.append({"prompt": "Set supplier positioning", "intent": "negotiation_approach_sp"})
        elif flag_bp:
            holder_str = "buyer positioning"
            holder_list.append({"prompt": "Set buyer positioning", "intent": "negotiation_approach_bp"})
        elif flag_sp:
            holder_str = "supplier positioning"
            holder_list.append({"prompt": "Set supplier positioning", "intent": "negotiation_approach_sp"})

        params["response_type"] = generation_type
        params["message"] = f"Please set {holder_str} before setting up tone and tactics."
        params["suggested_prompts"] = holder_list + [{
            "prompt": "Generate negotiation arguments",
            "intent": "negotiation_arguments",
        }]
        return convert_to_response_format(**params)

    if generation_type == "negotiation_approach_tnt":
        log.info("Setting new tone & tactics...")
        params["response_type"] = generation_type
        pinned_sp = re.sub(r"\W+|_", " ", pinned_elements["supplier_positioning"]["value"]).strip()
        pinned_ba = re.sub(r"\W+|_", " ", pinned_elements["buyer_attractiveness"]["value"]).strip()
        
        log.debug("Resolved positions - Supplier: %s, Buyer: %s", pinned_sp, pinned_ba)

        tones_n_tactics_df = reference_data["negotiation_strategy_tones_n_tactics"]
        tones_n_tactics_df = tones_n_tactics_df.loc[
            (tones_n_tactics_df["supplier_positioning"].str.lower() == pinned_sp.lower()) &
            (tones_n_tactics_df["buyer_attractiveness"].str.lower() == pinned_ba.lower())
        ]

        params["message"] = (
            f"""Based on selected supplier positioning as **{pinned_sp}** and """
            f"""buyer positioning as """
            f"""{'**strategic**' if (pinned_ba.lower() == 'high') else '**non-strategic**'}, """
            f"""it is recommended that you use **{tones_n_tactics_df["tone_name"].iloc[0]}** tone and tactic. You can adjust the tone and tactic as per your preferences."""
        )

        # tones_n_tactics_df = reference_data["negotiation_strategy_tones_n_tactics"]
        # tones_n_tactics_df = tones_n_tactics_df.loc[
        #     (tones_n_tactics_df["supplier_positioning"].str.lower() == pinned_sp.lower()) &
        #     (tones_n_tactics_df["buyer_attractiveness"].str.lower() == pinned_ba.lower())
        # ]
        # if tones_n_tactics_df.shape[0] != 1:
        #     error_msg = "Unexpected results received. Multiple tone & tactics are not allowed."
        #     log.error(error_msg)
        #     raise NegotiationFactoryException(error_msg)

        # log.info("Tone & tactic row matched successfully.")

        # params["tone"] = {
        #     "title": tones_n_tactics_df["tone_name"].iloc[0],
        #     "description": tones_n_tactics_df["tone_description"].iloc[0],
        #     "prioritize": ast.literal_eval(tones_n_tactics_df["prioritize"].iloc[0]),
        #     "tactics": [
        #         {
        #             "title": tactic["tactic"],
        #             "description": tactic["description"],
        #         }
        #         for tactic in ast.literal_eval(tones_n_tactics_df["tactics"].iloc[0])
        #     ],
        # }

        params["response_type"] = generation_type
        # params["message"] = "Based on your selection, here are the updated tones and and tactics "
        params["additional_data"] = {}

        tones_n_tactics_dict = reference_data["negotiation_strategy_tones_n_tactics"].to_dict(orient="records")
        unique_titles: list[str] = []
        holder: list[dict[str, Any]] = []

        for row in tones_n_tactics_dict:
            if row["tone_name"] in unique_titles:
                continue
            holder.append({
                "title": row["tone_name"],
                "description": row["tone_description"],
                "prioritize": ast.literal_eval(row["prioritize"]),
                "tactics": [
                    {
                        "title": tactic["tactic"],
                        "description": tactic["description"],
                    }
                    for tactic in ast.literal_eval(row["tactics"])
                ],
            })
            unique_titles.append(row["tone_name"])

        params["tones"] = holder

        lst_suggested_prompts = get_section_suggested_prompts(section_name="Define Negotiation Strategy")
        params["suggested_prompts"] = [
            prompt for prompt in lst_suggested_prompts if prompt["prompt"] not in [
                "Set tone & tactics",
                "Set carrots & sticks" if ("carrots" in pinned_elements or "sticks" in pinned_elements) else "Change carrots & sticks"
            ]
        ]

    elif generation_type == "negotiation_approach_tnt_change":
        log.info("Changing tone & tactics...")
        params["response_type"] = generation_type
        params["message"] = "Based on your selection, here are the updated tones and and tactics "
        params["additional_data"] = {}

        tones_n_tactics_dict = reference_data["negotiation_strategy_tones_n_tactics"].to_dict(orient="records")
        unique_titles: list[str] = []
        holder: list[dict[str, Any]] = []

        for row in tones_n_tactics_dict:
            if row["tone_name"] in unique_titles:
                continue
            holder.append({
                "title": row["tone_name"],
                "description": row["tone_description"],
                "prioritize": ast.literal_eval(row["prioritize"]),
                "tactics": [
                    {
                        "title": tactic["tactic"],
                        "description": tactic["description"],
                    }
                    for tactic in ast.literal_eval(row["tactics"])
                ],
            })
            unique_titles.append(row["tone_name"])

        params["tones"] = holder
        log.info("Total unique tones prepared: %d", len(holder))

        lst_suggested_prompts = get_section_suggested_prompts(section_name="Define Negotiation Strategy")
        params["suggested_prompts"] = [
            prompt for prompt in lst_suggested_prompts if prompt["prompt"] not in [
                "Set tone & tactics",
                "Change tone & tactics",
                "Set carrots & sticks" if ("carrots" in pinned_elements or "sticks" in pinned_elements) else "Change carrots & sticks"
            ]
        ]

    log.info("Tone & Tactics generation completed for generation_type: %s", generation_type)
    return convert_to_response_format(**params)


@log_time
def generate_csb_positioning(
    reference_data: dict[str, Any],
    pg_db_conn: PGConnector,
    sf_client: Any,
    category: str,
    user_query: str,
    pinned_elements: dict[str, Any],
    chat_history: list[dict[str, Any]],
    generation_type: str,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Generate category and supplier positioning of the supplier
    Args:
        reference_data (dict[str, Any]): tenant specific negotiation factory reference data
        pg_db_conn (PGConnector) : Connection object to postgres database
        category (str): user selected category
        user_query (str) : received user query
        pinned_elements (dict[str, Any]): elements pinned by the user
        chat_history (list[dict[str, Any]]) : chat history list
        generation_type (str): type of request
        kwargs (Any): Any additional arguments
    Returns:
        (dict[str, Any]: Return Negotiation strategy for the suppliers
    Raises:
        NegotiationFactoryUserException: If supplier name not present in user query
                                         or supplier data is not present for the category
    """
    log.info("Initiating Negotiation Approach with generation_type: %s and %d kwargs", generation_type, len(kwargs))

    _, supplier_profile = get_supplier_profile(
        pg_db_conn,
        sf_client,
        category,
        user_query,
        pinned_elements,
    )
    log.info("Fetched supplier profile for supplier: %s", supplier_profile.get("supplier_name", ""))

    if generation_type == "negotiation_approach_bp" or "buyer" in user_query.lower():
        log.info("Generating prompts for buyer positioning")
        params = {}
        remove_list: list[str] = []

        suggested_prompts = get_section_suggested_prompts(section_name="Create Negotiation Approach")
        remove_list = get_prompts_to_be_removed(
            generation_type=generation_type,
            pinned_elements=pinned_elements,
            user_query=user_query,
        )
        remove_list.extend([
            (
                f"{'Set' if 'negotiation_strategy' in pinned_elements else 'Change'} sourcing approach"
            ),
            (
                f"{'Set' if 'tone_and_stactics' in pinned_elements else 'Change'} tone & tactics"
            ),
            "Change market approach",
            "Change pricing methodology",
            "Change contracting methodology",
        ])

        log.debug("Prompts to be removed from suggestions: %s", remove_list)

        suggested_prompts = [prompt for prompt in suggested_prompts if prompt["prompt"] not in remove_list]
        
        # Override suggested_prompts based on pinned state
        category_set = "category_positioning" in pinned_elements
        supplier_set = "supplier_positioning" in pinned_elements
        buyer_set = "buyer_attractiveness" in pinned_elements
        tone_set = "tone_and_tactics" in pinned_elements
        carrots_sticks_set = "carrots" in pinned_elements or "sticks" in pinned_elements

        # Conditional overrides based on flow
        if generation_type == "negotiation_approach_cp" and not category_set:
            suggested_prompts = [
                {"prompt": "Change negotiation objectives", "intent": "negotiation_objective"},
                {"prompt": "Set supplier positioning", "intent": "negotiation_approach_sp"},
                {"prompt": "Set buyer positioning", "intent": "negotiation_approach_bp"},
            ]
        elif generation_type == "negotiation_approach_cp" and category_set:
            suggested_prompts = [
                {"prompt": "Change negotiation objectives", "intent": "negotiation_objective"},
                {"prompt": "Change category positioning", "intent": "negotiation_strategy_change"},
                {"prompt": "Set supplier positioning", "intent": "negotiation_approach_sp"},
                {"prompt": "Set buyer positioning", "intent": "negotiation_approach_bp"},
            ]
        elif generation_type == "negotiation_approach_sp" and not supplier_set and not buyer_set:
            suggested_prompts = [
                {"prompt": "Change negotiation objectives", "intent": "negotiation_objective"},
                {"prompt": "Change category positioning", "intent": "negotiation_strategy_change"},
                {"prompt": "Set buyer positioning", "intent": "negotiation_approach_bp"},
            ]
        elif generation_type == "negotiation_approach_bp" and category_set and supplier_set and not buyer_set and not tone_set:
            suggested_prompts = [
                {"prompt": "Change negotiation objectives", "intent": "negotiation_objective"},
                {"prompt": "Change category positioning", "intent": "negotiation_strategy_change"},
                {"prompt": "Change supplier positioning", "intent": "negotiation_approach_sp"},
                {"prompt": "Set tone & tactics", "intent": "negotiation_approach_tnt"},
            ]
        elif generation_type == "negotiation_approach_bp" and category_set and supplier_set and buyer_set and not tone_set:
            suggested_prompts = [
                {"prompt": "Change negotiation objectives", "intent": "negotiation_objective"},
                {"prompt": "Change category positioning", "intent": "negotiation_strategy_change"},
                {"prompt": "Change supplier positioning", "intent": "negotiation_approach_sp"},
                {"prompt": "Set tone & tactics", "intent": "negotiation_approach_tnt"},
            ]
        elif generation_type == "negotiation_approach_tnt" and tone_set and not carrots_sticks_set:
            suggested_prompts = [
                {"prompt": "Set carrots & sticks", "intent": "negotiation_select_carrot_sticks"},
                {"prompt": "Generate negotiation arguments", "intent": "negotiation_arguments"},
            ]
        elif generation_type == "negotiation_select_carrot_sticks" and carrots_sticks_set:
            suggested_prompts = [
                {"prompt": "Set/Change tone & tactics", "intent": "negotiation_approach_tnt"},
                {"prompt": "Generate negotiation arguments", "intent": "negotiation_arguments"},
            ]
        params["suggested_prompts"] = get_distinct_suggested_prompts(prompts=suggested_prompts)
        params["response_type"] = generation_type
        params["message"] = (
            f"What is the importance of your company for {supplier_profile.get('supplier_name', 'this company')}?"
        )
        params["additional_data"] = {
            "buyer_attractiveness_questions": [
                {
                    "question": "You are a strategic client to them.",
                    "value": "high",
                },
                {
                    "question": "You are not a very strategic client to them.",
                    "value": "low",
                },
            ],
        }
        log.info("Returning buyer positioning prompt options.")
        return convert_to_response_format(**params)

    log.info("Generating positioning data...")
    postitioning,pct = get_positioning_data(
        sf_client,
        profile=supplier_profile,
        category=category,
        reference_data=reference_data,
        user_query=user_query,
    )

    log.info("Positioning data computed.")

#     params = {
#         "category_positioning": postitioning["category_positioning"],
#         "supplier_positioning": postitioning["supplier_relationship"],
#         "market_approach": postitioning["filtered_market"].head(1)["market_approach"].values,
#         "pricing_methodology": postitioning["pricing_methodology"],
#         "contract_methodology": postitioning["contracting_methodology"],
#         "supplier_profile": supplier_profile,
#         "percentage_spend_on_catgory":pct
#     }

#     init_message = (
#     f"Based on our analysis, we recommend the following {postitioning["category_positioning"] if (generation_type == 'negotiation_approach_cp') else postitioning["supplier_relationship"}."
#     f"as {'category' if (generation_type == 'negotiation_approach_cp') else 'supplier'} positioning. "
#     "This is suggested as a starting point, and you can adjust the positioning as your preferences.\n"
# )
    # Build parameters
    params = {
        "category_positioning": postitioning["category_positioning"],
        "supplier_positioning": postitioning["supplier_relationship"],
        "market_approach": postitioning["filtered_market"].head(1)["market_approach"].values,
        "pricing_methodology": postitioning["pricing_methodology"],
        "contract_methodology": postitioning["contracting_methodology"],
        "supplier_profile": supplier_profile,
        "percentage_spend_on_catgory": pct
    }

    # Determine target type and positioning value
    is_category = generation_type == 'negotiation_approach_cp'
    positioning_label = "category" if is_category else "supplier"
    positioning_value = postitioning["category_positioning"] if is_category else postitioning["supplier_relationship"]

    # Build intro message
    init_message = (
        f"Based on our analysis, we recommend **{positioning_value.upper()}** as the most suitable {positioning_label} positioning."
        "You can adjust the positioning as per your preferences.\n"
    )

    positioning_field = "supplier_positioning" if generation_type == "negotiation_approach_cp" else "category_positioning"
    params[positioning_field] = pinned_elements.get(positioning_field, {}).get("value", "")

    log.debug("Generating LLM prompt for %s", generation_type)
    prompt = negotiation_set_positioning_prompt(**params)

    response_keys = [
        "category_positioning" if generation_type == "negotiation_approach_cp" else "supplier_positioning",
        "category_positioning_detail" if generation_type == "negotiation_approach_cp" else "supplier_positioning_detail",
        "message",
        "suggested_prompts",
    ]

    response = run_conversation_chat(
        chat_history,
        prompt,
        user_query,
        model=negotiation_conf["model"]["model_name"],
        temperature=0.3,
        window_size=negotiation_conf["model"]["conversation_buffer_window"],
    )

    log.info("Response from conversation model: %s", response)

    ai_response = get_airesponse_as_dict(response=response, response_keys=response_keys)

    params = process_approach_response_key_content(
        supplier_profile=supplier_profile,
        ai_response=ai_response,
        init_message=init_message,
        generation_type=generation_type,
        pinned_elements=pinned_elements,
    )
    
    params['selected_positioning'] = positioning_value
    
    log.info("Returning category/supplier positioning response.")
    return convert_to_response_format(**params)

@log_time
def get_objectives_ctas(pinned_elements: dict[str, Any], user_query: str) -> list[dict[str, Any]]:
    """
    Get the objectives CTAs
    Args:
        pinned_elements (dict[str, Any]): elements pinned by the user
        user_query (str): received user query
    Returns:
        (list[dict[str, Any]]): Return objectives CTAs
    """
    log.info("Generating objective CTAs for user_query: %s", user_query)
    suggested_prompts = get_section_suggested_prompts(
        section_name="Select Negotiation Objectives",
    )
    log.debug("Initial suggested prompts: %s", suggested_prompts)

    remove_list = []
    all_pinned_elemnts = list(pinned_elements.keys())
    log.debug("Pinned elements: %s", all_pinned_elemnts)

    if user_query.startswith("Change ") and "objectives" in user_query:
        remove_list.append("Change negotiation objectives")
        remove_list.append("Set negotiation objectives")
    elif user_query.startswith("Set ") and "objectives" in user_query:
        remove_list.append("Set negotiation objectives")
        remove_list.append("Change negotiation objectives")

    remove_list.append(
        f"{'Set' if 'category_positioning' in all_pinned_elemnts else 'Change'}"
        " category positioning",
    )
    remove_list.append(
        f"{'Set' if 'supplier_positioning' in all_pinned_elemnts else 'Change'}"
        " supplier positioning",
    )
    remove_list.append(
        f"{'Set' if 'buyer_attractiveness' in all_pinned_elemnts else 'Change'}"
        " buyer positioning",
    )
    # remove_list.append(
    #     f"{'Set' if 'negotiation_strategy' in all_pinned_elemnts else 'Change'}"
    #     " sourcing approach",
    # )
    remove_list.append("Change sourcing approach")
    remove_list.append("Set sourcing approach")

    log.debug("Prompts to be removed: %s", remove_list)

    suggested_prompts = [
        prompt for prompt in suggested_prompts if (prompt["prompt"] not in remove_list)
    ]

    log.info("Final CTAs returned: %s", suggested_prompts)
    return suggested_prompts
