"""Data retrival service"""

import json
from typing import Any

from ada.use_cases.news_insights.news_data_retriver import (
    retrieve_curated_news_insights_data,
    retrieve_news_pipeline_status,
)
from ada.utils.logs.logger import get_logger

log = get_logger("data_retrival_services")

PAYLOAD_DICT: dict[str, dict[str, Any]] = {
    "news_insights": {
        "required_keys": ["tenant_id", "date_int"],
        "function": retrieve_curated_news_insights_data,
    },
    "news_pipeline_status": {
        "required_keys": ["tenant_id", "date_int"],
        "function": retrieve_news_pipeline_status,
    },
}


def run_data_retrieval_service(input_str: str):
    """
    Processes a data retrieval request based on the input payload and executes the
    appropriate function.

    This function parses the input JSON string to determine the `request_type` and validates
    the required keys for that request type. Based on the `request_type`, it invokes a
    corresponding function from the `PAYLOAD_DICT` with the required arguments.

    Args:
        input_str (str): A JSON-formatted string containing the request payload.
                         Expected to include `request_type` and all required keys
                         for the specified request type.

    Returns:
        Any: The result of the function corresponding to the `request_type`.
    """
    payload_data = json.loads(input_str)

    if (request_type := payload_data.get("request_type", "")) == "":
        raise ValueError("request_type is missing in the payload")

    if request_type not in PAYLOAD_DICT:
        raise ValueError(f"Invalid request_type: {request_type}")

    for key in PAYLOAD_DICT.get(request_type, {}).get("required_keys", []):
        if key not in payload_data:
            raise ValueError(f"{key} is missing in the payload for request_type: {request_type}")

    kwargs = {key: payload_data[key] for key in PAYLOAD_DICT[request_type]["required_keys"]}
    return PAYLOAD_DICT[request_type]["function"](**kwargs)
