import json
from typing import Any
from ada.use_cases.negotiation_factory.negotiation_gameplan_components import extract_category_analytic_data
from ada.utils.logs.logger import get_logger
import pandas as pd
import re

from ada.use_cases.negotiation_factory.insight_generation_prompt import (generate_additional_supplier_insights_prompt,generate_market_insight_summary_prompt_v2,generate_insights_prompt_v2, generate_spend_insights_prompt_v2, generate_supplier_insights_prompt_v2, generate_market_insight_summary_prompt_v1)
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
    spend_increase_yoy_on_supplier,
    top_single_sourced_materials
)

from ada.components.llm_models.generic_calls import (
    generate_chat_response_with_chain,
    run_conversation_chat,
)
from ada.utils.logs.time_logger import log_time
from concurrent.futures import ThreadPoolExecutor, as_completed

log = get_logger("Negotiation_gameplan_components")

@log_time
def extract_supplier_level_data(supplier_name: str,category_name, sf_client):
    """
    Extracts supplier-level data for the current and previous year from NEGO_SUPPLIER_MASTER.

    Args:
        supplier_name (str): The name of the supplier to filter on.
        sf_client: A client instance used to fetch data from Snowflake.

    Returns:
        pd.DataFrame: DataFrame containing supplier-level data.
    """
    query = f"""
        SELECT * FROM DATA.NEGO_SUPPLIER_MASTER
        WHERE SUPPLIER = '{supplier_name}'
        AND CATEGORY = '{category_name}'
          AND YEAR IN (
              (SELECT MAX(YEAR) FROM DATA.NEGO_SUPPLIER_MASTER),
              (SELECT MAX(YEAR) - 1 FROM DATA.NEGO_SUPPLIER_MASTER)
          )
    """
    
    try:
        supplier_df = sf_client.fetch_dataframe(query)
        log.info(f"Fetched {len(supplier_df)} rows of supplier-level data.")
        return supplier_df
    except Exception as e:
        log.error(f"Failed to fetch supplier-level data: {str(e)}")
        return pd.DataFrame()

@log_time
def extract_market_insights(supplier_name: str, skus, category_name: str, sf_client):
    """
    Extracts market-level insights for a supplier-category combination.

    Args:
        supplier_name (str): The supplier name.
        skus (list): List of SKU names.
        category_name (str): The category name.
        sf_client: A client instance used to fetch data from Snowflake.

    Returns:
        dict: Dictionary with insights DataFrame under key "insights".
    """
    analytics_names = ('Market Analysis')

    # insight_query = f"""
    #     SELECT * FROM DATA.NEGOTIATION_INSIGHTS
    #     WHERE CATEGORY_NAME = '{category_name}'
    #       AND ANALYTICS_NAME IN ('{analytics_names}')
    # """
    if skus:
        safe_skus = [sku.replace("'", "''") for sku in skus]
        formatted_skus = "', '".join(safe_skus)

    market_query = f"""
    WITH YEAR_CHANGE AS (
            SELECT
                    YEAR,
                    CATEGORY,
                    AVG(CHANGE_IN_MARKET_PRICE_PERCENTAGE) AS CHANGE_IN_MARKET_PRICE_PERCENTAGE
            FROM DATA.SKU_PRICE_COMPARISON
            WHERE YEAR = YEAR = (SELECT MAX(YEAR) FROM DATA.SKU_PRICE_COMPARISON)
            GROUP BY YEAR,CATEGORY
        )
        SELECT
            SPC.YEAR,
            SPC.CATEGORY,
            SUPPLIER,
            SKU,
            AVG(CHANGE_IN_SKU_PRICE_PERCENTAGE) AS CHANGE_IN_SKU_PRICE_PERCENTAGE,
            YC.CHANGE_IN_MARKET_PRICE_PERCENTAGE
        FROM DATA.SKU_PRICE_COMPARISON SPC
        JOIN YEAR_CHANGE YC
        ON SPC.YEAR = YC.YEAR AND SPC.CATEGORY = YC.CATEGORY
        WHERE
            SUPPLIER = '{supplier_name}'
            AND SKU IN ('{formatted_skus}')
            AND SPC.CATEGORY = '{category_name}'
            AND SPC.YEAR = (SELECT MAX(YEAR) FROM DATA.SKU_PRICE_COMPARISON)
        GROUP BY SPC.YEAR, SUPPLIER,SKU,SPC.CATEGORY,YC.CHANGE_IN_MARKET_PRICE_PERCENTAGE
        ORDER BY SKU ;
    """
    
    try:
        # insight_df = sf_client.fetch_dataframe(insight_query)
        insight_df = sf_client.fetch_dataframe(market_query)
        log.info(f"Insights data fetched: {len(insight_df)} rows")
        return {"insights": insight_df if not insight_df.empty else pd.DataFrame()}
    except Exception as e:
        log.error(f"Failed to fetch insights or opportunity data: {str(e)}")
        return None

@log_time
def are_all_opportunities_zero_and_insights_empty(nego_insights):
    """
    Determines if all opportunities are zero and insights are empty.

    Args:
        nego_insights (dict): Dictionary of insight entries.

    Returns:
        bool: True if all insights are empty and opportunities are zero.
    """
    return all(
        entry.get("opportunity", 0) == 0 and not entry.get("insights")
        for entry in nego_insights.values()
    )

@log_time
def extract_sku_df_for_insights(supplier_name: str, skus, category_name: str, sf_client):
    """
    Extracts SKU-level spend data for a supplier-category combination.

    Args:
        supplier_name (str): Supplier name.
        skus (list): List of SKUs.
        category_name (str): Category name.
        sf_client: Snowflake client instance.

    Returns:
        dict: Dictionary containing 'spend' key with the spend DataFrame.
    """
    spend_query = f"""
        SELECT * FROM DATA.T_C_NEGOTIATION_FACTORY_T2
        WHERE CATEGORY_NAME = '{category_name}'
          AND SUPPLIER_NAME = '{supplier_name}'
          AND PERIOD IN (
              (SELECT MAX(PERIOD) FROM DATA.T_C_NEGOTIATION_FACTORY_T2),
              (SELECT MAX(PERIOD) - 1 FROM DATA.T_C_NEGOTIATION_FACTORY_T2)
          )
    """

    if skus:
        safe_skus = [sku.replace("'", "''") for sku in skus]
        formatted_skus = "', '".join(safe_skus)
        sku_query = f"AND SKU_NAME IN ('{formatted_skus}')"
        spend_query += f" {sku_query}"

    spend_price_volume_variance_query = f"""

    Select
    Supplier_name,
    SKU_NAME,
    category_name,
        (SUM(SPEND_YTD) - SUM(SPEND_LAST_YEAR)) AS spend_variance_absolute,
        (SUM(UNIT_PRICE) - SUM(UNIT_PRICE_LAST_YEAR)) AS price_variance_absolute,
        (SUM(QUANTITY) - SUM(QUANTITY_LAST_YEAR)) AS quantity_variance_absolute,
        CASE
            WHEN SUM(SPEND_LAST_YEAR) != 0 THEN  ((SUM(SPEND_YTD) - SUM(SPEND_LAST_YEAR))/ SUM(SPEND_LAST_YEAR))*100
            ELSE NULL
        END AS spend_variance_percentage,
        CASE
            WHEN SUM(UNIT_PRICE_LAST_YEAR) != 0 THEN ((SUM(UNIT_PRICE) - SUM(UNIT_PRICE_LAST_YEAR)) / SUM(UNIT_PRICE_LAST_YEAR))*100
            ELSE NULL
        END AS price_variance_percentage,
        CASE
            WHEN SUM(Quantity_LAST_YEAR) != 0 THEN ((SUM(QUANTITY) - SUM(QUANTITY_LAST_YEAR))/ SUM(Quantity_LAST_YEAR))*100
            ELSE NULL
        END AS quantity_variance_percentage
    From DATA.T_C_NEGOTIATION_FACTORY_T2
    where supplier_name='{supplier_name}' and category_name='{category_name}'  
    and SKU_NAME in ('{formatted_skus}') AND 
    SPEND_YTD > 0 and SPEND_LAST_YEAR!=0 and Period=(Select MAX(PERIOD) from DATA.T_C_NEGOTIATION_FACTORY_T2)
    group by Supplier_name , category_name, sku_name
    
    """

    single_multi_source_query = f"""

    With Avg_unit_price as
    (
    Select 
    SKU_NAME,
    AVG(UNIT_PRICE) AS AVERAGE_UNIT_PRICE_ACROSS_SUPPLIERS
    from DATA.T_C_NEGOTIATION_FACTORY_T2
    where SKU_NAME in ('{formatted_skus}')
    and CATEGORY_NAME='{category_name}'
    group by SKU_NAME
    )
    SELECT
        t1.Supplier_name,
        t1.SKU_NAME,
        CASE 
            WHEN SPEND_SINGLE_SOURCE_YTD IS NOT NULL AND SPEND_SINGLE_SOURCE_YTD != 0 THEN 'SINGLE SOURCED'
            WHEN MULTI_SOURCE_SPEND_YTD IS NOT NULL AND MULTI_SOURCE_SPEND_YTD != 0 THEN 'MULTI SOURCED'
            ELSE NULL
        END AS SOURCED_TYPE,
        CASE 
            WHEN SPEND_SINGLE_SOURCE_YTD IS NOT NULL AND SPEND_SINGLE_SOURCE_YTD != 0 THEN SPEND_SINGLE_SOURCE_YTD
            WHEN MULTI_SOURCE_SPEND_YTD IS NOT NULL AND MULTI_SOURCE_SPEND_YTD != 0 THEN MULTI_SOURCE_SPEND_YTD
            ELSE NULL
        END AS CURRENT_YEAR_SPEND,
        t1.UNIT_PRICE,
        CASE 
            WHEN SPEND_SINGLE_SOURCE_YTD IS NOT NULL AND SPEND_SINGLE_SOURCE_YTD != 0 THEN NULL
            WHEN MULTI_SOURCE_SPEND_YTD IS NOT NULL AND MULTI_SOURCE_SPEND_YTD != 0 THEN t2.AVERAGE_UNIT_PRICE_ACROSS_SUPPLIERS
            ELSE NULL
    END AS AVERAGE_UNIT_PRICE_ACROSS_SUPPLIERS,
    FROM DATA.T_C_NEGOTIATION_FACTORY_T2 t1
    join Avg_unit_price t2
    ON t1.SKU_NAME=t2.SKU_NAME
    WHERE t1.PERIOD = (Select MAX(PERIOD) from DATA.T_C_NEGOTIATION_FACTORY_T2)
    AND t1.SPEND_YTD IS NOT NULL
    AND t1.CATEGORY_NAME='{category_name}'
    AND t1.SKU_NAME in ('{formatted_skus}')
    AND SUPPLIER_NAME = '{supplier_name}'
    """


    try:
        spend_df = sf_client.fetch_dataframe(spend_query)
        log.info(f"Fetched {len(spend_df)} rows of SKU spend data.")
        spend_price_volume_variance_df = sf_client.fetch_dataframe(spend_price_volume_variance_query)
        log.info(f"Fetched {len(spend_price_volume_variance_df)} rows of SKU spend_price_volume_variance data.")
        single_multi_source_query_df = sf_client.fetch_dataframe(single_multi_source_query)
        log.info(f"Fetched {len(single_multi_source_query_df)} rows of SKU spend_price_volume_variance data.")
        return {"spend": spend_df if not spend_df.empty else pd.DataFrame(),"spend_price_volume_variance": spend_price_volume_variance_df if not spend_price_volume_variance_df.empty else pd.DataFrame(),"single_multi_source_data": single_multi_source_query_df if not single_multi_source_query_df.empty else pd.DataFrame()}
    except Exception as e:
        log.error(f"Failed to fetch spend data: {str(e)}")
        return None


def extract_supplier_insight_features(supplier_name: str, category_name: str, sf_client) -> dict:
    """
    Extracts supplier-specific negotiation features using robust query execution with fallback on failure.

    Args:
        supplier_name (str): Supplier of interest.
        category_name (str): Relevant procurement category.
        sf_client: Snowflake client.

    Returns:
        dict: Dictionary of feature groups, each safely queried and optionally present.
    """
    year_opp_subquery = "(SELECT MAX(YEAR) FROM DATA.t_c_total_savings_opportunity_frontend)"
    year_master_subquery = "(SELECT MAX(YEAR) FROM DATA.NEGO_SUPPLIER_MASTER)"

    features = {}

    # 4. Single Source Spend
    try:
        single_source_query = f"""
            SELECT SUM(SINGLE_SOURCE_SPEND_YTD) AS SINGLE_SOURCE_SPEND
            FROM DATA.NEGO_SUPPLIER_MASTER
            WHERE SUPPLIER = '{supplier_name}'
              AND CATEGORY = '{category_name}'
              AND YEAR = {year_master_subquery}
        """
        df = sf_client.fetch_dataframe(single_source_query)
        features["single_source_spend"] = df.to_dict(orient="records")
    except Exception as e:
        log.warning(f"Failed to fetch single source spend: {e}")
        features["single_source_spend"] = []

    # 5. High Spend / Low Invoice Risk
    try:
        high_spend_risk_query = f"""
            SELECT SUPPLIER,
                   SUM(SPEND_YTD) AS SPEND_YTD,
                   SUM(INVOICE_COUNT_YTD) AS INVOICE_COUNT_YTD,
                   SUM(SPEND_YTD) / NULLIF(SUM(INVOICE_COUNT_YTD), 0) AS SPEND_PER_INVOICE
            FROM DATA.NEGO_SUPPLIER_MASTER
            WHERE CATEGORY = '{category_name}'
              AND SUPPLIER = '{supplier_name}'
              AND YEAR = {year_master_subquery}
              AND INVOICE_COUNT_YTD > 0
            GROUP BY SUPPLIER
        """
        df = sf_client.fetch_dataframe(high_spend_risk_query)
        features["high_spend_low_invoice_risk"] = df.to_dict(orient="records")
    except Exception as e:
        log.warning(f"Failed to fetch high spend / low invoice risk: {e}")
        features["high_spend_low_invoice_risk"] = []

    # 6. Multi-Source Spend Drop Risk
    try:
        multi_source_risk_query = f"""
            SELECT SUPPLIER,
                   SUM(MULTI_SOURCE_SPEND_LAST_YEAR) AS MULTI_SOURCE_SPEND_LAST_YEAR,
                   SUM(MULTI_SOURCE_SPEND_YTD) AS MULTI_SOURCE_SPEND_YTD,
                   SUM(MULTI_SOURCE_SPEND_LAST_YEAR) - SUM(MULTI_SOURCE_SPEND_YTD) AS DROP_IN_MULTI_SOURCE_SPEND
            FROM DATA.NEGO_SUPPLIER_MASTER
            WHERE CATEGORY = '{category_name}'
              AND SUPPLIER = '{supplier_name}'
              AND YEAR = {year_master_subquery}
              AND MULTI_SOURCE_SPEND_LAST_YEAR > MULTI_SOURCE_SPEND_YTD
            GROUP BY SUPPLIER
        """
        df = sf_client.fetch_dataframe(multi_source_risk_query)
        features["multi_source_drop_risk"] = df.to_dict(orient="records")
    except Exception as e:
        log.warning(f"Failed to fetch multi-source drop risk: {e}")
        features["multi_source_drop_risk"] = []

    return features


# def render_structured_insights(spend_json: str, supplier_json: str, opportunity_json: str, market_insights=None, others=None):
#     """
#     Converts raw JSON strings into structured dictionary format for rendering insights.

#     Args:
#         spend_json (str): JSON string from spend insight response.
#         supplier_json (str): JSON string from supplier insight response.
#         opportunity_json (str): JSON string from opportunity insight response.
#         market_insights (list, optional): List of market-level insights.
#         others (list, optional): List of miscellaneous insights.

#     Returns:
#         dict: Structured dictionary containing organized insights.
#     """
#     try:
#         spend_data = json.loads(spend_json)
#         supplier_data = json.loads(supplier_json)
#         opportunity_data = json.loads(opportunity_json)
#         market_data = json.loads(market_insights)

#     except json.JSONDecodeError as e:
#         log.error(f"Invalid JSON format: {e}")
#         return {"error": "Invalid JSON"}

#     insights = {}

#     # 1. Add all analytics from opportunity_json
#     for analytic_name, value in opportunity_data.items():
#         insights[analytic_name] = {
#             "insights": value.get("insights", []),
#             "opportunity": value.get("opportunity", 0)
#         }

#     # 2. Add spend insights
#     spend_insights = spend_data.get("spend", {}).get("insights", [])
#     if spend_insights:
#         insights["spend"] = {
#             "insights": spend_insights,
#             "opportunity": 0
#         }

#     # 3. Add supplier insights
#     supplier_insights = supplier_data.get("supplier", {}).get("insights", [])
#     if supplier_insights:
#         insights["suppliers"] = {
#             "insights": supplier_insights,
#             "opportunity": 0
#         }

#     # 4. Add market insights
#     if market_insights:
#         insights["market"] = {
#             "insights": market_data['market'],
#             "opportunity": 0
#         }
#     # 5. Optionally add others if required in future
#     # if others:
#     #     insights["others"] = {
#     #         "insights": others,
#     #         "opportunity": 0
#     #     }

#     return {"insights": insights}

def render_structured_insights(spend_json: str, supplier_json: str, opportunity_json: str, market_insights=None, others=None):
    """
    Converts raw JSON strings into structured dictionary format for rendering insights.

    Args:
        spend_json (str): JSON string from spend insight response.
        supplier_json (str): JSON string from supplier insight response.
        opportunity_json (str): JSON string from opportunity insight response.
        market_insights (list, optional): List of market-level insights.
        others (list, optional): List of miscellaneous insights.

    Returns:
        dict: Structured dictionary containing organized insights.
    """
    try:
        spend_data = json.loads(spend_json)
        supplier_data = json.loads(supplier_json)
        opportunity_data = json.loads(opportunity_json)
        market_data = json.loads(market_insights)
    except json.JSONDecodeError as e:
        log.error(f"Invalid JSON format: {e}")
        return {"error": "Invalid JSON"}

    output = {
        "Spend": spend_data.get("spend", {}).get("insights", []),
        "Market": market_data.get('market', None),
        "Suppliers": supplier_data.get("supplier", {}).get("insights", []),
        "Opportunity": {},
        "Others": others or []
    }
    # Iterate over each analytic name and its associated value
    for analytic_name, value in opportunity_data.items():
        # Check if the opportunity is 0
        if value.get("opportunity", 0) == 0:
            output["Opportunity"][analytic_name] = {
                "opportunity": 0,
                "insight": []  # If opportunity is 0, assign an empty list to insight
            }
        else:
            output["Opportunity"][analytic_name] = {
                "opportunity": value.get("opportunity", 0),
                "insight": value.get("insights", [])  # Else, add the insights
            }

    return output


def render_structured_insights_from_db(db_results):
    """
    Converts raw JSON strings into structured dictionary format for rendering insights.

    Args:
        spend_json (str): JSON string from spend insight response.
        supplier_json (str): JSON string from supplier insight response.
        opportunity_json (str): JSON string from opportunity insight response.
        market_insights (list, optional): List of market-level insights.
        others (list, optional): List of miscellaneous insights.

    Returns:
        dict: Structured dictionary containing organized insights.
    """
    spend_insights = []
    supplier_insights = []
    market_insights = []
    opportunity_data = {}
    others = []

    for _, row in db_results.iterrows():
        analytics_type = row['ANALYTICS']
        try:
            response = json.loads(row['RESPONSE']) if isinstance(row['RESPONSE'], str) else row['RESPONSE']

            if analytics_type == "Spend":
                spend_insights.extend(response if isinstance(response, list) else [response])
            elif analytics_type == "Supplier":
                supplier_insights.extend(response if isinstance(response, list) else [response])
            elif analytics_type == "Market":
                market_insights.extend(response if isinstance(response, list) else [response])
            elif analytics_type == "Opportunity":
                for key, value in response.items():
                    if key not in opportunity_data:
                        opportunity_data[key] = {
                            "opportunity": value.get("opportunity", 0),
                            "insights": value.get("insights", []) if value.get("opportunity", 0) > 0 else []
                        }
                    else:
                        # Combine opportunity values
                        opportunity_data[key]["opportunity"] += value.get("opportunity", 0)
                        opportunity_data[key]["insights"].extend(
                            value.get("insights", []) if value.get("opportunity", 0) > 0 else []
                        )
            else:
                others.append(row)

        except json.JSONDecodeError as e:
            log.error(f"Invalid JSON format in analytics '{analytics_type}': {e}")
            return {"error": f"Invalid JSON in {analytics_type}"}

    return {
        "Spend": spend_insights if spend_insights else [],
        "Market": market_insights if market_insights else [],
        "Suppliers": supplier_insights if supplier_insights else [],
        "Opportunity": opportunity_data if opportunity_data else {},
        "Others": others or []
    }



@log_time
def generate_nego_insights(pg_db_conn, sf_client, category, user_query, pinned_elements, generation_type="", skus=None, **kwargs):
    """
    Orchestrates the negotiation insight generation process using supplier, category, and SKU inputs.

    Args:
        pg_db_conn: PostgreSQL database connection.
        sf_client: Snowflake client.
        category (str): Category string.
        user_query (str): Raw user query string.
        pinned_elements (dict): Dictionary containing context like supplier profile.
        generation_type (str, optional): Generation mode (not used).
        skus (list, optional): List of SKUs.

    Returns:
        dict: Negotiation insight response with suggested prompts.
    """
    supplier_profile = pinned_elements.get("supplier_profile", {})
    currency_symbol =  {supplier_profile.get('currency_symbol', '€')}
    supplier_name = supplier_profile.get("supplier_name")
    category_name = supplier_profile.get("category_name")
    sku_names = pinned_elements.get("skus", [])
    skus = [sku.get("name", "") for sku in sku_names]

    log.info(f"Generating insights for supplier: {supplier_name}, category: {category_name}, skus: {sku_names}")

    if skus:
        safe_skus = [sku.replace("'", "''") for sku in skus]
        formatted_skus = "', '".join(safe_skus)

    try:
        check_db_sql_query = f"""
        SELECT * FROM DATA.NEGOTIATION_INSIGHTS_MASTER
        WHERE 
            (SUPPLIER = '{supplier_name}' AND MATERIAL IN ('{formatted_skus}')) OR (SUPPLIER = '{supplier_name}' AND MATERIAL = 'NULL')
            AND CATEGORY = '{category_name}'
        """
        db_result = sf_client.fetch_dataframe(check_db_sql_query)

        structured_output_db = render_structured_insights_from_db(db_result)

        if len(structured_output_db['Spend']) == 0:
            spend_data = extract_sku_df_for_insights(supplier_name, skus, category_name, sf_client)
            spend_insight = generate_chat_response_with_chain(prompt=generate_spend_insights_prompt_v2({"spend": spend_data["spend"].to_dict(orient="records"),"spend_price_volume_variance": spend_data["spend_price_volume_variance"].to_dict(orient="records"),"single_multi_source_data": spend_data["single_multi_source_data"].to_dict(orient="records")},currency_symbol=currency_symbol),temperature=0.7)
            spend_insight = json.loads(spend_insight)
            spend_insight = spend_insight.get("spend", {}).get("insights", [])
            structured_output_db["Spend"] = spend_insight
    

        
        if len(structured_output_db['Suppliers']) == 0:
            supplier_features = extract_supplier_insight_features(supplier_name, category_name, sf_client)
            supplier_df = extract_supplier_level_data(supplier_name, category_name, sf_client)
            prompt = generate_supplier_insights_prompt_v2({"supplier": supplier_df.to_dict(orient="records"),"features": supplier_features}, currency_symbol=currency_symbol)
            supplier_insight = generate_chat_response_with_chain(prompt=prompt, temperature=0.7)
            supplier_insight = json.loads(supplier_insight)
            supplier_insight = supplier_insight.get("supplier", {}).get("insights",[])
            
            # Additional Insights

            top_single_sourced_materials_data = top_single_sourced_materials(supplier_name,category_name,sf_client)
            spend_increase_yoy_on_supplier_data = spend_increase_yoy_on_supplier(supplier_name,category_name,sf_client)
            prompt = generate_additional_supplier_insights_prompt(top_single_sourced_materials_data,spend_increase_yoy_on_supplier_data,currency_symbol,supplier_name,category)
            response = json.loads(generate_chat_response_with_chain(prompt=prompt, temperature=0.7,model='gpt-4o').replace('```json','').replace('```',''))
            supplier_additional_insights = response.get("supplier",[])
        
            structured_output_db["Suppliers"] = supplier_insight + supplier_additional_insights


        if len(structured_output_db['Market']) == 0:
            market_data = extract_market_insights(supplier_name, skus, category_name, sf_client)
            df = market_data.get("insights")
            market_dict = df.to_dict(orient='records')
            prompt = generate_market_insight_summary_prompt_v2(market_dict)
            market_insights = generate_chat_response_with_chain(prompt=prompt, temperature=0.7)
            market_insights = json.loads(market_insights)
            structured_output_db["Market"] = market_insights.get("market",[])


        if structured_output_db["Opportunity"] == {}:
            
            features = {}
            year_opp_subquery = "(SELECT MAX(YEAR) FROM DATA.t_c_total_savings_opportunity_frontend)"

            try:
                top_materials_query = f"""
                    SELECT SUPPLIER,MATERIAL, SUM(KPI_VALUE) AS TOTAL_OPPORTUNITY
                    FROM DATA.t_c_total_savings_opportunity_frontend
                    WHERE SUPPLIER = '{supplier_name}'
                    AND CATEGORY = '{category_name}'
                    AND YEAR = {year_opp_subquery}
                    AND KPI_NAME = 'Total saving opportunity'
                    GROUP BY SUPPLIER,MATERIAL
                    ORDER BY TOTAL_OPPORTUNITY DESC
                    LIMIT 5
                """
                df = sf_client.fetch_dataframe(top_materials_query)
                features["top_materials_by_opportunity"] = df.to_dict(orient="records")
            except Exception as e:
                log.warning(f"Failed to fetch top materials: {e}")
                features["top_materials_by_opportunity"] = []

            # 2. Top Plants by Opportunity
            try:
                top_plants_query = f"""
                    SELECT SUPPLIER,PLANT, SUM(KPI_VALUE) AS TOTAL_OPPORTUNITY
                    FROM DATA.t_c_total_savings_opportunity_frontend
                    WHERE SUPPLIER = '{supplier_name}'
                    AND CATEGORY = '{category_name}'
                    AND YEAR = {year_opp_subquery}
                    AND KPI_NAME = 'Total saving opportunity'
                    GROUP BY SUPPLIER,PLANT
                    ORDER BY TOTAL_OPPORTUNITY DESC
                    LIMIT 5
                """
                df = sf_client.fetch_dataframe(top_plants_query)
                features["top_plants_by_opportunity"] = df.to_dict(orient="records")
            except Exception as e:
                log.warning(f"Failed to fetch top plants: {e}")
                features["top_plants_by_opportunity"] = []

            # 3. Top Regions by Opportunity
            try:
                top_regions_query = f"""
                    SELECT SUPPLIER,COUNTRY, SUM(KPI_VALUE) AS TOTAL_OPPORTUNITY
                    FROM DATA.t_c_total_savings_opportunity_frontend
                    WHERE SUPPLIER = '{supplier_name}'
                    AND CATEGORY = '{category_name}'
                    AND YEAR = {year_opp_subquery}
                    AND KPI_NAME = 'Total saving opportunity'
                    GROUP BY SUPPLIER,COUNTRY
                    ORDER BY TOTAL_OPPORTUNITY DESC
                    LIMIT 5
                """
                df = sf_client.fetch_dataframe(top_regions_query)
                features["top_regions_by_opportunity"] = df.to_dict(orient="records")
            except Exception as e:
                log.warning(f"Failed to fetch top regions: {e}")
                features["top_regions_by_opportunity"] = []

            opportunity_insight = {}
            prompt=generate_insights_prompt_v2(name="General",info=features,currency_symbol=currency_symbol)
            response = generate_chat_response_with_chain(prompt=prompt, temperature=0.1)
            opportunity_insight["General"] = json.loads(response)
            
            opportunity_data = extract_category_analytic_data(supplier_name=supplier_name, category_name=category_name, skus=skus, sf_client=sf_client)
            opportunity_data = {key: value[0].to_dict() for key, value in opportunity_data.items()}

            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = {
                    executor.submit(
                        lambda name, df: (name, generate_chat_response_with_chain(
                            prompt=generate_insights_prompt_v2(name=name,info=df,currency_symbol=currency_symbol), temperature=0.1,model='gpt-4o')),
                        name, df
                    ): name
                    for name, df in opportunity_data.items()
                }

                for future in as_completed(futures):
                    name, insight = future.result()
                    opportunity_insight[name] = json.loads(insight.replace('```json','').replace('```',''))

            structured_output_db["Opportunity"] = opportunity_insight

    except Exception as e1:
        structured_output_db = {
        "Spend": [],
        "Market": [],
        "Suppliers": [],
        "Opportunity": {},
        "Others": []
        }
        log.error("Error",e1)    

    pinned_elements['insights'] = structured_output_db

    message = "Review the insights relevant to your selected suppliers and proceed to setting the negotiation objectives by selecting the suggested prompt."

    response = {
        "response_type": "negotiation_insights_all",
        "message": message,
        "insights": structured_output_db,
        "suggested_prompts": [{
            "prompt": "Set negotiation objectives",
            "intent": "negotiation_objective"
        }],
    }

    log.info(f"Generated response: {response}")
    return response

    # year_opp_subquery = "(SELECT MAX(YEAR) FROM DATA.t_c_total_savings_opportunity_frontend)"

    # features = {}

    # # 1. Top Materials by Opportunity
    # try:
    #     top_materials_query = f"""
    #         SELECT SUPPLIER,MATERIAL, SUM(KPI_VALUE) AS TOTAL_OPPORTUNITY
    #         FROM DATA.t_c_total_savings_opportunity_frontend
    #         WHERE SUPPLIER = '{supplier_name}'
    #           AND CATEGORY = '{category_name}'
    #           AND YEAR = {year_opp_subquery}
    #           AND KPI_NAME = 'Total saving opportunity'
    #         GROUP BY SUPPLIER,MATERIAL
    #         ORDER BY TOTAL_OPPORTUNITY DESC
    #         LIMIT 5
    #     """
    #     df = sf_client.fetch_dataframe(top_materials_query)
    #     features["top_materials_by_opportunity"] = df.to_dict(orient="records")
    # except Exception as e:
    #     log.warning(f"Failed to fetch top materials: {e}")
    #     features["top_materials_by_opportunity"] = []

    # # 2. Top Plants by Opportunity
    # try:
    #     top_plants_query = f"""
    #         SELECT SUPPLIER,PLANT, SUM(KPI_VALUE) AS TOTAL_OPPORTUNITY
    #         FROM DATA.t_c_total_savings_opportunity_frontend
    #         WHERE SUPPLIER = '{supplier_name}'
    #           AND CATEGORY = '{category_name}'
    #           AND YEAR = {year_opp_subquery}
    #           AND KPI_NAME = 'Total saving opportunity'
    #         GROUP BY SUPPLIER,PLANT
    #         ORDER BY TOTAL_OPPORTUNITY DESC
    #         LIMIT 5
    #     """
    #     df = sf_client.fetch_dataframe(top_plants_query)
    #     features["top_plants_by_opportunity"] = df.to_dict(orient="records")
    # except Exception as e:
    #     log.warning(f"Failed to fetch top plants: {e}")
    #     features["top_plants_by_opportunity"] = []

    # # 3. Top Regions by Opportunity
    # try:
    #     top_regions_query = f"""
    #         SELECT SUPPLIER,COUNTRY, SUM(KPI_VALUE) AS TOTAL_OPPORTUNITY
    #         FROM DATA.t_c_total_savings_opportunity_frontend
    #         WHERE SUPPLIER = '{supplier_name}'
    #           AND CATEGORY = '{category_name}'
    #           AND YEAR = {year_opp_subquery}
    #           AND KPI_NAME = 'Total saving opportunity'
    #         GROUP BY SUPPLIER,COUNTRY
    #         ORDER BY TOTAL_OPPORTUNITY DESC
    #         LIMIT 5
    #     """
    #     df = sf_client.fetch_dataframe(top_regions_query)
    #     features["top_regions_by_opportunity"] = df.to_dict(orient="records")
    # except Exception as e:
    #     log.warning(f"Failed to fetch top regions: {e}")
    #     features["top_regions_by_opportunity"] = []

    # opportunity_insight = {}
    # prompt=generate_insights_prompt_v2(name="General",info=features,currency_symbol=currency_symbol)
    # response = generate_chat_response_with_chain(prompt=prompt, temperature=0.1)
    # opportunity_insight["General"] = json.loads(response)
    
    # opportunity_data = extract_category_analytic_data(supplier_name=supplier_name, category_name=category_name, skus=skus, sf_client=sf_client)

    # with ThreadPoolExecutor(max_workers=10) as executor:
    #     futures = {
    #         executor.submit(
    #             lambda name, df: (name, generate_chat_response_with_chain(
    #                 prompt=generate_insights_prompt_v2(name=name,info=df,currency_symbol=currency_symbol), temperature=0.1)),
    #             name, df
    #         ): name
    #         for name, df in opportunity_data.items()
    #     }

    #     for future in as_completed(futures):
    #         name, insight = future.result()
    #         opportunity_insight[name] = json.loads(insight)

    # # breakpoint()

    # executor = ThreadPoolExecutor(max_workers=10)
    # insights = {}
    # futures = {}

    # # Kick off supplier features early
    # futures["supplier_features"] = executor.submit(
    #     lambda: extract_supplier_insight_features(supplier_name, category_name, sf_client)
    # )

    # # SPEND: extract sku_df → then generate spend insight
    # futures["sku_df"] = executor.submit(
    #     lambda: extract_sku_df_for_insights(supplier_name, skus, category_name, sf_client)
    # )
    # futures["sku_df"].add_done_callback(
    #     lambda fut: insights.update({
    #         "spend_insight": generate_chat_response_with_chain(
    #             prompt=generate_spend_insights_prompt_v2({
    #                 "spend": fut.result()["spend"].to_dict(orient="records"),
    #                 "spend_price_volume_variance": fut.result()["spend_price_volume_variance"].to_dict(orient="records"),
    #                 "single_multi_source_data": fut.result()["single_multi_source_data"].to_dict(orient="records")
    #             },currency_symbol=currency_symbol),
    #             temperature=0.7
    #         )
    #     }) if not fut.exception() else log.error(f"Spend insight error: {fut.exception()}")
    # )

    # # SUPPLIER: extract supplier_df → wait for supplier_features → then generate supplier insight
    # futures["supplier_df"] = executor.submit(
    #     lambda: extract_supplier_level_data(supplier_name, category_name, sf_client)
    # )
    # def supplier_insight_callback(fut):
    #     try:
    #         supplier_df = fut.result()
    #         supplier_features = futures["supplier_features"].result()
    #         prompt = generate_supplier_insights_prompt_v2({
    #             "supplier": supplier_df.to_dict(orient="records"),
    #             "features": supplier_features
    #         }, currency_symbol=currency_symbol)
    #         insights["supplier_insight"] = generate_chat_response_with_chain(prompt=prompt, temperature=0.7)
    #     except Exception as e:
    #         log.error(f"Supplier insight error: {e}")
    # futures["supplier_df"].add_done_callback(supplier_insight_callback)

    # # MARKET: extract market_insight_data → wait for supplier_features → generate market insights
    # futures["market_insight_data"] = executor.submit(
    #     lambda: extract_market_insights(supplier_name, skus, category_name, sf_client)
    # )
    # def market_insight_callback(fut):
    #     try:
    #         market_data = fut.result()
    #         df = market_data.get("insights")
    #         market_dict = df.to_dict(orient='records')

    #         prompt = generate_market_insight_summary_prompt_v2(market_dict)
    #         insights["market_insights"] = generate_chat_response_with_chain(prompt=prompt, temperature=0.7)

    #         # if df is not None and len(df) > 0:
    #         #     df.columns = df.columns.str.lower()
    #         #     if "label" in df.columns:
    #         #         labels = df["label"].dropna().tolist()
    #         #         supplier_features = futures["supplier_features"].result()
    #         #         prompt = generate_market_insight_summary_prompt_v1({
    #         #             "market_insights": labels,
    #         #             "supplier_name": supplier_name,
    #         #             "category_name": category_name,
    #         #             "supplier_features": supplier_features
    #         #         })
    #         #         insights["market_insights"] = generate_chat_response_with_chain(prompt=prompt, temperature=0.7)
    #         return
    #     except Exception as e:
    #         log.error(f"Market insight error: {e}")
    #         insights["market_insights"] = {}
    # futures["market_insight_data"].add_done_callback(market_insight_callback)

    # # Wait for everything to finish
    # executor.shutdown(wait=True)

    # # Final response
    # try:
    #     response_dict = render_structured_insights(
    #         spend_json=insights.get("spend_insight", {}),
    #         supplier_json=insights.get("supplier_insight", {}),
    #         opportunity_json=json.dumps(opportunity_insight),
    #         market_insights=insights.get("market_insights", {}),
    #         others=[]
    #     )
    # except json.JSONDecodeError as e:
    #     log.error(f"Failed to decode JSON response: {e}")
    #     response_dict = {"error": "Failed to parse JSON response"}

    #####################################################################

    # try:
    #     response_dict = render_structured_insights(
    #         spend_json=spend_insight,
    #         supplier_json=supplier_insight,
    #         opportunity_json=json.dumps(opportunity_insight),
    #         market_insights=market_insights,
    #         others=[]
    #     )
    # except json.JSONDecodeError as e:
    #     log.error(f"Failed to decode JSON response: {e}")
    #     response_dict = {"error": "Failed to parse JSON response"}

    
    # pinned_elements['insights'] = response_dict
    
    # if are_all_opportunities_zero_and_insights_empty(response_dict):
    #     message = "No insights or opportunities found for this negotiation."
    # else:
    # message = "Review the insights relevant to your selected suppliers and proceed to setting the negotiation objectives by selecting the suggested prompt."

    # response = {
    #     "response_type": "negotiation_insights_all",
    #     "message": message,
    #     "insights": response_dict,
    #     "suggested_prompts": [{
    #         "prompt": "Set negotiation objectives",
    #         "intent": "negotiation_objective"
    #     }],
    # }

    # log.info(f"Generated response: {response}")
    # return response



@log_time
def generate_nego_insights_bulk(
    pg_db_conn,
    sf_client,
    category,
    user_query,
    pinned_elements,
    generation_type="",
    skus=None,
    cached_supplier_df=None,
    cached_market_insights=None,
    **kwargs
):
    """
    Optimized version of generate_nego_insights that avoids recomputing supplier and market insights repeatedly.

    Args:
        pg_db_conn: PostgreSQL database connection.
        sf_client: Snowflake client.
        category (str): Category name.
        user_query (str): Insight generation context.
        pinned_elements (dict): Includes supplier_profile and skus.
        generation_type (str): Unused.
        skus (list): List of SKU names.
        cached_supplier_df (pd.DataFrame): Precomputed supplier-level DataFrame.
        cached_market_insights (dict): Precomputed market insights.

    Returns:
        dict: Structured response with insights and prompts.
    """
    supplier_profile = pinned_elements.get("supplier_profile", {})
    supplier_name = supplier_profile.get("supplier_name")
    category_name = supplier_profile.get("category_name")
    sku_names = pinned_elements.get("skus", [])
    skus = [sku.get("name", "") for sku in sku_names]

    log.info(f"Generating insights for supplier: {supplier_name}, category: {category_name}, skus: {sku_names}")

    # Fetch opportunity insights
    opportunity_data = extract_category_analytic_data(supplier_name, category_name, skus, sf_client)

    # Fetch SKU-level spend data
    sku_df = extract_sku_df_for_insights(supplier_name, skus, category_name, sf_client)
    spend_prompt = generate_spend_insights_prompt_v2({"spend": sku_df["spend"].to_dict(orient="records")})
    spend_insight = generate_chat_response_with_chain(prompt=spend_prompt, temperature=0.7)
    log.info(f"Spend insight generated for {supplier_name}-{category_name}: {spend_insight}")

    # Use cached supplier insights or generate new
    if cached_supplier_df is None:
        cached_supplier_df = extract_supplier_level_data(supplier_name, category_name, sf_client)
    supplier_prompt = generate_supplier_insights_prompt_v2({"supplier": cached_supplier_df.to_dict(orient="records")})
    supplier_insight = generate_chat_response_with_chain(prompt=supplier_prompt, temperature=0.7)
    log.info(f"Supplier insight generated: {supplier_insight}")

    # Use cached market insights or fetch
    if cached_market_insights is None:
        market_insight_data = extract_market_insights(supplier_name, skus, category_name, sf_client)
    else:
        market_insight_data = cached_market_insights

    # Generate opportunity insights
    opportunity_prompt = generate_insights_prompt_v2(data=opportunity_data)
    opportunity_insight = generate_chat_response_with_chain(prompt=opportunity_prompt, temperature=0.7)
    log.info(f"Generated opportunity insight: {opportunity_insight}")

    # Combine into structured output
    try:
        response_dict = render_structured_insights(
            spend_json=spend_insight,
            supplier_json=supplier_insight,
            opportunity_json=opportunity_insight,
            market_insights=market_insight_data.get("insights") if market_insight_data else [],
            others=[]
        )
    except json.JSONDecodeError as e:
        log.error(f"Failed to decode JSON response: {e}")
        response_dict = {"error": "Failed to parse JSON response"}

    pinned_elements["insights"] = response_dict

    response = {
        "response_type": "negotiation_insights_all",
        "message": "Please see below important insights.",
        "insights": response_dict,
        "suggested_prompts": [{
            "prompt": "Set negotiation objectives",
            "intent": "negotiation_objective"
        }],
    }

    log.info(f"Generated response for {supplier_name}-{category_name}-{skus}: {response}")
    return response
