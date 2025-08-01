"""Key facts utilities."""

import re
from typing import Any

import pandas as pd

from ada.use_cases.key_facts.pydantic_parsing import DaxEntityValue
from ada.utils.format.format import exception_response


def format_columns(to_format_df: pd.DataFrame) -> list[dict[str, Any]]:
    """Formats the columns
    Args:
        to_format_df: columns dataframe
    Returns:
        list of columns
    """
    return list(
        map(
            lambda x: {"name": x[0], "description": x[1]},
            zip(to_format_df["Column Name"].values, to_format_df["Column Description"]),
        ),
    )


def get_reports_description(query_report_mapping: pd.DataFrame) -> str:
    """Generate a JSON string representation of the report descriptions.

    Args:
        query_report_mapping (pd.DataFrame): DataFrame containing report descriptions.

    Returns:
        str: JSON string representation of the report descriptions.
    """
    report_description = query_report_mapping.to_json(orient="records")
    return report_description


def get_few_shot_examples(dataset_definition: dict[str, pd.DataFrame]) -> tuple:
    """
    Get few shot examples for key facts. Sets:
        - few_shot_questions: questions for few shot examples
        - few_shot_query: query for few shot examples
        - few_shot_query_filtered: query with filters for few shot examples
    Args:
        dataset_definition: dataset definition for key facts
    Returns:

    """
    few_shot_questions = dataset_definition["Few-shot examples"]["Question"].values
    few_shot_query = dataset_definition["Few-shot examples"]["Query without filters"].values
    few_shot_query_filtered = dataset_definition["Few-shot examples"]["Query with filters"].values

    return few_shot_questions, few_shot_query, few_shot_query_filtered


# TODO: this function is not used
def get_category_bucket(category: str, tenant_id: str, key_facts_conf: dict) -> str:
    """
    Determine the bucket of the given category for a specified tenant.

    Args:
        category (str): The category to classify.
        tenant_id (str): The tenant's unique identifier.
        key_facts_conf (dict): Configuration dictionary containing category mappings.

    Returns:
        str: The bucket name where the category belongs ('category_alpha' or 'category_beta').

    Raises:
        Exception: If the category is not supported.
    """
    for bucket in ["category_alpha", "category_beta"]:
        if category in key_facts_conf[tenant_id][bucket]["category_list"]:
            return bucket
    raise ValueError(f"category {category} not supported")


# TODO: this function is not used
def get_category_filter_level(
    category: str,
    tenant_id: str,
    key_facts_conf: dict,
) -> dict[str, Any] | Any:
    """
    Determine the filter level of the given category for a specified tenant.

    Args:
        category (str): The category to determine the filter level for.
        tenant_id (str): The tenant's unique identifier.
        key_facts_conf (dict): Configuration dictionary containing category mappings.

    Returns:
        str: The filter level corresponding to the category.

    Raises:
        KeyError: If the category is not found in any level categories.
        Exception: If the category is not supported.
    """
    category_tree_mapping = key_facts_conf[tenant_id]["category_tree_mapping"]
    common_config = key_facts_conf["common_config"]

    level_mapping = [
        ("level_2_categories", "parent_category_level_2"),
        ("level_3_categories", "parent_category_level_3"),
        ("level_4_categories", "parent_category_level_4"),
    ]

    for level, parent_level in level_mapping:
        if category in category_tree_mapping[level]:
            return common_config[parent_level]

    return exception_response(
        response_type="dax",
        message=(
            f"Selected category {category} is not supported by ada. "
            "Please select another category to proceed."
        ),
    )


def extract_dax_entities(dax_query: str) -> dict[str, list[DaxEntityValue]]:
    """Extract entities from a DAX query string.

    This function searches for specific patterns in the provided DAX query
    to extract various entities such as regions, suppliers, countries,
    continents, market regions, and plants.

    Args:
        dax_query (str): The DAX query string from which to extract entities.

    Returns:
        extracted_entities (dict): containing lists of extracted DAX entities(DaxEntityValue)
        categorized by region, supplier, country, continent, market region, and plant."""
    dax_query = dax_query.replace("''", "'")
    extracted_entities = {}

    patterns = get_dax_patterns()
    for key, pattern in patterns.items():
        match = re.search(pattern["regex"], dax_query, flags=re.IGNORECASE)
        if match:
            content_list = match.group(1).strip().replace('"', "").split(",")
            extracted_entities[key] = [
                DaxEntityValue(raw_value=content.strip()) for content in content_list
            ]

    return extracted_entities


def get_dax_patterns() -> dict:
    """
    Retrieve a dictionary of DAX patterns for entity extraction and replacement.

    Returns:
        dict: each key represents a DAX entity type(e.g., region, supplier, country)
        and each value is a dict containing:
        - "regex": A regex pattern for matching the DAX entity.
        - "replace": A string format for replacing the matched entity in the DAX query.
    """
    return {
        "region": {
            "regex": r"TREATAS\(\{(.*?)\},\s*\'?SUPPLIER COUNTRY\'?\s*\[TXT_REGION\]\)",
            "replace": "TREATAS({ \"<replace>\" }, 'SUPPLIER COUNTRY'[TXT_REGION])",
        },
        "supplier": {
            "regex": r"TREATAS\(\{(.*?)\},\s*\'?SUPPLIER\'?\s*\[TXT_SUPPLIER\]\)",
            "replace": "TREATAS({ \"<replace>\" }, 'SUPPLIER'[TXT_SUPPLIER])",
        },
        "country": {
            "regex": r"TREATAS\(\{(.*?)\},\s*\'?SUPPLIER COUNTRY\'?\s*\[TXT_COUNTRY\]\)",
            "replace": "TREATAS({ \"<replace>\" }, 'SUPPLIER COUNTRY'[TXT_COUNTRY])",
        },
        "continent": {
            "regex": r"TREATAS\(\{(.*?)\},\s*\'?SUPPLIER COUNTRY\'?\s*\[TXT_CONTINENT\]\)",
            "replace": "TREATAS({ \"<replace>\" }, 'SUPPLIER COUNTRY'[TXT_CONTINENT])",
        },
        "market_region": {
            "regex": r"TREATAS\(\{(.*?)\},\s*\'?MARKET REGIONS\'?\s*\[TXT_LOCATION\]\)",
            "replace": "TREATAS({ \"<replace>\" }, 'MARKET REGIONS'[TXT_LOCATION])",
        },
        "plant": {
            "regex": r"TREATAS\(\{(.*?)\},\s*\'?PLANT\'?\s*\[TXT_PLANT\]\)",
            "replace": "TREATAS({ \"<replace>\" }, 'PLANT'[TXT_PLANT])",
        },
        "company": {
            "regex": r"TREATAS\(\{(.*?)\},\s*\'?COMPANY\'?\s*\[TXT_LEVEL_4\]\)",
            "replace": "TREATAS({ \"<replace>\" }, 'COMPANY'[TXT_LEVEL_4])",
        },
    }
