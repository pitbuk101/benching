""" Utility functions for the Negotiation factory use case """

# pylint: disable=C0302

from __future__ import annotations

import copy
import json
import random
import re
import string
import time
from itertools import chain
from typing import Any

import numpy as np
import pandas as pd
import asyncio
from rapidfuzz import process, fuzz

from ada.components.db.pg_connector import PGConnector
from ada.components.db.sf_connector import SnowflakeClient
from ada.components.llm_models.generic_calls import (
    generate_chat_response_with_chain,
    generate_embeddings_from_string,
)
from ada.use_cases.negotiation_factory.exception import (
    NegotiationFactoryException,
    NegotiationFactoryUserException,
)
from ada.use_cases.negotiation_factory.util_prompts import extract_supplier_prompt
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time
from ada.utils.metrics.similarity import get_best_match_from_list
from ada.use_cases.key_facts_chatbot.call_keyfact_chatbot import fetch


negotiation_conf = read_config("use-cases.yml")["negotiation_factory"]
negotiation_tables = negotiation_conf["tables"]
log = get_logger("Negotiation_factory_util")



@log_time
def extract_supplier_name_from_user_query(user_query: str) -> str:
    """
    This function identify and extract the supplier name
    from user query using GenAi model.
    Args:
        user_query (str): received user query
    Returns:
        (str): extracted supplier name from user query
    Raises:
        NegotiationFactoryUserException: If no supplier name present in user query
    """
    log.info("extract_supplier_name_from_user_query called with user query: %s", user_query)

    prompt = extract_supplier_prompt(user_query=user_query)
    log.debug("Generated supplier extraction prompt")

    llm_response = generate_chat_response_with_chain(
        prompt=prompt,
        model=negotiation_conf["model"]["fast_model_name"],
    )
    log.info("Response from LLM: %s", llm_response)

    try:
        llm_response = json.loads(llm_response)
        log.debug("Successfully parsed LLM response as JSON")
    except json.decoder.JSONDecodeError as exc:
        log.warning("LLM output had JSON formatting error: %s", exc)
        llm_response = json_regex(llm_response, ["supplier_name"])

    supplier_name = llm_response.get("supplier_name", "")
    if isinstance(supplier_name, str):
        supplier_name = supplier_name.strip()

    log.info("Extracted supplier name: '%s'", supplier_name)

    if not supplier_name:
        log.error("No supplier name found in query. Raising exception.")
        raise NegotiationFactoryUserException(
            "Before we proceed with negotiations, please provide the name of the supplier",
        )

    return supplier_name

@log_time
def extract_supplier_name_from_user_query_general(user_query: str) -> str:
    """
    This function identify and extract the supplier name
    from user query using GenAi model.
    Args:
        user_query (str): received user query
    Returns:
        (str): extracted supplier name from user query
    Raises:
        NegotiationFactoryUserException: If no supplier name present in user query
    """
    log.info("extract_supplier_name_from_user_query called with user query: %s", user_query)

    prompt = extract_supplier_prompt(user_query=user_query)
    log.debug("Generated supplier extraction prompt")

    llm_response = generate_chat_response_with_chain(
        prompt=prompt,
        model=negotiation_conf["model"]["fast_model_name"],
    )
    log.info("Response from LLM: %s", llm_response)

    try:
        llm_response = json.loads(llm_response)
        log.debug("Successfully parsed LLM response as JSON")
    except json.decoder.JSONDecodeError as exc:
        log.warning("LLM output had JSON formatting error: %s", exc)
        llm_response = json_regex(llm_response, ["supplier_name"])

    supplier_name = llm_response.get("supplier_name", "")
    if isinstance(supplier_name, str):
        supplier_name = supplier_name.strip()

    log.info("Extracted supplier name: '%s'", supplier_name)

    if not supplier_name:
        log.error("No supplier name found in query. Raising exception.")
        return None

    return supplier_name


@log_time
def supplier_exists(sf_client: SnowflakeClient, category: str, supplier_names: list) -> bool:
    """
    This function checks if the supplier exists in the database.
    Args:
        sf_client (SnowflakeClient): The Snowflake client object.
        category (str): The category name to filter the supplier details.
        supplier_names (list): A list of supplier names to search for.
    Returns:
        bool: True if the supplier exists, False otherwise.
    """
    log.info("Checking existence of suppliers: %s in category: %s", supplier_names, category)

    supplier_names_str = ', '.join([f"'{name.lower()}'" for name in supplier_names])
    query = f"""
        SELECT DISTINCT SUPPLIER 
        FROM {negotiation_tables["supplier_details"]} 
        WHERE LOWER(SUPPLIER) IN ({supplier_names_str}) 
        AND CATEGORY = '{category}'  
        AND YEAR = (SELECT MAX(YEAR) FROM {negotiation_tables["supplier_details"]})
    """
    log.debug("Supplier existence SQL query: %s", query.strip())

    data = sf_client.fetch_dataframe(query=query)
    log.info("Query returned %d rows", len(data))

    if data.empty:
        log.warning("No matching suppliers found in the database")
        return []

    supplier_list = data['SUPPLIER'].unique().tolist()
    log.info("Suppliers found in database: %s", supplier_list)
    return supplier_list


@log_time
def create_supplier_profile(
    pg_db_conn: PGConnector,
    sf_client: SnowflakeClient,
    supplier_details: pd.DataFrame,
    category: str,
    supplier_name: str,
) -> tuple[pd.Series, list[dict[str, Any]], list[dict[str, Any]]]:
    """
    This function create supplier profile for the selected supplier
    from the data present in database related to supplier
    Args:
        supplier_details (pd.DataFrame): The details for the top suppliers
        category (str):  user selected category supplier belongs to
        supplier_name (str) : supplier name received in user query
    Returns:
        (tuple[dict[str, Any], list[dict[str, Any]]]):Supplier profile,insights,objectives in tuple
    Raises:
        NegotiationFactoryUserException: If supplier data is not present
          for the category or if the supplier name does not exactly match data
            it gives approximate matches
    """
    log.info("Creating supplier profile for supplier: %s in category: %s", supplier_name, category)
#     extracted_data = supplier_details.copy()
#     # extracted_data["cosine_distance"] = extracted_data["cosine_distance"].astype(float)

#     initial_count = len(extracted_data)
#     extracted_data = extracted_data[
#         extracted_data["cosine_distance"] < negotiation_conf["supplier_similarity_threshold"]
#     ]
#     log.info("Filtered %d → %d rows using cosine threshold", initial_count, len(extracted_data))

#     similar_supplier_list = extracted_data['supplier_name'].unique().tolist()
#     supplier_series = sf_client.fetch_dataframe(
#     f"""
#     SELECT DISTINCT LOWER(SUPPLIER) as supplier_name
#     FROM {negotiation_tables["supplier_details"]} 
#     WHERE LOWER(SUPPLIER) LIKE '{supplier_name[:2].lower()}%' 
#     AND CATEGORY = '{category}'  
#     AND YEAR = (SELECT MAX(YEAR) FROM {negotiation_tables["supplier_details"]})
#     """
# )
#     matches = []
#     if not supplier_series.empty:
#         supplier_list = supplier_series['SUPPLIER_NAME'].tolist()
#         matches = [match[0] for match in process.extract(supplier_name[:2].lower(), supplier_list, scorer=fuzz.token_set_ratio, limit=10)]

#     similar_supplier_list.extend(matches)
#     available_suppliers = supplier_exists(
#         sf_client=sf_client,
#         category=category,
#         supplier_names=similar_supplier_list,
#     )
#     log.info("Available similar suppliers in DB: %s", available_suppliers)
#     suggested_prompts = [
#         {
#             "prompt": f"{match_val}",
#             "intent": "supplier_name",
#         }
#         for match_val in available_suppliers
#         # extracted_data.head(negotiation_conf["num_similar_suppliers"])["supplier_name"].unique().tolist()
#         # if match_val in available_suppliers
#     ]

#     min_distance = extracted_data.head(1)["cosine_distance"].values[0]
#     log.info("Minimum cosine distance for top match: %f", min_distance)
#     extracted_name = extracted_data.head(1)['supplier_name'].values[0]
#     if (min_distance <= 0.05 or (extracted_name.strip().lower()==supplier_name.strip().lower())) and available_suppliers:
#         log.info("Cosine distance ≤ 0.05, creating supplier profile from KF")
    return create_supplier_profile_from_kf(
        pg_db_conn,
        sf_client,
        supplier_details,
        category,
        supplier_name=supplier_details[0],
        suggested_prompts=[],
    )

    log.warning("No exact supplier match found below 0.05 threshold")
    message = f"We could not find the exact {supplier_name} in {category}, for current year."
    if suggested_prompts:
        message += "Is the supplier you are looking for one of these?"
    raise NegotiationFactoryUserException(message, suggested_prompts)

@log_time
def create_supplier_profile_from_kf(
    pg_db_conn: PGConnector,
    sf_client: SnowflakeClient,
    supplier_details: pd.DataFrame,
    category: str,
    supplier_name: str,
    suggested_prompts,
) -> tuple[pd.Series, list[dict[str, Any]], list[dict[str, Any]]]:
    """
    This function create supplier profile for the selected supplier
    from the data present in database related to supplier
    Args:
        supplier_details (pd.DataFrame): The details for the top suppliers
        category (str):  user selected category supplier belongs to
        supplier_name (str) : supplier name received in user query
    Returns:
        (tuple[dict[str, Any], list[dict[str, Any]]]):Supplier profile,insights,objectives in tuple
    Raises:
        NegotiationFactoryUserException: If supplier data is not present
          for the category or if the supplier name does not exactly match data
            it gives approximate matches
    """
    log.info("Calling get_supplier_profiles for: %s", supplier_name)
    supplier_profile = get_supplier_profiles(
        pg_db_conn,
        sf_client,
        category,
        supplier_name,
        suggested_prompts,
    )
    if not supplier_profile.empty:
        log.info("Supplier profile successfully created for %s", supplier_name)
        return supplier_profile, [], []

    log.error("Supplier profile is empty after fetch — raising user exception")
    message = f"We could not find the exact {supplier_name} in {category}, for current year."
    if suggested_prompts:
        message += " Is the supplier you are looking for one of these?"
    raise NegotiationFactoryUserException(message, suggested_prompts)


# @log_time
# def enrich_supplier_profile(supplier_profile: pd.DataFrame) -> pd.Series:
#     """
#     Modify supplier profile for better visual representation.
#     Args:
#         supplier_profile (pd.DataFrame): The supplier profile data as a Pandas DataFrame.
#     Returns:
#         pd.Series: The modified supplier profile with enriched data.
#     """
#     log.info("Starting enrichment of supplier profile")

#     def get_savings_df(value: pd.Series) -> pd.DataFrame:
#         """
#         Get savings data for the supplier.
#         Args:
#             value (pd.Series): The supplier profile data.
#         Returns:
#             pd.DataFrame: The savings data for the supplier.
#         """
#         log.debug("Extracting savings data from analytics_name column")
#         value_pop = value[~value.eq({})]
#         if len(value_pop) > 0:
#             key_vals = [list(item.keys())[0] for item in value_pop.iloc[0]]
#             dict_val: dict[str, list[Any]] = {key: [] for key in key_vals}
#             for row in value:
#                 for key in key_vals:
#                     val = {list(item.keys())[0]: list(item.values())[0] for item in row}
#                     dict_val[key].append(val.get(key, 0))
#             return_df = pd.DataFrame(dict_val)
#             return_df.columns = return_df.columns.str.replace("_", " ")
#             return_df.columns = return_df.columns.str.lower()
#             log.debug("Constructed savings DataFrame with columns: %s", return_df.columns.tolist())
#             return return_df
#         return pd.DataFrame(value)

#     log.debug("Initial supplier profile shape: %s", supplier_profile.shape)

#     supplier_profile.drop(
#         [
#             "supplier_name_embedding",
#             "cosine_distance",
#             "sku_list_name",
#             "payment_terms",
#             "payment_term_days",
#         ],
#         inplace=True,
#         axis=1,
#         errors="ignore",
#     )
#     log.debug("Dropped unused columns from supplier profile")

#     if "analytics_name" in supplier_profile.columns:
#         analytics_df = get_savings_df(supplier_profile["analytics_name"])
#         if "analytics_name" not in analytics_df:
#             supplier_profile = supplier_profile.join(analytics_df)
#         supplier_profile.drop("analytics_name", axis=1, inplace=True)
#         log.debug("Processed and dropped analytics_name column")

#     agg_dict = {
#         key: np.nansum
#         for key in supplier_profile.select_dtypes(include=negotiation_conf["numerics"]).columns
#     }
#     agg_dict["number_of_supplier_in_category"] = np.nanmean
#     agg_dict["sku_list"] = lambda x: list(dict.fromkeys(chain.from_iterable(x)))
#     agg_dict["supplier_relationship"] = lambda x: next(iter(list(x)))
#     agg_dict["period"] = lambda x: next(iter(list(x)))
#     agg_dict["payment_term_avg"] = lambda x: round(np.nanmean(x)) if not np.isnan(np.nanmean(x)) else ""
#     agg_dict["currency_symbol"] = lambda x: next(iter(list(x)))

#     log.debug("Aggregation dictionary constructed")

#     supplier_profile = (
#         supplier_profile.groupby(["supplier_name", "category_name"])
#         .agg(agg_dict)
#         .reset_index()
#         .squeeze()
#     )
#     log.debug("Aggregated supplier profile: keys = %s", list(supplier_profile.keys()))

#     supplier_profile["insights"] = []
#     supplier_profile["objectives"] = []

#     sku_list = supplier_profile["sku_list"]
#     supplier_profile["number_of_sku"] = len(sku_list)
#     supplier_profile["sku_list"] = sku_list[: negotiation_conf["context_max_skus_num"]]
#     supplier_profile["spend_ytd"] = round(supplier_profile.get("spend_ytd", 0), 2)
#     supplier_profile["spend_last_year"] = round(supplier_profile.get("spend_last_year", 0), 2)

#     currency_str = supplier_profile.pop("currency_symbol")
#     supplier_profile["currency_symbol"] = negotiation_conf["currency_map"].get(currency_str, currency_str)
#     supplier_profile["currency_position"] = negotiation_conf.get("currency_position")

#     supplier_profile["percentage_spend_across_category_ytd"] = round(
#         supplier_profile.get("percentage_spend_across_category_ytd", 0), 2
#     )
#     supplier_profile["single_source_spend_ytd"] = round(
#         supplier_profile.get("single_source_spend_ytd", 0), 2
#     )
#     supplier_profile["spend_no_po_ytd"] = round(
#         supplier_profile.get("spend_no_po_ytd", 0), 2
#     )

#     spend_denom = 1 if supplier_profile["spend_ytd"] == 0.0 else supplier_profile.get("spend_ytd")
#     supplier_profile["percentage_spend_which_is_single_sourced"] = round(
#         supplier_profile.get("single_source_spend_ytd", 0) / spend_denom, 1
#     )
#     supplier_profile["percentage_spend_without_po"] = round(
#         supplier_profile.get("spend_no_po_ytd", 0) / spend_denom, 1
#     )
#     supplier_profile["target_savings"] = supplier_profile.get("total_saving_opportunity", 0) or 0

#     supplier_profile = supplier_profile.fillna("")
#     log.info("Enrichment complete for supplier: %s", supplier_profile.get("supplier_name", "<unknown>"))
#     return supplier_profile

@log_time
def enrich_supplier_profile(supplier_profile: pd.DataFrame) -> pd.Series:
    """
    Enrich and aggregate supplier profile data for response.

    - Drops unnecessary columns
    - Aggregates numeric and categorical fields safely
    - Extracts structured savings data from analytics
    - Formats values for downstream serialization (e.g., JSON-safe)
    
    Args:
        supplier_profile (pd.DataFrame): Raw supplier profile rows

    Returns:
        pd.Series: Cleaned and aggregated supplier profile
    """
    import numbers

    log.info("Starting enrichment of supplier profile")

    def get_savings_df(value: pd.Series) -> pd.DataFrame:
        """
        Extracts savings data into a structured DataFrame from embedded dictionaries.

        Args:
            value (pd.Series): Column with list of dictionaries

        Returns:
            pd.DataFrame: Structured savings data or empty if invalid
        """
        value_pop = value[~value.eq({})]
        if len(value_pop) > 0:
            key_vals = [list(item.keys())[0] for item in value_pop.iloc[0]]
            dict_val: dict[str, list[Any]] = {key: [] for key in key_vals}
            for row in value:
                for key in key_vals:
                    val = {list(item.keys())[0]: list(item.values())[0] for item in row}
                    dict_val[key].append(val.get(key, 0))
            return_df = pd.DataFrame(dict_val)
            return_df.columns = return_df.columns.str.replace("_", " ").str.lower()
            log.debug("Constructed savings DataFrame with columns: %s", return_df.columns.tolist())
            return return_df
        return pd.DataFrame(value)

    # Drop fields that are unnecessary
    supplier_profile.drop(
        [
            "supplier_name_embedding",
            "cosine_distance",
            "sku_list_name",
            "payment_terms",
            "payment_term_days",
        ],
        inplace=True,
        axis=1,
        errors="ignore",
    )
    log.debug("Dropped unused columns from supplier profile")

    # Process analytics if present
    if "analytics_name" in supplier_profile.columns:
        analytics_df = get_savings_df(supplier_profile["analytics_name"])
        if "analytics_name" not in analytics_df:
            supplier_profile = supplier_profile.join(analytics_df)
        supplier_profile.drop("analytics_name", axis=1, inplace=True)
        log.debug("Processed and dropped analytics_name column")

    # Safe aggregators
    def safe_mean(x):
        try:
            return float(np.nanmean(x)) if len(x) else 0.0
        except Exception:
            return 0.0

    def safe_round_mean(x):
        try:
            return round(np.nanmean(x)) if not np.isnan(np.nanmean(x)) else ""
        except Exception:
            return ""

    def safe_first(x):
        return next(iter(x), "")

    # Construct aggregation mapping
    agg_dict = {
        key: np.nansum
        for key in supplier_profile.select_dtypes(include=negotiation_conf["numerics"]).columns
    }
    agg_dict.update({
        "number_of_supplier_in_category": safe_mean,
        "sku_list": lambda x: list(dict.fromkeys(chain.from_iterable(x))),
        "supplier_relationship": safe_first,
        "period": safe_first,
        "payment_term_avg": safe_round_mean,
        "currency_symbol": safe_first,
    })

    log.debug("Aggregation dictionary constructed")

    # Group and aggregate
    supplier_profile = (
        supplier_profile.groupby(["supplier_name", "category_name"])
        .agg(agg_dict)
        .reset_index()
        .squeeze()
    )
    log.debug("Aggregated supplier profile: keys = %s", list(supplier_profile.keys()))

    # Enrich with default fields
    supplier_profile["insights"] = []
    supplier_profile["objectives"] = []

    sku_list = supplier_profile["sku_list"]
    supplier_profile["number_of_sku"] = len(sku_list)
    supplier_profile["sku_list"] = sku_list[: negotiation_conf["context_max_skus_num"]]

    supplier_profile["spend_ytd"] = round(supplier_profile.get("spend_ytd", 0), 2)
    supplier_profile["spend_last_year"] = round(supplier_profile.get("spend_last_year", 0), 2)

    # Format currency
    currency_str = supplier_profile.pop("currency_symbol")
    supplier_profile["currency_symbol"] = negotiation_conf["currency_map"].get(currency_str, currency_str)
    supplier_profile["currency_position"] = negotiation_conf.get("currency_position")

    # Derived spend percentages
    supplier_profile["percentage_spend_across_category_ytd"] = round(
        supplier_profile.get("percentage_spend_across_category_ytd", 0), 2
    )
    supplier_profile["single_source_spend_ytd"] = round(
        supplier_profile.get("single_source_spend_ytd", 0), 2
    )
    supplier_profile["spend_no_po_ytd"] = round(
        supplier_profile.get("spend_no_po_ytd", 0), 2
    )

    spend_denom = supplier_profile["spend_ytd"] or 1
    supplier_profile["percentage_spend_which_is_single_sourced"] = round(
        supplier_profile.get("single_source_spend_ytd", 0) / spend_denom, 1
    )
    supplier_profile["percentage_spend_without_po"] = round(
        supplier_profile.get("spend_no_po_ytd", 0) / spend_denom, 1
    )

    supplier_profile["target_savings"] = supplier_profile.get("total_saving_opportunity", 0) or 0

    # Final null cleanup
    supplier_profile = supplier_profile.fillna("")

    # Final validation (optional safety check)
    for k, v in supplier_profile.items():
        if callable(v):
            supplier_profile[k] = ""

    log.info("Enrichment complete for supplier: %s", supplier_profile.get("supplier_name", "<unknown>"))
    return supplier_profile


@log_time
def extract_supplier_details(
    category: str,
    pg_db_conn: PGConnector,
    sf_client: SnowflakeClient,
    supplier_name: str,
) -> pd.DataFrame:
    """
    Get supplier details from the database with vector search.
    Args:
        category (str): The category name to filter the supplier details.
        pg_db_conn (PGConnector): The database connector object for PostgreSQL.
        supplier_name (str): The name of the supplier to search for.
    Returns:
        pd.DataFrame: A DataFrame containing the extracted supplier details.

    Raises:
        NegotiationFactoryUserException: If the supplier details are not available or the
        cosine distance is above the similarity threshold.
    """
    log.info("Extracting supplier details for: '%s' in category: '%s'", supplier_name, category)

    # table = 'supplier_embeddings'
    # # table = 'supplier_profile_with_insights_with_objectives_view_with_saving'
    # log.debug("Using table: %s for vector similarity search", table)

    # embedding = generate_embeddings_from_string(supplier_name)
    # log.debug("Generated embedding for supplier name")

    # extracted_data = pd.DataFrame(
    #     pg_db_conn.search_by_vector_similarity(
    #         table_name=table,
    #         query_emb=embedding,
    #         emb_column_name="supplier_name_embedding",
    #         num_records=negotiation_conf["num_similar_suppliers"],
    #     ),
    # )

    # log.info("Extracted data shape: %s", extracted_data.shape)
    # log.debug("Extracted data columns: %s", list(extracted_data.columns))

    # if not extracted_data.empty:
    #     top_row = extracted_data.head(1).squeeze().to_dict()
    #     cosine_distance = top_row.get("cosine_distance", 0)
    #     log.info("Top match cosine distance: %.4f", cosine_distance)
    # else:
        
    #     log.warning("No records returned from similarity search")
    #     cosine_distance = None

    # if extracted_data.empty or (
    #     cosine_distance is not None and cosine_distance > negotiation_conf["supplier_similarity_threshold"]
    # ):
    #     log.warning(
    #         "No match or top cosine distance %.4f exceeded threshold %.4f",
    #         cosine_distance,
    #         negotiation_conf["supplier_similarity_threshold"]
    #     )
    supplier_series = sf_client.fetch_dataframe(
        f"""
        SELECT DISTINCT SUPPLIER as supplier_name
        FROM {negotiation_tables["supplier_details"]} 
        WHERE LOWER(SUPPLIER) = '{supplier_name.lower()}' 
        AND CATEGORY = '{category}'  
        AND YEAR = (SELECT MAX(YEAR) FROM {negotiation_tables["supplier_details"]})
        """
    )
    if not supplier_series.empty:
        supplier_name_ = supplier_series["SUPPLIER_NAME"].values[0]
        log.info("Filtered supplier series: %s", supplier_series)  
    else:
        supplier_series = sf_client.fetch_dataframe(
            f"""
            SELECT DISTINCT LOWER(SUPPLIER) as supplier_name
            FROM {negotiation_tables["supplier_details"]} 
            WHERE LOWER(SUPPLIER) like '{supplier_name[:2].lower()}%' 
            AND CATEGORY = '{category}'  
            AND YEAR = (SELECT MAX(YEAR) FROM {negotiation_tables["supplier_details"]})
            """
        )

        if supplier_series.empty:
            log.info("No suppliers found with the first two characters. Searching with the first character.")
            supplier_series = sf_client.fetch_dataframe(
            f"""
            SELECT DISTINCT LOWER(SUPPLIER) as supplier_name
            FROM {negotiation_tables["supplier_details"]} 
            WHERE LOWER(SUPPLIER) like '{supplier_name[:1].lower()}%' 
            AND CATEGORY = '{category}'  
            AND YEAR = (SELECT MAX(YEAR) FROM {negotiation_tables["supplier_details"]})
            """
            )
        supplier_series = supplier_series.drop_duplicates(subset=["SUPPLIER_NAME"])
        supplier_list = supplier_series["SUPPLIER_NAME"].tolist()
        log.warning("No supplier series found for the given name")
        matches = []
        matches = [match[0] for match in process.extract(supplier_name[:2].lower(), supplier_list, scorer=fuzz.token_set_ratio, limit=10)]
        # breakpoint()
        if matches:
            supplier_list = supplier_exists(sf_client, category, matches)
            if len(supplier_list) > 0:
                log.info("Found similar suppliers: %s", supplier_list)
                raise NegotiationFactoryUserException(
                    f"There is no supplier {supplier_name} exist for category {category} If you'd like, you can check for other suppliers",
                    [
                        {
                            "prompt": f"{match_val}",
                            "intent": "supplier_name",
                        }
                        for match_val in supplier_list
                    ],
                )
        else:
            raise NegotiationFactoryUserException(
                f"There is no supplier {supplier_name} exist for category {category}. even there is no similar supplier exist for the category",
            )            
    return [supplier_name_]


@log_time
def extract_supplier_details_from_kf(
    category: str,
    pg_db_conn: PGConnector,
    sf_client: SnowflakeClient,
    supplier_name: str,
) -> pd.DataFrame:
    """
    Get supplier details from the database with vector search.
    Args:
        category (str): The category name to filter the supplier details.
        pg_db_conn (PGConnector): The database connector object for PostgreSQL.
        supplier_name (str): The name of the supplier to search for.
    Returns:
        pd.DataFrame: A DataFrame containing the extracted supplier details.

    Raises:
        NegotiationFactoryUserException: If the supplier details are not available or the
        cosine distance is above the similarity threshold.
    """
    log.info("Extracting supplier details from Snowflake for supplier: '%s' in category: '%s'", supplier_name, category)

    
    query = f"""
        SELECT DISTINCT SUPPLIER_ID, SUPPLIER 
        FROM {negotiation_tables["supplier_details"]} 
        WHERE SUPPLIER = '{supplier_name}' 
        AND CATEGORY = '{category}'  
        AND YEAR = (SELECT MAX(YEAR) FROM {negotiation_tables["supplier_details"]})
    """
    log.debug("Executing Snowflake query: %s", query.strip())

    data = sf_client.fetch_dataframe(query=query)
    log.info("Fetched %d rows for supplier '%s'", len(data), supplier_name)

    if data.empty:
        log.warning("No data found for supplier '%s' in category '%s'", supplier_name, category)
        raise NegotiationFactoryUserException(
            f"Apologies, but the data for supplier {supplier_name} in category {category} "
            "is not available at the moment. If you'd like, you can check for other suppliers",
        )

    return data


@log_time
def get_supplier_profile_insights_objectives(
    pg_db_conn: PGConnector,
    sf_client: SnowflakeClient,
    category: str,
    user_query: str,
    pinned_elements: dict[str, Any],
) -> tuple[str, dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    """
    This function extracts supplier profile from pinned elements if present
    else it gets supplier name from user query and generates the profile.
    Args:
        pg_db_conn (PGConnector) : Connection object to postgres database
        category (str): user selected category
        user_query (str) : received user query
        pinned_elements (dict[str, Any]): Pinned elements including supplier profile
    Returns:
        (tuple[str, dict[str, Any], dict[str, Any], dict[str, Any]]): supplier name,
          supplier profile, insights and objectives in tuple
    Raises:
        NegotiationFactoryUserException: If supplier name not present in user query
                                         or supplier data is not present for the category
    """
    log.info("get_supplier_profile_insights_objectives invoked")
    log.debug("Pinned elements keys: %s", list(pinned_elements.keys()))

    supplier_name = pinned_elements.get("supplier_profile", {}).get("supplier_name",) or extract_supplier_name_from_user_query(user_query)
    log.info("Resolved supplier name: %s", supplier_name)

    if "supplier_profile" in pinned_elements:
        log.info("Using supplier profile from pinned elements for: %s", supplier_name)
        return supplier_name, pinned_elements.get("supplier_profile"), None, None
    log.info("No pinned supplier profile found. Extracting from database.")
    supplier_details = extract_supplier_details(category, pg_db_conn, sf_client, supplier_name)
    
    log.info("Supplier details extracted successfully. Starting profile generation.")

    supplier_profile, insights, objectives = create_supplier_profile(
        pg_db_conn,
        sf_client,
        supplier_details,
        category,
        supplier_name,
    )

    log.info("Supplier profile, insights, and objectives created for: %s", supplier_name)
    return supplier_name, supplier_profile.to_dict(), insights, objectives


@log_time
def get_supplier_profile(
    pg_db_conn: PGConnector,
    sf_client: SnowflakeClient,
    category: str,
    user_query: str,
    pinned_elements: dict[str, Any],
    elements_required: bool = True,
) -> tuple[str, dict[str, Any]]:
    """
    This function extract the supplier profile from pinned elements.
    If supplier profile not present in pinned elements,
    It extracts the supplier name from user query
    and generate supplier profile with Data from database.
    Args:
        pg_db_conn (PGConnector) : Connection object to postgres database
        category (str): user selected category
        user_query (str) : received user query
        pinned_elements (dict[str, Any]): Pinned elements including supplier profile
        elements_required (bool): Flag for ensuring that elements are required.
    Returns:
        ( tuple[str, dict[str, Any]] ): supplier name and supplier profile in tuple
    Raises:
        NegotiationFactoryUserException: If supplier name not present in user query
                                     or supplier data is not present for the category
    """
    log.info("get_supplier_profile called")
    log.debug("Pinned elements received: %s", list(pinned_elements.keys()))

    try:
        supplier_profile = ensure_key_exist(
            "supplier_profile",
            pinned_elements,
            return_element=True,
        )
        log.info("Found supplier_profile in pinned elements")

        supplier_name = ensure_key_exist(
            "supplier_name",
            pinned_elements["supplier_profile"],
            return_element=True,
        )
        log.info("Supplier name extracted from pinned elements: %s", supplier_name)

    except NegotiationFactoryException as e:
        log.warning("Supplier profile or name not found in pinned elements: %s", str(e))
        try:
            supplier_name, supplier_profile, _, _ = get_supplier_profile_insights_objectives(
                pg_db_conn,
                sf_client,
                category,
                user_query,
                pinned_elements,
            )
            log.info("Extracted supplier profile and name from user query")
        except NegotiationFactoryUserException as e:
            log.warning("Failed to extract supplier profile from user query: %s", str(e))
            if elements_required:
                raise
            return "", {}

    return supplier_name, supplier_profile

@log_time
def extract_objective_description(reference_data: dict[str, Any], objective: str) -> str | None:
    """
    Extract objective description for the chosen objective
    from the database. It returns None if objective is not present.
    Args:
        reference_data (dict[str, Any]): tenant specific negotiation factory reference data
        objective (str): chosen objective value
    Returns:
        (str): Definition of objective
    """
    log.info("extract_objective_description called with objective: %s", objective)
    try:
        reference_key = negotiation_conf["reference_tables"]["common"]["negotiation_references"]
        objective_df: pd.DataFrame = reference_data[reference_key]
        log.debug("Reference DataFrame loaded with %d rows", len(objective_df))

        filtered_objective_df: pd.DataFrame = (
            objective_df[objective_df["l1_objective"].str.lower() == objective.lower()]
            if objective
            else pd.DataFrame(columns=objective_df.columns)
        )

        if filtered_objective_df.empty:
            log.warning("No matching objective found for: %s", objective)
            return None

        description = filtered_objective_df[
            filtered_objective_df["l1_objective_description"].notna()
        ].iloc[0]["l1_objective_description"]

        log.info("Extracted description for objective '%s'", objective)
        return description

    except Exception as exc:
        log.error("Error while extracting objective description for '%s': %s", objective, exc)
        return None


@log_time
def get_samples(
    reference_data: dict[str, Any],
    objective_types: list[str],
    generation_type: str,
) -> list[dict[str, str]]:
    """
    Get examples of argument , counter-arguments and rebuttals
    for the chosen objective if available in database.
    Args:
        reference_data (dict[str, Any]): tenant specific negotiation factory reference data
        objective_types (list[str]): selected objective type
        generation_type (str): type of response being generated
    Returns:
        (list[dict[str, str]] ): sample arguments, counter-arguments and rebuttals
    """
    log.info("get_samples called with generation_type: %s and objective_types: %s", generation_type, objective_types)

    reference_key = negotiation_conf["reference_tables"]["common"]["negotiation_references"]
    objective_df = reference_data.get(reference_key, pd.DataFrame())

    if objective_df.empty:
        log.warning("Reference DataFrame is empty or missing for key: %s", reference_key)
        return [{"example": ""}]

    filtered_objective_df = (
        objective_df[objective_df["l1_objective"].str.lower().isin(objective_types)]
        if objective_types else pd.DataFrame(columns=objective_df.columns)
    )

    log.debug("Filtered DataFrame has %d matching objectives", len(filtered_objective_df))

    if len(filtered_objective_df) > 0:
        filtered_list = filtered_objective_df.to_dict(orient="records")[0].get("samples", [])
        examples = [
            {"example": item.get(generation_type[:-1])}
            for item in filtered_list
            if item.get(generation_type[:-1])
        ]
        examples = random.choices(examples, k=3) if examples else [{"example": ""}]
        log.info("Returning %d examples for generation type: %s", len(examples), generation_type)
        return examples

    log.warning("No examples found for given objective types")
    return [{"example": ""}]

@log_time
def get_argument_conversation_history(
    chat_history_from_db: list,
    generation_type: str,
) -> list[dict[str, Any]]:
    """
    Extracts only those records whose `response_type` matches
    `generation_type` and which actually produced arguments.
    Returns a list of {"user_query": ..., "arguments": [...]}
    where each argument is {"id": ..., "text": ...}.
    """
    log.info("get_argument_conversation_history called for generation_type: %s", generation_type)
    history: list[dict[str, Any]] = []

    for idx, record in enumerate(chat_history_from_db):
        if record.get("response_type") != generation_type:
            continue

        args = record.get("response", {}).get(generation_type, [])
        if not args:
            # no real argument objects here → skip
            continue

        user_query = record.get("request", {}).get("user_query", "")
        simplified_args = [
            {"id": arg["id"], "text": arg["raw"]}
            for arg in args
        ]

        log.debug("  [%d] %r → %d arguments", idx, user_query, len(simplified_args))
        history.append({
            "user_query": user_query,
            "arguments": simplified_args
        })

    log.info("Collected %d argument‐sets for generation_type %s", len(history), generation_type)
    return history[::-1] # reverse order for better context




@log_time
def update_negotiation_details(
    generated_details: list,
    **kwargs: Any,
) -> list[dict[str, Any]]:
    """
    Updates the generated arguments, counter_arguments, emails, rebuttals into
    negotiation details table.
    Args:
        generated_details (list): data to be updated
        kwargs: additional arguments
    Returns:
         (list[dict[str, Any]]): ids of the data updated in table
    """
    log.info("update_negotiation_details called with %d generated items", len(generated_details))

    ids = kwargs.get("previous_ids", []) or [
        f"{round(time.time())}{i}" for i in range(len(generated_details))
    ]
    log.debug("Initial IDs count: %d", len(ids))

    if len(generated_details) > len(ids):
        new_ids = [f"{round(time.time())}{i}" for i in range(len(ids), len(generated_details))]
        ids.extend(new_ids)
        log.debug("Extended ID list to match generated details length: %d", len(ids))

    data_formatted = [
        {"id": ids[i], "raw": data[0], "details": data[-1]} for i, data in enumerate(generated_details)
    ]
    log.info("Formatted %d records for update", len(data_formatted))
    return data_formatted

@log_time
def get_modified_insights(insights: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Modify extracted insights from database into appropriate format
    Args:
        insights (list[dict[str, Any]]): list of insights extracted from database
    Returns:
        (list[dict[str, Any]]): list of modified insights
    Raises:
        NegotiationFactoryUserException when there are no insights or objectives
    """
    log.info("get_modified_insights called with %d insights", len(insights))

    if insights:
        modified = [
            {
                "id": insight.get("insight_id", str(i)),
                "insight": insight.get("label") or insight.get("objective_summary"),
                "insight_objective": insight.get("objective"),
                "insight_reinforcements": insight.get("reinforcements", ""),
                "analytics_name": insight.get("analytics_name", ""),
                "list_of_skus": [],
            }
            for i, insight in enumerate(insights)
            if insight.get("label") or insight.get("objective_summary")
        ]
        log.info("Modified %d insights", len(modified))
        return modified

    log.warning("No insights or objectives found to modify")
    message = (
        "Apologies, but at the moment, "
        """we dont have any insights or objectives for the supplier"""
    )
    raise NegotiationFactoryUserException(message)

@log_time
def fetch_insights_for_supplier(
    objectives_in_action: list[dict[str, Any]] = None,  # type: ignore
    objective_types_lower: list[str] = None,  # type: ignore
    pinned_elements: dict[str, Any] = None,  # type: ignore
) -> list[dict[str, Any]]:
    """
    This function fetch insights for the supplier from database.
    It has optional parameter such as objective and reinforcements to filter the insights
    Args:
        objectives_in_action (list[str]): filtered objectives which we can use in argument
                                          generation
        objective_types_lower (list[str]): objective name in lower case
        pinned_elements (dict[str, Any]): Pinned elements including insights
    Returns:
        (list[dict[str]]): list of insight with details such as id, objective reinforcements
    """
    log.info("fetch_insights_for_supplier called")
    all_analytic_names: list[str] = []
    if objectives_in_action:
        for objective in objectives_in_action:
            for analytic_name in objective.get("analytics_names", []):
                if analytic_name not in all_analytic_names:
                    all_analytic_names.append(analytic_name)
        log.debug("Extracted analytic names from objectives: %s", all_analytic_names)

    filtered_insights: list[dict[str, Any]] = []
    sku_list = pinned_elements.get("skus", []) if pinned_elements else []
    sku_ids = [sku.get("id") for sku in sku_list if sku.get("id")]
    log.debug("Extracted SKU IDs from pinned elements: %s", sku_ids)
    insights = pinned_elements.get("insights", []) if pinned_elements else []

    for insight in insights:
        analytics_name = insight.get("analytics_name", "").lower()
        insight_objective = insight.get("insight_objective", "").lower()

        if (
            analytics_name == "general insights"
            or analytics_name in all_analytic_names
            or insight_objective in (objective_types_lower or [])
        ):
            # insight_skus = [
            #     sku.get("id") for sku in insight.get("list_of_skus", []) if sku.get("id")
            # ]
            insight_skus = insight.get("list_of_skus", [])

            if not insight_skus or any(sku_id in sku_ids for sku_id in insight_skus):
                filtered_insights.append(insight)
    log.info("Filtered %d relevant insights", len(filtered_insights))
    return filtered_insights

@log_time
def fetch_insights_for_supplier_v1(
    objective_types_lower,  # type: ignore
    nego_insights,  # type: ignore
) :
    """
    This function fetch insights for the supplier based on objective types.
    Args:
        objective_types_lower (list[str]): objective name in lower case
        nego_insights (dict[str, Any]): Pinned elements including insights
    Returns:
        (dict[str, list[str]]): dictionary with objective type names as keys and associated insights as values
    """

    # Initialize dictionary to store filtered insights by objective type
    filtered_insights = {}
    # Loop through all insights in the nego_insights
    if nego_insights:
        for objective_type, data in nego_insights.items():
            # Check if any element in objective_types_lower is contained within the objective_type
            
            if objective_type.lower() == 'opportunity':
                for objective_opportunity, data_ in nego_insights['Opportunity'].items():
                    if len(data_.get('insight', [])) > 0:
                        filtered_insights[objective_opportunity] = data_.get('insight', [])
            elif len(data) > 0:
                filtered_insights[objective_type] = data

    
    return filtered_insights




@log_time
def filter_insight_by_reinforcement(
    insights: list[dict[str, Any]],
    reinforcement: str,
) -> list[dict[str, Any]]:
    """
    filter insights based on matched reinforcements
    Args:
        insights (list[dict[str, Any]]) : list of insights need to be filtered
        reinforcement (str): reinforcements to filter with
    Returns:
        list[dict[str, Any]]: returns filtered insight
    """
    log.info("Filtering insights with reinforcement: %s", reinforcement)
    filtered = [insight for insight in insights if reinforcement in insight["insight_reinforcements"]]
    log.info("Filtered %d insights with reinforcement match", len(filtered))
    return filtered


@log_time
def ensure_key_exist(
    required_key: str,
    source_dict: dict[str, Any],
    can_inform_user: bool = False,
    return_element: bool = False,
) -> Any:
    """
    The function checks whether a specific key is present in a dictionary
    and returns the corresponding value if needed.
    Args:
        required_key (str): The key to be checked in the dictionary.
        source_dict (dict[str, Any]): The dictionary where the key is to be checked.
        can_inform_user (bool): If True, the user can be informed if the key is missing.
                        If False, the user cannot be informed as it's an internal matter.
        return_element (bool): If True, the function returns the corresponding value of the key.
                                If False, it only checks for the key's presence.
    Returns:
        (Any): Returns the corresponding value of the key if asked, otherwise None.
    Raises:
        NegotiationFactoryUserException: Raised when the key is missing and user can be informed.
        NegotiationFactoryException: Raised when key is missing but the user cannot be informed.
    """
    if required_key not in source_dict:
        if can_inform_user:
            error_msg = f"{required_key} is Not available."
            log.error("User-visible key missing: %s", error_msg)
            raise NegotiationFactoryUserException(error_msg)
        error_msg = f"{required_key} is missing."
        log.error("Internal key missing: %s", error_msg)
        raise NegotiationFactoryException(error_msg)

    log.debug("Key '%s' found in source dict", required_key)
    return source_dict[required_key] if return_element else None


@log_time
def convert_qna_to_string(qna_list: list[list[dict[str, Any]]]) -> str:
    """
    takes list of qna as argument and convert it into a multiline string of question and answer
    Args:
        qna_list (list[list[dict[str, Any]]]): list of question and answer
    Returns:
        (str) : multiline string with question and answer
    """
    if qna_list and qna_list[0]:
        log.info("Converting %d QnA pairs to string", len(qna_list[0]))
        result = " ,".join(
            [f"answer: {qna['answer']} question: {qna['question']}" for qna in qna_list[0]],
        )
    else:
        log.info("No QnA pairs to convert")
        result = ""
    return result

@log_time
def extract_qa_context(
    pg_db_conn: PGConnector,
    category_name: str,
    supplier_name: str,
    sku_list: list,
) -> tuple[str, str, str]:
    """
    Extract the context needed for general purpose queries
    Args:
        pg_db_conn (PGConnector): Connection object to postgres database
        category_name (str): The name of the category selected
        supplier_name (str): The name of the supplier if available
        sku_list (list): list of skus for the supplier
    Returns:
        (tuple[str, str, str]): The category qna, supplier qna and the sku qna formatted
        as a string for LLM calls
    """
    log.info("Extracting QnA context for category: '%s', supplier: '%s', with %d SKUs", category_name, supplier_name, len(sku_list))

    sku_cond = (
        f"""or {pg_db_conn.get_condition_string(("sku_id", "in", sku_list))}""" if sku_list else ""
    )
    filter_condition = " ".join(
        [
            pg_db_conn.get_condition_string(("category_name", "=", category_name)),
            "or",
            pg_db_conn.get_condition_string(("supplier_name", "=", supplier_name)),
            sku_cond,
        ],
    )

    log.debug("QnA filter condition: %s", filter_condition)

    extracted_qna = pg_db_conn.select_records_with_filter(
        table_name=negotiation_conf["tables"]["qna_view"],
        filter_condition=filter_condition,
    )

    df_qna = pd.DataFrame(extracted_qna)
    log.info("Fetched QnA records: %d", len(df_qna))

    qna_column = negotiation_conf["qna_column"]
    category_qna, supplier_qna, sku_qna = [], [], []

    if not df_qna.empty:
        category_qna = df_qna.loc[
            (df_qna["category_name"] == category_name)
            & (df_qna["supplier_name"].isna())
            & (df_qna["sku_id"].isna()),
            qna_column,
        ].to_list()
        supplier_qna = df_qna.loc[
            (df_qna["category_name"] == category_name)
            & (df_qna["supplier_name"] == supplier_name)
            & (df_qna["sku_id"].isna()),
            qna_column,
        ].to_list()
        sku_qna = df_qna.loc[
            (df_qna["category_name"] == category_name)
            & (df_qna["supplier_name"].isna())
            & (df_qna["sku_id"].isin(sku_list)),
            qna_column,
        ].to_list()

        log.debug("Category QnA count: %d | Supplier QnA count: %d | SKU QnA count: %d", len(category_qna), len(supplier_qna), len(sku_qna))

        return (
            convert_qna_to_string(category_qna),
            convert_qna_to_string(supplier_qna),
            convert_qna_to_string(sku_qna),
        )

    log.warning("No QnA records found for category '%s' and supplier '%s'", category_name, supplier_name)
    return ("", "", "")


@log_time
def extract_model_context(
    reference_data: dict[str, Any],
    pg_db_conn: PGConnector,
    sf_client: SnowflakeClient,
    category: str,
    user_query: str,
    pinned_elements: dict[str, Any],
    pinned_objective_types: list[str],
    elements_required: bool = True,
) -> tuple:
    """
    Extracts the model context for each of the models
    Args:
        reference_data (dict[str, Any]) : tenant specific negotiation factory reference data
        pg_db_conn (PGConnector) : Connection object to postgres database
        category (str): user selected category
        user_query (str) : received user query
        pinned_elements (dict): Dictionary of pinned elements
        pinned_objective_types (list[str]): pinned negotiation objective types
        elements_required (bool): Are all elements required
    """
    log.info("Extracting model context for category '%s'", category)

    supplier_name, supplier_profile = get_supplier_profile(
        pg_db_conn=pg_db_conn,
        sf_client=sf_client,
        category=category,
        user_query=user_query,
        pinned_elements=pinned_elements,
        elements_required=elements_required,
    )

    log.debug("Resolved supplier name: '%s'", supplier_name)
    log.debug("Supplier profile keys: %s", list(supplier_profile.keys()) if isinstance(supplier_profile, dict) else "Invalid format")

    objective_descriptions: list[str] = []

    return (
        supplier_name,
        supplier_profile,
        objective_descriptions,
    )


@log_time
def get_negotiation_model_context(
    pg_db_conn: PGConnector,
    sf_client: SnowflakeClient,
    category: str,
    user_query: str,
    pinned_elements: dict[str, Any],
    generation_type: str,
    is_all_objectives_in_action: bool = False,
    reference_data: dict[str, Any] = {},
    current_round: int = 1,
) -> dict[str, Any]:
    """
    Generated the context needed by argument, counter-argument and rebuttal models
    Args:
        reference_data (dict[str, Any]): tenant specific negotiation factory reference data
        pg_db_conn (PGConnector) : Connection object to postgres database
        category (str): user selected category
        user_query (str) : received user query
        pinned_elements (dict[str, Any]): Pinned elements including insights
        selected_elements (dict[str, Any]): Selected elements including argument
        objective_types (list[str]): negotiation objective from the payload
        generation_type (str): Type of output generated e.g. arguments, counter_arguments, rebuttals
        is_all_objectives_in_action(bool): if we need to consider all objectives
        current_round (int): current round of negotiation
    Returns:
        (dict[str, Any]): model context"""

    def get_strategy_approach_list(
        pinned_elements: dict[str, Any],
        strategy_type: str,
    ) -> list[str]:
        """
        Take the negotiation strategy or negotiation approach object and returns a list
        Args:
            pinned_elements (dict[str, Any]): Pinned elements from the UI
            strategy_type (str): negotiation_approach or negotiation_strategy
        Returns:
            (list[str]): The parses dictionary to be used as context in arguments
        """
        value = pinned_elements.get(strategy_type, {})
        return [
            (
                f"""**{key.capitalize().replace("_", " ")}**: """
                f"""{item.get("value", "")} - """
                f"""{item.get("details", "")}"""
            )
            for key, item in value.items()
            if isinstance(item, dict) and item.get("value", "")
        ]

    # pylint: disable=R0801
    objectives_in_action = identify_negotiation_objective(
        pinned_elements=pinned_elements,
        is_all_objectives_in_action=is_all_objectives_in_action,
    )
    objective_types = [
        objective.get("objective_type", "")
        for objective in objectives_in_action
        if objective.get("objective_type", "").lower() != "key facts"
    ]
    objective_types_lower = [objective_type.lower() for objective_type in objective_types]
    (
        supplier_name,
        supplier_profile,
        objective_descriptions,
    ) = extract_model_context(
        reference_data,
        pg_db_conn,
        sf_client,
        category,
        user_query,
        pinned_elements,
        objective_types,
    )
    # pylint: enable=R0801
    nego_insights = pinned_elements.get("nego_insights", {})
    filtered_insights = fetch_insights_for_supplier_v1(
        objective_types_lower=objective_types_lower,
        nego_insights=nego_insights,
    )

    if  reference_data:
        past_examples = get_samples(reference_data, objective_types_lower, generation_type)
        past_examples = [value.get("example") for value in past_examples if value.get("example")]
    else:
        past_examples = []
    sourcing_approach = get_strategy_approach_list(pinned_elements, "negotiation_strategy")
    category_positioning = pinned_elements.get("category_positioning", {})
    supplier_positioning = pinned_elements.get("supplier_positioning", {})
    buyer_attractiveness = pinned_elements.get("buyer_attractiveness", {})
    target_list = [
        "".join(
            [
                (
                    f"""For the objective {objective.get("objective_type", "")}: """
                    if objective.get("objective_type", "")
                    else ""
                ),
                (
                    (
                        f"""(IMPORTANT) Target {objective.get("objective_param", "")} for """
                        "overall portfolio is"
                    )
                    if objective.get("objective_param", "")
                    else ""
                ),
                (
                    f"""{objective.get("target")} {objective.get("unit")}"""
                    if objective.get("target", "")
                    else ""
                ),
                (
                    f"""against a current value of {objective.get("current_value", "")}."""
                    if objective.get("current_value", "")
                    and objective.get("current_value", -1) != 0
                    else ""
                ),
                (
                    (
                        f"""\n (IMPORTANT) Latest offer is {objective.get("current_offer", "")}"""
                        f""" {objective.get("unit")}"""
                    )
                    if objective.get("current_offer", "")
                    else ""
                ),
                (
                    (
                        "\n(IMPORTANT) Supplier's reason for not accepting offer"
                        f"""{objective.get("reason", "")}"""
                    )
                    if objective.get("reason", "")
                    else ""
                ),
            ],
        )
        for objective in objectives_in_action
    ]
    target_list = [target for target in target_list if target]
    sku_data = [json.dumps(sku, indent=4) for sku in pinned_elements.get("skus", [])]
    sku_str = "\n ".join(sku_data)

    prioritization = (pinned_elements.get("tone_and_tactics", {}) or {}).get("prioritize", {})

    carrots = pinned_elements.get("carrots", []) # if current_round > 1 else []
    carrots = [
        (
            f"""{i+1} {carrot.get("title", "")}: """
            f"""{carrot.get("parameter", "")} {carrot.get("value", "")}"""
        )
        for i, carrot in enumerate(carrots)
        if (carrot or {}).get("title", "") and (carrot or {}).get("description", "")
    ]
    carrots = carrots if prioritization.get("carrots", "") != "NA" else []
    sticks = pinned_elements.get("sticks", []) # if current_round > 1 else []
    sticks = [
        (
            f"""{i+1} {stick.get("title", "")}: """
            f"""{stick.get("parameter", "")} {stick.get("value", "")}"""
        )
        for i, stick in enumerate(sticks)
        if (stick or {}).get("title", "") and (stick or {}).get("description", "")
    ]
    sticks = sticks if prioritization.get("sticks", "") != "NA" else []

    log.info("Carrots %s", carrots)
    log.info("Sticks %s", sticks)
    return {
        "supplier_name": supplier_name,
        "supplier_profile": supplier_profile,
        # "objective_descriptions": objective_descriptions,
        "objective_types": objective_types,
        "filtered_objectives": objectives_in_action,
        "filtered_insights": filtered_insights,
        "sourcing_approach": sourcing_approach,
        "category_positioning": (
            f"""{category_positioning.get("value", "")} """
            f"""{category_positioning.get("details", "")}"""
        ),
        "supplier_positioning": (
            f"""{supplier_positioning.get("value", "")} """
            f"""{supplier_positioning.get("details", "")}"""
        ),
        "buyer_attractiveness": buyer_attractiveness,
        "tone": pinned_elements.get("tone_and_tactics", {}),
        "past_examples": past_examples,
        "target_list": target_list,
        "Selected SKUs": sku_str,
        "carrots": carrots,
        "sticks": sticks,
        "priority": prioritization,
    }


def convert_to_response_format(
    response_type: str,
    message: str | None,
    suggested_prompts: list[Any] | dict[str, Any] | None = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Generate a response dictionary based on the provided parameters.
    Args:
        response_type (str): The type of response.
        message (str): The output message for the user query
        suggested_prompts (list): List of suggested prompts
        **kwargs (Any): It can contain any of below parameter based on response type
                    arguments: List of arguments i.e. argument id and details
                    counter_arguments: List of counter-arguments i.e. counter-argument id
                                        and details
                    rebuttals: List of rebuttals i.e. rebuttals id and details
                    insights: List of insights i.e. id, insight and skus
    Returns:
        Dict[str, Any]: A dictionary representing the generated response."""
    return {
        "response_type": response_type,
        "message": message,
        "suggested_prompts": suggested_prompts if suggested_prompts else [],
        **kwargs,
    }


@log_time
def get_negotiation_strategy_data(reference_data: dict[str, Any], category: str) -> dict:
    """
    Get negotiation strategy data from the database for the given category
    Args:
        reference_data (dict[str, Any]): Unique id to determine the tenant
        category (str): Category name user is operating in
    Returns:
         (dict): All positioning and methodology details
    Raises:
        NegotiationFactoryException: if data is not found in the negotiation
                strategy database"""
    
    # [IMPORTANT] This part fetches the category market complexity data[ negotiation strategy] from RDS. The data is not updated with proper category
    # Thereby will reference the data from csv
    
    strategy_df = reference_data[
        negotiation_conf["reference_tables"]["common"]["negotiation_strategy"]
    ]
    
    # filtered_strategy_df = (
    #     strategy_df[strategy_df["TXT_CATEGORY_LEVEL_3"].str.lower() == category.lower()]
    #     if category
    #     else []
    # )

    filtered_strategy_df = (
        strategy_df[strategy_df["category_name"].str.lower() == category.lower()]
        if category
        else []
    )
 
    # strategy_df = pd.read_csv("src/ada/use_cases/negotiation_factory/category_market_complexity.csv")
   

    if len(filtered_strategy_df) > 0:
        negotiation_strategy_data = filtered_strategy_df.to_dict(orient="records")[0]
        return negotiation_strategy_data
    raise NegotiationFactoryException(
        "Data not found in Strategy Database \
        hence negotiation strategy cannot be generated",
    )


@log_time
def identify_negotiation_objective(
    pinned_elements: dict[str, Any],
    is_all_objectives_in_action: bool = False,
) -> list[dict[str, Any]]:
    """
    Identify negotiation objective from pinned objectives
    Args:
        pinned_elements (dict[str, Any]): Pinned elements including objectives
        is_all_objectives_in_action(bool) : should we consider all objectives
    Returns:
        (list[dict[str, Any]]) : list of negotiation objectives
    Raises:
        (NegotiationFactoryUserException): When the objectives pinned are all from
                keyfacts or no objectives are pinned
    """
    log.info("Starting identify negotiation target")
    pinned_objectives = ensure_key_exist(
        "objectives",
        pinned_elements,
        return_element=True,
    )

    # filter pinned objectives for mark as final criterion
    pinned_objectives = [
        objective
        for objective in pinned_objectives
        if (
            True
            if (is_all_objectives_in_action)
            else not objective.get("mark_as_final", False)
            and objective.get("objective_type", "").lower() != "key facts"
        )
    ]

    if len(pinned_objectives) == 0:
        log.info("No active pinned objectives to generate negotiation arguments")
        message = (
            "Currently, there are no active objectives pinned."
            "please pin some objectives which you find important "
            "so that Ada can assist you in preparing for negotiation."
        )
        suggested_prompts = [
            {
                "prompt": negotiation_conf["cta_button_map"]["objective"],
                "intent": "negotiation_objective",
            },
        ]
        raise NegotiationFactoryUserException(message, suggested_prompts)

    return pinned_objectives


def format_details_string(
    prev_step_item: dict[str, Any],
    current_step_item: dict[str, Any],
    header_string: str,
) -> str:
    """
    Format a details string based on previous and current step items.

    This function creates a formatted string that includes a header, previous element details
    (if available), and Ada's reply from the current step.

    Args:
        prev_step_item (dict[str, Any]): A dictionary containing information
        about the previous step.
            Expected keys: 'reference_raw' or 'details'.
        current_step_item (dict[str, Any]): A dictionary containing
        information about the current step.
            Expected key: 'raw'.
        header_string (str): A string to be used as the header for the formatted output.

    Returns:
        str: A formatted string containing the header, previous element details (if available),
             and Ada's reply.

    Note:
        If the previous element is empty (i.e., both 'reference_raw'
        and 'details' are missing or empty),
        the function will only include Ada's reply in the output.
    """
    previous_element = prev_step_item.get("reference_raw", "") or prev_step_item.get("details", "")
    if previous_element:
        detail_string = (
            f"""{header_string}"""
            + (
                f"{prev_step_item.get('reference_raw', '')}"
                or f"{prev_step_item.get('details', '')}"
            )
            + "\n"
            + " **Ada's reply ** \n"
            + f"""{current_step_item["raw"]}"""
        )
    else:
        detail_string = " **Ada's reply ** \n" + f"""{current_step_item["raw"]}"""
    return detail_string


def json_regex(response: str, json_keys: list) -> dict[str, str]:
    """
    Takes the malformed json response and returns a valid json after regex
    Args:
        response (str): Malformed GenAI json response
        json_keys (list): list of expected json keys
    Returns:
        (dict): Correct json with the expected keys
    """
    response = re.sub(r"[:'\"{}]+", "", response)
    response_dict = {}
    for i, key in enumerate(json_keys):
        if len(re.split(key, response, flags=re.IGNORECASE)) >= 2:
            val = re.split(key, response, flags=re.IGNORECASE)[1]
            response_dict[key] = (
                next(iter(re.split(json_keys[i + 1], val, flags=re.IGNORECASE)))
                if i < (len(json_keys) - 1)
                else val
            )
            response_dict[key] = response_dict[key].strip()
            response_dict[key] = (
                ""
                if all(char in string.punctuation for char in response_dict[key])
                else response_dict[key]
            )
    return response_dict


def get_workflow_suggested_prompts(
    pinned_elements: dict[str, Any],
    need_supplier_profile_check: bool = True,
    include_insights: bool = True,
    starts_with: str = "",
    current_step: str = "",
    strategy_flow: bool = False,
) -> list[dict[str, str]]:
    """
    Get Negotiation workflow (i.e. Objective/arguments/counter-arguments/rebuttal/email)
    related prompts if user has not pinned the appropriate output
    Args:
        pinned_elements (dict[str, Any]): pinned elements received in payload
        need_supplier_profile_check (bool): True if we need to check supplier profile
                                        in pinned elements else False
        include_insights (bool): if True, include insights related suggested prompts
                            along with suggested prompts for objective
        starts_with (str): String if we need to remove steps from the workflow
        current_step (str): String of current step to ensure its not on the suggested prompts.
        strategy_flow (bool): If its a strategy workflow
    Returns:
        (list[dict[str, str]]): list of suggested prompts for workflow
    """
    suggested_prompts: list[dict] = []
    if need_supplier_profile_check and not pinned_elements.get("supplier_profile"):
        return suggested_prompts
    model_workflow = (
        copy.deepcopy(negotiation_conf["strategy_flow"])
        if strategy_flow
        else copy.deepcopy(negotiation_conf["new_workflow"])
    )
    if starts_with and starts_with in model_workflow:
        model_workflow.remove(starts_with)

    # Added below if condition to remove the entry from workflow if the item is already pinned
    selected_entries = get_pinned_workflow_entries(selected=pinned_elements)
    for item in selected_entries:
        if item in model_workflow:
            model_workflow.remove(item)
    if len(model_workflow) == 0:
        return suggested_prompts
    model = ""
    for i, model in enumerate(reversed(model_workflow[:-1])):
        if model in pinned_elements or f"negotiation_{model}" in pinned_elements:
            next_model = model_workflow[len(model_workflow) - i - 1]
            if next_model != current_step:
                suggested_prompts.append(
                    {
                        "prompt": negotiation_conf["cta_button_map"][next_model].capitalize(),
                        "intent": f"negotiation_{next_model}",
                    },
                )
                log.info("next model %s", next_model)
                if next_model == "emails":
                    suggested_prompts.append(
                        {
                            "prompt": negotiation_conf["cta_email_map"][
                                "negotiation_emails_reply_to_supplier"
                            ],
                            "intent": "negotiation_emails_reply_to_supplier",
                        },
                    )
            return suggested_prompts
    if model:
        suggested_prompts.append(
            {
                "prompt": negotiation_conf["cta_button_map"][model].capitalize(),
                "intent": f"negotiation_{model}",
            },
        )
        log.info("next model %s", model)
        if "emails" in model:
            suggested_prompts.append(
                {
                    "prompt": negotiation_conf["cta_email_map"][
                        "negotiation_emails_reply_to_supplier"
                    ],
                    "intent": "negotiation_emails_reply_to_supplier",
                },
            )
        if include_insights:
            suggested_prompts.append(
                {
                    "prompt": negotiation_conf["cta_button_map"]["insights"],
                    "intent": "negotiation_insights",
                },
            )
    return suggested_prompts


def check_intents(data: dict | list, function_map: dict) -> None:
    """
    Recursively check if all intents in the given data structure are present in the function map.

    This function traverses through a nested dictionary or list structure,
    looking for 'intent' keys. When found, it verifies if the corresponding
    intent value exists in the provided function map.

    Args:
        data (Union[Dict, List]): The data structure to check. Can be a dictionary or a list,
                                  potentially nested with multiple levels.
        function_map (Dict[str, Any]): A dictionary mapping intent names\
              to their corresponding functions.

    Raises:
        ValueError: If an intent is found that is not present in the function map.

    Notes:
        - The function recursively checks nested dictionaries and lists.
        - It specifically looks for keys named 'intent' in dictionaries.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "intent":
                if value not in function_map:
                    raise ValueError(f"Intent '{value}' not found in function_map")
            else:
                check_intents(value, function_map)
    elif isinstance(data, list):
        for item in data:
            check_intents(item, function_map)


def get_probable_intent(previous_response: str) -> str:
    """
    Determines the probable intent based on previous response
    Args:
        previous_response (str): Type of previous response
    Returns:
        (str) probable current intent
    """
    next_intent_dict = {
        "arguments_modify": "arguments_generic",
        "arguments_reply": "rebuttals",
        "counter_arguments_modify": "counter_arguments",
        "rebuttals_modify": "rebuttals",
        "negotiation_counter_arguments_reply": "rebuttals",
        "negotiation_emails": "emails_generic",
        "negotiation_emails_continue": "emails_generic",
        "negotiation_emails_reply_to_supplier": "emails_generic",
        "negotiation_emails_new": "emails_generic",
        "negotiation_emails_modify": "emails_generic",
    }

    probable_intent = next_intent_dict.get(previous_response, "")
    log.info("Probable intent %s", probable_intent)
    return probable_intent


def get_strategy_suggested_prompt(
    ai_response: dict[str, str],
    generation_type: str = "",
) -> list[dict[str, str]]:
    """
    This function returns suggested prompts from ai response.
    related prompts if user has not pinned the appropriate output
    Args:
        ai_response (dict[str, str]): ai response from generate strategy call
        generation_type (str): intent value received from frontend
    Returns:
        (list[dict[str, str]]): list of suggested prompts for workflow
    """
    result = []
    for item in ai_response.get("suggested_prompts", []):
        holder = {}
        flag = False
        if isinstance(item, dict):
            holder["prompt"] = item.get("prompt", "")
            flag = (
                generation_type in ["negotiation_approach_cp", "negotiation_approach_sp"]
            ) and item.get("prompt", "").startswith("Set ")
        else:
            holder["prompt"] = item.capitalize()
            flag = item.capitalize().startswith("Set ")

        if flag:
            holder["intent"] = ai_response.get("request_type") or (
                "negotiation_approach_sp"
                if (generation_type == "negotiation_approach_cp")
                else "negotiation_approach_cp"
            )
        else:
            holder["intent"] = ai_response.get("request_type") or "negotiation_strategy_change"

        result.append(holder)
    return result


def get_pinned_workflow_entries(selected: dict[str, Any]) -> list:
    """
    This function returns workflow entries if corresponding item is in pinned section.

    Args:
        selected (dict[str, Any]): Pinned elements including supplier profile

    Returns:
        result (list): list of pinned workflow entries.
    """
    section_map = negotiation_conf["section_vs_intent"]
    result = []
    for key in selected.keys():
        if key in section_map.keys():
            result.append(section_map[key])

    return result


def get_generation_type(
    cta_map: dict[str, str],
    user_query: str,
    threshold: float,
    default_str: str,
) -> str:
    """Generates the generation type for a user query based on similarity

    Args:
        cta_map (dict[str, str]): The cta map from which we find the best match
        user_query (str): The user query
        threshold (float): cut off value
        default_str: defaults
    Returns:
        str: _description_
    """

    matched_str = get_best_match_from_list(
        list(cta_map.values()),
        user_query,
        threshold=threshold,
        similarity_model=negotiation_conf["model"]["similarity_model"],
    )
    log.info("Matched str %s", matched_str)
    cta_maps = list(cta_map.values())
    generation_type_index = cta_maps.index(matched_str) if matched_str else -1  # type: ignore
    generation_type = (
        list(cta_map.keys())[generation_type_index] if generation_type_index != -1 else default_str
    )
    log.info("Generation type %s", generation_type)

    return generation_type


def get_airesponse_as_dict(response: str, response_keys: list) -> dict:
    """
    Get response back as a dictionary

    Args:
        response (str): response from conversational chat
        response_keys list(str): names of the response_keys
    Returns:
        dict: dictionary made from response
    """
    try:
        ai_response = json.loads(response)
    except json.decoder.JSONDecodeError as json_loads_exception:
        log.info("Json decode error %s", str(json_loads_exception))
        ai_response = json_regex(response, response_keys)
        val = ai_response["suggested_prompts"]
        val = val.split("[")[1] if len(val.split("[")) >= 2 else val
        val = next(iter(val.split("]")))
        ai_response["suggested_prompts"] = val.split(",")
        for key, value in ai_response.items():
            if key != "suggested_prompts":
                ai_response[key] = value.split("[")[0]

    return ai_response


def get_prompts_to_be_removed(
    generation_type: str,
    pinned_elements: dict[str, Any],
    user_query: str = "",
) -> list[str]:
    """
    Get updated prompts for category/supplier positioning, sourcing approach as per pinned elements

    Args:
        generation_type (str): intent
        pinned_elements (dict[str, Any]): elements pinned by the user
    Returns:
        list[str]: list of items to be removed from suggested prompts
    """
    remove_list = []
    set_cat_pos = "Set category positioning"
    change_cat_pos = "Change category positioning"
    set_sup_pos = "Set supplier positioning"
    change_sup_pos = "Change supplier positioning"
    set_buy_pos = "Set buyer positioning"
    change_buy_pos = "Change buyer positioning"
    set_sou_appr = "Set sourcing approach"
    change_sou_appr = "Change sourcing approach"
    set_ton_tac = "Set tone & tactics"
    change_ton_tac = "Change tone & tactics"
    set_carrots_sticks = "Set carrots & sticks"
    change_carrot_sticks = "Change carrots & sticks"

    sourcing_approach_group_names = [
        "Change market approach",
        "Change pricing methodology",
        "Change contracting methodology",
    ]

    cat_pos_present = "category_positioning" in pinned_elements.keys()
    sup_pos_present = "supplier_positioning" in pinned_elements.keys()
    buy_pos_present = "buyer_attractiveness" in pinned_elements.keys()
    sou_appr_present = "negotiation_strategy" in pinned_elements.keys()
    ton_tac_present = "tone_and_tactics" in pinned_elements.keys()
    carrot_stick_present = "carrots" in pinned_elements.keys() or "sticks" in pinned_elements.keys()

    # Handling category/supplier/buyer positioning
    if generation_type == "negotiation_approach_cp":
        remove_list.extend([set_cat_pos, set_sup_pos if (sup_pos_present) else change_sup_pos])
        remove_list.extend([set_buy_pos if (buy_pos_present) else change_buy_pos])
        remove_list.extend([set_carrots_sticks if (carrot_stick_present) else change_carrot_sticks])
    elif generation_type == "negotiation_approach_sp":
        remove_list.extend([set_cat_pos if (cat_pos_present) else change_cat_pos, set_sup_pos])
        remove_list.extend([set_buy_pos if (buy_pos_present) else change_buy_pos])
        remove_list.extend([set_carrots_sticks if (carrot_stick_present) else change_carrot_sticks])
    elif generation_type == "negotiation_approach_bp":
        remove_list.extend(
            [
                set_buy_pos,
                change_buy_pos,
                set_cat_pos if (cat_pos_present) else change_cat_pos,
                set_sup_pos if (sup_pos_present) else change_sup_pos,
            ],
        )
    elif generation_type == "negotiation_select_carrots_sticks":
        remove_list.extend(
            [
                set_carrots_sticks,
                change_carrot_sticks if ("change " in user_query.lower()) else set_carrots_sticks,
                set_cat_pos if (cat_pos_present) else change_cat_pos,
                set_sup_pos if (sup_pos_present) else change_sup_pos,
                set_buy_pos if (buy_pos_present) else change_buy_pos,
            ],
        )
    else:
        remove_list.extend(
            [
                set_cat_pos if (cat_pos_present) else change_cat_pos,
                set_sup_pos if (sup_pos_present) else change_sup_pos,
                set_buy_pos if (buy_pos_present) else change_buy_pos,
                set_carrots_sticks if (carrot_stick_present) else change_carrot_sticks,
            ],
        )

    # Handling sourcing approach
    if sou_appr_present:  # if set sourcing approach pinned
        remove_list.extend([set_sou_appr])
    else:  # Set sourcing approach is not pinned or called for the first time
        if generation_type == "negotiation_strategy":
            remove_list.extend(
                [
                    set_sou_appr,
                    change_sou_appr,
                    set_cat_pos,
                    change_cat_pos,
                    set_sup_pos,
                    change_sup_pos,
                    set_buy_pos,
                    change_buy_pos,
                ],
            )
        else:
            remove_list.extend(sourcing_approach_group_names)

    # Handling tones & tactics
    remove_list.extend([f"{set_ton_tac if ton_tac_present else change_ton_tac}"])

    # Handling change sourcing approach/category-supplier positioning
    if generation_type == "negotiation_strategy_change":
        remove_list = [
            f"{set_cat_pos if cat_pos_present else change_cat_pos}",
            f"{set_sup_pos if sup_pos_present else change_sup_pos}",
            f"{set_buy_pos if buy_pos_present else change_buy_pos}",
            f"{set_sou_appr if sou_appr_present else change_sou_appr}",
            f"{set_ton_tac if ton_tac_present else change_ton_tac}",
        ]
        remove_list.extend(sourcing_approach_group_names)

    # Handling change sourcing approach corner case
    if generation_type in ["negotiation_strategy", "negotiation_strategy_change"]:
        if "change sourcing" in user_query.lower() or "change to " in user_query.lower():
            remove_list = [
                set_cat_pos,
                change_cat_pos,
                set_sup_pos,
                change_sup_pos,
                set_buy_pos,
                change_buy_pos,
                set_sou_appr,
                change_sou_appr,
                f"{set_ton_tac if ton_tac_present else change_ton_tac}",
            ]
    return remove_list


# def process_approach_response_key_content(
#     supplier_profile: str,
#     ai_response: dict,
#     init_message: str,
#     generation_type: str,
#     pinned_elements: dict[str, Any],
# ) -> dict:
#     """
#     Process parameter of the response

#     Args:
#         supplier_profile (str): response from conversational chat
#         ai_response (str): ai response as dict
#         init_message (str): iniitial heading of the message
#         generation_type (str): intent
#         pinned_elements (dict[str, Any]): elements pinned by the user
#     Returns:
#         dict: transformed param as a dictionary
#     """
#     section_name = (
#         "Create Negotiation Approach"
#         if (
#             generation_type
#             in [
#                 "negotiation_approach_cp",
#                 "negotiation_approach_sp",
#                 "negotiation_approach_bp",
#             ]
#         )
#         else ""
#     )
#     suggested_prompts = get_section_suggested_prompts(
#         section_name=section_name,
#     )
#     message = [
#         (
#             f"""**{key.capitalize().replace("_", " ")}**: {ai_response.get(key)} - """
#             f"""{ai_response.get(f"{key}_detail", "")}"""
#         )
#         for key in negotiation_conf[f"{generation_type}_keys"]
#     ]
#     params = {
#         "response_type": generation_type,
#         "message": (
#             init_message + "\n".join(message)
#             or ai_response.get("message", "").replace("\n\n", "\n")
#         ),
#         "supplier_profile": supplier_profile,
#     }

#     params[
#         (
#             "category_positions"
#             if (generation_type == "negotiation_approach_cp")
#             else "supplier_positions"
#         )
#     ] = [
#         {
#             "value": ai_response.get(key, "").title(),
#             "details": ai_response.get(f"{key}_detail", ""),
#         }
#         for key in negotiation_conf[f"{generation_type}_keys"]
#     ]
#     params["message"] = init_message.replace("\n\n", "\n").replace("\n", "")
#     if generation_type in [
#         "negotiation_approach_cp",
#         "negotiation_approach_sp",
#         "negotiation_approach_bp",
#     ]:
#         remove_list: list[str] = []
#         remove_list = get_prompts_to_be_removed(
#             generation_type=generation_type,
#             pinned_elements=pinned_elements,
#         )

#         remove_list.extend(
#             [
#                 (
#                     f"{'Set' if 'negotiation_strategy' in pinned_elements.keys() else 'Change'}"
#                     " sourcing approach"
#                 ),
#                 (
#                     f"{'Set' if 'tone_and_  stactics' in pinned_elements.keys() else 'Change'}"
#                     " tone & tactics"
#                 ),
#                 "Change market approach",
#                 "Change pricing methodology",
#                 "Change contracting methodology",
#             ],
#         )
#         suggested_prompts = [
#             prompt for prompt in suggested_prompts if prompt["prompt"] not in remove_list
#         ]
#     params["suggested_prompts"] = get_distinct_suggested_prompts(
#         prompts=suggested_prompts,
#     )

#     return params

def process_approach_response_key_content(
    supplier_profile: str,
    ai_response: dict,
    init_message: str,
    generation_type: str,
    pinned_elements: dict[str, Any],
) -> dict:
    """
    Process parameter of the response

    Args:
        supplier_profile (str): response from conversational chat
        ai_response (dict): ai response as dict
        init_message (str): initial heading of the message
        generation_type (str): intent
        pinned_elements (dict[str, Any]): elements pinned by the user
    Returns:
        dict: transformed param as a dictionary
    """
    section_name = (
        "Create Negotiation Approach"
        if generation_type in [
            "negotiation_approach_cp",
            "negotiation_approach_sp",
            "negotiation_approach_bp",
        ]
        else ""
    )

    suggested_prompts = get_section_suggested_prompts(section_name=section_name)

    message = [
        f"**{key.capitalize().replace('_', ' ')}**: {ai_response.get(key)} - {ai_response.get(f'{key}_detail', '')}"
        for key in negotiation_conf[f"{generation_type}_keys"]
    ]

    params = {
        "response_type": generation_type,
        "message": (init_message + "\n".join(message)) or ai_response.get("message", "").replace("\n\n", "\n"),
        "supplier_profile": supplier_profile,
    }

    # Full positioning maps with descriptions
    CATEGORY_POSITIONING_MAP = {
        "leverage": "This positioning suggests that the category has a high potential for cost savings and efficiency improvements. By leveraging volume and negotiating power, you can achieve better terms and lower prices. Typically, 60-80% of procurement savings can be realized through leverage strategies.",
        "shop": "This approach focuses on competitive bidding and shopping around for the best deals. It is ideal when there are multiple suppliers and the market is competitive, allowing for price reductions of up to 20%.",
        "bottleneck": "Categories in this position are critical but have limited suppliers, leading to potential supply risks. Managing these requires strategic planning to ensure continuity, often resulting in a 10-15% increase in security of supply.",
        "strategic partnership": "This involves forming long-term relationships with key suppliers to drive innovation and value. It can lead to a 15-30% improvement in service levels and collaborative growth."
    }

    SUPPLIER_POSITIONING_MAP = {
        "ramp down": "Consider ramping down suppliers that are underperforming or not aligning with strategic goals. This can free up resources and reduce costs by 15-20%, allowing focus on more beneficial partnerships.",
        "grow": "Focus on growing relationships with suppliers that show potential for increased collaboration. This can lead to improved terms and conditions, potentially saving 10% on procurement costs and enhancing supply chain resilience.",
        "core": "Identify core suppliers that are critical to operations. Strengthening these relationships can ensure stability and reliability, reducing risks by 25% and securing long-term benefits.",
        "nuisance": "Suppliers that consistently cause issues or require excessive management should be categorized as nuisances. Redirecting efforts away from these can improve efficiency by 30% and allow focus on more strategic partnerships."
    }

    is_category = generation_type == "negotiation_approach_cp"
    position_key = "category_positions" if is_category else "supplier_positions"
    position_map = CATEGORY_POSITIONING_MAP if is_category else SUPPLIER_POSITIONING_MAP
    response_keys = negotiation_conf[f"{generation_type}_keys"]

    selected_position = ai_response.get(response_keys[0], "").strip().lower()

    positions = []
    added = set()

    if selected_position in position_map:
        # Always prioritize AI response detail if present
        detail = ai_response.get(f"{response_keys[0]}_detail")
        positions.append({
            "value": selected_position.title(),
            "details": detail if detail else position_map[selected_position]
        })
        added.add(selected_position)

    for pos, detail in position_map.items():
        if pos not in added:
            positions.append({
                "value": pos.title(),
                "details": detail
            })

    params[position_key] = positions

    params["message"] = init_message.replace("\n\n", "\n").replace("\n", "")

    if generation_type in [
        "negotiation_approach_cp",
        "negotiation_approach_sp",
        "negotiation_approach_bp",
    ]:
        remove_list: list[str] = get_prompts_to_be_removed(
            generation_type=generation_type,
            pinned_elements=pinned_elements,
        )

        remove_list.extend([
            ("Set" if "tone_and_stactics" in pinned_elements.keys() else "Change") + " tone & tactics",
            "Change market approach",
            "Change pricing methodology",
            "Change contracting methodology",
        ])

        suggested_prompts = [
            prompt for prompt in suggested_prompts if prompt["prompt"] not in remove_list
        ]
    # breakpoint()
    # ... your code that prepares init_message, positioning, etc.

# Optional: Default pin tone if generation_type is tone_and_tactics and not already set

    # Override suggested_prompts based on pinned state
    # Determine if objectives are set and contain data
    objectives_present = (
        "objectives" in pinned_elements and 
        isinstance(pinned_elements["objectives"], list) and 
        len(pinned_elements["objectives"]) > 0
    )

    # Helper for dynamic label
    objective_prompt_text = (
        "Change negotiation objectives" if objectives_present else "Set negotiation objectives"
    )

    # Override suggested_prompts based on pinned state
    category_set = "category_positioning" in pinned_elements
    supplier_set = "supplier_positioning" in pinned_elements
    buyer_set = "buyer_attractiveness" in pinned_elements
    tone_set = "tone_and_tactics" in pinned_elements
    carrots_sticks_set = "carrots" in pinned_elements or "sticks" in pinned_elements

    # Conditional overrides based on flow
    if generation_type == "negotiation_approach_cp" and not category_set:
        suggested_prompts = [
            {"prompt": objective_prompt_text, "intent": "negotiation_objective"},
            {"prompt": "Set supplier positioning", "intent": "negotiation_approach_sp"},
            {"prompt": "Set buyer positioning", "intent": "negotiation_approach_bp"},
        ]
    elif generation_type == "negotiation_approach_cp" and category_set:
        suggested_prompts = [
            {"prompt": objective_prompt_text, "intent": "negotiation_objective"},
            {"prompt": "Change category positioning", "intent": "negotiation_strategy_change"},
            {"prompt": "Set supplier positioning", "intent": "negotiation_approach_sp"},
            {"prompt": "Set buyer positioning", "intent": "negotiation_approach_bp"},
        ]
    elif generation_type == "negotiation_approach_sp" and not supplier_set and not buyer_set:
        suggested_prompts = [
            {"prompt": objective_prompt_text, "intent": "negotiation_objective"},
            {"prompt": "Change category positioning", "intent": "negotiation_strategy_change"},
            {"prompt": "Set buyer positioning", "intent": "negotiation_approach_bp"},
        ]
    elif generation_type == "negotiation_approach_bp" and category_set and supplier_set and not buyer_set and not tone_set:
        suggested_prompts = [
            {"prompt": objective_prompt_text, "intent": "negotiation_objective"},
            {"prompt": "Change category positioning", "intent": "negotiation_strategy_change"},
            {"prompt": "Change supplier positioning", "intent": "negotiation_approach_sp"},
            {"prompt": "Set tone & tactics", "intent": "negotiation_approach_tnt"},
        ]
    elif generation_type == "negotiation_approach_bp" and category_set and supplier_set and buyer_set and not tone_set:
        suggested_prompts = [
            {"prompt": objective_prompt_text, "intent": "negotiation_objective"},
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

    return params

def process_strategy_response_key_content(
    supplier_profile: str,
    ai_response: dict,
    init_message: str,
    generation_type: str,
    pinned_elements: dict[str, Any],
    user_query: str,
) -> dict:
    """
    Process parameter of the response

    Args:
        supplier_profile (str): response from conversational chat
        ai_response (str): ai response as dict
        init_message (str): iniitial heading of the message
        generation_type (str): intent
        pinned_elements (dict[str, Any]): elements pinned by the user
        user_query (str): user query from user
    Returns:
        dict: transformed param as a dictionary
    """
    all_prompts = get_section_suggested_prompts(
        section_name="Create Negotiation Approach",
    )
    section = {}
    for item in negotiation_conf["section_vs_ctas_propertise"]:
        if item["section_name"] == "Create Negotiation Approach":
            section = item
            break

    remove_list = get_prompts_to_be_removed(
        generation_type=generation_type,
        pinned_elements=pinned_elements,
        user_query=user_query,
    )

    if generation_type == "negotiation_strategy" and len(all_prompts) == section["size"]:
        sourcing_approach_order = section["begin_with_appoach"]["sequence"]
        all_prompts = [all_prompts[i] for i in sourcing_approach_order]

    suggested_prompts = [prompt for prompt in all_prompts if prompt["prompt"] not in remove_list]
    message = [
        (
            f"""**{key.capitalize().replace("_", " ")}**: {ai_response.get(key)} - """
            f"""{ai_response.get(f"{key}_detail", "")}"""
        )
        for key in negotiation_conf[f"{generation_type}_keys"]
    ]
    params = {
        "response_type": generation_type,
        "message": (
            init_message + "\n".join(message)
            or ai_response.get("message", "").replace("\n\n", "\n")
        ),
        "supplier_profile": supplier_profile,
        "suggested_prompts": suggested_prompts,
    }
    return params


def get_distinct_suggested_prompts(
    prompts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    delete duplicate suggested prompts and send distinct list

    Args:
        prompts (list[dict[str, Any]]): list of suggested prompts
    Returns:
        list[dict[str, Any]]: unique suggested prompt list
    """
    result: list[dict[str, Any]] = []
    for item in prompts:
        if item not in result:
            result.append(item)
    return result


def get_section_suggested_prompts(
    section_name: str,
) -> list[dict[str, Any]]:
    """
    Get Suggested prompts from section name
    Args:
        section_name (str): name of the section
    Returns:
        list[dict[str, Any]]: list of suggested prompts
    """
    section = {}
    suggested_prompts: list[dict[str, Any]] = []

    for item in negotiation_conf["section_vs_ctas"]:
        if item["section_name"] == section_name:
            section = item
            break

    if section["section_name"] in [
        "Select Supplier",
        "Select Negotiation Objectives",
        "Create Negotiation Approach",
        "Define Negotiation Strategy",
        "Generate Arguments",
    ]:  # Section 1, 2, 3, 4, 5
        suggested_prompts = [
            {
                "prompt": key,
                "intent": value,
            }
            for key, value in dict(
                zip(section["ctas"]["prompts"], section["ctas"]["intents"]),
            ).items()
        ]
    elif section["section_name"] == "Generate Emails":  # Section 6
        pass
    else:
        return suggested_prompts
    # breakpoint()
    return suggested_prompts


def get_argument_section_suggested_prompts(
    intent: str,
) -> list[dict[str, str]]:
    """
    get suggested prompt from intent

    Args:
        intent (str): intent
    Returns:
        list[dict[str, Any]]: unique suggested prompt list
    """
    result: list[dict[str, str]] = []

    suggested_prompts = get_section_suggested_prompts(
        section_name="Generate Arguments",
    )
    if intent == "arguments_new":
        add_list = [
            {
                "prompt": "Modify arguments",
                "intent": "negotiation_arguments_modify",
            },
            {
                "prompt": "Generate negotiation counter arguments",
                "intent": "negotiation_counter_arguments",
            },
        ]
        remove_list = ["Generate new arguments"]
        for index, item in enumerate(add_list):
            suggested_prompts.insert(index, item)
        result = [prompt for prompt in suggested_prompts if prompt["prompt"] not in remove_list]
    elif intent == "arguments_modify":
        add_list = [
            {
                "prompt": "Generate negotiation counter arguments",
                "intent": "negotiation_counter_arguments",
            },
        ]
        remove_list = ["Modify arguments"]
        for index, item in enumerate(add_list):
            suggested_prompts.insert(index, item)
        result = [prompt for prompt in suggested_prompts if prompt["prompt"] not in remove_list]
    elif intent == "arguments_reply":
        add_list = [
            {
                "prompt": "Modify reply to supplier arguments",
                "intent": "negotiation_rebuttals_modify",
            },
        ]
        remove_list = ["Reply to supplier arguments"]
        for index, item in enumerate(add_list):
            suggested_prompts.insert(index, item)
        result = [prompt for prompt in suggested_prompts if prompt["prompt"] not in remove_list]
    else:
        result = suggested_prompts
    # breakpoint()
    return result


def perform_argument_prerequisite_check(
    key: str,
    suggested_prompt: list[dict[str, Any]],
    pinned_keys: list[str],
) -> tuple[bool, str, list[dict[str, Any]]]:
    """
    Perform pre-requisite check to procced with argumet flow

    Args:
        key (str): key to check in pinned elements
        suggested_prompt (list[dict[str, Any]]): name of the section
        pinned_keys (list[str]): pinned elements names
    Returns:
        tuple[Literal[True], Literal[''], list[dict[str, Any]]]: tuple of flag, message,
        and suggested prompt
    """
    
    flag: bool = False
    msg: str = ""
    prompts: list[dict[str, Any]] = []
    if key == "objectives":
        if key in pinned_keys:  # Preequisite passed
            flag = False
            msg = ""
            prompts = suggested_prompt
        else:  # Preequisite failed
            flag = True
            msg = (
                "To effectively work with arguments, it's imperative to have objective "
                "pinned/selected."
                "Please select `Set negotiation objectives` to proceed further."
            )
            suggested_prompt.insert(
                0,
                {"prompt": "Set negotiation objectives", "intent": "negotiation_objective"},
            )
            prompts = [
                prompt
                for prompt in suggested_prompt
                if (
                    prompt["prompt"]
                    not in [
                        "Generate new arguments",
                        "Reply to supplier arguments",
                    ]
                )
            ]
    elif key == "arguments":
        if key in pinned_keys:  # Preequisite passed
            flag = False
            msg = ""
            prompts = suggested_prompt
        else:  # Preequisite failed
            flag = True
            msg = (
                "To effectively work with counter arguments, it's imperative to have argument "
                "pinned/selected."
                "Please select `Generate new arguments` to proceed further."
            )
            prompts = suggested_prompt

    return flag, msg, prompts


def perform_offer_prerequisite_check(
    generation_type: str,
    pinned_keys: list[str],
) -> tuple[bool, str, list[dict[str, Any]]]:
    """
    Perform pre-requisite check to procced with offer flow
    Args:
        generation_type (str) : request type from front end
        pinned_keys (list[str]): pinned elements names
    Returns:
        tuple[Literal[True], Literal[''], list[dict[str, Any]]]: tuple of flag, message,
        and suggested prompt
    """
    flag: bool = False
    objectives_flag: bool = "objectives" not in pinned_keys
    message: str = ""
    suggested_prompts: list[dict[str, Any]] = []
    if generation_type != "":  # from CTA
        if objectives_flag:
            flag = True
            suggested_prompts = []
            message = (
                "To effectively work with latest offer and next rounds, "
                "it's imperative to have objective pinned/selected."
                "\nPlease take necessary actions to proceed further"
            )
    else:  # from Ada Chat
        flag = True
        suggested_prompts = []
        message = (
            "Add/Save latest offer is possible through navigation section only."
            "\nPlease click `+ Add Latest Offer` to add offers."
        )
    return flag, message, suggested_prompts


def perform_finish_negotiation_prerequisite_check(
    pinned_keys: list[str],
) -> tuple[bool, str]:
    """
    Perform pre-requisite check to complete the negotiation
    Args:
        pinned_elements (dict[str, Any]): pinned elements names
    Returns:
        tuple[Literal[True], Literal['']]: tuple of flag and message
    """
    flag: bool = False
    objectives_flag: bool = "objectives" not in pinned_keys
    message: str = (
        "To effectively finish the negotiation, "
        "it's imperative to have objective and latest offer to be pinned/selected."
        "\nPlease take necessary actions to proceed further."
    )
    if objectives_flag:
        flag = True

    return flag, message


def clear_chat_history(chat_id: str, pg_db_conn: PGConnector, **kwargs: Any) -> dict[str, Any]:
    """
    Clear chat history from database
    Args:
        chat_id (str): negotiation id
        pg_db_conn (PGConnector): Connection object to postgres database
        kwargs (Any): additional parameters
    Returns:
        (dict[str, Any]): transformed param as a dictionary
    """
    log.info("Clear chat history with additional args %d", len(kwargs))
    pg_db_conn.delete_values(
        table_name=negotiation_conf["tables"]["chat_history_table"],
        conditions={"chat_id": chat_id},
    )
    return convert_to_response_format(
        response_type="clear_chat_success",
        message=f"chat history successfully deleted for negotiation id: {chat_id}",
    )


def convert_insights_to_objectives(
    insights: list[dict[str, Any]],
    objectives: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    convert insights to objectives
    Args:
        insights (list[dict[str, Any]]): list of insights from supplier profile
        objectives (list[dict[str, Any]]): list of objectives from supplier profile
    Returns:
        list[dict[str, Any]]: list of objectives
    """

    def get_analytics_name_fr_insights(
        insights: list[dict[str, Any]],
        insight_objective: str,
    ) -> list[str]:
        analytics_name = []
        for insight in insights:
            if insight.get("insight_objective", "").lower() == insight_objective.lower():
                analytics_name.append(insight.get("analytics_name", ""))
        return analytics_name

    objectives_lst = []
    for objective in objectives:
        holder = {}
        holder["id"] = objective.get("id", "")
        holder["objective"] = objective.get("insight", "")
        holder["objective_type"] = objective.get("insight_objective", "")
        holder["objective_reinforcements"] = objective.get("insight_reinforcements", "")
        holder["list_of_skus"] = objective.get("list_of_skus", "")
        holder["analytics_names"] = get_analytics_name_fr_insights(
            insights=insights,
            insight_objective=objective.get("insight_objective", ""),
        )
        objectives_lst.append(holder)

    return objectives_lst


def weighted_average(group: pd.DataFrame, term: str, average_term: str) -> float:
    """
    calculate weighted average for a group.
    Args:
        group (pd.DataFrame): group of data
    Returns:
        (float): weighted average
    """
    spend_sum = group[average_term].sum()
    if spend_sum == 0:
        return 0
    return (group[average_term] * group[term]).sum() / spend_sum




def get_supplier_profiles( #NOSONAR
    pg_db_conn: PGConnector,
    sf_client: SnowflakeClient,
    category: str,
    supplier_names,
    suggested_prompts
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
    if isinstance(supplier_names, str):
        supplier_names = [supplier_names.lower()]
        log.info("Supplier names %s", supplier_names)
    all_supplier_data = pd.DataFrame(
        sf_client.select_records_with_filter(
            table_name= negotiation_tables["supplier_details"],
            filter_condition=(
                f"""LOWER(category) = LOWER('{category}') AND  YEAR = (SELECT MAX(YEAR)  """
                f"""FROM {negotiation_tables["supplier_details"]}) AND """
                f"""{sf_client.get_condition_string(("LOWER(SUPPLIER)",
                              "in", (supplier_names)))}"""
            ),
        ),
    )
    # all_supplier_data = all_supplier_data.drop_duplicates(subset=["SUPPLIER"], keep="first")
    if all_supplier_data.empty:
        message = f"We could not find the exact {supplier_names[0]} in {category}, for current year."
        if suggested_prompts:
            message += " Is the supplier you are looking for one of these?"
        raise NegotiationFactoryUserException(message, suggested_prompts)

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


    supplier_profile = enrich_supplier_profile(
            all_supplier_data.loc[all_supplier_data["supplier_name"] == supplier_names[0]],
        )
    return supplier_profile


def top_single_sourced_materials(supplier,category,sf_client):
    sql = f"""
    SELECT
    PERIOD,
    CATEGORY_NAME,
    SUPPLIER_NAME,
    SKU_NAME,
    SUM(SPEND_SINGLE_SOURCE_YTD) AS SPEND_ON_SINGLE_SOURCE_MATERIAL,
    FROM
        data.t_c_negotiation_factory_t2
    WHERE
        SUPPLIER_NAME ='{supplier}'
        AND PERIOD = (SELECT MAX(PERIOD) from DATA.T_C_NEGOTIATION_FACTORY_T2)
        AND SPEND_SINGLE_SOURCE_YTD > 0
        AND CATEGORY_NAME = '{category}'
    GROUP BY
        SKU_NAME, CATEGORY_NAME, SUPPLIER_NAME,PERIOD
    ORDER BY
        SPEND_ON_SINGLE_SOURCE_MATERIAL DESC
    LIMIT 3;
    """

    result = sf_client.fetch_dataframe(sql)
    result = result.to_dict(orient='records')

    return result


def spend_increase_yoy_on_supplier(supplier,category,sf_client):
    sql = f"""
    WITH current_year_cte AS (
        SELECT MAX(TO_NUMBER(PERIOD)) AS year_now
        FROM DATA.T_C_NEGOTIATION_FACTORY_T2
    ),
    spend_summary AS (
        SELECT
            SUPPLIER_NAME,
            CATEGORY_NAME,
            SUM(CASE 
                    WHEN TO_NUMBER(PERIOD) = (SELECT year_now - 1 FROM current_year_cte) 
                    THEN SPEND_LAST_YEAR 
                    ELSE 0 
                END) AS total_spend_last_year,
            SUM(CASE 
                    WHEN TO_NUMBER(PERIOD) = (SELECT year_now FROM current_year_cte) 
                    THEN SPEND_YTD 
                    ELSE 0 
                END) AS total_spend_ytd
        FROM
            data.t_c_negotiation_factory_t2
        WHERE
            SUPPLIER_NAME = '{supplier}'
            AND CATEGORY_NAME = '{category}'
            AND TO_NUMBER(PERIOD) IN (
                (SELECT year_now FROM current_year_cte),
                (SELECT year_now - 1 FROM current_year_cte)
            )
        GROUP BY
            SUPPLIER_NAME,
            CATEGORY_NAME
    )
    SELECT
        SUPPLIER_NAME,
        CATEGORY_NAME,
        total_spend_last_year,
        total_spend_ytd,
        total_spend_ytd - total_spend_last_year AS absolute_change_eur,
        ROUND(
            ((total_spend_ytd - total_spend_last_year) / NULLIF(total_spend_last_year, 0)) * 100,
            2
        ) AS percent_change
    FROM
        spend_summary;

    """

    result = sf_client.fetch_dataframe(sql)
    result = result.to_dict(orient='records')

    return result