"""Azure ML Endpoint for Key facts deployment."""

import pathlib
import sys
from typing import Any

# pylint: disable=C0413
sys.path.append(str(pathlib.Path(__file__).parents[2]))
# pylint: enable=C0413

from ada.use_cases.key_facts.configuration import Configuration
from ada.use_cases.key_facts.key_facts_v3 import run_key_facts


def read_context():
    """
    Reads the on text needed for key facts returns the configuration
    needed for speedup
    Returns:
        (Configuration): Configuration needed for speedups
    """
    return Configuration(
        required_configuration_keys={
            "data_model",
            "measures_description",
            "filters_description",
            "category_filter",
            "currency",
        },
    )


def init():
    """
    Initialize configuration loader class for key facts.
    """
    global category_configuration

    category_configuration = read_context()


def run(json_file: str, configuration_val: Configuration = None) -> dict[str, Any]:
    """
    Entrypoint function for Key facts
    Args:
        json_file (str): Input payload json
        configuration_val (Configuration): The data load prerequisite
    Returns:
        (dict): response for user query

    """
    if configuration_val:
        global category_configuration
        category_configuration = configuration_val

    return run_key_facts(json_file=json_file, category_configuration=category_configuration)
