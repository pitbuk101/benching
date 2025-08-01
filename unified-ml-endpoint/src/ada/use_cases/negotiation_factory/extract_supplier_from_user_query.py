"""Module to get supplier data based on user request"""

from __future__ import annotations

import json
import re
from typing import Any, List

import numpy
import pandas as pd
from datetime import datetime
from datetime import date

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

@log_time
def extract_year_from_user_query(user_query: str) -> int:
    """
    Extract the year from the user query.

    Args:
        user_query (str): The user query string.

    Returns:
        int: The extracted year, or the current year if not found.
    """
    log.info("Extracting year from user query")
    match = re.search(r"\b\d{4}\b", user_query)
    if match:
        year = int(match.group(0))
        log.info("Extracted year: %d", year)
        return year
    log.warning("No year found in user query, using current year")
    return None

@log_time
def get_supplier_data(  # pylint: disable=too-many-branches
    pg_db_conn: PGConnector,
    sf_client: SnowflakeClient,
    category: str,
    script_type: str,
    value=None,
    user_query: str = None,
) -> tuple[pd.DataFrame, str]:
    """
    Get supplier data based on the script type and category.
    """
    log.info("Fetching supplier data: category='%s', script_type='%s', value='%s'", category, script_type, value)

    supplier_data = pd.DataFrame()
    message = ""
    year_message = ""
    percentage_contribution = 0.0
    current_year = datetime.now().year

    if user_query is not None:
        year = extract_year_from_user_query(user_query)
        if year:
            year_message = (
                f"\nPlease note, negotiation is based on the most recent data available from {year} YTD."
                if year == current_year
                else f"\nPlease note, negotiation is based on data available from {year}."
            )

    if script_type == "top_supplier" or script_type == "top_suppliers_tail_spend":
        order = "desc" if script_type == "top_supplier" else "asc"
        supplier_data = pd.DataFrame(
            sf_client.select_records_with_filter(
                table_name=negotiation_tables["supplier_details"],
                filtered_columns=[
                    "SUPPLIER as supplier_name",
                    "YEAR",
                    "SUM(spend_ytd) as spend",
                    "MAX(CURRENCY_SYMBOL) AS CURRENCY_SYMBOL",
                    "(ROUND(SUM(PERCENTAGE_SPEND_ACROSS_CATEGORY_YTD),2)) AS PERCENTAGE_SPEND_CONTRIBUTION",
                ],
                filter_condition=(
                    f"LOWER(category) = LOWER('{category}') AND NUMBER_OF_SKU>=1 AND YEAR = (SELECT MAX(YEAR) "
                    f"FROM {negotiation_tables['supplier_details']})"
                ),
                group_by=["supplier_name", "YEAR"],
                order_by=("sum(spend_ytd)", order),
                num_records=value,
            )
        )
        supplier_data.columns = supplier_data.columns.str.lower()
        supplier_data["currency_symbol"].fillna(" ", inplace=True)
        supplier_data["percentage_spend_contribution"] = supplier_data["percentage_spend_contribution"].astype(float)
        valid_suppliers_df = sf_client.fetch_dataframe("""
            SELECT DISTINCT SUPPLIER_NAME AS supplier_name
            FROM Data.T_C_NEGOTIATION_FACTORY_T2
            WHERE SKU_ID != '-1'
        """)
        valid_suppliers_df.columns = valid_suppliers_df.columns.str.lower()
        
        if not valid_suppliers_df.empty:
            supplier_data = supplier_data[supplier_data["supplier_name"].isin(valid_suppliers_df["supplier_name"])]
        else:
            supplier_data = pd.DataFrame()

    elif script_type == "top_supplier_by_opportunity":

        query = """
            SELECT DIM_CURRENCY_DOCUMENT AS currency, TXT_CURRENCY_SYMBOL AS currency_symbol
            FROM data.T_DIM_CURRENCY_SYMBOLS
            WHERE DIM_CURRENCY_DOCUMENT = (
                SELECT TXT_REPORTING_CURRENCY
                FROM data.VT_DIM_REPORTINGCURRENCY
                WHERE NUM_ORDER = 1
            )
            LIMIT 1;
        """
        result = sf_client.execute_query(query)
        currency_symbol = result[0][1] if result else None
        log.info("Fetched currency symbol: %s", currency_symbol)
    
        supplier_data = sf_client.fetch_dataframe(f"""
        WITH TOTAL_OPP AS (
            SELECT YEAR, CATEGORY, SUPPLIER, SUM(KPI_VALUE) AS SUPPLIER_OPPORTUNITY  FROM {negotiation_tables['supplier_opportunity']}
            WHERE CATEGORY = '{category}'
            AND YEAR = (SELECT MAX(YEAR) FROM {negotiation_tables['supplier_opportunity']})
            AND KPI_NAME = 'Total saving opportunity'
            GROUP BY YEAR, CATEGORY, SUPPLIER
        ),
        SPEND_DATA AS (
            SELECT YEAR, CATEGORY, SUM(KPI_VALUE) AS TOTAL_OPPORTUNITY  FROM {negotiation_tables['supplier_opportunity']}
            WHERE CATEGORY = '{category}'
            AND YEAR = (SELECT MAX(YEAR) FROM {negotiation_tables['supplier_opportunity']})
            AND KPI_NAME = 'Total saving opportunity'
            GROUP BY YEAR, CATEGORY
        )
        SELECT SD.YEAR, SD.CATEGORY, TOPP.SUPPLIER, SD.TOTAL_OPPORTUNITY, COALESCE(TOPP.SUPPLIER_OPPORTUNITY,0) AS SUPPLIER_OPPORTUNITY, CASE WHEN SD.TOTAL_OPPORTUNITY > 0 THEN (TOPP.SUPPLIER_OPPORTUNITY/SD.TOTAL_OPPORTUNITY)*100 ELSE 0 END AS TOTAL_OPPORTUNITY_PERCENTAGE
        FROM SPEND_DATA SD
        LEFT JOIN TOTAL_OPP TOPP ON SD.YEAR = TOPP.YEAR AND SD.CATEGORY = TOPP.CATEGORY 
        ORDER BY TOTAL_OPPORTUNITY_PERCENTAGE DESC
        LIMIT {value}                                                                  
        """)
        supplier_data['currency_symbol'] = currency_symbol
        supplier_data.columns = supplier_data.columns.str.lower()

    elif script_type == "largest_gap":
        supplier_data = pd.DataFrame(
            sf_client.select_records_with_filter(
                table_name=negotiation_tables["supplier_details"],
                filtered_columns=[
                    "SUPPLIER as supplier_name",
                    "SUM(spend_ytd) as spend",
                    "MAX(CURRENCY_SYMBOL) AS CURRENCY_SYMBOL",
                    "SUM(percentage_spend_across_category_ytd) as percentage_spend_contribution",
                    "SUM(percentage_spend_across_category_ytd - percentage_spend_across_category_last_year) as percentage_change_in_spend",
                ],
                filter_condition=(
                    f"LOWER(category) = LOWER('{category}') AND YEAR = (SELECT MAX(YEAR) FROM {negotiation_tables['supplier_details']})"
                ),
                group_by=["SUPPLIER"],
                order_by=("percentage_change_in_spend", "desc"),
                num_records=value,
            )
        )
        supplier_data.columns = supplier_data.columns.str.lower()
        supplier_data["currency_symbol"].fillna(" ", inplace=True)

    elif script_type == "spend_without_po":
        supplier_data = pd.DataFrame(
            sf_client.select_records_with_filter(
                table_name=negotiation_tables["supplier_details"],
                filtered_columns=[
                    "SUPPLIER as supplier_name",
                    "SUM(spend_no_po_ytd) as spend_no_po_ytd",
                    "SUM(spend_ytd) as spend",
                    "MAX(CURRENCY_SYMBOL) AS CURRENCY_SYMBOL",
                    "CASE WHEN SUM(spend_ytd) = 0 THEN NULL ELSE SUM(spend_no_po_ytd) * 100.0 / NULLIF(SUM(spend_ytd), 0) END AS percentage_spend_without_po",
                ],
                filter_condition=(
                    f"LOWER(category) = LOWER('{category}') AND YEAR = (SELECT MAX(YEAR) FROM {negotiation_tables['supplier_details']})"
                ),
                group_by=["SUPPLIER"],
                order_by=("spend_no_po_ytd", "desc"),
                num_records=value,
            )
        )
        supplier_data.columns = supplier_data.columns.str.lower()
        supplier_data["currency_symbol"].fillna(" ", inplace=True)
        total_spend = sf_client.select_records_with_filter(
            table_name=negotiation_tables["supplier_details"],
            filtered_columns=["SUM(spend_no_po_ytd) AS total_spend_no_po_ytd"],
            filter_condition=(
                f"LOWER(category) = LOWER('{category}') AND YEAR = (SELECT MAX(YEAR) FROM {negotiation_tables['supplier_details']})"
            ),
        )
        total_spend.columns = total_spend.columns.str.lower()
        total = int(total_spend.iloc[0][0]) if not total_spend.empty else 0
        percentage_contribution = supplier_data.spend_no_po_ytd.sum() * 100 / total if total else 0.0

    elif script_type == "highest_single_spend":
        supplier_data = pd.DataFrame(
            sf_client.select_records_with_filter(
                table_name=negotiation_tables["supplier_details"],
                filtered_columns=[
                    "SUPPLIER as supplier_name",
                    "YEAR",
                    "SUM(spend_ytd) as spend",
                    "SUM(single_source_spend_ytd) as single_source_spend",
                    "MAX(CURRENCY_SYMBOL) AS CURRENCY_SYMBOL",
                ],
                filter_condition=(
                    f"LOWER(category) = LOWER('{category}') AND YEAR =(SELECT MAX(YEAR) FROM {negotiation_tables['supplier_details']})"
                ),
                group_by=["SUPPLIER", "YEAR"],
                order_by=("single_source_spend", "desc"),
                num_records=value,
            )
        )
        supplier_data.columns = supplier_data.columns.str.lower()
        supplier_data["currency_symbol"].fillna(" ", inplace=True)
        total_ss = sf_client.select_records_with_filter(
            table_name=negotiation_tables["supplier_details"],
            filtered_columns=["SUM(single_source_spend_ytd) AS total_single_source_spend"],
            filter_condition=(
                f"LOWER(category) = LOWER('{category}') AND YEAR = (SELECT MAX(YEAR) FROM {negotiation_tables['supplier_details']})"
            ),
        )
        total_ss.columns = total_ss.columns.str.lower()
        total = int(total_ss.iloc[0][0]) if not total_ss.empty else 0
        percentage_contribution = supplier_data.single_source_spend.sum() * 100 / total if total else 0.0

    else:
        log.error("Invalid script_type received: %s", script_type)
        raise NegotiationFactoryUserException("Not valid user request with request type negotiation_init")

    if supplier_data.empty:
        raise NegotiationFactoryQueryException(f"Requested supplier data not found for category: {category}. Please select another category.")

    log.info("Normalizing currency values and applying configuration mappings")
    supplier_data["currency_position"] = negotiation_conf["currency_position"]

    for col in [
        "percentage_spend_contribution",
        "percentage_change_in_spend",
        "percentage_spend_without_po",
        "percentage_spend_single_source_spend",
    ]:
        if col in supplier_data.columns:
            supplier_data[col] = supplier_data[col].round(2)
            if supplier_data[col].sum() > 110:
                log.warning("High %% total in column %s (%.2f). Normalizing by dividing by 100.", col, supplier_data[col].sum())
                supplier_data[col] /= 100

    year = supplier_data.year.max() if "year" in supplier_data.columns else current_year
    ytd_label = f"{year} YTD" if year == current_year else str(year)

    if script_type == "top_supplier":
        total = supplier_data["percentage_spend_contribution"].sum()
        if total < 0.1:
            message = f"Here are the top {value} suppliers, accounting for {total:.2f}% of {ytd_label} spend in the {category} category. {year_message}"
        else:
            message = f"Here are the top {value} suppliers, accounting for {total:.2f}% of {ytd_label} spend in the {category} category. See below the spend breakdown. {year_message}"

    elif script_type == "top_supplier_by_opportunity":
        total = supplier_data["total_opportunity_percentage"].sum()
        if total < 0.1:
            message = f"Here are the top {value} suppliers by opportunity, accounting for {round(supplier_data['total_opportunity'].sum(), 2)} in total opportunity in {ytd_label}. {year_message}"
        else:
            message = f"Here are the top {value} suppliers by opportunity, contributing to {total:.2f}% of total opportunity in {ytd_label}. See below the spend breakdown. {year_message}"

    elif script_type == "largest_gap":
        total = supplier_data["percentage_spend_contribution"].sum()
        if total < 0.1:
            message = f"Here are the {value} suppliers with the largest year-on-year gap in spend, accounting for €{round(supplier_data['spend'].sum(), 2)} in total spend in {ytd_label}. {year_message}"
        else:
            message = f"Here are the top {value} suppliers with the largest year-on-year gap in spend, contributing to {total:.2f}% of total spend in {ytd_label}. See below the spend breakdown. {year_message}"

    elif script_type == "top_suppliers_tail_spend":
        total = supplier_data["percentage_spend_contribution"].sum()
        if total < 0.1:
            message = f"Here are the tail {value} suppliers based on total spend in {ytd_label}. {year_message}"
        else:
            message = f"Here are the tail {value} suppliers, contributing to {total:.2f}% of total spend in {ytd_label}. See below the spend breakdown. {year_message}"

    elif script_type == "spend_without_po":
        if percentage_contribution < 0.01:
            message = f"The {value} suppliers without purchase orders are listed below. The total spend by these suppliers is €{round(supplier_data['spend'].sum(), 2)}."
        else:
            message = f"The {value} suppliers account for {percentage_contribution:.2f}% of total spend without a purchase order. See the breakdown below."

    elif script_type == "highest_single_spend":
        if percentage_contribution == 0:
            message = f"The {value} suppliers identified as single-source suppliers currently have no recorded single-source spend in {ytd_label} for the {category} category. See the breakdown below:"
        elif percentage_contribution < 0.1:
            message = f"Here are the top {value} single-source suppliers, accounting for just {percentage_contribution:.2f}% of {ytd_label} spend in the {category} category. See the breakdown below:"
        else:
            message = f"Here are the top {value} single-source suppliers, accounting for {percentage_contribution:.2f}% of {ytd_label} spend in the {category} category. See the breakdown below:"
    
    return supplier_data, message


@log_time
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
    log.info("Processing user query to detect supplier data request pattern")
    log.debug("Category: %s | User query: %s", category, user_query)

    cta_values = {
        "Top `n` suppliers by spend": "top_supplier",
        "`n` Tail suppliers": "top_suppliers_tail_spend",
        "`n` Single source suppliers": "highest_single_spend",
        "`n` suppliers with missing PO": "spend_without_po",
        "`n` suppliers with largest YoY spend evolution": "largest_gap",
        "Top `n` suppliers by opportunity": "top_supplier_by_opportunity"
    }

    patterns = {
        "top_suppliers_tail_spend": r"(\d+)? ?tail (supplier|vendor)s",
        "largest_gap": r"(\d+)? ?(supplier|vendor)s with largest YOY spend evolution",
        "spend_without_po": r"(\d+)? ?(supplier|vendor)s with missing PO spend",
        "highest_single_spend": r"(\d+)? ?single source (supplier|vendor)s",
        "top_supplier": r"top (\d*)\s?(supplier|vendor)s by spend",
        "top_supplier_by_opportunity": r"top (\d+)?\s?(supplier|vendor)s? by opportunity"
    }

    prompt = str_match_prompt(user_query)
    log.debug("Generated prompt for LLM pattern detection")

    ai_response = generate_chat_response_with_chain(prompt)
    log.debug("AI response from pattern recognition: %s", ai_response)

    try:
    # Try loading as-is first
        result = json.loads(ai_response.strip())
        log.info("Successfully parsed AI response")
    except json.JSONDecodeError:
        # Fallback: try wrapping it in curly braces if needed
        try:
            wrapped = f'{{{ai_response.strip()}}}'
            result = json.loads(wrapped)
            log.info("Successfully parsed AI response after wrapping")
        except json.JSONDecodeError as e:
            log.error("Failed to parse AI response as JSON: %s", ai_response)


            raise NegotiationFactoryQueryException("Please try again") from e

    if result:
        log.info("Matched pattern key: %s", result.get("pattern_key"))
        log.info("Matched value: %s", result.get("value"))
        return get_supplier_data(pg_db_conn, sf_client, category, result['pattern_key'], result['value'], user_query=user_query)

    log.warning("No pattern matched for user query")
    raise NegotiationFactoryQueryException("request not supported as of now")

@log_time
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
    log.info("Fetching supplier profiles for category: %s", category)
    log.debug("Requested supplier names: %s", supplier_names.tolist() if isinstance(supplier_names, numpy.ndarray) else supplier_names)

    filter_condition = (
    f"""LOWER(category) = LOWER('{category}') AND YEAR = (SELECT MAX(YEAR) """
    f"""FROM {negotiation_tables["supplier_details"]}) AND """
    f"""{sf_client.get_condition_string(("LOWER(SUPPLIER)", "in", [s.lower() for s in supplier_names]))}"""
    )

    all_supplier_data = pd.DataFrame(
        sf_client.select_records_with_filter(
            table_name=negotiation_tables["supplier_details"],
            filter_condition=filter_condition,
        ),
    )
    log.info("Retrieved %d rows from supplier details table", len(all_supplier_data))

    all_supplier_data.columns = all_supplier_data.columns.str.lower()

    remane_map = {
        "supplier": "supplier_name",
        "category": "category_name",
        "year": "period",
    }

    for key, value in remane_map.items():
        if key in all_supplier_data.columns:
            all_supplier_data.rename(columns={key: value}, inplace=True)
            log.debug("Renamed column '%s' to '%s'", key, value)

    all_supplier_data.sort_values(
        by=["spend_ytd"],
        ascending=False,
        inplace=True,
    )
    log.info("Sorted supplier data by 'spend_ytd' descending")

    supplier_names = all_supplier_data["supplier_name"].unique().tolist()
    log.info("Unique suppliers to enrich: %d", len(supplier_names))

    all_supplier_data_modified = pd.DataFrame(
        [
            enrich_supplier_profile(
                pd.DataFrame(all_supplier_data.loc[all_supplier_data["supplier_name"] == supplier]),
            )
            for supplier in supplier_names
        ],
    )
    log.info("Enriched supplier profiles generated for all suppliers")

    all_supplier_data_modified.drop(
        ["insights", "objectives"],
        axis=1,
        errors="ignore",
        inplace=True,
    )
    log.info("Dropped insights and objectives columns if present")

    return all_supplier_data_modified


@log_time
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
    log.info("Starting negotiation_init for category: %s", category)
    log.debug("User query: %s", user_query)
    log.info("Additional kwargs received: %d", len(kwargs))

    log.info("Calling get_supplier_data_based_on_user_query")
    supplier_data, message = get_supplier_data_based_on_user_query(
        pg_db_conn,
        sf_client,
        category,
        user_query
    )
    log.info("Supplier data fetched — rows: %d", len(supplier_data))

    log.info("Calling get_supplier_profiles for %d suppliers", len(supplier_data))
    
    try:
        supplier_data = supplier_data.drop(columns=['year','category','total_opportunity'])
        supplier_data = supplier_data.rename(columns={'supplier': 'supplier_name','supplier_opportunity':'opportunity','total_opportunity_percentage': 'percentage_of_total_opportunity'})
    except Exception as e:
        log.warning("Columns not found in supplier_data: %s", str(e))


    suppliers_profiles = get_supplier_profiles(
        pg_db_conn,
        sf_client,
        category,
        supplier_data.supplier_name.values,
    )
    log.info("Supplier profiles enriched")

    ctas = {
        "prompt": negotiation_conf["cta_button_map"]["select_skus"],
        "intent": "negotiation_select_skus",
    }

    log.debug("Preparing response payload for negotiation initialization")
    
    params = {
        "response_type": "supplier_details",
        "message": message,
        "suppliers_profiles": json.loads(
            suppliers_profiles.to_json(orient="records", double_precision=2),
        ),
        "additional_data": {
            "suppliers_data": json.loads(
                supplier_data.to_json(orient="records", double_precision=2),
            ),
            "follow_up_prompt": ctas,
            "welcome_message": "Thank you for selecting SUPPLIER_NAME. Here are few"
                               " probable next steps:",
        },
    }

    log.info("Returning final response from negotiation_init")
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
    # current_date = date.today()
    # log.info("Initiating generate_scoping with %d extra arguments", len(kwargs))

    # supplier_name = pinned_elements.get("supplier_profile", {}).get("supplier_name", "")
    # log.info("Supplier selected for scoping: %s", supplier_name)

    # if not supplier_name:
    #     raise NegotiationFactoryUserException("Supplier name not found in pinned elements")

    # table_name = negotiation_conf["tables"]["sku_details"]
    # supplier_name = supplier_name.replace("'", "''")

    # filter_string = (
    #     f"""category_name = '{category}' AND """
    #     f"""period = (select Max(PERIOD) from {table_name}) AND """
    #     f"""supplier_name = '{supplier_name}'"""
    # )

    # log.debug("SKU data filter condition: %s", filter_string)

    # sku_data = sf_client.select_records_with_filter(
    #     table_name=table_name,
    #     filtered_columns=[
    #         "sku_id",
    #         "sku_name",
    #         "unit_price",
    #         "quantity",
    #         "unit_of_measurement",
    #         "spend_ytd",
    #     ],
    #     order_by=("spend_ytd", "DESC"),
    #     filter_condition=filter_string,
    # )
    

    current_date = date.today()
    log.info("Initiating generate_scoping with %d extra arguments", len(kwargs))

    supplier_name = pinned_elements.get("supplier_profile", {}).get("supplier_name", "")
    log.info("Supplier selected for scoping: %s", supplier_name)

    if not supplier_name:
        raise NegotiationFactoryUserException("Supplier name not found in pinned elements")

    table_name = negotiation_conf["tables"]["sku_details"]
    supplier_name = supplier_name.replace("'", "''")

    query = f"""
        SELECT sku_id,
            sku_name,
            unit_price,
            quantity,
            unit_of_measurement,
            spend_ytd,
            REPORTING_CURRENCY,
            period,
        FROM {table_name}
        WHERE category_name = '{category}'
        AND period = (SELECT MAX(PERIOD) FROM {table_name})
        AND supplier_name = '{supplier_name}'
        ORDER BY spend_ytd DESC
    """

    log.debug("SKU data query: %s", query)

    try:
        sku_data = sf_client.fetch_dataframe(query)
        sku_data.rename(columns={"REPORTING_CURRENCY": "currency_symbol"}, inplace=True)
        sku_data['currency_symbol'] = sku_data['currency_symbol'].apply(    
            lambda x: negotiation_conf["currency_map"].get(x, " "),
        )
        log.info("Fetched SKU data successfully")
    except Exception as e:
        log.error("Failed to fetch SKU data: %s", str(e))
        sku_data = pd.DataFrame()  # fallback empty DataFrame

    # breakpoint()
    if sku_data.empty:
        log.warning("No SKU data found for supplier: %s", supplier_name)
        raise NegotiationFactoryUserException(f"No sku data found for the supplier {supplier_name}")

    log.info("Fetched %d SKU rows for supplier", len(sku_data))

    sku_data_df = pd.DataFrame(sku_data)
    sku_data_df.columns = sku_data_df.columns.str.lower()
    year_ = sku_data_df.period.max()    
    log.info("Latest period in SKU data: %s", year_)
    sku_data_df = (
        sku_data_df.groupby(["sku_id", "sku_name","currency_symbol"])
        .agg({
            "quantity": "sum",
            "spend_ytd": "sum",
            "unit_price": lambda x: weighted_average(
                sku_data_df.loc[x.index],
                term="unit_price",
                average_term="quantity",
            ),
            "unit_of_measurement": lambda x: (
                x[x != ""].value_counts().index[0]
                if ((x != "") & (x.notnull())).any()
                else ""
            ),
        })
        .reset_index()
    )

    log.info("SKU aggregation completed")

    rename_list = {
        "sku_id": "id",
        "sku_name": "name",
        "unit_of_measurement": "uom",
        "spend_ytd": "spend",
    }
    sku_data_df.rename(columns=rename_list, inplace=True)
    sku_data_df.sort_values(by="spend", ascending=False, inplace=True)
    log.info("Renamed and sorted SKU data")

    if "insights" in pinned_elements:
        pinned_elements.pop("insights")
        log.debug("Removed 'insights' from pinned_elements")

    suggested_prompts = [
        # {"prompt": "Learn more about supplier", "intent": "negotiation_user_questions"},
        {
            "prompt": negotiation_conf["cta_button_map"]["objective"],
            "intent": "negotiation_objective",
        },
    ]

    # params = {
    #     "message": f"Select the SKUs from {supplier_name} that you want to consider in the negotiation ({current_date.year} YTD data):",
    #     "response_type": "sku_details",
    #     "skus": sku_data_df.to_dict(orient="records"),
    #     "suggested_prompts": suggested_prompts,
    # }

    if sku_data_df.empty:
        params = {
            "message": "There is no SKU available for the selected supplier on which negotiation can happen. Please try with other suppliers.",
            "response_type": "sku_details",
            "skus": [],
            "suggested_prompts": []
        }
    elif len(sku_data_df) == 1:
        params = {
            "message": f"Select the SKU from {supplier_name} to consider in the negotiation ({year_} YTD data):",
            "response_type": "sku_details",
            "skus": sku_data_df.to_dict(orient="records"),
            "suggested_prompts": suggested_prompts,
        }
    else:
        params = {
            "message": f"Select the SKUs from {supplier_name} that you want to consider in the negotiation ({year_} YTD data):",
            "response_type": "sku_details",
            "skus": sku_data_df.to_dict(orient="records"),
            "suggested_prompts": suggested_prompts,
        }


    log.info("Returning SKU scoping response for %s", supplier_name)
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
    log.info("Initiating generate_carrots_and_sticks with %d extra arguments", len(kwargs))

    reference_carrots_sticks = kwargs.get("reference_data", {}).get("carrots_and_sticks")

    if reference_carrots_sticks is None or len(reference_carrots_sticks) == 0:
        log.warning("No carrots and sticks data found in reference_data")
        raise NegotiationFactoryUserException("No carrots and sticks found")

    log.info("Fetched carrots and sticks reference data — total rows: %d", len(reference_carrots_sticks))

    carrots = reference_carrots_sticks[reference_carrots_sticks["type"] == "carrot"]
    sticks = reference_carrots_sticks[reference_carrots_sticks["type"] == "stick"]
    carrots.drop("type", axis=1, inplace=True)
    sticks.drop("type", axis=1, inplace=True)

    log.info("Separated %d carrots and %d sticks", len(carrots), len(sticks))

    suggested_prompts = get_section_suggested_prompts(
        section_name="Define Negotiation Strategy",
    )
    remove_prompts = [
        "Set tone & tactics" if "tone_and_tactics" in pinned_elements.keys() else "Change tone & tactics",
        "Set carrots & sticks",
        "Change carrots & sticks",
    ]

    suggested_prompts = [
        prompt for prompt in suggested_prompts if prompt["prompt"] not in remove_prompts
    ]

    log.info("Filtered suggested prompts based on pinned elements")

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

    log.info("Returning carrots and sticks scoping response")
    return convert_to_response_format(**params)
