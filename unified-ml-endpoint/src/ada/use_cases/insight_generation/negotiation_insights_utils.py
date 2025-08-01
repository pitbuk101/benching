import pandas as pd
import ast
import re
import sys
from pathlib import Path
import json

import concurrent.futures

current_file = Path(__file__)
sys.path.append(str(current_file.parents[3]))

from ada.components.llm_models.generic_calls import generate_chat_response_with_chain
from negotiation_insights_prompt import generate_additional_supplier_insights_prompt,generate_additional_spend_insights_prompt,classify_prompt,generate_market_insight_summary_prompt_v2,generate_spend_insights_prompt_v2,generate_supplier_insights_prompt_v2,generate_insights_prompt_v2
from concurrent.futures import ThreadPoolExecutor, as_completed

from negotiation_insight_queries.spend import get_spend_without_po, get_supplier_ranking, get_top_business_units, get_top_materials, get_top_payment_terms, get_spend, get_price_volume, get_single_multi_source
from negotiation_insight_queries.supplier import top_single_sourced_materials, spend_increase_yoy_on_supplier, get_high_spend_invoice_risk, get_multi_spend_drop_risk, get_single_source_data
from negotiation_insight_queries.market import get_market_data

from ada.utils.logs.logger import get_logger

log = get_logger("negotiation_insights_utils")


def cleaned_response(combined_data):
    for item in combined_data:
        cleaned_responses = []
        for r in item.get("response", []):
            # Fix currency: -€1.94M or €-1.94M → €1.94M
            r = re.sub(r'[-]?([€$])[-]?([0-9.,]+[MKMB]?)', r'\1\2', r)
            
            # Fix percentage: (-20.39% decrease) or (-20.39%) → (20.39% decrease) or (20.39%)
            r = re.sub(r'\(-?([0-9.,]+%)', r'(\1', r)

            cleaned_responses.append(r)

        item["response"] = cleaned_responses

    return combined_data

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
        return supplier_df
    except Exception as e:
        return pd.DataFrame()


def extract_market_insights(category,records,sf_client,year):
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

    log.debug("Generating market insights for category: %s", category)
    market_results = []

    for record in records:

        try:
            market_dict = get_market_data(record['SUPPLIER'], record['MATERIAL'], category, sf_client)

            if len(market_dict) ==0:
                log.info("No market data found for supplier: %s, material: %s, category: %s", record['SUPPLIER'], record['MATERIAL'], category)
                continue

            log.info("Market data fetched for supplier: %s, material: %s, category: %s", record['SUPPLIER'], record['MATERIAL'], category)

            prompt = generate_market_insight_summary_prompt_v2(market_dict)
            response = json.loads(generate_chat_response_with_chain(prompt=prompt, temperature=0.5,model='gpt-4o').replace('```json','').replace('```',''))
            log.info("Market insights: %s", str(response))

            market_results.append({"supplier":record['SUPPLIER'],"material":record['MATERIAL'],"category":category,"response":response.get("market",[]),"analytics":"Market"})

            # with open (f"{current_file.parent}/market_{category}.json", "w") as file:
            #     json.dump(market_results, file, indent=4, ensure_ascii=False) 
        
        except Exception as e:
            log.error("Error extracting market insights for supplier: %s, material: %s, category: %s, Error: %s", record['SUPPLIER'], record['MATERIAL'], category, str(e))
            continue
    
    log.info("Market insights extraction completed for category: %s", category)

    return market_results
    

def fetch_currency(sf_client):
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
    return currency_symbol


def process_supplier(supplier, category, currency, sf_client,year):
    try:
        log.debug("Processing spend insights for supplier: %s for category: %s", supplier, category)
        spend_without_po = get_spend_without_po(supplier, category, sf_client)
        supplier_ranking = get_supplier_ranking(supplier, category, sf_client)
        top_business_units = get_top_business_units(supplier, category, sf_client)
        top_materials = get_top_materials(supplier, category, sf_client)
        top_payment_terms = get_top_payment_terms(supplier, category, sf_client)

        prompt = generate_additional_spend_insights_prompt(
            spend_without_po,
            supplier_ranking,
            top_business_units,
            top_materials,
            top_payment_terms,
            currency,
            supplier,
            category,
            year
        )

        response = generate_chat_response_with_chain(
            prompt=prompt, temperature=0.7, model='gpt-4o'
        ).replace('```json', '').replace('```', '')

        parsed_response = json.loads(response)
        spend = parsed_response.get("spend", [])
        log.info("Supplier %s spend insights generated.", supplier)
        return {"supplier": supplier, "material": "NULL", "category": category, "response": spend, "analytics": "Spend"}

    except Exception as e:
        log.error("Error processing spend insights for supplier %s: %s", supplier, e)
        return None


def process_record(record, category, currency, sf_client,year):
    try:
        supplier = record['SUPPLIER']
        material = record['MATERIAL']

        spend = get_spend(supplier, category, sf_client)
        spend_price_volume_variance = get_price_volume(supplier, material, category, sf_client)
        single_multi_source_data = get_single_multi_source(supplier, material, category, sf_client)

        data = {
            "spend": spend if spend else {},
            "spend_price_volume_variance": spend_price_volume_variance if spend_price_volume_variance else {},
            "single_multi_source_data": single_multi_source_data if single_multi_source_data else {}
        }

        log.info("Compiled data for supplier %s, material %s: %s", supplier, material, data)

        prompt = generate_spend_insights_prompt_v2(supplier, material, data, currency,year)
        response = generate_chat_response_with_chain(prompt=prompt, temperature=0.7, model='gpt-4o').replace('```json', '').replace('```', '')
        parsed_response = json.loads(response)
        spend = parsed_response.get("spend", [])

        log.info("Generated spend insights for %s - %s", supplier, material)
        return {"supplier": supplier, "material": material, "category": category, "response": spend, "analytics": "Spend"}

    except Exception as e:
        log.error("Error processing record %s - %s: %s", record.get('SUPPLIER'), record.get('MATERIAL'), e)
        return None


def extract_sku_df_for_insights(unique_suppliers, category, records, sf_client,year):

    log.info("Generating spend insights for category: %s", category)
    currency = fetch_currency(sf_client)

    log.info("Fetched currency symbol: %s", currency)

    spend_results = []
    spend_results_additional = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        supplier_futures = [executor.submit(process_supplier, supplier, category, currency, sf_client,year) for supplier in unique_suppliers]
        for future in concurrent.futures.as_completed(supplier_futures):
            result = future.result()
            if result:
                spend_results_additional.append(result)


        record_futures = [executor.submit(process_record, record, category, currency, sf_client,year) for record in records]
        for future in concurrent.futures.as_completed(record_futures):
            result = future.result()
            if result:
                spend_results.append(result)

    log.info("Finished spend insight generation for category: %s", category)
    return spend_results + spend_results_additional


def process_supplier_insights(supplier, category, currency, year_master_subquery, sf_client,year):
    """
    Processes individual supplier features and generates insights.
    """
    supplier_data = []

    try:
        log.info(f"Processing supplier: {supplier}")
        top_single_sourced_materials_data = top_single_sourced_materials(supplier, category, sf_client)
        spend_increase_yoy_on_supplier_data = spend_increase_yoy_on_supplier(supplier, category, sf_client)

        prompt = generate_additional_supplier_insights_prompt(
            top_single_sourced_materials_data,
            spend_increase_yoy_on_supplier_data,
            currency,
            supplier,
            category,
            year
        )
        response = json.loads(
            generate_chat_response_with_chain(prompt=prompt, temperature=0.7, model='gpt-4o')
            .replace('```json', '').replace('```', '')
        )
        supplier_data.append({
            "supplier": supplier,
            "material": "NULL",
            "category": category,
            "response": response.get("supplier", []),
            "analytics": "Supplier"
        })
        log.info(f"Initial insights generated for {supplier}")

       
        features = {}
        try:
            features["single_source_spend"] = get_single_source_data(supplier, category, year_master_subquery, sf_client)
        except Exception as e:
            log.error(f"{supplier} - Failed to fetch single_source_spend: {e}")
            features["single_source_spend"] = []

        try:
            features["high_spend_low_invoice_risk"] = get_high_spend_invoice_risk(supplier, category, year_master_subquery, sf_client)
        except Exception as e:
            log.error(f"{supplier} - Failed to fetch high_spend_low_invoice_risk: {e}")
            features["high_spend_low_invoice_risk"] = []

        try:
            features["multi_source_drop_risk"] = get_multi_spend_drop_risk(supplier, category, year_master_subquery, sf_client)
        except Exception as e:
            log.error(f"{supplier} - Failed to fetch multi_source_drop_risk: {e}")
            features["multi_source_drop_risk"] = []


        try:
            prompt = generate_supplier_insights_prompt_v2(features, currency, supplier,year)
            response = json.loads(
                generate_chat_response_with_chain(prompt=prompt, temperature=0.7, model='gpt-4o')
                .replace('```json', '').replace('```', '')
            )
            supplier_data.append({
                "supplier": supplier,
                "material": "NULL",
                "category": category,
                "response": response.get("supplier", []),
                "analytics": "Supplier"
            })
            log.info(f"Final insights generated for {supplier}")
        except Exception as e:
            log.error(f"{supplier} - Failed to generate final supplier insights: {e}")

    except Exception as e:
        log.error(f"Unexpected error while processing {supplier}: {e}")

    return supplier_data

def extract_supplier_insight_features(category, unique_suppliers, sf_client,year) -> dict:
    """
    Extracts supplier-specific negotiation features using robust query execution with fallback on failure.
    """

    log.info(f"Starting supplier feature extraction for category: {category}")
    supplier_results = []
    currency = fetch_currency(sf_client)
    year_master_subquery = "(SELECT MAX(YEAR) FROM DATA.NEGO_SUPPLIER_MASTER)"

    # Run in parallel using multithreading
    with ThreadPoolExecutor(max_workers=25) as executor:
        future_to_supplier = {
            executor.submit(process_supplier_insights, supplier, category, currency, year_master_subquery, sf_client,year): supplier
            for supplier in unique_suppliers
        }

        for future in as_completed(future_to_supplier):
            supplier = future_to_supplier[future]
            try:
                results = future.result()
                supplier_results.extend(results)
            except Exception as e:
                log.error(f"{supplier} - Failed in future thread: {e}")

    # Write results to JSON
    # try:
    #     output_path = current_file.parent / f"supplier_{category}.json"
    #     with open(output_path, "w", encoding="utf-8") as file:
    #         json.dump(supplier_results, file, indent=4, ensure_ascii=False)
    #     log.info(f"Results written to {output_path}")
    # except Exception as e:
    #     log.error(f"Failed to write output JSON file: {e}")

    return supplier_results

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

    return filtered_df

def opportunity_insights(category,records,sf_client,year):
    
    log.info(f"Starting opportunity insights for category: {category} with {len(records)} records.")

    opportunity_results = []    
    currency = fetch_currency(sf_client)
    log.info(f"Fetched currency symbol: {currency}")

    for record in records:

        opportunity_insight = {}
        opportunity_data = extract_category_analytic_data(record['SUPPLIER'],[record['MATERIAL']],category,sf_client)

        opportunity_data = {key: value[0].to_dict() for key, value in opportunity_data.items()}

        if opportunity_data == None:
            log.warning(f"No opportunity data found for Supplier={record['SUPPLIER']}, Material={record['MATERIAL']}. Skipping.")
            continue

        log.debug(f"Extracted opportunity data for supplier: {record['SUPPLIER']} and material: {record['MATERIAL']} \n Opportunity Data: {opportunity_data}")
  
        try:
            with ThreadPoolExecutor(max_workers=1000) as executor:
                futures = {
                    executor.submit(
                        lambda name, df: (name, generate_chat_response_with_chain(
                            prompt=generate_insights_prompt_v2(supplier=record['SUPPLIER'],material=record['MATERIAL'],name=name,info=df,currency_symbol=currency), temperature=0.2,model='gpt-4o')),
                        name, df
                    ): name
                    for name, df in opportunity_data.items()
                }

                for future in as_completed(futures):
                    try:
                        name, insight = future.result()
                        opportunity_insight[name] = json.loads(insight.replace('```json','').replace('```',''))
                    except Exception as e:
                        log.error(f"Error processing future for {futures[future]}: {e}")
            
                opportunity_results.append({"supplier":record['SUPPLIER'],"material":record['MATERIAL'],"category":category,"response":opportunity_insight,"analytics":"Opportunity"})
                # with open (f"{current_file.parent}/opportunity_{category}.json", "w") as file:
                #     json.dump(opportunity_results, file, indent=4, ensure_ascii=False)

        except Exception as e:
            log.error(f"Error generating insights for supplier: {record['SUPPLIER']}, material: {record['MATERIAL']}, category: {category}. Error: {e}")

    log.info(f"Opportunity insights extraction completed for category: {category}. Total records processed: {len(opportunity_results)}")

    return opportunity_results

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

    analytic_map_df['KPI_TABLE_NAME'] = analytic_map_df['KPI_TABLE_NAME'].str.replace("_FRONTEND", "", regex=False)
    analytic_map_df = filter_valid_kpi_tables(analytic_map_df, sf_client)

    data_dict = {}

    def process_row(row):
        try:
            if not row.KPI_TABLE_NAME:
                return None

            column_query = f"""
            SELECT COLUMN_NAME
            FROM information_schema.columns
            WHERE TABLE_SCHEMA = 'DATA'
            AND TABLE_NAME = '{row.KPI_TABLE_NAME}'
            AND COLUMN_NAME IN ('MATERIAL', 'SUPPLIER')
            """
            column_names = sf_client.fetch_dataframe(column_query)['COLUMN_NAME'].str.upper().tolist()

            log.debug("Column names found for table %s: %s", row.KPI_TABLE_NAME, column_names)

            has_material_column = "MATERIAL" in column_names
            has_supplier_column = "SUPPLIER" in column_names

            log.debug("Does table %s have 'MATERIAL' column? %s", row.KPI_TABLE_NAME, has_material_column)
            log.debug("Does table %s have 'SUPPLIER' column? %s", row.KPI_TABLE_NAME, has_supplier_column)

            sku_query = ""
            if skus and has_material_column:
                safe_skus = [sku.replace("'", "''") for sku in skus]
                formatted_skus = "', '".join(safe_skus)
                sku_query = f"AND MATERIAL IN ('{formatted_skus}')"

            if not has_supplier_column:
                return None

            filter_condition = f"""
                SUPPLIER = '{supplier_name.replace("'", "''")}'
                AND LOWER(category) = LOWER('{category_name}')
                AND YEAR = (SELECT MAX(YEAR) FROM DATA.{row.KPI_TABLE_NAME})
                {sku_query}
            """

            analytic_data = pd.DataFrame(
                sf_client.select_records_with_filter(
                    table_name=f'DATA.{row.KPI_TABLE_NAME}',
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

    with ThreadPoolExecutor(max_workers=20) as executor:
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


### Previous version of extract_category_analytic_data

# def extract_category_analytic_data(supplier_name: str, skus, category_name: str, sf_client):
#     """
#     Extracts category analytic data for a supplier and category from the KPI tables.
#     """

#     analytic_map_query = f"""
#         SELECT * FROM DATA.T_C_KPI_TABLE_MAPPING_FRONTEND
#         WHERE LOWER(CATEGORY) = LOWER('{category_name}')
#     """
#     analytic_map_df = sf_client.fetch_dataframe(analytic_map_query)


#     if analytic_map_df.empty:
#         print("No KPI table mapping found for category: %s", category_name)
#         return None

#     # Normalize table names
#     analytic_map_df['KPI_TABLE_NAME'] = analytic_map_df['KPI_TABLE_NAME'].str.replace("_FRONTEND", "", regex=False)
#     analytic_map_df = filter_valid_kpi_tables(analytic_map_df, sf_client)

#     data_dict = {}

#     for row in analytic_map_df.itertuples():
#         if not row.KPI_TABLE_NAME:
#             continue

#         column_query = f"""
#         SELECT COLUMN_NAME
#         FROM information_schema.columns
#         WHERE TABLE_SCHEMA = 'DATA'
#         AND TABLE_NAME = '{row.KPI_TABLE_NAME}'
#         AND COLUMN_NAME IN ('MATERIAL', 'SUPPLIER')
#         """

#         column_names = sf_client.fetch_dataframe(column_query)['COLUMN_NAME'].str.upper().tolist()
#         print("Column names found for table %s: %s", row.KPI_TABLE_NAME, column_names)

#         has_material_column = "MATERIAL" in column_names
#         has_supplier_column = "SUPPLIER" in column_names
#         print("Does table %s have 'MATERIAL' column? %s", row.KPI_TABLE_NAME, has_material_column)
#         print("Does table %s have 'SUPPLIER' column? %s", row.KPI_TABLE_NAME, has_supplier_column)
#         # Dynamically construct SKU filter if applicable

#         try:
#             # Format SKU clause
#             sku_query = ""
#             filter_condition=""
#             if skus and has_material_column:
#                 # Ensure all SKUs are treated as full items, even if they contain commas
#                 safe_skus = [sku.replace("'", "''") for sku in skus]  # escape single quotes
#                 formatted_skus = "', '".join(safe_skus)
#                 sku_query = f"AND MATERIAL IN ('{formatted_skus}')"

#             if has_supplier_column:# Query the analytic table
#                 filter_condition = f"""
#                     SUPPLIER = '{supplier_name.replace("'", "''")}'
#                     AND LOWER(category) = LOWER('{category_name}')
#                     AND YEAR = (SELECT MAX(YEAR) FROM DATA.{row.KPI_TABLE_NAME})
#                     {sku_query}
#                 """

#             analytic_data = pd.DataFrame(
#                 sf_client.select_records_with_filter(
#                     table_name=f'DATA.{row.KPI_TABLE_NAME}',
#                     filter_condition=filter_condition,
#                 )
#             )

#             if analytic_data.empty:
#                 continue

#             obj_cols = analytic_data.select_dtypes(include="object").columns
#             if "MATERIAL" in obj_cols:
#                 obj_cols = obj_cols.drop("MATERIAL")

#             obj_map = {col: "first" for col in obj_cols}

#             # Prompt LLM to classify numeric aggregations
#             numeric_cols = [col for col in analytic_data.select_dtypes(include='number').columns if col != 'YEAR']
#             prompt = classify_prompt(analytic_data[numeric_cols].head(2))

#             agg_map_raw = generate_chat_response_with_chain(prompt=prompt, model='gpt-4o')
#             agg_map_raw = re.sub(r"(?:python)?\s*", "", agg_map_raw).strip("`\n ")
#             agg_map = ast.literal_eval(agg_map_raw)

#             groupby_cols = ["YEAR"]
#             if "MATERIAL" in analytic_data.columns:
#                 groupby_cols.append("MATERIAL")

#             clean_obj_map = {k: v for k, v in obj_map.items() if k not in groupby_cols}
#             year_df = analytic_data.groupby(groupby_cols).agg(agg_map | clean_obj_map).reset_index()

#             print("Query executed for KPI: %s", row.KPI_NAME)
#             data_dict[row.KPI_NAME] = [year_df,row.KPI_OPPORTUNITY_COLUMN_NAME]

#         except Exception as e:
#             print("Failed processing table %s for supplier %s in category %s. Error: %s",
#                       row.KPI_TABLE_NAME, supplier_name, category_name, str(e))
#             continue

#     if not data_dict:
#         print("No analytic data extracted for category: %s", category_name)
#         return None

#     return data_dict
