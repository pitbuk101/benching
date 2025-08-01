import json
from unittest.mock import MagicMock, patch

from ada.use_cases.idea_generation.top_ideas import (
    PGConnector,
    run_top_ideas,
    top_ideas_conf,
)

top_ideas_conf["tables"]["top_ideas_tbl"] = "top_ideas_table"
top_ideas_conf["columns"]["top_ideas_tbl_cols"] = [
    "category_name",
    "idea",
    "analytics_name",
    "impact",
    "linked_insight",
    "updated_ts",
    "file_timestamp",
    "idea_number"
]


@patch("ada.use_cases.idea_generation.top_ideas.PGConnector")
def test_run_top_ideas_success(mock_pg_connector_class):
    tenant_id = 123
    input_json = json.dumps({"tenant_id": tenant_id})

    mock_pg_connector = MagicMock(spec=PGConnector)
    mock_pg_connector_class.return_value = mock_pg_connector

    mock_pg_connector.select_records_with_filter.return_value = [
        (
            "Category1",
            json.dumps({"top_idea": "Title", "description": "Description"}),
            "Analytics1",
            "EUR 100M",
            ["insight: insight 1", "insight: insight 2"],
            "2024-09-23 14:30:45",
            "10000",
            1
        ),
    ]

    result = run_top_ideas(input_json)

    expected_result = {
        "top_ideas": [
            {
                "top_idea_id": "Category1_100001",
                "category": "category1",
                "analytic_name": "Analytics1",
                "title": "Title",
                "description": "Description",
                "impact": "EUR 100M",
                "update_info": [],
                "linked_insights": [
                    {"label": "insight 1"},
                    {"label": "insight 2"},
                ],
                "created_at": "2024-09-23 14:30:45",
            },
        ],
        "message": "Top Ideas data shared successfully",
        "response_type": "success",
    }

    assert result == expected_result, f"Expected {expected_result}, but got {result}"
