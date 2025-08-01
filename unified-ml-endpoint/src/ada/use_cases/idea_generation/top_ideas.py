"""Module to send top ideas data to Source AI app"""

import json
from typing import Any

import pandas as pd

from ada.components.db.pg_connector import PGConnector
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger

log = get_logger("top_ideas")
top_ideas_conf = read_config("use-cases.yml")["top_ideas"]


def run_top_ideas(json_file: str) -> dict[str, Any]:
    """
    Extracts the top ideas data from database and returns a dictionary
    with the top-ideas information.

    Args:
        json_file (str): JSON string containing the tenant id .

    Returns:
        dict[str, Any]: A dictionary containing the top ideas data or an error message.
    """

    json_data = json.loads(json_file)
    tenant_id = json_data["tenant_id"]

    pg_db_conn = PGConnector(tenant_id=tenant_id)
    top_ideas_tbl = top_ideas_conf["tables"]["top_ideas_tbl"]
    filtered_columns = top_ideas_conf["columns"]["top_ideas_tbl_cols"]
    filter_condition = (
        f"CAST(file_timestamp AS BIGINT) = "
        f"(SELECT MAX(CAST(file_timestamp AS BIGINT)) FROM {top_ideas_tbl})"
    )

    top_ideas_df = pd.DataFrame(
        pg_db_conn.select_records_with_filter(
            table_name=top_ideas_tbl,
            filtered_columns=filtered_columns,
            filter_condition=filter_condition,
        ),
        columns=filtered_columns,
    )
    if len(top_ideas_df) > 0:
        top_ideas_df = top_ideas_df.copy()
        top_ideas_df = top_ideas_df.dropna(subset=["category_name", "idea", "analytics_name"])

        top_ideas_df["title"] = top_ideas_df["idea"].apply(lambda x: json.loads(x).get("top_idea"))
        top_ideas_df["description"] = top_ideas_df["idea"].apply(
            lambda x: json.loads(x).get("description"),
        )

        top_ideas_df.drop(columns=["idea"], inplace=True)
        top_ideas_df["updated_ts"] = top_ideas_df["updated_ts"].astype(str)
        top_ideas_df["top_idea_id"] = top_ideas_df[
            ["category_name", "file_timestamp", "idea_number"]
        ].agg(lambda x: f"{x.iloc[0]}_{x.iloc[1]}{x.iloc[2]}", axis=1)

        response = {
            "top_ideas": [
                {
                    "top_idea_id": row["top_idea_id"],
                    "category": row["category_name"].lower(),
                    "analytic_name": row["analytics_name"],
                    "title": row["title"],
                    "description": row["description"],
                    "impact": row["impact"],
                    "update_info": [],  # Empty list
                    "linked_insights": [
                        {"label": insight.strip().replace("insight: ", "").strip()}
                        for insight in row["linked_insight"]
                    ],
                    "created_at": row["updated_ts"],
                }
                for _, row in top_ideas_df.iterrows()
            ],
        }
        response.update(
            {"message": "Top Ideas data shared successfully", "response_type": "success"},
        )
        return response

    return {"message": "top ideas data not available", "response_type": "failure"}
