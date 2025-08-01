"""This module provides a blueprint for the DBConnector class."""
from abc import ABC
from typing import Tuple


# pylint: disable=too-few-public-methods
class DBConnector(ABC):
    """Abstract class to connect to database."""

    def _submit_query(self, query: str) -> None:
        """Load Data from DB."""

    def _retrieve_query(self, query: str) -> Tuple:
        """Perform DB write or update operation."""

    def close_connection(self):
        """Close database connection."""
