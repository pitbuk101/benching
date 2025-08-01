"""Class to process key facts configuration in Postgres."""

import os
import pathlib
from typing import Set

import pandas as pd

from ada.components.db.pg_connector import PGConnector
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger

log = get_logger("key_facts_configuration")

key_facts_conf = read_config("use-cases.yml")["key_facts_v3"]
data_dir = os.path.join(pathlib.Path(__file__).parents[4], "data")


class Configuration:
    """Class to process key facts configuration in Postgres."""

    def __init__(
        self,
        required_configuration_keys: Set[str],
        category_column: str = "category_name",
        configuration_key_column: str = "config_name",
        configuration_column: str = "config",
    ):
        """Initialize configuration loader.

        Args:
            required_configuration_keys: configuration types to process
            category_column: column name for category in configuration table
            configuration_key_column: column name for configuration type in configuration table
            configuration_column: column name for configuration under configuration type
        """
        self.required_configuration_keys = required_configuration_keys
        self.configuration_dict: dict = {}

        self.category_column = category_column
        self.configuration_key_column = configuration_key_column
        self.configuration_column = configuration_column

    def load_configuration(
        self,
        pg_connector: PGConnector,
        category: str,
        configuration_table: str = "key_facts_config",
    ):
        """Load category-specific configuration.

        Args:
            pg_connector: PGConnector class to connect to Postgres DB
            category: category for which to load configuration
            configuration_table: configuration table name
        """
        log.info("Loading configuration for category %s.", category)
        category_filter = f"LOWER({self.category_column}) = '{category.lower()}'"
        category_configuration = pg_connector.select_records_with_filter(
            table_name=configuration_table,
            filter_condition=category_filter,
        )
        category_configuration_df = pd.DataFrame(
            category_configuration,
            columns=[
                self.category_column,
                self.configuration_key_column,
                self.configuration_column,
                "updated_ts",
            ],
        )

        for key in self.required_configuration_keys:
            if key not in category_configuration_df[self.configuration_key_column].values:
                raise ValueError(f"No configuration available for configuration key {key}.")
            self.configuration_dict[key] = category_configuration_df[
                category_configuration_df[self.configuration_key_column] == key
            ].iloc[0][self.configuration_column]

        log.info("Configuration for category %s loaded.", category)

    def get_supported_categories(
        self,
        pg_connector: PGConnector,
        configuration_table: str = "key_facts_config",
    ) -> list[str]:
        """
        Retrieve a list of supported categories from the specified configuration table.

        Args:
            pg_connector (PGConnector): PGConnector class.
            configuration_table (str): table to query. Defaults to "key_facts_config".

        Returns:
            list[str]: A list of unique supported category names retrieved from the database."""
        supported_categories = pg_connector.select_records_with_filter(
            table_name=configuration_table,
            filtered_columns=["category_name"],
            distinct=True,
        )
        supported_categories = [item[0] for item in supported_categories if item]
        log.info("List of supported categories in KF %s .", supported_categories)
        return supported_categories
