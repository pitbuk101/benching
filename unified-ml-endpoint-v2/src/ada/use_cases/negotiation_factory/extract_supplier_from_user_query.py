"""Module to get supplier data based on user request"""

from __future__ import annotations

import json
import re
from typing import Any, List

import numpy
import pandas as pd

from ada.components.db.pg_connector import PGConnector
from ada.components.db.sf_connector import SnowflakeClient
from ada.use_cases.negotiation_factory.exception import (
    NegotiationFactoryException,
    NegotiationFactoryQueryException,
    NegotiationFactoryUserException,
)
from ada.use_cases.negotiation_factory.negotiation_factory_utils import (
    convert_to_response_format,
    enrich_supplier_profile,
    get_section_suggested_prompts,
    weighted_average,
)
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time
from ada.utils.metrics.similarity import get_best_match_from_list
from ada.use_cases.negotiation_factory.prompts import str_match_prompt
from ada.components.llm_models.generic_calls import generate_chat_response_with_chain
negotiation_conf = read_config("use-cases.yml")["negotiation_factory"]
negotiation_tables = negotiation_conf["tables"]

log = get_logger("extract_supplier_from_user_query")
from datetime import date
from ada.components.db.sf_connector import SnowflakeClient

def get_supplier_data(  # pylint: disable=too-many-branches
    pg_db_conn: PGConnector,
    sf_client:SnowflakeClient,
    category: str,
    script_type: str,
    value=None,
) -> tuple[pd.DataFrame, str]:
    
    """
    Get supplier data based on the script type and category.

    Args:
        pg_db_conn (PGConnector): The PostgreSQL database connection object.
        category (str): The category name to filter suppliers by.
        script_type (str): The type of script to determine which data to fetch.
                           Valid values are "top_supplier", "top_suppliers_tail_spend",
                           "largest_gap", "spend_without_po", and "highest_single_spend".
        value (int, optional): The number of top suppliers to fetch. Default is None.

    Returns:
        tuple[pd.DataFrame, str]: A tuple containing:
                                  - A DataFrame with the supplier data.
                                  - A string message summarizing the data.

    Raises:
        NegotiationFactoryUserException: If the script_type is not valid.
        NegotiationFactoryQueryException: If the supplier data for the given category is not found.
    """
    if script_type == "top_supplier":
        supplier_data = pd.DataFrame(
            sf_client.select_records_with_filter(
                table_name=negotiation_tables["supplier_details"],

                filtered_columns=[
                    "SUPPLIER as supplier_name",
                    "AVG(spend_ytd) as spend",
                    "MAX(CURRENCY_SYMBOL) AS CURRENCY_SYMBOL",
                    (
                        "(ROUND(AVG(PERCENTAGE_SPEND_ACROSS_CATEGORY_YTD),2)) AS PERCENTAGE_SPEND_CONTRIBUTION"
                    ),
                ],
                filter_condition=(
                    f"LOWER(category) = LOWER('{category}') AND YEAR = (SELECT MAX(YEAR) "
                    f"""FROM {negotiation_tables["supplier_details"]})"""

                ),
                group_by=["supplier_name"],
                order_by=("avg(spend_ytd)", "desc"),
                num_records=value,
            ),
        )
        
        supplier_data.columns = supplier_data.columns.str.lower()
        supplier_data["currency_symbol"].fillna(" ", inplace=True)
        supplier_data["percentage_spend_contribution"] = supplier_data["percentage_spend_contribution"].astype(float)

    elif script_type == "top_suppliers_tail_spend":
        supplier_data = pd.DataFrame(
            sf_client.get_tail_spend_supplier_data(
                table_name=negotiation_tables["supplier_details"],
                category=category,
                tail_threshold=negotiation_conf["tail_spend_threshold"],
                num_records=value,
            ),
        )
        supplier_data.columns = supplier_data.columns.str.lower()
    elif script_type == "largest_gap": #migrated to sf
        supplier_data = pd.DataFrame(
            sf_client.select_records_with_filter(
                table_name=negotiation_tables["supplier_details"],
                filtered_columns=[
                    "SUPPLIER as supplier_name",
                    "AVG(spend_ytd) as spend",
                    "MAX(CURRENCY_SYMBOL) AS CURRENCY_SYMBOL",
                    "AVG(percentage_spend_across_category_ytd) as percentage_spend_contribution",
                    "AVG(percentage_spend_across_category_ytd - percentage_spend_across_category_last_year) as percentage_change_in_spend",
                ],
                filter_condition=(
                    f"LOWER(category) = LOWER('{category}') AND YEAR = (SELECT MAX(YEAR) "
                    f"""FROM {negotiation_tables["supplier_details"]})"""
                ),
                group_by=["SUPPLIER"],
                order_by=("percentage_change_in_spend", "desc"),
                num_records=value,
            ),
        )
        supplier_data.columns = supplier_data.columns.str.lower()
        supplier_data["currency_symbol"].fillna(" ", inplace=True)

    elif script_type == "spend_without_po":  #migrated to sf
        supplier_data = pd.DataFrame(
            sf_client.select_records_with_filter(
                table_name=negotiation_tables["supplier_details"],
                filtered_columns=[
                    "SUPPLIER as supplier_name",
                    "SUM(spend_no_po_ytd) as spend_no_po_ytd",
                    "SUM(spend_ytd) as spend",
                    "MAX(CURRENCY_SYMBOL) AS CURRENCY_SYMBOL",
                    # "CASE WHEN SUM(spend_ytd) = 0 THEN NULL ELSE SUM(spend_no_po_ytd) * 100.0 / NULLIF(SUM(spend_ytd), 0) END AS percentage_spend_without_po",
                ],
                filter_condition=(
                    f"LOWER(category) = LOWER('{category}') AND YEAR = (SELECT MAX(YEAR) "
                    f"""FROM {negotiation_tables["supplier_details"]})"""
                ),
                group_by=["SUPPLIER"],
                order_by=("spend_no_po_ytd", "desc"),
                num_records=value,
            ),
        )
        supplier_data.columns = supplier_data.columns.str.lower()
        supplier_data["currency_symbol"].fillna(" ", inplace=True)
        
        records_from_db = sf_client.select_records_with_filter(
            table_name=negotiation_tables["supplier_details"],
            filtered_columns=["SUM(spend_no_po_ytd) AS total_spend_no_po_ytd"],
            filter_condition=(
                f"LOWER(category) = LOWER('{category}') AND YEAR = (SELECT MAX(YEAR) "
                f"""FROM {negotiation_tables["supplier_details"]})"""
            ),
        )

        records_from_db.columns = records_from_db.columns.str.lower()
        total_spend_without_po = (dict(records_from_db) or {}).get("total_spend_no_po_ytd", 0)
        total_spend_without_po = int(total_spend_without_po.iloc[0])
        log.info(
            "total_spend_without_po: %s, type: %s",
            total_spend_without_po,
            type(total_spend_without_po),
        )
        percentage_contribution = (
            supplier_data.spend_no_po_ytd.sum() * 100 / total_spend_without_po
            if total_spend_without_po != 0
            else 0.0
        )
        message = (
            f"The top {value} supplier contributes to {percentage_contribution:.1f}% total spend "
            f"without PO and see below the spend break up:"
        )
    elif script_type == "highest_single_spend": #migrated to sf

        supplier_data = pd.DataFrame(
            sf_client.select_records_with_filter(
                table_name= negotiation_tables["supplier_details"],
                filtered_columns=[
                    "SUPPLIER as supplier_name",
                    "AVG(spend_ytd) as spend",
                    "AVG(single_source_spend_ytd) as single_source_spend",
                    "MAX(CURRENCY_SYMBOL) AS CURRENCY_SYMBOL",
                    # "CASE WHEN SUM(spend_ytd) = 0 THEN NULL ELSE SUM(single_source_spend_ytd) * 100.0 / NULLIF(SUM(spend_ytd), 0) END AS percentage_spend_single_source_spend",
                ],
                filter_condition=(
                    f"LOWER(category) = LOWER('{category}') AND YEAR =(SELECT MAX(YEAR) "
                    f"""FROM {negotiation_tables["supplier_details"]})"""
                ),
                group_by=["SUPPLIER"],
                order_by=("single_source_spend", "desc"),
                num_records=value,
            ),
        )
        supplier_data.columns = supplier_data.columns.str.lower()
        supplier_data["currency_symbol"].fillna(" ", inplace=True)

        records_from_db = sf_client.select_records_with_filter(
            table_name=negotiation_tables["supplier_details"],
            filtered_columns=["SUM(single_source_spend_ytd) AS total_single_source_spend"],
            filter_condition=(
                f"LOWER(category) = LOWER('{category}') AND YEAR = (SELECT MAX(YEAR) "
                f"""FROM {negotiation_tables["supplier_details"]})"""
            ),
        )
        records_from_db.columns = records_from_db.columns.str.lower()
        total_single_source_spend = (dict(records_from_db) or {}).get(
            "total_single_source_spend",
            0,
        )
        total_single_source_spend = int(total_single_source_spend.iloc[0])

        percentage_contribution = (
            supplier_data.single_source_spend.sum() * 100 / total_single_source_spend
            if total_single_source_spend != 0
            else 0.0
        )
        message = (
            f"The top {value} supplier contributes to {percentage_contribution:.1f}% total single"
            f" source spend and see below the spend break up:"
        )
    else:
        raise NegotiationFactoryUserException(
            "Not valid user request with request type negotiation_init",
        )
    if supplier_data.empty:
        space = " "
        raise NegotiationFactoryQueryException(
            f"Requested supplier data not found for category: {category}.{space}"
            f"Please select another category.",
        )

    log.info("supplier data: %s", supplier_data)   
    supplier_data["currency_symbol"] = supplier_data["currency_symbol"].apply(
        lambda x: negotiation_conf["currency_map"].get(x[0], " "),
    )

    supplier_data_columns = supplier_data.columns.tolist()
    percentage_columns = [
        "percentage_spend_contribution",
        "percentage_change_in_spend",
        "percentage_spend_without_po",
        "percentage_spend_single_source_spend",
    ]
    
    for column in percentage_columns:
        if column in supplier_data_columns:
            if supplier_data[column].sum() > 105:
                supplier_data[column] = supplier_data[column] / 100
    supplier_data["currency_position"] = negotiation_conf["currency_position"]

    if script_type in ("top_supplier", "top_suppliers_tail_spend", "largest_gap"):
        message = (
            f"The top {value} supplier contributes to "
            f"{supplier_data.percentage_spend_contribution.sum():.1f}% total spend "
            f"and see below the spend break up:"
        )
    return supplier_data, message


def get_supplier_data_based_on_user_query(
    pg_db_conn: PGConnector,
    sf_client: SnowflakeClient,
    category: str,
    user_query: str,
) -> tuple[pd.DataFrame, str]:
    """
    Recognize script type from user query and get supplier data.

    Args:
        pg_db_conn (PGConnector): The PostgreSQL database connection object.
        category (str): The category name to filter suppliers by.
        user_query (str): The user query string to determine the script type.

    Returns:
        tuple[pd.DataFrame, str]: A tuple containing:
                                  - A DataFrame with the supplier data.
                                  - A string message summarizing the data.

    Raises:
        NegotiationFactoryQueryException: If the user query does not match any known pattern.
    """
    cta_values = {
        "Top `n` suppliers by spend": "top_supplier",
        "`n` Tail suppliers": "top_suppliers_tail_spend",
        "`n` Single source suppliers": "highest_single_spend",
        "`n` suppliers with missing PO": "spend_without_po",
        "`n` suppliers with largest YoY spend evolution": "largest_gap",
    }
    patterns = {
        "top_suppliers_tail_spend": r"(\d+)? ?tail (supplier|vendor)s",
        "largest_gap": r"(\d+)? ?(supplier|vendor)s with largest YOY spend evolution",
        "spend_without_po": r"(\d+)? ?(supplier|vendor)s with missing PO spend",
        "highest_single_spend": r"(\d+)? ?single source (supplier|vendor)s",
        "top_supplier": r"top (\d*)\s?(supplier|vendor)s by spend",
    }

    prompt = str_match_prompt(user_query)
    ai_response = generate_chat_response_with_chain(prompt)
    try:
        result = json.loads(f'{{{ai_response}}}')
    except json.JSONDecodeError as e:
        log.error("Failed to parse AI response as JSON: %s", ai_response)
        raise NegotiationFactoryQueryException("Please try again") from e

    if result:
        # value = (match.group(1) if match.groups() else None) or "5"
        log.info("matched pattern for user query: %s", result['pattern_key'])
        log.info("matched value for user query: %s", result['value'])
        return get_supplier_data(pg_db_conn,sf_client, category, result['pattern_key'], result['value'])
    # match_str: str = get_best_match_from_list(
    #     list(cta_values),
    #     user_query,
    #     threshold=negotiation_conf["cta_similarity_threshold"],
    #     similarity_model=negotiation_conf["model"]["similarity_model"],
    # )
    # log.info("matched pattern for loop 2 user query: %s", match_str)
    # if match_str:
    #     value = re.findall(r"\d+", user_query)
    #     value = str(next(iter(value))) if value else "5"
    #     log.info("matched value for user query: %s", value)
    #     script_type_str = cta_values[match_str]
    #     return get_supplier_data(pg_db_conn, category, script_type_str, value)
    raise NegotiationFactoryQueryException("request not supported as of now")


def get_supplier_profiles(
    pg_db_conn: PGConnector,
    sf_client: SnowflakeClient,
    category: str,
    supplier_names: numpy.ndarray,
) -> pd.DataFrame:
    """
    Get supplier profiles for given supplier names.

    Args:
        pg_db_conn (PGConnector): The PostgreSQL database connection object.
        category (str): The category name to filter suppliers by.
        supplier_names (numpy.ndarray): An array of supplier names to retrieve profiles for.

    Returns:
        pd.DataFrame: A DataFrame containing the enriched supplier profiles.
    """
    all_supplier_data = pd.DataFrame(
        sf_client.select_records_with_filter(
            table_name=negotiation_tables["supplier_details"],
            filter_condition=(
                f"""LOWER(category) = LOWER('{category}') AND  YEAR = (SELECT MAX(YEAR)  """
                f"""FROM {negotiation_tables["supplier_details"]}) AND """
                f"""{sf_client.get_condition_string(("SUPPLIER",
                              "in", list(supplier_names)))}"""
            ),
        ),
    )
    all_supplier_data = all_supplier_data.drop_duplicates(subset=["SUPPLIER"], keep="first")
    remane_map = {"supplier": "supplier_name",
                "category": "category_name",
                "year": "period"}
                # "earlyPayment": "early payments"}
    all_supplier_data.columns = all_supplier_data.columns.str.lower()
    for key, value in remane_map.items():
        all_supplier_data.rename(columns={key: value}, inplace=True)

    all_supplier_data.sort_values(
        by=["spend_ytd"],
        ascending=False,
        inplace=True,
    )
    supplier_names = all_supplier_data["supplier_name"].unique().tolist()
    all_supplier_data_modified = pd.DataFrame(
        [
            enrich_supplier_profile(
                pd.DataFrame(all_supplier_data.loc[all_supplier_data["supplier_name"] == supplier]),
            )
            for supplier in supplier_names
        ],
    )
    all_supplier_data_modified.drop(
        ["insights", "objectives"],
        axis=1,
        errors="ignore",
        inplace=True,
    )

    return all_supplier_data_modified


def negotiation_init(
    pg_db_conn: PGConnector,
    sf_client: SnowflakeClient,
    category: str,
    user_query: str,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Performs negotiation init function
    Args:
        pg_db_conn (PGConnector) : connection to Postgres database
        category (str): user selected category
        user_query (str): User question with key instructions.
        pinned_elements (dict[str, Any]): Pinned elements including supplier profile
        kwargs (Any): Additional arguments
    Return:
        (dict[str, Any]): Response with the supplier profiles and sorted data
    Raises:
        NegotiationFactoryUserException: If the script_type is not valid.
        NegotiationFactoryQueryException: If the supplier data for the given category
          is not found.
    """
    log.info("additional data %d", len(kwargs))
    supplier_data, message = get_supplier_data_based_on_user_query(pg_db_conn,sf_client, category, user_query)
    suppliers_profiles = get_supplier_profiles(
        pg_db_conn,
        sf_client,
        category,
        supplier_data.supplier_name.values,
    )

    

    ctas = {
        "prompt": negotiation_conf["cta_button_map"]["select_skus"],
        "intent": "negotiation_select_skus",
    }

    params = {
        "response_type": "supplier_details",
        "message": message,
        "suppliers_profiles": json.loads(
            suppliers_profiles.to_json(orient="records", double_precision=1),
        ),
        "additional_data": {
            "suppliers_data": json.loads(
                supplier_data.to_json(orient="records", double_precision=1),
            ),
            "follow_up_prompt": ctas,
            "welcome_message": "Thank you for selecting SUPLLIER_NAME. Here are few"
            " probable next steps:",
        },
    }
    return convert_to_response_format(**params)


@log_time
def generate_scoping(
    pg_db_conn: PGConnector,
    sf_client: SnowflakeClient,
    category: str,
    pinned_elements: dict[str, Any],
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Generate scoping for the supplier
    Args:
        pg_db_conn (PGConnector) : Connection object to postgres database
        category (str): user selected category
        pinned_elements (dict[str, Any]): elements pinned by the user
        kwargs (Any): Any additional arguments
    Returns:
        (dict[str, Any]: Return scoping for the suppliers
    Raises:
        NegotiationFactoryUserException: If supplier name not present in user query
                                         or supplier data is not present for the category
    """
    current_date = date.today()
    log.info("Initiating Scoping %d", len(kwargs))
    supplier_name = pinned_elements.get("supplier_profile", {}).get("supplier_name", "")
    table_name = negotiation_conf["tables"]["sku_details"]
    supplier_name = supplier_name.replace("'", "''") 
    filter_string = (
        f"""category_name = '{category}' AND """
        f"""period = {current_date.year} """
        f""" AND supplier_name  = '{supplier_name}'"""
    )
    sku_data = sf_client.select_records_with_filter(
        table_name=table_name,
        filtered_columns=[
            "sku_id",
            "sku_name",
            "unit_price",
            "quantity",
            "unit_of_measurement",
            "spend_ytd",
        ],
        order_by=("spend_ytd", "DESC"),
        filter_condition=filter_string,
    )
   
    if sku_data.empty:
        raise NegotiationFactoryUserException(f"No sku data found for the supplier {supplier_name}")
    
    sku_data_df = pd.DataFrame(sku_data)
    sku_data_df.columns = sku_data_df.columns.str.lower()
    sku_data_df = (
        sku_data_df.groupby(["sku_id", "sku_name"])
        .agg(
            {
                "quantity": "sum",
                "spend_ytd": "sum",
                "unit_price": lambda x: weighted_average(
                    sku_data_df.loc[x.index],
                    term="unit_price",
                    average_term="quantity",
                ),
                "unit_of_measurement": lambda x: (
                    x[x != ""].value_counts().index[0] if ((x != "") & (x.notnull())).any() else ""
                ),
            },
        )
        .reset_index()
    )
    rename_list = {
        "sku_id": "id",
        "sku_name": "name",
        "unit_of_measurement": "uom",
        "spend_ytd": "spend",
    }
    sku_data_df.rename(columns=rename_list, inplace=True)
    sku_data_df.sort_values(by="spend", ascending=False, inplace=True)

    if "insights" in pinned_elements:
        pinned_elements.pop("insights")

    suggested_prompts = [
        {
            "prompt": "Learn more about supplier",
            "intent": "negotiation_user_questions",
        },
        {
            "prompt": negotiation_conf["cta_button_map"]["objective"],
            "intent": "negotiation_objective",
        },
    ]

    params = {
        "message": (
            f"Select the SKUs from {supplier_name} that you want to consider in the " "negotiation"
        ),
        "response_type": "sku_details",
        "skus": sku_data_df.to_dict(orient="records"),
        "suggested_prompts": suggested_prompts,
    }
    return convert_to_response_format(**params)


@log_time
def generate_carrots_and_sticks(
    pinned_elements: dict[str, Any],
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Generate carrots and sticks for the supplier
    Args:
        pinned_elements (dict[str, Any]): elements pinned by the user
        user_query (str): User question with key instructions.
        kwargs (Any): Any additional arguments
    Returns:
        (dict[str, Any]: Return scoping for the suppliers
    Raises:
        NegotiationFactoryUserException: If supplier name not present in user query
                                         or supplier data is not present for the category
    """
    log.info("Initiating Scoping %d", len(kwargs))
    reference_carrots_sticks = kwargs.get("reference_data", {}).get("carrots_and_sticks")

    if reference_carrots_sticks is None or len(reference_carrots_sticks) == 0:
        raise NegotiationFactoryUserException("No carrots and sticks found")

    carrots = reference_carrots_sticks[reference_carrots_sticks["type"] == "carrot"]
    sticks = reference_carrots_sticks[reference_carrots_sticks["type"] == "stick"]
    carrots.drop("type", axis=1, inplace=True)
    sticks.drop("type", axis=1, inplace=True)

    suggested_prompts = get_section_suggested_prompts(
        section_name="Define Negotiation Strategy",
    )

    remove_prompts = [
        "Set tone & tactics" if "tone_and_tactics" in pinned_elements else "Change tone & tactics",
        "Set carrots & sticks",
        "Change carrots & sticks",
    ]

    suggested_prompts = [
        prompt for prompt in suggested_prompts if prompt["prompt"] not in remove_prompts
    ]

    params = {
        "message": (
            "These are the most common carrots and sticks used in negotiations. "
            "You can also create your own or add custom options to select from."
        ),
        "response_type": "carrots_sticks",
        "carrots": carrots.to_dict(orient="records"),
        "sticks": sticks.to_dict(orient="records"),
        "suggested_prompts": suggested_prompts,
    }
    return convert_to_response_format(**params)
