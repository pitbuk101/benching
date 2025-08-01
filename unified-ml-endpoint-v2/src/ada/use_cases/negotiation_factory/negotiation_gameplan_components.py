"""Module to generate insight , set negotiation target """

from __future__ import annotations

import ast
import json
import re
from typing import Any
import pandas as pd

from ada.components.db.pg_connector import PGConnector
from ada.components.llm_models.generic_calls import (
    generate_chat_response_with_chain,
    run_conversation_chat,
)
from ada.use_cases.negotiation_factory.analytics_queries import get_early_payments_query, get_parametric_cost_modeling_query, get_payment_terms_query, get_unused_discount_query, get_price_arbitrage_query
from ada.use_cases.negotiation_factory.prompts import generate_objective_summary_prompt, generate_price_reduction_prompt, generate_payment_terms_prompt
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


from ada.use_cases.negotiation_factory.util_prompts import extract_objectives_prompt
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time
from datetime import datetime

log = get_logger("Negotiation_gameplan_components")
negotiation_conf = read_config("use-cases.yml")["negotiation_factory"]
model_conf = read_config("models.yml")


def get_positioning_data(
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
    positioning: dict[str, Any] = {}
    # pylint: enable=R0801
    strategy_data = get_negotiation_strategy_data(
        reference_data,
        category,
    )
    incumbency = int(profile.get("number_of_supplier_in_category", "0"))
    positioning["supplier_relationship"] = profile.get("supplier_relationship", "")
    positioning["all_supplier_relationships"] = negotiation_conf["supplier_positioning"]
    positioning["category_positioning"] = strategy_data.get(
        negotiation_conf["category_positioning_column"],
        "",
    )
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
    positioning["filtered_market"] = positioning["market_map_df"][
        (
            positioning["market_map_df"][negotiation_conf["category_auction_map"]]
            == strategy_data.get(negotiation_conf["category_auction_map"], "")
        )
        & (positioning["market_map_df"]["incumbency"] <= incumbency)
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
    if len(positioning["filtered_market"]) == 0:
        error_msg = """Market approach not found based on the selected parameters. Please
            change the parameters to get a relevant market approach for strategy."""
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
    return positioning


@log_time
def generate_strategy(
    reference_data: dict[str, Any],
    pg_db_conn: PGConnector,
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
    log.info("Initiating Negotiation Strategy %d", len(kwargs))
    # pylint: disable=R0801
    _, supplier_profile = get_supplier_profile(
        pg_db_conn,
        category,
        user_query,
        pinned_elements,
    )
    postitioning = get_positioning_data(
        profile=supplier_profile,
        category=category,
        reference_data=reference_data,
        user_query=user_query,
    )
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
    # pylint: disable=R0801
    response = run_conversation_chat(
        chat_history,
        prompt,
        user_query,
        model=negotiation_conf["model"]["model_name"],
        window_size=negotiation_conf["model"]["conversation_buffer_window"],
    )
    response = response.replace("json", "").replace("`", "")
    log.info("Response from negotiation strategy conversation chain: %s", response)
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
    # pylint: disable=R0913
    # pylint: disable=R0912
    # pylint: disable=R0915

    # def classify the query in nego_intent or nego_bein()
    log.info("Starting insight generation. %d", len(kwargs))
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
    if before_update_request_type == "" or generation_type == "negotiation_begin":  # request came from Ada chat
        
        #Direcring the user to select skus for given supplier
        ctas = {
            "prompt": negotiation_conf["cta_button_map"]["select_skus"],
            "intent": "negotiation_select_skus",
        }
        
        suggested_prompts = get_section_suggested_prompts(
            section_name="Select Supplier",
        )
        remove_list = []
        # if negoiation objective is pinned
        remove_list.append(
            f"{'Set' if 'insights' in pinned_elements.keys() else 'Change'} negotiation objectives",
        )
        suggested_prompts = [
            prompt for prompt in suggested_prompts if (prompt["prompt"] not in remove_list)
        ]
        params = {
            "response_type": "supplier_details",
            "message": (
                """Insights are accessible from `Select Supplier` section of navigation panel."""
                """\nPlease click `view` option in `Insights` to access them."""
                        ),
            "additional_data": {
            "suppliers_data": [{
                    "supplierName": supplier_profile['supplier_name'],
                    "spend": supplier_profile['spend_ytd'],
                    "currencySymbol": supplier_profile['currency_symbol'],
                    "percentageSpendContribution": supplier_profile['percentage_spend_across_category_ytd'],
                    "currencyPosition": supplier_profile['currency_position']
                }],
            "follow_up_prompt": ctas,
            "welcome_message": "Thank you for selecting SUPPLIER_NAME. Here are few"
            "probable next steps:",
        },
            "suppliers_profiles": [supplier_profile],
            # "suggested_prompts": suggested_prompts,
        }
        return convert_to_response_format(**params)  # type:ignore

    log.info("request_type %s", generation_type)
    
    display_val = insights if generation_type == "negotiation_insights" else objectives
    log.info(f"** display_val **\n{display_val}\n")
    if len(display_val) == 0:
        return convert_to_response_format(
            response_type=generation_type.replace("negotiation_", ""),
            message=(
                "Apologies, but at the moment, "
                f"""we dont have any {generation_type.replace("negotiation_", "")} for"""
                f" supplier {supplier_name}"
            ),
            supplier_profile=supplier_profile,
        )
    probable_objectives = list(
        {insight["insight_objective"] for insight in display_val},
    )
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
        log.info(ai_response)
        try:
            extracted_objectives = json.loads(ai_response)
        except json.decoder.JSONDecodeError as json_error:
            log.error("Error in decoding JSON: %s", json_error)
            extracted_objectives = json_regex(
                ai_response,
                ["extracted_objectives"],
            )
            if not extracted_objectives:
                extracted_objectives["extracted_objectives"] = []
        matched_objectives = (
            extracted_objectives.get("extracted_objectives", []) or probable_objectives
        )
    matched_objectives = [objective_val.lower() for objective_val in matched_objectives]
    insights_objectives = [
        insight
        for insight in display_val
        if insight["insight_objective"].lower() in matched_objectives
    ]
    log.info(
        "Number of values fetched for %s :  %s",
        supplier_name,
        len(insights_objectives),
    )
    if not insights_objectives:
        return convert_to_response_format(
            response_type=generation_type.replace("negotiation_", ""),
            message=(
                "I'm sorry, but I couldn't find any "
                f"""{generation_type.replace("negotiation_", "")}"""
                " matching with specified goal [ i.e. "
                f"{', '.join(matched_objectives)} ]"
                f"for supplier {supplier_name}. Is there anything else I can assist you with ?"
            ),
            supplier_profile=supplier_profile,
        )
    if generation_type == "negotiation_insights":  # List insights
        suggested_prompts = get_section_suggested_prompts(
            section_name="Select Supplier",
        )
        remove_list = []
        # if negoiation objective is pinned
        remove_list.append(
            f"{'Set' if 'objectives' in all_keys else 'Change'} negotiation objectives",
        )
        suggested_prompts = [
            prompt for prompt in suggested_prompts if (prompt["prompt"] not in remove_list)
        ]
    else:
        suggested_prompts = get_workflow_suggested_prompts(
            pinned_elements,
            need_supplier_profile_check=False,
            include_insights=generation_type != "negotiation_insights",
            starts_with="objective",
        )

    log.info(f"** suggested_prompts **\n{suggested_prompts}\n")

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
    return convert_to_response_format(**params)  # type:ignore


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
    """
    Extract objectives related to supplier from database
    """
    log.info("Starting objective generation. %d", len(kwargs))
    log.info("request_type %s", generation_type)
    log.info("skus %s", skus)

    supplier_name, supplier_profile, insights_fr_db, objectives_fr_db = get_supplier_profile_insights_objectives(
        pg_db_conn,
        sf_client,
        category,
        user_query,
        pinned_elements,
    )

    sku_names = [item['name'] for item in skus] if skus else None
    formatted_sku = "('{}')".format("', '".join(sku_names)) if sku_names else None
    log.info(f"** sku_names **\n{sku_names}\n")

    objective_analytic_config = {
        "Payment Terms": {
            "analytic_name": ["payment terms standardization"],
            "queries": [get_payment_terms_query],
            "rename": [
                {
                    "SPEND": "Total Spend",
                    "SELECTED_PAYMENT_TERM_DAYS": "Avg Payment Term Days",
                    "POTENTIAL_SAVINGS": "Potential Cost Savings"
                }
            ],
            "aggregation": [
                {
                    'SPEND': 'sum',
                    'SELECTED_PAYMENT_TERM_DAYS': 'mean',
                    'POTENTIAL_SAVINGS': 'sum'
                }
            ],
            "groupby_cols": [
                {
                    "current_year": ['YEAR', 'QUARTER', 'MATERIAL'],
                    "last_year": ['YEAR', 'MATERIAL']
                }
            ],
            "sorting_cols" : [["POTENTIAL_SAVINGS"]],
        },
        "Price Reduction": {
            "analytic_name": ["early payments", "unused discount", "Total Saving Achieved", "price arbitrage query"],
            "queries": [get_early_payments_query, get_unused_discount_query, get_parametric_cost_modeling_query, get_price_arbitrage_query],
            "rename": [
                {
                    "TOTAL_SPENDS": "Total Spends",
                    "DIFF_EARLY_PAYMENT": "Avg Early Payment Days",
                    "EARLY_PAYMENT_OPPORTUNITY": "Early Payment Opportunity"
                },
                {"DISCOUNT": "DISCOUNT USED"},
                {
                    "COMPONENT": "COMPONENT",
                    "CLEANSHEET_OPPORTUNITY": "Cleansheet Opportunity",
                    "PCM_GAP_PERCENTAGE_PER_UNIT": "PCM Gap %"
                },
                {
                    "MINIMUM_AVERAGE_PRICE": "Min Avg Price",
                    "PRICE_AVERAGE": "Price Avg",
                    "PRICE_ARBITRAGE": "Price Arbitrage",
                    "PRICE_ARBITRAGE_PERCENTAGE": "Arbitrage %"
                }
            ],
            "aggregation": [
                {
                    'TOTAL_SPENDS': 'sum',
                    'DIFF_EARLY_PAYMENT': 'mean',
                    'EARLY_PAYMENT_OPPORTUNITY': 'sum'
                },
                {
                    'DISCOUNT': 'mean',
                    'DISCOUNT_POSSIBLE': 'mean',
                    'DISCOUNT_NOT_USED': 'mean'
                },
                {
                    'CLEANSHEET_OPPORTUNITY': 'sum',
                    'PCM_GAP_PERCENTAGE_PER_UNIT': 'mean'
                },
                {
                    'MINIMUM_AVERAGE_PRICE': 'mean',
                    'PRICE_AVERAGE': 'mean',
                    'PRICE_ARBITRAGE': 'mean',
                    'PRICE_ARBITRAGE_PERCENTAGE': 'mean'
                }
            ],
            "groupby_cols": [
                {
                    "current_year": ['YEAR', 'QUARTER', 'MATERIAL'],
                    "last_year": ['YEAR', 'MATERIAL']
                },
                {
                    "current_year": ['YEAR', 'QUARTER', 'MATERIAL'],
                    "last_year": ['YEAR', 'MATERIAL']
                },
                {
                    "current_year": ['YEAR', 'QUARTER', 'MATERIAL', 'COMPONENT'],
                    "last_year": ['YEAR', 'MATERIAL', 'COMPONENT']
                },
                {
                    "current_year": ['YEAR', 'QUARTER', 'MATERIAL'],
                    "last_year": ['YEAR', 'MATERIAL']
                }
            ],
            "sorting_cols" : [["EARLY_PAYMENT_OPPORTUNITY"],["DISCOUNT_NOT_USED"],["CLEANSHEET_OPPORTUNITY"],["PRICE_ARBITRAGE_PERCENTAGE"]]
        }
    }

    objectives = []

    for objective_name, config in objective_analytic_config.items():
        context_dict = {
            "objective": objective_name,
            "supplier": supplier_name,
            "category": category,
            # "supplier_profile": supplier_profile,
            "supplier_profile": supplier_profile,
            "data": {}
        }
        analytics_names = []

        for query_func, agg, analytic_name, rename_cols, groupby_cols, sorting_col in zip(
            config["queries"],
            config["aggregation"],
            config["analytic_name"],
            config["rename"],
            config["groupby_cols"],
            config["sorting_cols"]
        ):
            # query = query_func(supplier_name=supplier_name, sku_names=formatted_sku, category=category)
            query = query_func(supplier_name=supplier_name, sku_names=formatted_sku) #, category=category)
            df = sf_client.fetch_dataframe(query)

            if df.empty:
                continue

            current_year = datetime.now().year
            df_current = df[df['YEAR'] == current_year].groupby(groupby_cols['current_year']).agg(agg).reset_index()
            df_past = df[df['YEAR'] < current_year].groupby(groupby_cols['last_year']).agg(agg).reset_index()

            if len(sorting_col)>1:
                final_df = pd.concat([df_current, df_past], ignore_index=True).sort_values(['YEAR', 'QUARTER']+sorting_col, ascending=[False, False, False])
            else:
                final_df = pd.concat([df_current, df_past], ignore_index=True).sort_values(['YEAR', 'QUARTER'], ascending=[False, False])
            final_df.reset_index(drop=True, inplace=True)
            if not sku_names:
                top_5_materials = final_df.dropna(subset = ['MATERIAL','QUARTER']).sort_values(sorting_col)['MATERIAL'].unique()[:5]
                final_df = final_df[final_df['MATERIAL'].isin(top_5_materials)]

            final_df.rename(columns=rename_cols, inplace=True)
            context_dict["data"][analytic_name] = final_df.to_dict(orient="records")
            analytics_names.append(analytic_name)

        if context_dict["data"]:
            log.info(f"** context_dict **\n{context_dict}\n")
            if objective_name == 'Payment Terms':
                objective_generation_prompt = generate_payment_terms_prompt(context_dict)
                summary = generate_chat_response_with_chain(
                    prompt=objective_generation_prompt,
                    temperature=0.3
                )
            else:
                objective_generation_prompt = generate_price_reduction_prompt(context_dict)
                summary = generate_chat_response_with_chain(
                    prompt=objective_generation_prompt,
                    temperature=0.3
                )
            summary = summary.replace('*','')
            objectives.append({
                "id": len(objectives),
                "objective": summary,
                "objective_type": objective_name,
                "objective_reinforcements": [],
                "list_of_skus": sku_names,
                "analytics_names": analytics_names
            })

    if len(objectives) == 0:
        return convert_to_response_format(
            response_type=generation_type.replace("negotiation_", ""),
            message=(
                "I'm sorry, but I couldn't find any "
                f"{generation_type.replace('negotiation_', '')}"
                " matching with specified goal "
                f"for supplier {supplier_name}. Is there anything else I can assist you with?"
            ),
            supplier_profile=supplier_profile,
        )

    suggested_prompts = get_objectives_ctas(pinned_elements=pinned_elements, user_query=user_query)

    params = {
        "response_type": generation_type.replace("negotiation_", ""),
        "message": (
            f"""Please see below important {generation_type.replace('negotiation_', '')}"""
            f""" for supplier {supplier_name}."""
        ),
        "objectives": objectives,
        "supplier_profile": supplier_profile,
        "suggested_prompts": suggested_prompts,
    }
    return convert_to_response_format(**params)



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
    market_map_df = kwargs["market_map"]
    action = ""
    if generation_type == "negotiation_strategy":
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
    elif (generation_type == "negotiation_strategy_change") and (
        ("category" in kwargs["user_query"].lower()) or ("supplier" in kwargs["user_query"].lower())
    ):
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
        init_message = ""
        response_keys = ["message", "suggested_prompts", "request_type"]
        action = "negotiation_change_positioning"
    else:
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
    log.info("Initiating Negotiation Approach for Tone & Tactics %d", len(kwargs))
    params: dict[str, Any] = {}
    all_pinned_keys = pinned_elements.keys()
    flag_bp = "buyer_attractiveness" not in all_pinned_keys
    flag_sp = "supplier_positioning" not in all_pinned_keys
    if flag_bp or flag_sp:
        holder_str = ""
        holder_list = []
        if flag_bp and flag_sp:
            holder_str = "buyer positioning & supplier postioning"
            holder_list.append(
                {
                    "prompt": "Set buyer positioning",
                    "intent": "negotiation_approach_bp",
                },
            )
            holder_list.append(
                {
                    "prompt": "Set supplier positioning",
                    "intent": "negotiation_approach_sp",
                },
            )
        elif flag_bp and not flag_sp:
            holder_str = "buyer positioning"
            holder_list.append(
                {
                    "prompt": "Set buyer positioning",
                    "intent": "negotiation_approach_bp",
                },
            )
        elif flag_sp and not flag_bp:
            holder_str = "supplier positioning"
            holder_list.append(
                {
                    "prompt": "Set supplier positioning",
                    "intent": "negotiation_approach_sp",
                },
            )
        params["response_type"] = generation_type
        params["message"] = f"Please set {holder_str} before setting up tone and tactics."
        params["suggested_prompts"] = holder_list
        params["suggested_prompts"].extend(
            [
                {
                    "prompt": "Generate negotiation arguments",
                    "intent": "negotiation_arguments",
                },
            ],
        )
        return convert_to_response_format(**params)
    if generation_type == "negotiation_approach_tnt":
        params["response_type"] = generation_type
        pinned_sp = re.sub(
            r"\W+|_",
            " ",
            pinned_elements["supplier_positioning"]["value"],
        ).strip()
        pinned_ba = re.sub(
            r"\W+|_",
            " ",
            pinned_elements["buyer_attractiveness"]["value"],
        ).strip()
        params["message"] = (
            f"""Based on selected supplier positioning as '{pinned_sp}' and """
            f"""buyer positioning as """
            f"""{'strategic' if (pinned_ba.lower() == 'high') else 'non-strategic'}, """
            f"""it is recommended that you use the following tone and tactic"""
        )
        tones_n_tactics_df = reference_data["negotiation_strategy_tones_n_tactics"]
        tones_n_tactics_df = tones_n_tactics_df.pipe(
            lambda x: x.loc[
                (x["supplier_positioning"].str.lower() == pinned_sp.lower())
                & (x["buyer_attractiveness"].str.lower() == pinned_ba.lower())
            ],
        )
        if tones_n_tactics_df.shape[0] != 1:
            error_msg = """Unexpected results received.Multiple tone & tactics are not allowed."""
            raise NegotiationFactoryException(error_msg)

        params["tone"] = {
            "title": tones_n_tactics_df["tone_name"].iloc[0],
            "description": tones_n_tactics_df["tone_description"].iloc[0],
            "prioritize": ast.literal_eval(tones_n_tactics_df["prioritize"].iloc[0]),
            "tactics": [
                {
                    "title": tactic["tactic"],
                    "description": tactic["description"],
                }
                for tactic in ast.literal_eval(tones_n_tactics_df["tactics"].iloc[0])
            ],
        }
        lst_suggested_prompts = get_section_suggested_prompts(
            section_name="Define Negotiation Strategy",
        )
        params["suggested_prompts"] = [
            prompt
            for prompt in lst_suggested_prompts
            if (
                prompt["prompt"]
                not in [
                    "Set tone & tactics",
                    (
                        "Set carrots & sticks"
                        if ("carrots" in pinned_elements or "sticks" in pinned_elements)
                        else "Change carrots & sticks"
                    ),
                ]
            )
        ]
    elif generation_type == "negotiation_approach_tnt_change":  # Change tones & tactics
        params["response_type"] = generation_type
        params["message"] = "Based on your selection, here are the updated tones and and tactics "
        params["additional_data"] = {}

        tones_n_tactics_dict = reference_data["negotiation_strategy_tones_n_tactics"].to_dict(
            orient="records",
        )
        unique_titles: list[str] = []
        holder: list[dict[str, Any]] = []
        for row in tones_n_tactics_dict:
            if row["tone_name"] in unique_titles:
                continue
            row_dict: dict[str, Any] = {}
            row_dict["title"] = row["tone_name"]
            row_dict["description"] = row["tone_description"]
            row_dict["prioritize"] = ast.literal_eval(row["prioritize"])
            row_dict["tactics"] = [
                {
                    "title": tactic["tactic"],
                    "description": tactic["description"],
                }
                for tactic in ast.literal_eval(row["tactics"])
            ]
            holder.append(row_dict)
            unique_titles.append(row["tone_name"])
        params["tones"] = holder
        lst_suggested_prompts = get_section_suggested_prompts(
            section_name="Define Negotiation Strategy",
        )
        params["suggested_prompts"] = [
            prompt
            for prompt in lst_suggested_prompts
            if (
                prompt["prompt"]
                not in [
                    "Set tone & tactics",
                    "Change tone & tactics",
                    (
                        "Set carrots & sticks"
                        if ("carrots" in pinned_elements or "sticks" in pinned_elements)
                        else "Change carrots & sticks"
                    ),
                ]
            )
        ]
    return convert_to_response_format(**params)


@log_time
def generate_csb_positioning(
    reference_data: dict[str, Any],
    pg_db_conn: PGConnector,
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
    log.info("Initiating Negotiation Approach %d", len(kwargs))

    # pylint: disable=R0801
    _, supplier_profile = get_supplier_profile(
        pg_db_conn,
        category,
        user_query,
        pinned_elements,
    )
    # handling Set/Change buyer positioning
    if generation_type == "negotiation_approach_bp" or "buyer" in user_query.lower():
        params = {}  # type:ignore
        remove_list: list[str] = []
        suggested_prompts = get_section_suggested_prompts(
            section_name="Create Negotiation Approach",
        )
        remove_list = get_prompts_to_be_removed(
            generation_type=generation_type,
            pinned_elements=pinned_elements,
            user_query=user_query,
        )
        remove_list.extend(
            [
                (
                    f"{'Set' if 'negotiation_strategy' in pinned_elements.keys() else 'Change'}"
                    " sourcing approach"
                ),
                (
                    f"{'Set' if 'tone_and_  stactics' in pinned_elements.keys() else 'Change'}"
                    " tone & tactics"
                ),
                "Change market approach",
                "Change pricing methodology",
                "Change contracting methodology",
            ],
        )
        suggested_prompts = [
            prompt for prompt in suggested_prompts if prompt["prompt"] not in remove_list
        ]
        params["suggested_prompts"] = get_distinct_suggested_prompts(
            prompts=suggested_prompts,
        )
        params["response_type"] = generation_type  # type:ignore
        params[
            "message"
        ] = f"""What is the importance of your company for {
                supplier_profile.get("supplier_name", "this company")
        }?"""  # type:ignore

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
        }  # type:ignore
        return convert_to_response_format(**params)  # type:ignore

    postitioning = get_positioning_data(
        profile=supplier_profile,
        category=category,
        reference_data=reference_data,
        user_query=user_query,
    )

    params = {
        "category_positioning": postitioning["category_positioning"],
        "supplier_positioning": postitioning["supplier_relationship"],
        "market_approach": postitioning["filtered_market"].head(1)["market_approach"].values,
        "pricing_methodology": postitioning["pricing_methodology"],
        "contract_methodology": postitioning["contracting_methodology"],
        "supplier_profile": supplier_profile,
    }

    init_message = (
        f"Let’s align first on our understanding of the "
        f"{'category' if (generation_type == 'negotiation_approach_cp') else 'supplier'} "
        "positioning. Based on our analysis: \n"
    )
    params[
        (
            "supplier_positioning"
            if (generation_type == "negotiation_approach_cp")
            else "category_positioning"
        )
    ] = (
        pinned_elements.get("supplier_positioning", {}).get("value", "")
        if (generation_type == "negotiation_approach_cp")
        else pinned_elements.get("category_positioning", {}).get("value", "")
    )
    prompt = negotiation_set_positioning_prompt(**params)
    response_keys = [
        (
            "category_positioning"
            if generation_type == "negotiation_approach_cp"
            else "supplier_positioning"
        ),
        (
            "category_positioning_detail"
            if generation_type == "negotiation_approach_cp"
            else "supplier_positioning_detail"
        ),
        "message",
        "suggested_prompts",
    ]

    # pylint: disable=R0801
    response = run_conversation_chat(
        chat_history,
        prompt,
        user_query,
        model=negotiation_conf["model"]["model_name"],
        temperature = 0.3,
        window_size=negotiation_conf["model"]["conversation_buffer_window"],
    )

    log.info("Response from negotiation approach conversation chain: %s", response)

    ai_response = get_airesponse_as_dict(
        response=response,
        response_keys=response_keys,
    )
    params = process_approach_response_key_content(
        supplier_profile=supplier_profile,
        ai_response=ai_response,
        init_message=init_message,
        generation_type=generation_type,
        pinned_elements=pinned_elements,
    )  # type:ignore
    return convert_to_response_format(**params)  # type:ignore


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
    suggested_prompts = get_section_suggested_prompts(
        section_name="Select Negotiation Objectives",
    )
    remove_list = []
    all_pinned_elemnts = list(pinned_elements.keys())

    # if Negotiation objective/Category positioning/Supplier positioning/Buyer positioning
    # Sourcing approach is pinned
    if user_query.startswith("Change ") and "objectives" in user_query:
        remove_list.append("Change negotiation objectives")
        remove_list.append("Set negotiation objectives")
    elif user_query.startswith("Set ") and "objectives" in user_query:
        remove_list.append("Set negotiation objectives")
    remove_list.append(
        f"{'Set' if 'category_positioning' in all_pinned_elemnts else 'Change'}"
        " category positioning",
    )
    remove_list.append(
        f"{'Set' if 'supplier_positioning' in all_pinned_elemnts else 'Change'}"
        " supplier positioning",
    )
    remove_list.append(
        f"{'Set' if 'buyer_positioning' in all_pinned_elemnts else 'Change'}" " buyer positioning",
    )
    remove_list.append(
        f"{'Set' if 'negotiation_strategy' in all_pinned_elemnts else 'Change'}"
        " sourcing approach",
    )
    suggested_prompts = [
        prompt for prompt in suggested_prompts if (prompt["prompt"] not in remove_list)
    ]
    return suggested_prompts
