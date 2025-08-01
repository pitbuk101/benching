"""Utils for Dynamic ideas"""

import json
from collections import defaultdict
from typing import Any

import pandas as pd

from ada.components.db.pg_connector import PGConnector
from ada.utils.config.config_loader import read_config
from ada.components.llm_models.generic_calls import (
    generate_chat_response_with_chain
)
import ast

from ada.utils.logs.logger import get_logger
from ada.use_cases.idea_generation.dynamic_ideas.dyn_ideas_prompts import classify_prompt
import re

dynamic_ideas_conf = read_config("use-cases.yml")["dynamic_ideas"]
analytics_list_tbl = dynamic_ideas_conf["tables"]["analytics_list_tbl"]
extended_opportunity_insights_tbl = dynamic_ideas_conf["tables"][
    "extended_opportunity_insights_tbl"
]

log = get_logger("dynamic_ideas_utils")


def get_analytics_values(pg_db_conn: PGConnector, category: str) -> list[dict]:
    """
    Fetches analytics values for a given tenant and category.

    Args:
        pg_db_conn (PGConnector): Postgress connection object
        category (str): The category name.

    Returns:
        list[dict]: A list of dictionaries containing analytics values.
    """
    values = pg_db_conn.select_records_with_filter(
        table_name=analytics_list_tbl,
        filtered_columns=["analytics_name"],
        distinct=True,
        filter_condition=f"""
            LOWER(category_name) = '{category.lower()}'
            AND file_timestamp = (select max(file_timestamp) from {analytics_list_tbl})
            """,
    )
    values_in_dict = [dict(row) for row in values]
    return values_in_dict



def extract_category_analytic_data(supplier_name:str, skus, category_name: str, sf_client):
    """
    Extracts category analytic data from the dataframe.
    """

    analytic_map = f"""
        SELECT * FROM DATA.T_C_KPI_TABLE_MAPPING_FRONTEND
        WHERE LOWER(CATEGORY) = LOWER('{category_name}')

    """
    analytic_map_df = sf_client.fetch_dataframe(analytic_map)
    if analytic_map_df.empty:
        log.error("No data found for category: %s", category_name)
        return None
    data_dict = {}
    for row in analytic_map_df.itertuples():

        if row.KPI_TABLE_NAME == None:
            continue
        
        column_query = f'''SELECT COLUMN_NAME
        FROM information_schema.columns
        WHERE TABLE_SCHEMA = 'DATA'
        AND TABLE_NAME   = '{row.KPI_TABLE_NAME}'
        ORDER BY ORDINAL_POSITION;'''

        column_names = sf_client.fetch_dataframe(column_query)['COLUMN_NAME'].tolist()
        log.debug("Column names for table %s: %s", row.KPI_TABLE_NAME, column_names)
        sku_query = ""
        if "MATERIAL" in column_names and skus:
            sku_names = [item for item in skus]
            formatted_sku = "('{}')".format("', '".join(sku_names))
            log.debug("SKU Names: %s", sku_names)
            sku_query = f"""
                AND MATERIAL IN {formatted_sku}
            """
        analytic_data = pd.DataFrame(
            sf_client.select_records_with_filter(
                table_name='DATA.'+row.KPI_TABLE_NAME,

                filter_condition=(
                    f"""
                    SUPPLIER = '{supplier_name}'
                    AND
                    LOWER(category) = LOWER('{category_name}')
                    AND 
                    YEAR = (SELECT MAX(YEAR) FROM {'DATA.'+row.KPI_TABLE_NAME})""" 
                    + sku_query
                    
                ),

            ),
        )
        if not analytic_data.empty:
            # Filter out columns with object dtype to avoid incorrect aggregation
            obj_cols = analytic_data.select_dtypes(include="object").columns
            if "MATERIAL" in obj_cols:
                obj_cols = obj_cols.drop("MATERIAL")
            obj_map = { col: "first" for col in obj_cols }

            
            # Generate the prompt for classification
            numeric_cols = [col for col in analytic_data.select_dtypes(include='number').columns if col != 'YEAR']
            prompt = classify_prompt(analytic_data[numeric_cols].head(2))

            agg_map = generate_chat_response_with_chain(prompt=prompt, model='gpt-4o')
            agg_map = re.sub(r"```(?:python)?\s*", "", agg_map).strip("`\n ")

            agg_map = ast.literal_eval(agg_map)

            # group & aggregate
            groupby_cols = ["YEAR"]
            if "MATERIAL" in analytic_data.columns:
                groupby_cols.append("MATERIAL")
            year_df = analytic_data.groupby(groupby_cols).agg(agg_map | obj_map).reset_index()
            log.info("Executing query for analytic: %s", row.KPI_NAME)
       

            data_dict[row.KPI_NAME] = year_df #column_names #analytic_data
    if data_dict:
        return data_dict
    else:
        log.error("No data found for category: %s", category_name)
        return None

def prepare_response_payload(
    dynamic_ideas: list | None = None,
    insights: list | None = None,
    objectives: list | None = None,
    response_type: str = "dynamic_qna",
    message: str = "",
) -> dict[str, Any]:
    """
    Prepare the response payload for dynamic ideas.

    Args:
        dynamic_ideas (list or None): A list of dynamic ideas, defaults to None.
        insights (list or None): A list of insights, defaults to None.
        response_type (str): The type of response, defaults to "dynamic_qna".
        message (str): The message to be included in the response, defaults to an empty string.

    Returns:
        dict: A dictionary representing the response payload.
    """
    return {
        "message": message or "",
        "response_type": response_type,
        "dynamic_ideas": dynamic_ideas or [],
        "insights": insights or [],
        "objectives": objectives or []
    }


def prepare_analytics_json(analytics_df: pd.DataFrame, category_name: str) -> list[dict]:
    """
    Prepare a list of analytics JSON objects from a DataFrame.

    This function processes a DataFrame containing analytics data
    and formats it into a list of JSON objects.
    Each JSON object represents an analytics entry with associated ideas,
    opportunity insights, expert inputs,
    and linked insights.

    Args:
    analytics_df (pd.DataFrame): The DataFrame containing analytics data.
    It must have the following columns:
        - 'analytics_name': The name of the analytics.
        - 'file_timestamp': The timestamp of the file.
        - 'idea_number': The number of the idea.
        - 'idea': A JSON string containing the idea details.
        - 'opportunity_insight': Insights related to the opportunity.
        - 'expert_inputs': Expert inputs related to the analytics.
        - 'linked_insight': Linked insights related to the analytics.
    category_name (str): The category name to be associated with the analytics.

    Returns:
    list[dict]: list of dictionaries, each representing an analytics entry with the following keys:
        - 'analytics_name': The name of the analytics.
        - 'category_name': The category name associated with the analytics.
        - 'ideas': list of dictionaries, containing 'idea_id', 'idea_title', and 'idea_description'.
        - 'opportunity_insights': A list of unique opportunity insights.
        - 'expert_inputs': A list of unique expert inputs.
        - 'linked_insights': A list of unique linked insights.
    """
    analytics_list = []
    for analytics in analytics_df["analytics_name"].unique():
        analytics_json = {"analytics_name": analytics, "category_name": category_name}
        each_analytics_df = analytics_df[analytics_df["analytics_name"] == analytics]

        # format ideas
        each_analytics_df["idea_id"] = each_analytics_df[["file_timestamp", "idea_number"]].agg(
            lambda x: f"{category_name}_{x.iloc[0]}{x.iloc[1]}",
            axis=1,
        )
        each_analytics_df["idea_title"] = each_analytics_df["idea"].apply(
            lambda x: json.loads(x)["top_idea"],
        )
        each_analytics_df["idea_description"] = each_analytics_df["idea"].apply(
            lambda x: json.loads(x)["description"],
        )
        ideas_df = each_analytics_df[
            ["idea_id", "idea_title", "idea_description"]
        ].drop_duplicates()
        analytics_json["ideas"] = ideas_df.to_dict(orient="records")

        # format opportunity insights
        analytics_json["opportunity_insights"] = list(set(each_analytics_df["opportunity_insight"]))

        # format  expert inputs
        analytics_json["expert_inputs"] = (
            each_analytics_df["expert_inputs"].drop_duplicates().tolist()
        )

        # format linked insights
        analytics_json["linked_insights"] = (
            each_analytics_df["linked_insight"].explode().drop_duplicates().tolist()
        )

        # append to overall analytics list
        analytics_list.append(analytics_json)
    return analytics_list


def fetch_linked_insights_with_ids(
    linked_insights: list,
    pg_db_conn: PGConnector,
    category_name: str,
):
    """
    Fetches linked insights from the insights_master table for the given tenant and category.

    Args:
        linked_insights (list(str)): List of linked insights to fetch.
        pg_db_conn (PGConnector): Database connection object.
        category_name (str): Category name to filter the linked insights.

    Returns:
        pandas.DataFrame: DataFrame containing the fetched linked insights.
    """
    linked_insight_list = [
        value.strip().lower().replace("insight: ", "") for value in linked_insights
    ]
    linked_insight_list = list(set(linked_insight_list))
    if len(linked_insight_list) == 0:
        return []

    linked_insight_condition = pg_db_conn.get_condition_string(
        ("TRIM(LOWER(label))", "in", linked_insight_list),
    )
    filtered_columns = ["insight_id", "label", "created_time"]
    try:
        linked_insights_data = pg_db_conn.select_records_with_filter(
            table_name="insights_master",
            filtered_columns=filtered_columns,
            distinct_on=["label"],
            filter_condition=f"""lower(category_name) = '{category_name.lower()}' AND alert_type = 1
                    AND {linked_insight_condition}""",
            order_by=("label, created_time", "DESC"),
        )
    except Exception as ex:  # pylint: disable=broad-exception-caught
        log.error("Error in fetching insight ids - %s", str(ex))
        linked_insights_data = []
    linked_insights_df = pd.DataFrame(linked_insights_data, columns=filtered_columns)

    if linked_insights_df.empty:
        return []

    linked_insights_df["label"] = linked_insights_df["label"].str.strip()
    linked_insights_df.sort_values(by="created_time", ascending=False).drop_duplicates(
        subset="label",
        keep="first",
    )
    return linked_insights_df[["label", "insight_id"]].to_dict(orient="records")


def fetch_linked_insights_for_suppliers(
    pg_db_conn: PGConnector,
    category_name: str,
    *,
    supplier_name: str | None = None,
    supplier_id: str | None = None,
):
    """
    Fetches linked insights for a given supplier and category.

    Args:
        pg_db_conn (PGConnector): Database connection object.
        supplier_name (str): Name of the supplier to fetch linked insights for.
        category_name (str): Category name to filter the linked insights.
        supplier_id (str): ID of the supplier to fetch linked insights for.

    Returns:
        list[dict]: A list of dictionaries containing the linked insights.
    """
    if not supplier_name and not supplier_id:
        raise ValueError("Supplier name or ID must be provided.")
    if supplier_name and supplier_id:
        raise ValueError("Only one of supplier name or ID should be provided.")
    filter_condition = f"""LOWER(category_name) = '{category_name.lower()}'"""
    if supplier_name:
        filter_condition += f""" AND linked_insight::text ILIKE '%{supplier_name}%'"""
    elif supplier_id:
        filter_condition += f""" AND linked_insight::text ILIKE '%{supplier_id}%'"""
    kwargs = {
        "table_name": dynamic_ideas_conf["tables"]["opportunity_insights_tbl"],
        "filter_condition": filter_condition,
        "filtered_columns": ["linked_insight"],
    }
    return pg_db_conn.select_records_with_filter(**kwargs)


def update_ner_format(list_output):
    """
    Updates the NER format by converting the first value in the list output to a string tuple.

    Args:
        list_output (list): A list containing dictionaries with NER output.

    Returns:
        str: A string representation of the first value in the list output as a tuple.
    """
    return str(tuple(list_output[0]["value"])).replace(",)", ")")


def filter_supplier_data_for_max_period(supplier_data: list[dict]) -> list[dict]:
    """
    Filters supplier data to retain only the entries with the maximum period for each supplier.

    Args:
        supplier_data (list[dict]): A list of dictionaries containing supplier data.

    Returns:
        list[dict]: A list of dictionaries containing filtered supplier data
                    with the maximum period for each supplier.
    """
    grouped_data = defaultdict(list)

    for item in supplier_data:
        grouped_data[item["SUPPLIER"]].append(item)

    filtered_data = []
    for _, items in grouped_data.items():
        if all(item.get("YEAR") is None for item in items):
            filtered_data.extend(items)
        else:
            max_period = max(
                (item["YEAR"] for item in items if item.get("YEAR") is not None),
                default=None,
            )
            filtered_data.extend([item for item in items if item.get("YEAR") == max_period])
    return filtered_data
