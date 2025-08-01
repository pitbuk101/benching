import re
import json
import sys
from pathlib import Path 
from datetime import datetime
import pandas as pd

current_file = Path(__file__)
sys.path.append(str(current_file.parents[3]))


from ada.utils.config.config_loader import read_config

insight_generation_conf = read_config("use-cases.yml")["insight_generation"]
objectives_conf = insight_generation_conf["objectives"]


def json_to_excel(json_file, excel_file):
    """Convert a JSON file to an Excel file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Convert JSON data to a DataFrame
    df = pd.json_normalize(data)  # Flattens nested JSON if necessary

    # Save to an Excel file
    df = df.drop_duplicates(subset=["top_ideas"], keep="first")
    df.to_excel(excel_file, index=False)

    print(f"Conversion successful! Excel file saved as: {excel_file}")


def extract_json(text):
    """
    Extracts all JSON arrays from the given text and merges them into a single list.

    :param text: The input text containing JSON data.
    :return: A list of extracted JSON objects.
    """

    json_pattern = r'\[\s*\{.*?\}\s*\]'  
    matches = re.findall(json_pattern, text, re.DOTALL)

    extracted_list = []
    for match in matches:
        try:
            json_data = json.loads(match)  
            if isinstance(json_data, list):
                extracted_list.extend(json_data)  
        except json.JSONDecodeError:
            print("Invalid JSON extracted!")
            return []

    return extracted_list


def process_insight_queries(insight_queries, insight_generation_conf):
    '''
    Process insight queries to add category and generate insight queries for each category
    Args:
        insight_queries: List of dictionaries containing analytics_name, segment, cols, and insight_query.
        insight_generation_conf: Configuration file containing categories.
    Returns:
        processed_data: List of dictionaries containing analytics_name, segment, cols, insight_query, and category.
    '''
    processed_data = []
    for item in insight_queries:
        if item["segment"] == "Category":
            new_item = item.copy()
            new_item["category"] = "General"
            processed_data.append(new_item)
        else:
            for category in insight_generation_conf["categories"]:
                new_item = item.copy()
                new_item["insight_query"] = f"In category {category}, for current year " + new_item['insight_query'].rstrip(".").rstrip("?").lower() + f" along with the total value and the percentage contribution of each result relative to the total."
                new_item["category"] = category
                processed_data.append(new_item)
    
    return processed_data
        

def get_linked_insights(insights:json):
    '''
    Extracts linked insights from the data.
    Args:
        data: List of dictionaries containing analytics_name,segment,cols,insight_query,category and insights.
    Returns:
        insights: List of dictionaries containing analytics_name,segment,cols,insight_query,insights,category,sql,linked_insights.
    '''

    for i, insight in enumerate(insights):
        linked = []
        if insight["insight"] == "NULL":
                insight["linked_insights"] = []
                continue
        for j, other_insight in enumerate(insights):
            if i != j and insight["analytics_name"] == other_insight["analytics_name"] and other_insight["insight"] != "NULL" and insight["category"] == other_insight["category"] and insight["segment"] == other_insight["segment"]:
                linked.append(other_insight["insight"])
        
        # Add linked_insights key
        insight["linked_insights"] = linked


    return insights


def find_related_insights(insights):

    for current_element in insights:
        category = current_element.get("category", "").strip()
        analytics_name = current_element.get("analytics_name", "").strip()
        current_insight = current_element.get("insight", "").strip()

        if not current_insight or current_insight.upper() == "NULL":  
            current_element["related_insights"] = []
            continue

        # Find all insights with the same category, non-empty, and not the current one
        related_insights = [
            item.get("insight", "").strip() for item in insights
            if item.get("category", "").strip() == category 
            and item.get("analytics_name", "").strip() == analytics_name
            and item.get("insight", "").strip() 
            and item.get("insight", "").strip().upper() != "NULL"
            and item.get("insight", "").strip() != current_insight
        ]

        current_element["related_insights"] = related_insights

    return insights

def objective_mapping(insights):

    for insight in insights:
        if insight["analytics_name"] in objectives_conf:
            insight["objective"] = str(objectives_conf[insight["analytics_name"]])
        else:
            insight["objective"] = ""
    
    return insights


def insert_insights_master(sf_client, data):
    rca_data = data.get("rca", {})
    supplier_sku_information_data = data.get("supplier_sku_information", {})

    created_at_str = data.get("created_at", "")
    created_at = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S") if created_at_str else None

    top_ideas = data.get("top_ideas", [])

    # Convert lists to JSON strings
    values = (
        data.get("insight_query", "NULL"),
        data.get("analytics_name", "NULL"),
        data.get("segment", "NULL"),
        data.get("category", "NULL"),
        data.get("sql", "NULL"),
        json.dumps(data.get("data", [[]])),  # Convert list to JSON
        data.get("insight", "NULL"),
        json.dumps(data.get("linked_insights", [])),  # Convert list to JSON
        json.dumps(data.get("related_insights", [])),  
        rca_data.get("heading", "NULL"),
        json.dumps(rca_data.get("description", [])),  
        data.get("objective", "NULL"),
        json.dumps(supplier_sku_information_data.get("supplier", [])),  
        json.dumps(supplier_sku_information_data.get("sku", [])),  
        data.get("id", "NULL"),
        created_at,  
        json.dumps(top_ideas),  
        json.dumps(data.get("impact", [])),  # Impact
    )

    sql = """
        INSERT INTO SAI_770ABBC_PROD_DB.DATA.INSIGHTS_MASTER (
            INSIGHT_QUERY, ANALYTICS_NAME, SEGMENT, CATEGORY, SQL_QUERY, DATA, INSIGHT, LINKED_INSIGHTS,
            RELATED_INSIGHTS, RCA_HEADING, RCA_DESCRIPTION, OBJECTIVE, SUPPLIER_INFORMATION,
            SKU_INFORMATION, ID, CREATED_AT, TOP_IDEAS, IMPACT
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
    """

    # formatted_sql = sql % tuple(repr(v) if v is not None else "NULL" for v in values)
    # print("Final SQL Query:", formatted_sql)

    sf_client.execute_query(sql,values)


def insert_negotiation_insights(sf_client, data):
    
    if len(data["supplier_sku_information"]["supplier"]) != 0:
        for supplier in data["supplier_sku_information"]["supplier"]:

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

            sql = """
            INSERT INTO SAI_770ABBC_PROD_DB.DATA.NEGOTIATION_INSIGHTS (
                INSIGHT_ID, SUPPLIER_NAME, CATEGORY_NAME, LABEL, OBJECTIVE, REINFORCEMENTS, 
                MINIMUM_SPEND_THRESHOLD,ANALYTICS_NAME
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
            );
            """

            # formatted_sql = sql % tuple(repr(v) if v is not None else "NULL" for v in values)
            # print(formatted_sql)

            sf_client.execute_query(sql,values)

    else:

        values = (
                data.get("id", "NULL"),
                "NULL",
                data.get("category", "NULL"),
                data.get("insight", "NULL"),
                data.get("objective", ""),
                json.dumps(data.get("reinforcements", [])),
                data.get("minimum_spend_threshold", '10000'),
                data.get("analytics_name", "")
            )

        sql = """
            INSERT INTO SAI_770ABBC_PROD_DB.DATA.NEGOTIATION_INSIGHTS (
                INSIGHT_ID, SUPPLIER_NAME, CATEGORY_NAME, LABEL, OBJECTIVE, REINFORCEMENTS, 
                MINIMUM_SPEND_THRESHOLD,ANALYTICS_NAME
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
            );
            """

        # formatted_sql = sql % tuple(repr(v) if v is not None else "NULL" for v in values)
        # print(formatted_sql)

        sf_client.execute_query(sql,values)




    


