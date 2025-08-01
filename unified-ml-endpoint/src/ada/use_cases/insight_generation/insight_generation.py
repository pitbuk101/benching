import sys
from pathlib import Path
import re
from insight_utils import sanitize_pythonic_json_string,find_linked_insights_ids,insert_top_ideas,json_to_excel, extract_json,process_insight_queries, get_linked_insights, find_related_insights, objective_mapping, insert_insights_master, insert_negotiation_insights
import json
import ast
import uuid
from datetime import datetime
from sf_connector import SnowflakeClient
import argparse
import concurrent.futures
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

current_file = Path(__file__)
sys.path.append(str(current_file.parents[3]))

from prompts import generate_procurement_categorization_prompt,generate_insights_prompt_uhg,generate_top_ideas_prompt_uhg,generate_insights_prompt_v2,generate_top_ideas_prompt_v3,generate_rca_prompt_for_ideas,find_linked_and_related_insights_for_top_ideas_prompt,find_linked_related_insights_top_ideas_prompt,generate_top_ideas_prompt_v2,generate_refine_idea_titles_prompt,generate_top_ideas_prompt,extract_impact_prompt, generate_rca_prompt,extract_supplier_sku_prompt
from ada.components.llm_models.generic_calls import generate_chat_response_with_chain
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger
from sql_queries.negotiation_queries import top_suppliers_with_most_opportunity, supplier_opportunity_breakdown, supplier_top_opportunity_materials, supplier_top_opportunity_plants, supplier_top_opportunity_regions, suppliers_with_yoy_increase_in_single_source_spend, single_source_spend_by_supplier, top_tail_spend_suppliers, total_spend_by_supplier, category_supplier_stats

insight_generation_conf = read_config("use-cases.yml")["insight_generation"]
log = get_logger("insights_top_ideas_generation")

def generate_rca_for_top_ideas(ideas:list):
    """
    Generate RCA for each insights using analytics, linked insights and related insights
    Args:
        insights (list): Insights to generate RCA for
    Returns
        insights: List of dictionaries containing rca,top_idea,category,analytic_name,title,description,impact,update_info and linked_insights.
    """

    output = []

    for idea in ideas:

        prompt = generate_rca_prompt_for_ideas(idea)
        response = generate_chat_response_with_chain(prompt,temperature=insight_model_conf["temperature"],model =insight_model_conf["model_name"])

        match = re.search(r"```dict(.*?)```", response, re.DOTALL)
        if match:
            dict_str = match.group(1).strip()  
            data_dict = ast.literal_eval(dict_str)
            idea["rca"] = data_dict 

        output.append(idea)   

    return output



def generate_rca(insights:list):
    """
    Generate RCA for each insights using analytics, linked insights and related insights
    Args:
        insights (list): Insights to generate RCA for
    Returns
        insights: List of dictionaries containing rca,top_idea,category,analytic_name,title,description,impact,update_info and linked_insights.
    """

    output = []

    # insights = find_related_insights(insights)

    for insight in insights:
        if insight["insight"] == "NULL":
            insight["rca"] = {}
            output.append(insight)
            continue

        prompt = generate_rca_prompt(insight["analytics_name"],insight["insight"],insight["linked_insights"],insight["related_insights"])
        response = generate_chat_response_with_chain(prompt,temperature=insight_model_conf["temperature"],model =insight_model_conf["model_name"])

        match = re.search(r"```dict(.*?)```", response, re.DOTALL)
        if match:
            dict_str = match.group(1).strip()  
            data_dict = ast.literal_eval(dict_str)
            insight["rca"] = data_dict 

        output.append(insight)   

    return output


def extract_supplier_sku_details(insights:json):

    all_insights = []

    for insight in insights:

        try:
            
            if insight["insight"] == "NULL":
                insight["supplier_sku_information"] = {"supplier": [], "sku": []}
                insight["id"] = str(uuid.uuid4())
                insight["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                all_insights.append(insight)
                continue 

            prompt = extract_supplier_sku_prompt(insight["insight"])

            response = generate_chat_response_with_chain(prompt,temperature=insight_model_conf["temperature"],model=insight_model_conf["model_name"])
            match = re.search(r"```dict(.*?)```", response, re.DOTALL)
            if match:
                dict_str = match.group(1).strip()  
                data_dict = ast.literal_eval(dict_str)
                insight["supplier_sku_information"] = data_dict 
                insight["id"] = str(uuid.uuid4())
                insight["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                all_insights.append(insight)
            else:
                insight["supplier_sku_information"] = {"supplier": [], "sku": []}
                insight["id"] = str(uuid.uuid4())
                insight["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                all_insights.append(insight)


        except Exception as e:
            insight["supplier_sku_information"] = {"supplier": [], "sku": []}
            insight["id"] = str(uuid.uuid4())
            insight["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            all_insights.append(insight)
            print("Error",e)

    return all_insights


def extract_impact(top_ideas:json):

    all_insights = []

    for idea in top_ideas:

        try:
            
            prompt = extract_impact_prompt(idea["description"])
            response = generate_chat_response_with_chain(prompt,temperature=insight_model_conf["temperature"],model=insight_model_conf["model_name"])
            match = re.search(r"```dict(.*?)```", response, re.DOTALL)
            if match:
                dict_str = match.group(1).strip()  
                data_dict = ast.literal_eval(dict_str)
                idea.update(data_dict)
                all_insights.append(idea)
            else:
                idea["impact"] = []
                all_insights.append(idea)

        except Exception as e:
            idea["impact"] = []
            all_insights.append(idea)
            print("Error",e)

    return all_insights


def generate_top_ideas(tenantId, insights, category):
    log.info(f"Generating top ideas for category: {category}")

    combined_insights = []
    all_insights = []
    top_ideas_details = []

    for insight in insights:
        if insight["insight"] == "NULL":
            continue
        if insight.get("insight"):
            all_insights.append(insight["insight"])
            combined_insights.append(insight["insight"])
        else:
            continue

    log.debug("Combined insights for ideas generation.")

    if tenantId in [
        "920a2f73-c7db-405f-98ea-f768c6da864f",
        "fce26b80-b826-4c35-a519-765872745aa0",
        "dc6b5f00-0718-4089-bb70-7d3d14df7cbf",
        "048ee4ca-43b3-48e5-b95a-bd442ba15c91",
        "6566983b-2977-4deb-9bb4-2d3ba7b7ac8c"
    ]: 
        if category.lower() == 'marketing svcs':
            prompt = generate_top_ideas_prompt_uhg(all_insights)
        else:
            prompt = generate_top_ideas_prompt_v3(all_insights,category)
    elif tenantId == "519f6dbf-da97-47ba-9f4f-298e832e34bb":
        prompt = generate_top_ideas_prompt_uhg(all_insights)

    top_ideas = generate_chat_response_with_chain(prompt, model=insight_model_conf["model_name"], temperature=insight_model_conf["temperature"])
    log.info("Generated Top Ideas for category %s: %s", category, top_ideas)

    top_ideas = extract_json(top_ideas)
    log.debug("JSON for top ideas extracted successfully for category %s", category)

    # Step 1: Segment Categorization in Parallel
    def categorize_segment(idea):
        main_idea = json.dumps(idea).replace("{", "{{{{").replace("}", "}}}}")
        segment_prompt = generate_procurement_categorization_prompt(main_idea)
        segment_info = generate_chat_response_with_chain(segment_prompt, temperature=insight_model_conf["temperature"], model=insight_model_conf["model_name"])
        match = re.search(r"```dict(.*?)```", segment_info, re.DOTALL)
        if match:
            try:
                dict_str = match.group(1).strip()
                data_dict = ast.literal_eval(dict_str)
                idea["segment"] = data_dict.get("segment", None)
            except Exception as e:
                log.error(f"Segment parsing failed: {e}")
        return idea

    with ThreadPoolExecutor(max_workers=5) as executor:
        top_ideas = list(executor.map(categorize_segment, top_ideas))

    log.info("Segment categorization complete.")

    # Step 2: Link and related insights for top ideas - Parallel
    def enrich_top_idea(idea):
        try:
            prompt = find_linked_and_related_insights_for_top_ideas_prompt(idea, combined_insights, top_ideas)
            info = generate_chat_response_with_chain(prompt, temperature=insight_model_conf["temperature"], model=insight_model_conf["model_name"])
            match = re.search(r"```dict(.*?)```", info, re.DOTALL)
            if match:
                dict_str = match.group(1).strip()
                data_dict = ast.literal_eval(dict_str)
                idea["id"] = str(uuid.uuid4())
                idea["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                idea["category"] = category
                idea.update(data_dict)
        except Exception as e:
            log.error(f"Enriching top idea failed: {e}")
        return idea

    with ThreadPoolExecutor(max_workers=5) as executor:
        top_ideas_details = list(executor.map(enrich_top_idea, top_ideas))

    log.info("Linked and related insights for top ideas identified.")

    top_ideas = extract_impact(top_ideas_details)
    log.info("Impact value extracted for top ideas.")

    top_ideas = generate_rca_for_top_ideas(top_ideas)
    log.info("RCA generated for top ideas")

    # with open(f"{current_file.parent}/top_ideas_temp_{category}.json", "w") as file:
    #     json.dump(top_ideas, file, indent=4, ensure_ascii=False)

    # Step 3: Linked/related insights per insight - Parallel
    def enrich_insight(insight):
        if insight["insight"] == "NULL":
            insight["top_ideas"] = []
            insight["linked_insights"] = []
            insight["related_insights"] = []
            return insight

        try:
            prompt = find_linked_related_insights_top_ideas_prompt(insight["insight"], combined_insights, top_ideas)
            result = generate_chat_response_with_chain(prompt, temperature=insight_model_conf["temperature"], model=insight_model_conf["model_name"])
            match = re.search(r"```dict(.*?)```", result, re.DOTALL)
            if match:
                dict_str = match.group(1).strip()
                data_dict = ast.literal_eval(dict_str)
                insight.update(data_dict)
        except Exception as e:
            log.error(f"Enriching insight failed: {e}")
        return insight

    with ThreadPoolExecutor(max_workers=5) as executor:
        final_insights = list(executor.map(enrich_insight, insights))

    log.info("Linked and related insights for each insight identified.")

    # with open(f"{current_file.parent}/checkpoint3_{category}.json", "w") as file:
    #     json.dump(final_insights, file, indent=4)

    insights = generate_rca(final_insights)
    log.info("RCA generated for insights")

    insights = objective_mapping(objectives_conf, insights)
    log.info("Objective Mapping done for insights")

    insights = extract_supplier_sku_details(insights)
    log.info("Supplier-SKU details extracted from insights")

    with open(f"{current_file.parent}/insights_master_{category}.json", "w") as file:
        json.dump(insights, file, indent=4, ensure_ascii=False)

    top_ideas = find_linked_insights_ids(top_ideas, insights)
    log.info("Linked insight IDs identified and mapped.")

    with open(f"{current_file.parent}/top_ideas_{category}.json", "w") as file:
        json.dump(top_ideas, file, indent=4, ensure_ascii=False)

    return {"top_ideas": top_ideas, "insights": insights}


def enforce_limit(sql_query,limit=50):

    query = sql_query.strip().rstrip(';')
    limit_pattern = re.compile(r'\bLIMIT\s+\d+(\s*,\s*\d+)?\b', re.IGNORECASE)

    if limit_pattern.search(query):
        query = limit_pattern.sub(f"LIMIT {limit}", query)
    else:
        query += f" LIMIT {limit}"

    log.info("Applying LIMIT clause to SQL query")

    return query + ';'


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
    currency_symbol = result[0][0] if result else None
    log.info("Fetched currency symbol: %s", currency_symbol)
    return currency_symbol


def process_queries(path,category,tenantId,sf_client):

    log.debug("Processing SQL queries for category: %s",category)

    data = []

    for root, _, files in os.walk(path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            if file_name.lower().endswith('.sql'):
                insight_query = os.path.splitext(file_name)[0] 

                if tenantId in ["920a2f73-c7db-405f-98ea-f768c6da864f","fce26b80-b826-4c35-a519-765872745aa0","dc6b5f00-0718-4089-bb70-7d3d14df7cbf"]:
                    insight_query = insight_query.lower()
                    insight_query = insight_query.replace("_"," ").replace("valves",category.lower()).replace("bearings",category.lower())

                    if "agency cleansheet" in insight_query or "agency fees benchmarks" in insight_query:
                        analytics_name = "Agency Cleansheet"
                    elif "bill rate" in insight_query:
                        analytics_name = "Bill Rate Benchmarks"
                    elif "operating unit" in insight_query:
                        analytics_name = "Single-OU Suppliers Elimination"
                    elif "deliverable benchmarks" in insight_query:
                        analytics_name = "Deliverable Benchmarking"
                    elif "labour rate" in insight_query:
                        analytics_name = "Labor Rate Benchmarking"
                    elif "media" in insight_query:
                        analytics_name = "Media Benchmarking"
                    elif "non working" in insight_query or "working" in insight_query:
                        analytics_name = "Working vs Non-Working Benchmarks"
                    elif "technology" in insight_query:
                        analytics_name = "Technology Benchmarks"
                    elif "early payment" in insight_query:
                        analytics_name = "Early Payments"
                    elif "hcc lcc" in insight_query:
                        analytics_name = "LCC-HCC-Opportunity"
                    elif "oem" in insight_query:
                        analytics_name = "OEM-Non-OEM Opportunity"
                    elif "parametric cost" in insight_query:
                        analytics_name = "Parametric Cost Modelling"
                    elif "price arbitrage" in insight_query:
                        analytics_name = "Price Arbitrage"
                    elif "rate harmonization" in insight_query:
                        analytics_name = "Rate Harmonization"
                    elif "unused discount" in insight_query:
                        analytics_name = "Unused Discounts"
                    elif "standardization" in insight_query:
                        analytics_name = "Payment Term Standardization"
                    elif "spend" in insight_query:
                        analytics_name = "Spend Analysis"
                    elif "market" in insight_query or "variation" in insight_query or "forecast" in insight_query or "cost driver" in insight_query or "component share" in insight_query or "cost breakdown" in insight_query or "global market" in insight_query or "latest" in insight_query or "updates" in insight_query:
                        analytics_name = "Market Analysis"
                    else:
                        analytics_name = "Others"

                    with open(file_path, 'r') as f:
                        sql_query = f.read()
                        sql_query = sql_query.replace('Valves',category).replace("YEAR(CURRENT_DATE())",'2025').replace("YEAR(CURRENT_DATE())","'2025'").replace("bearings",category).replace("Bearings",category).replace("BEARINGS",category).replace("YEAR(CURRENT_DATE())","'2025'").replace("YEAR(CURRENT_DATE)","'2025'").replace("YEAR (CURRENT_DATE)","'2025'").replace("YEAR (CURRENT_DATE())","'2025'").replace("valves",category).replace("Valves",category).replace("VALVES",category)
                        sql_query = enforce_limit(sql_query)
                    
                    log.info(f"DEMO - Insights Query: {insight_query} - Analytics: {analytics_name} - SQL Query: {sql_query}")


                elif tenantId == "519f6dbf-da97-47ba-9f4f-298e832e34bb":
                    
                    insight_query = insight_query.lower()
                    insight_query = insight_query.replace("_"," ").replace("current","2024").lower().replace("bearings",category.lower())

                    if "agency cleansheet" in insight_query or "agency fees benchmarks" in insight_query:
                        analytics_name = "Agency Cleansheet"
                    elif "bill rate" in insight_query:
                        analytics_name = "Bill Rate Benchmarks"
                    elif "operating unit" in insight_query:
                        analytics_name = "Single-OU Suppliers Elimination"
                    elif "deliverable benchmarks" in insight_query:
                        analytics_name = "Deliverable Benchmarking"
                    elif "labour rate" in insight_query:
                        analytics_name = "Labor Rate Benchmarking"
                    elif "media" in insight_query:
                        analytics_name = "Media Benchmarking"
                    elif "non working" in insight_query or "working" in insight_query:
                        analytics_name = "Working vs Non-Working Benchmarks"
                    elif "technology" in insight_query:
                        analytics_name = "Technology Benchmarks"
                    else:
                        analytics_name = "Others"

                    with open(file_path, 'r') as f:
                        sql_query = f.read()    
                        sql_query = sql_query.replace("YEAR(CURRENT_DATE())",'2024').replace("YEAR(CURRENT_DATE())","'2024'").replace("bearings",category.lower()).replace("Bearings",category.lower()).replace("BEARINGS",category.lower()).replace("YEAR(CURRENT_DATE())","'2024'").replace("YEAR(CURRENT_DATE)","'2024'").replace("YEAR (CURRENT_DATE)","'2024'").replace("YEAR (CURRENT_DATE())","'2024'")
                        sql_query = enforce_limit(sql_query)

                    log.info(f"UHG - Insights Query: {insight_query} - Analytics: {analytics_name} - SQL Query: {sql_query}")


                elif tenantId == "048ee4ca-43b3-48e5-b95a-bd442ba15c91":
                    
                    insight_query = insight_query.lower()
                    insight_query = insight_query.replace("_"," ").replace("current","2023").lower().replace("valves",category.lower()).replace("cibc",category.lower())

                    if "lpp" in insight_query:
                        analytics_name = "Linear Performance Pricing"
                    elif "parametric cost modelling" in insight_query:
                        analytics_name = "Parametric Cost Modelling"
                    elif "price arbitrage" in insight_query:
                        analytics_name = "Price Arbitrage"
                    elif "market" in insight_query:
                        analytics_name = "Market Analysis"
                    elif "tail" in insight_query or "key" in insight_query or "spend" in insight_query:
                        analytics_name = "Supplier Consolidation"
                    else:
                        analytics_name = "Others"

                    with open(file_path, 'r') as f:
                        sql_query = f.read()    
                        sql_query = sql_query.replace("YEAR(CURRENT_DATE())","'2023'").replace("valves",category.lower()).replace("Valves",category.lower()).replace("VALVES",category.lower()).replace("YEAR(CURRENT_DATE())","'2023'").replace("YEAR(CURRENT_DATE)","'2023'").replace("YEAR (CURRENT_DATE)","'2023'").replace("YEAR (CURRENT_DATE())","'2023'").replace("cibc",category.lower()).replace("CIBC",category.lower()).replace("Cibc",category.lower())
                        sql_query = enforce_limit(sql_query)

                    log.info(f"ZXD - Insights Query: {insight_query} - Analytics: {analytics_name} - SQL Query: {sql_query}")

                elif tenantId == "6566983b-2977-4deb-9bb4-2d3ba7b7ac8c":

                    insight_query = insight_query.lower()
                    insight_query = insight_query.replace("_"," ").replace("current","2025").lower().replace("valves",category.lower()).replace("cibc",category.lower()).replace("batteries",category.lower())

                    if "payment term" in insight_query:
                        analytics_name = "Payment Term Standardization"
                    elif "market" in insight_query or "trend" in insight_query or "variation" in insight_query or "forecast" in insight_query or "cost driver" in insight_query or "component share" in insight_query or "cost breakdown" in insight_query or "global market" in insight_query or "latest" in insight_query or "updates" in insight_query or "net" in insight_query:
                        analytics_name = "Market Analysis"
                    elif "early payment" in insight_query:
                        analytics_name = "Early Payments"
                    elif "tail" in insight_query or "key" in insight_query or "spend" in insight_query or "unit price" in insight_query:
                        analytics_name = "Spend Analysis"
                    elif "price arbitrage" in insight_query:
                        analytics_name = "Price Arbitrage"
                    elif "hcc lcc" in insight_query:
                        analytics_name = "LCC-HCC-Opportunity"
                    elif "oem" in insight_query:
                        analytics_name = "OEM-Non-OEM Opportunity"
                    elif "contracts" in insight_query:
                        analytics_name = "Contracts"
                    else:
                        analytics_name = "Others"

                    with open(file_path, 'r') as f:
                        sql_query = f.read()  
                        sql_query = sql_query.replace("YEAR(CURRENT_DATE())","'2025'").replace("valves",category.lower()).replace("Valves",category.lower()).replace("VALVES",category.lower()).replace("YEAR(CURRENT_DATE())","'2025'").replace("YEAR(CURRENT_DATE)","'2025'").replace("YEAR (CURRENT_DATE)","'2025'").replace("YEAR (CURRENT_DATE())","'2025'").replace("cibc",category.lower()).replace("CIBC",category.lower()).replace("Cibc",category.lower()).replace("Batteries",category.lower()).replace("batteries",category.lower()).replace("BATTERIES",category.lower())
                        sql_query = enforce_limit(sql_query)

                    log.info(f"EGA - Insights Query: {insight_query} - Analytics: {analytics_name} - SQL Query: {sql_query}")

                data.append({
                    "insight_query": insight_query,
                    "analytics_name": analytics_name,
                    "segment":"General",
                    "category": category,
                    "sql": sql_query,
                })

    log.info("SQL Queries processed successfully")

    return data
    

def generate_insights(item, tenantId,sf_client,category):

    try:
        result = sf_client.execute_query(item.get("sql",""))
        log.info("SQL query executed successfully")  
    except Exception as e:
        log.error("Error processing SQL: %s",str(e))
        item["data"] = []
        item["insight"] = "NULL"
        return item
        
    if len(result) == 0 or result == [[None]] or result == [[None],[None]]:
        log.warning("No data found")
        item["data"] = []
        item["insight"] = "NULL"
        return item
    
    currency = fetch_currency(sf_client)

    item["data"] = result
    item_str = str(item).replace("{", "{{").replace("}", "}}")

    if tenantId in ["920a2f73-c7db-405f-98ea-f768c6da864f","fce26b80-b826-4c35-a519-765872745aa0" ,"dc6b5f00-0718-4089-bb70-7d3d14df7cbf","048ee4ca-43b3-48e5-b95a-bd442ba15c91","6566983b-2977-4deb-9bb4-2d3ba7b7ac8c"]: 
        if item['category'].lower() == "marketing svcs":
            insight_prompt = generate_insights_prompt_uhg(data=item_str,currency=currency,category=category)
        else:
            insight_prompt = generate_insights_prompt_v2(data=item_str,currency=currency,category=category)
    elif tenantId == "519f6dbf-da97-47ba-9f4f-298e832e34bb":
        insight_prompt = generate_insights_prompt_uhg(data=item_str,currency=currency)

    log.debug(f"Prompt Initialized - Generating insights for query {item.get('insight_query','')} in category {category}")
    response = generate_chat_response_with_chain(insight_prompt,temperature=insight_model_conf["temperature"],model=insight_model_conf["model_name"])
    log.info("Model Response: %s",str(response))
    
    try:
        response = extract_json(response)
        item = response[0]
        log.info("Category %s - Insight: %s",category,str(item["insight"]))

        # match = re.search(r"```dict(.*?)```", response, re.DOTALL)
        # if match:
        #     dict_str = match.group(1).strip().replace("\\n","").replace("\\","")
        #     data_dict = ast.literal_eval(dict_str)
        #     data_dict["insight"] = data_dict["insight"].encode('utf-8').decode('unicode_escape').encode('latin1').decode('utf-8')
        #     data_dict["sql"] = str(item['sql'])
        #     data_dict["data"] = str(result)
        #     item = data_dict
        #     log.info("Category %s - Insight: %s",category,str(item["insight"]))
        #     return item        
    except Exception as e:
            log.error("Error parsing output: %s",str(e))
            item["data"] = []
            item["insight"] = "NULL"
            return item

    return item


def process_category(category,tenantId,sf_client):

    additional_data = []

    log.debug(f"Processing category: {category}")
    data = process_queries(path=f"{current_file.parent}/sql_queries/{tenantId}/",category=category,tenantId=tenantId,sf_client=sf_client)
    
    log.info(f"Processed SQL Queries for category {category}: {len(data)}")

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(generate_insights, item,tenantId,sf_client,category): "insights"
            for item in data
        }
        
        results = []
        for future in as_completed(futures):
            key = futures[future]
            results.append(future.result())
            log.info(f"Insights processed:{str(len(results))}")


    log.info("Generated Insights for Category: %s",category)
    log.info(f"Total insights for category {category}: {str(len(results))}")
    log.debug("Generating additional insights for negotiation")

    category_supplier_stat = category_supplier_stats(category=category,sf_client=sf_client)
    additional_data.append({
        "insight_query": "Find the category-supplier stats.",
        "analytics_name": "Negotiation",
        "segment":"General",
        "category": category,
        "sql": str(category_supplier_stat[1]),
        "data": str(category_supplier_stat[0])
    })
    log.info("Category-supplier stats fetched")
    
    suppliers_with_yoy_increase_in_single_source_spends = suppliers_with_yoy_increase_in_single_source_spend(category=category,sf_client=sf_client)
    additional_data.append({
        "insight_query": "Find the top 5 suppliers with YoY increase in single source spend.",
        "analytics_name": "Negotiation",
        "segment":"General",
        "category": category,
        "sql": str(suppliers_with_yoy_increase_in_single_source_spends[1]),
        "data": str(suppliers_with_yoy_increase_in_single_source_spends[0])
    })
    log.info("suppliers_with_yoy_increase_in_single_source_spend fetched")

    top_tail_spend_supplier = top_tail_spend_suppliers(category=category,sf_client=sf_client)
    additional_data.append({
        "insight_query": "Find the top 5 tail spend suppliers.",
        "analytics_name": "Negotiation",
        "segment":"General",
        "category": category,
        "sql": str(top_tail_spend_supplier[1]),
        "data": str(top_tail_spend_supplier[0])
    })
    log.info("top_tail_spend_suppliers fetched")

    top_supplier_with_most_opportunity = top_suppliers_with_most_opportunity(category,sf_client)
    additional_data.append({
        "insight_query": "Find the top 10 suppliers with most opportunity",
        "analytics_name": "Negotiation",
        "segment":"General",
        "category": category,
        "sql": str(top_supplier_with_most_opportunity[1]),
        "data": str(top_supplier_with_most_opportunity[0])
    })
    log.info("top_suppliers_with_most_opportunity fetched")

    for supplier_info in top_supplier_with_most_opportunity[0]:
        supplier = supplier_info['SUPPLIER']

        supplier_opportunity_breakdowns = supplier_opportunity_breakdown(supplier, category, sf_client)
        additional_data.append({
        "insight_query": f"Find the analytic-wise opportunity breakdown for supplier {supplier}",
        "analytics_name": "Negotiation",
        "segment":"General",
        "category": category,
        "sql": str(supplier_opportunity_breakdowns[1]),
        "data": str(supplier_opportunity_breakdowns[0])
        })
        log.info("supplier_opportunity_breakdown fetched for supplier %s",supplier)

        supplier_top_opportunity_material = supplier_top_opportunity_materials(supplier, category, sf_client)
        additional_data.append({
        "insight_query": f"Find the top 10 materials with most opportunity for supplier {supplier}",
        "analytics_name": "Negotiation",
        "segment":"General",
        "category": category,
        "sql": str(supplier_top_opportunity_material[1]),
        "data": str(supplier_top_opportunity_material[0])
        })
        log.info("supplier_top_opportunity_materials fetched for supplier %s",supplier)

        supplier_top_opportunity_plant = supplier_top_opportunity_plants(supplier, category, sf_client)
        additional_data.append({
        "insight_query": f"Find the top 10 plants with most opportunity for supplier {supplier}",
        "analytics_name": "Negotiation",
        "segment":"General",
        "category": category,
        "sql": str(supplier_top_opportunity_plant[1]),
        "data": str(supplier_top_opportunity_plant[0])
        })
        log.info("supplier_top_opportunity_plants fetched for supplier %s",supplier)

        supplier_top_opportunity_region = supplier_top_opportunity_regions(supplier, category, sf_client)
        additional_data.append({
        "insight_query": f"Find the top 10 countries with most opportunity for supplier {supplier}",
        "analytics_name": "Negotiation",
        "segment":"General",
        "category": category,
        "sql": str(supplier_top_opportunity_region[1]),
        "data": str(supplier_top_opportunity_region[0])
        })
        log.info("supplier_top_opportunity_regions fetched for supplier %s",supplier)

        total_spend_by_suppliers = total_spend_by_supplier(supplier, category, sf_client)
        additional_data.append({
        "insight_query": f"Find the total spend by supplier {supplier}",
        "analytics_name": "Negotiation",
        "segment":"General",
        "category": category,
        "sql": str(total_spend_by_suppliers[1]),
        "data": str(total_spend_by_suppliers[0])
        })
        log.info("total_spend_by_supplier fetched for supplier %s",supplier)

        single_source_spend_by_suppliers = single_source_spend_by_supplier(supplier, category, sf_client)
        additional_data.append({
        "insight_query": f"Find the single-source spend by supplier {supplier}",
        "analytics_name": "Negotiation",
        "segment":"General",
        "category": category,
        "sql": str(single_source_spend_by_suppliers[1]),
        "data": str(single_source_spend_by_suppliers[0])
        })
        log.info("single_source_spend_by_supplier fetched for supplier %s",supplier)

    additional_insights = []

    log.debug("Generating additional insights for category %s",category)

    for item in additional_data:

        if len(item['data']) == 0 or item['data'] == [[None]] or item['data'] == [[None],[None]]:
            item["insight"] = "NULL"
            log.warning("No data found")
            continue

        currency = fetch_currency(sf_client)
        item_str = str(item).replace("{", "{{").replace("}", "}}")

        insight_prompt = generate_insights_prompt_v2(data=item_str,currency=currency,category=category)
        log.debug("Prompt initialized for additional insights")
        response = generate_chat_response_with_chain(insight_prompt,temperature=insight_model_conf["temperature"],model=insight_model_conf["model_name"])
        log.info("Model Response: %s",str(response))
    
        try:

            response = extract_json(response)
            item = response[0]
            log.info("Category %s - Insight: %s",category,str(item["insight"]))

            # match = re.search(r"```dict(.*?)```", response, re.DOTALL)
            # if match:
                
            #     dict_str = match.group(1).strip().replace("\\n","").replace("\\","")
            #     data_dict = ast.literal_eval(dict_str)
            #     data_dict["insight"] = data_dict["insight"].encode('utf-8').decode('unicode_escape').encode('latin1').decode('utf-8')
            #     data_dict["sql"] = str(item['sql'])
            #     data_dict["data"] = str(item['data'])
            #     item = data_dict
            #     additional_insights.append(item)
            #     log.info("Category %s - Insight: %s",category,str(item["insight"]))

        except Exception as e:
            log.error("Error: %s",str(e))

    log.debug("Combining insights for category %s",category)

    results.extend(additional_insights)

    # with open(f"{current_file.parent}/insights_master_{category.lower()}_temp.json", "w") as file:
    #     json.dump(results, file, indent=4, ensure_ascii=False)

    top_ideas_insights_combined = generate_top_ideas(tenantId=tenantId,insights=results,category=category)

    return top_ideas_insights_combined


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate and refine top ideas for a given tenant ID.")
    parser.add_argument("--tenantId", type=str, required=True, help="Tenant ID for which to generate insights")

    args = parser.parse_args()
    tenantId = args.tenantId

    log.debug(f"Starting insights and top ideas generation process for tenantID: {tenantId}")

    if tenantId not in insight_generation_conf.get("tenant_ids", []):
        log.error(f"Tenant ID '{tenantId}' not found in configuration.")
        raise ValueError(f"Tenant ID '{tenantId}' not found in configuration.")

    sf_client = SnowflakeClient(tenant_id=tenantId)
    log.debug(f"Snowflake client initialized for tenant {tenantId}")

    tenant_conf = insight_generation_conf[f"{tenantId}"]
    insight_model_conf = tenant_conf["model"]
    log.debug(f"Model configuration for tenant {tenantId}: {insight_model_conf}")

    sf_categories = sf_client.execute_query(f"""
    SELECT DISTINCT TXT_CATEGORY_LEVEL_2 FROM 
    DATA.VT_C_FACT_INVOICEPOSITION_MULTIPLIED IVP
    JOIN DATA.VT_C_DIM_SOURCINGTREE_TECHCME SOUR ON SOUR.DIM_SOURCING_TREE = IVP.DIM_SOURCING_TREE
    ORDER BY TXT_CATEGORY_LEVEL_2
    """)

    categories = [item[0] for item in sf_categories if item[0] != 'Marketing Svcs']
    # categories = categories[:165]

    # categories = tenant_conf["categories"] + tenant_conf["additional_categories"]
    # categories = ["Accounting Services", "Actuators", "Air Freight", "Aluminum bars", "Audit Services - External", "Beams", "Bearings and bushings and wheels and gears", "Building Maintenance/Construction/Fix Services", "Business Function Specific Software", "Coating systems", "Community And Social Services", "Compounds and mixtures", "Concrete and cement and plaster", "Connectors", "Consulting Services - Management Consulting", "Copying, Printing, Scanning", "Corporate Services", "Corrugated Boards", "Electrical Engineering Services", "Electricity", "End User Devices - Desktops/ Laptops/Notebook", "Extrusions", "Faucet and shower heads, jets and parts and accessories", "Filters/Filter Media And Combo Bags", "Fire Detection And Burglar Alarm Systems Installation Service", "Flooring", "Foil", "Food Benefits", "Gaskets / Seals", "Gears", "HR Services", "HVAC Services", "Hardware", "Healthcare/Health Insurance", "IT Network/Infrastructure Hardware", "IT/ Telecom", "Metal cutting machine attachments", "Metal cutting machinery and accessories", "Metal cutting machines", "Metal cutting tools", "Metal forming dies and tooling", "Metal forming machinery and accessories", "Metal rolling machines", "Minerals", "Minerals and ores and metals", "Miscellaneous Expenses", "Miscellaneous fasteners", "Miscellaneous finishes", "Mobile/ Wireless Data", "Molded gaskets", "Moldings", "Motors", "Mounting hardware", "Newspaper & Magazines (Offline)", "Nickel sheets and ingots", "Non edible plant and forestry products", "Nonhazardous Waste Disposal", "Nonwoven fabrics", "Not Categorized", "Nuts", "Ocean - Container", "Office Furniture", "Office Supplies", "Outsourced Transportation Services / Admin", "Packaging", "Packaging Tubes And Cores And Accessories", "Paper making and paper processing machinery and equipment and supplies", "Pipe, Hose, Tube & Fittings", "Plastic films", "Plate", "Plumbing fixtures", "Pneumatic and hydraulic and electric control systems", "Politics And Civic Affairs Services", "Powdered metal components", "Printer Catridges, Toners, Ribbons", "Processed and synthetic rubber", "Promotional Activities / Materials", "Public Administration And Finance Services", "Pumps, Compressors & Parts", "Raw Materials", "Recruiting Services", "Research Or Testing Facilities", "Road Freight", "Rope and chain and cable and wire and strap", "Screws", "Security", "Security Equipment", "Separation machinery and equipment", "Software Maintenance And Support", "Specialty fabrics or cloth", "Specialty insulation", "Specialty steel coils", "Stamped components", "Structural materials", "Structural products", "Synthetic fabrics", "Technical Building Maintenance", "Textile and fabric machinery and accessories", "Tin sheet", "Tools (Clamps, Pliers, Wrenches, Tool Kits, Etc.)", "Transport Services / Admin", "Turbines & Parts", "Underground roof support structures", "Utilities", "Valves", "Warehousing", "Washers", "Waste Management", "Water Treatment Services", "Welding and soldering and brazing machinery and accessories and supplies", "Welding and soldering and brazing supplies", "Z-Other Cleaning", "Z-Other Engineering, Technical Or Consulting Service", "Z-Other Financial Services", "Z-Other Office Equipment", "Z-Other Telecom"]

    log.debug(f"Categories: {str(categories)}")

    objectives_conf = tenant_conf["objectives"]
    log.debug(f"Objectives configuartion: {objectives_conf}")

    with ThreadPoolExecutor(max_workers=len(categories)) as executor:
        futures = {
            executor.submit(process_category, cat, tenantId,sf_client): cat
            for cat in categories
        }

        final_combined_list_insights = []
        final_combined_list_top_ideas = []

        for future in as_completed(futures):
            cat = futures[future]
            try:
                result = future.result()
                final_combined_list_insights.extend(result["insights"])
                final_combined_list_top_ideas.extend(result["top_ideas"])
                log.info(f"Finished processing: {cat}")
            except Exception as e:
                log.info(f"Error processing {cat}: {e}")
    

    with open(f"{current_file.parent}/combined_insights_master.json", "r") as file:
        insights = json.load(file)

    flattened_data = []

    for record in insights:
        data = record
        rca_data = data.get("rca", {})
        supplier_sku_information_data = data.get("supplier_sku_information", {})
        created_at_str = data.get("created_at", "")
        created_at = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S") if created_at_str else None
        top_ideas = data.get("top_ideas", [])

        values = (
            data.get("insight_query", "NULL"),
            data.get("analytics_name", "NULL"),
            data.get("segment", "NULL"),
            data.get("category", "NULL"),
            data.get("sql", "NULL"),
            json.dumps(data.get("data", [[]])),
            data.get("insight", "NULL"),
            json.dumps(data.get("linked_insights", [])),
            json.dumps(data.get("related_insights", [])),
            rca_data.get("heading", "NULL"),
            json.dumps(rca_data.get("description", [])),
            data.get("objective", "NULL"),
            json.dumps(supplier_sku_information_data.get("supplier", [])),
            json.dumps(supplier_sku_information_data.get("sku", [])),
            data.get("id", "NULL"),
            created_at,
            json.dumps(top_ideas),
            json.dumps(data.get("impact", [])),
        )

        flattened_data.append(values)

    print(len(flattened_data))
    print(flattened_data[0])

    table_path = f'"DATA"."INSIGHTS_MASTER"'

    sql = f"""
        INSERT INTO {table_path} (
            INSIGHT_QUERY, ANALYTICS_NAME, SEGMENT, CATEGORY, SQL_QUERY, DATA, INSIGHT, LINKED_INSIGHTS,
            RELATED_INSIGHTS, RCA_HEADING, RCA_DESCRIPTION, OBJECTIVE, SUPPLIER_INFORMATION,
            SKU_INFORMATION, ID, CREATED_AT, TOP_IDEAS, IMPACT
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
    """

    sf_client.execute_query(sql, flattened_data)





    ###############################################



    with open(f"{current_file.parent}/combined_top_ideas_master.json", "r") as file:
        top_ideas = json.load(file)

    flattened_data = []

    for record in top_ideas:
        data = record
        rca_data = data.get("rca", {})

        created_at_str = data.get("created_at", "")
        created_at = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S") if created_at_str else None

        top_ideas = data.get("top_ideas", [])

        values = (
            data.get("category", "NULL"),
            data.get("idea", "NULL"),
            data.get("description", "NULL"),
            json.dumps(data.get("linked_insights", [])),
            json.dumps(data.get("related_insights", [])),
            rca_data.get("heading", "NULL"),
            json.dumps(rca_data.get("description", [])),
            data.get("id", "NULL"),
            created_at,
            json.dumps(top_ideas),
            json.dumps(data.get("impact", [])),
            json.dumps(data.get("linked_insights_ids", [])),
            data.get("segment", "NULL")
        )

        flattened_data.append(values)

    print(len(flattened_data))
    print(flattened_data[0])

    table_path = f'"DATA"."T_C_TOP_IDEAS"'

    sql = f"""
        INSERT INTO {table_path} (
            CATEGORY, IDEA, DESCRIPTION, LINKED_INSIGHTS,
            RELATED_INSIGHTS, RCA_HEADING, RCA_DESCRIPTION, ID, CREATED_AT,
            TOP_IDEAS, IMPACT, LINKED_INSIGHTS_IDS, SEGMENT
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
    """

    sf_client.execute_query(sql, flattened_data)



    #####################################################


    with open(f"{current_file.parent}/combined_insights_master.json", "r") as file:
        insights = json.load(file)

    flattened_data = []

    for data in insights:
        suppliers = data.get("supplier_sku_information", {}).get("supplier", [])

        if suppliers:
            for supplier in suppliers:
                values = (
                    data.get("id", "NULL"),
                    supplier,
                    data.get("category", "NULL"),
                    data.get("insight", "NULL"),
                    data.get("objective", "NULL"),
                    json.dumps(data.get("reinforcements", [])),
                    data.get("minimum_spend_threshold", '10000'),
                    data.get("analytics_name", "NULL")
                )
                flattened_data.append(values)
        else:
            values = (
                data.get("id", "NULL"),
                "NULL",
                data.get("category", "NULL"),
                data.get("insight", "NULL"),
                data.get("objective", "NULL"),
                json.dumps(data.get("reinforcements", [])),
                data.get("minimum_spend_threshold", '10000'),
                data.get("analytics_name", "NULL")
            )
            flattened_data.append(values)

    print(len(flattened_data))
    print(flattened_data[0])

    table_path = f'"DATA"."NEGOTIATION_INSIGHTS"'

    sql = f"""
        INSERT INTO {table_path} (
            INSIGHT_ID, SUPPLIER_NAME, CATEGORY_NAME, LABEL, OBJECTIVE, REINFORCEMENTS, 
            MINIMUM_SPEND_THRESHOLD, ANALYTICS_NAME
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s
        );
    """

    sf_client.execute_query(sql, flattened_data)
