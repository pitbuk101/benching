import json
from unittest.mock import MagicMock, patch

from ada.use_cases.news_insights.news_data_retriver import (
    PGConnector,
    retrieve_curated_news_insights_data,
)

@patch("ada.use_cases.news_insights.news_data_retriver.PGConnector")
def test_run_news_insights_success(mock_pg_connector_class):
    tenant_id = 123
    date_int = 20241219

    mock_pg_connector = MagicMock(spec=PGConnector)
    mock_pg_connector_class.return_value = mock_pg_connector

    mock_pg_connector.select_records_with_filter.return_value = [
        {
            "news": "dummy_news",
        },
    ]

    result = retrieve_curated_news_insights_data(tenant_id, date_int)

    expected_result = {
        "curated_news_insights": [
            {
                "news": "dummy_news",
            }
        ],
    }

    assert result == expected_result, f"Expected {expected_result}, but got {result}"
