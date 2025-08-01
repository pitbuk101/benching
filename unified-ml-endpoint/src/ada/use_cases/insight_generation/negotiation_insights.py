import sys
from pathlib import Path
import json
import ast
import uuid
from datetime import datetime
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from negotiation_insights_utils import extract_market_insights,extract_sku_df_for_insights,extract_supplier_insight_features,extract_supplier_level_data,extract_category_analytic_data,opportunity_insights, cleaned_response
import pandas as pd
import re 

current_file = Path(__file__)
sys.path.append(str(current_file.parents[3]))

from ada.utils.config.config_loader import read_config
from sf_connector import SnowflakeClient
from ada.utils.logs.logger import get_logger

log = get_logger("negotiation_insights")
insight_generation_conf = read_config("use-cases.yml")["insight_generation"]

def process_category(category, sf_client):

    try:
        log.debug("Processing category: %s",category)

        result = sf_client.fetch_dataframe(f"""
        SELECT YEAR,SUPPLIER, MATERIAL, KPI_VALUE AS TOTAL_OPPORTUNITY 
        FROM DATA.T_C_TOTAL_SAVINGS_OPPORTUNITY_FRONTEND
        WHERE KPI_NAME = 'Total saving opportunity' 
        AND KPI_VALUE > 0 AND CATEGORY = '{category}' 
        AND YEAR=(SELECT MAX(YEAR) FROM DATA.T_C_TOTAL_SAVINGS_OPPORTUNITY_FRONTEND)
        GROUP BY YEAR,SUPPLIER,MATERIAL, TOTAL_OPPORTUNITY
        ORDER BY TOTAL_OPPORTUNITY DESC                            
        """)

        log.debug("Supplier & SKU combinations with opportunity fetched. Total records: %d", len(result))

    except Exception as e:
        print("Error executing query:", e)
        result = pd.DataFrame()

    year = result['YEAR'].iloc[0] if not result.empty else None
    records = result.drop(columns=['TOTAL_OPPORTUNITY','YEAR']).to_dict(orient='records')
    unique_suppliers = list({item['SUPPLIER'] for item in records})

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(extract_market_insights, category,records,sf_client,year): "extract_market_insights",
            executor.submit(extract_sku_df_for_insights, unique_suppliers,category,records,sf_client,year): "extract_sku_df_for_insights",
            executor.submit(extract_supplier_insight_features, category,unique_suppliers,sf_client,year): "extract_supplier_insight_features",
            executor.submit(opportunity_insights, category,records,sf_client,year): "opportunity_insights",
        }

        results = {}
        for future in as_completed(futures):
            key = futures[future]
            results[key] = future.result()
    
    return results


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate and refine top ideas for a given tenant ID.")
    parser.add_argument("--tenantId", type=str, required=True, help="Tenant ID for which to generate insights")

    args = parser.parse_args()
    tenantId = args.tenantId

    log.debug("Negotiation Insights Generation started for tenantId: %s",tenantId)

    tenant_conf = insight_generation_conf[f"{tenantId}"]
    insight_model_conf = tenant_conf["model"]
    categories = tenant_conf['categories'] + tenant_conf['additional_categories']

    log.debug("Fetched tenant configuration")
    log.debug("Model: %s",insight_model_conf)
    log.debug("Categories: %s",categories)

    final_result = {}

    sf_client = SnowflakeClient(tenant_id=tenantId)
    log.debug("Snowflake client initialized for tenantId: %s", tenantId)

    with ThreadPoolExecutor(max_workers=len(categories)) as executor:
            futures = {
                executor.submit(process_category, cat, sf_client): cat
                for cat in categories
            }

            for future in as_completed(futures):
                cat = futures[future]
                try:
                    result = future.result()
                    final_result[cat] = result
                    log.info(f"Finished processing: {cat}")
                except Exception as e:
                    log.info(f"Error processing {cat}: {e}")
    
    log.info("Final result: %s", final_result)

    combined_data = []

    for category in categories:
        log.debug("Processing category: %s", category)
    
        try:
            market = final_result[category]['extract_market_insights']
            spend = final_result[category]['extract_sku_df_for_insights']
            supplier = final_result[category]['extract_supplier_insight_features']
    
            combined_data = combined_data + market + spend + supplier
            combined_data = cleaned_response(combined_data)

        except Exception as e:
            log.error(f"Error refining data for category {category}: {e}")  

    for category in categories:
        opportunity = final_result[category]['opportunity_insights']
        combined_data.extend(opportunity)

    log.info("Combined Records: %d",len(combined_data))

    with open(f"{current_file.parent}/combined.json", "w", encoding="utf-8") as file:
        json.dump(combined_data, file, indent=4, ensure_ascii=False)

    flattened_data = []

    for record in combined_data:

        supplier = record.get("supplier")
        material = record.get("material")
        category = record.get("category")
        response = json.dumps(record.get("response"))
        analytics = record.get("analytics")

        flattened_data.append((supplier, material, category, response, analytics))

    try:
        insert_sql = """
            INSERT INTO DATA.NEGOTIATION_INSIGHTS_MASTER (
                SUPPLIER,
                MATERIAL,
                CATEGORY,
                RESPONSE,
                ANALYTICS
            ) VALUES (%s, %s, %s, %s, %s)
        """

        sf_client.execute_query(insert_sql, flattened_data)

        log.info("Negotiation Insights Generation completed for tenantId: %s", tenantId)

    except Exception as e:
        log.error("Error inserting data into NEGOTIATION_INSIGHTS_MASTER: %s",e)
