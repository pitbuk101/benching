import re
import json
import sys
from pathlib import Path 
from datetime import datetime
import pandas as pd
import difflib

current_file = Path(__file__)
sys.path.append(str(current_file.parents[3]))


from ada.utils.config.config_loader import read_config
import difflib

def find_linked_insights_ids(top_ideas, insights):
    for idea in top_ideas:
        ids = []
        matched_insights = []
        unmatched_insights = []

        linked_insights = idea["linked_insights"]

        for insight in linked_insights:
            matched = False
            best_match = None
            best_ratio = 0
            best_id = None

            # First try exact match
            for element in insights:
                if insight.strip() == element["insight"].strip():
                    ids.append(element["id"])
                    matched_insights.append(insight)
                    matched = True
                    break

            # If not exact, find best fuzzy match
            if not matched:
                for element in insights:
                    ratio = difflib.SequenceMatcher(
                        None,
                        insight.strip().lower(),
                        element["insight"].strip().lower()
                    ).ratio()
                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_match = element["insight"]
                        best_id = element["id"]

                if best_match:
                    ids.append(best_id)
                    matched_insights.append(insight)
                else:
                    unmatched_insights.append(insight)

        # Update idea with matched data only
        idea["linked_insights"] = matched_insights
        idea["linked_insights_ids"] = ids

        # Debug prints
        print(f"Linked ids: {len(ids)}")
        print(f"Linked insights: {len(idea['linked_insights'])}")
        if unmatched_insights:
            print(f"⚠️ Unmatched insights for idea: {unmatched_insights}")

    return top_ideas

def json_to_excel(json_file, excel_file):
    """Convert a JSON file to an Excel file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Convert JSON data to a DataFrame
    df = pd.json_normalize(data)  # Flattens nested JSON if necessary

    # Save to an Excel file
    # df = df.drop_duplicates(subset=["top_ideas"], keep="first")
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
                new_item["insight_query"] = new_item['insight_query'].rstrip(".").rstrip("?") + f" for category '{category}', for 2023 year."  #+ f" along with the total value and the percentage contribution of each result relative to the total."
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

def objective_mapping(objectives_conf,insights):

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

    sf_client.execute_query(sql, values)
    

def insert_negotiation_insights(sf_client, data):
    import json

    table_path = f'"DATA"."NEGOTIATION_INSIGHTS"'

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

            sql = f"""
                INSERT INTO {table_path} (
                    INSIGHT_ID, SUPPLIER_NAME, CATEGORY_NAME, LABEL, OBJECTIVE, REINFORCEMENTS, 
                    MINIMUM_SPEND_THRESHOLD, ANALYTICS_NAME
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s
                );
            """

            sf_client.execute_query(sql, values)

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

        sql = f"""
            INSERT INTO {table_path} (
                INSIGHT_ID, SUPPLIER_NAME, CATEGORY_NAME, LABEL, OBJECTIVE, REINFORCEMENTS, 
                MINIMUM_SPEND_THRESHOLD, ANALYTICS_NAME
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
            );
        """

        sf_client.execute_query(sql, values)


def insert_top_ideas(sf_client, data):

    rca_data = data.get("rca", {})

    created_at_str = data.get("created_at", "")
    created_at = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S") if created_at_str else None

    top_ideas = data.get("top_ideas", [])

    values = (
        data.get("category", "NULL"),
        data.get("idea", "NULL"),
        data.get("description","NULL"),
        json.dumps(data.get("linked_insights", [])),
        json.dumps(data.get("related_insights", [])),
        rca_data.get("heading", "NULL"),
        json.dumps(rca_data.get("description", [])),
        data.get("id", "NULL"),
        created_at,
        json.dumps(top_ideas),
        json.dumps(data.get("impact", [])),
        json.dumps(data.get("linked_insights_ids", [])),
        data.get("segment","NULL")
    )

    table_path = f'"DATA"."T_C_TOP_IDEAS"'

    sql = f"""
        INSERT INTO {table_path} (
            CATEGORY, IDEA, DESCRIPTION, LINKED_INSIGHTS,
            RELATED_INSIGHTS, RCA_HEADING, RCA_DESCRIPTION, ID, CREATED_AT, TOP_IDEAS, IMPACT, LINKED_INSIGHTS_IDS, SEGMENT
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
    """

    sf_client.execute_query(sql, values)

def sanitize_pythonic_json_string(s):
    """
    Sanitize Python-like strings for JSON parsing by:
    - Replacing Decimal with plain numbers.
    - Converting Python `None` to JSON `null`.
    - Converting Python `True`/`False` to JSON `true`/`false`.
    - Handling tuples and other non-JSON compatible structures.
    """
    # Step 1: Replace Decimal('value') with the float value
    s = re.sub(r"Decimal\('([^']+)'\)", r"\1", s)
    
    # Step 2: Convert None to null and True/False to true/false
    s = s.replace("None", "null").replace("True", "true").replace("False", "false")
    
    # Step 3: Handle tuples (convert them to lists)
    s = re.sub(r"\(([^)]+)\)", r"[\1]", s)
    
    # Step 4: Ensure valid JSON quotes
    s = s.replace("'", '"')  # Convert single quotes to double quotes
    
    return s



    


