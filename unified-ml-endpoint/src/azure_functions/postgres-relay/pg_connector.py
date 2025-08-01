"""Class to connect to Postgres database."""

import logging
from typing import Any, Tuple

import psycopg2
import psycopg2.extras
from auth import get_secrets, read_config
from sqlalchemy import create_engine

tenant_secret_caches = {}


class TenantSecretCaches:
    @staticmethod
    def add_to_cache(key, value):
        global tenant_secret_caches
        tenant_secret_caches[key] = value

    @staticmethod
    def get_from_cache(key):
        return tenant_secret_caches.get(key)


class PGConnector:
    """Class to connect to Postgres database."""

    def __init__(
        self,
        tenant_key: str,
        tenant_id: str,
        credentials_file: str = "pg_credentials.yml",
        cursor_type: str | None = None,
    ):
        """Creates a connector object.
        Args:
            tenant_id: ID of the tenant to connect to.
            credentials_file: Name of the file containing the credentials.
            cursor_type: Type of cursor to use. Defaults to None, which is a tuple cursor.
        """
        self.cursor_factory = getattr(psycopg2.extras, cursor_type) if cursor_type else None
        self.tenant_key = tenant_key
        credentials = read_config(credentials_file)
        secret_names = {"db_password": tenant_key}
        secret_keys = TenantSecretCaches.get_from_cache(tenant_key)
        if not secret_keys:
            secret_keys = get_secrets(
                secret_names=secret_names,
            )
            TenantSecretCaches.add_to_cache(tenant_key, secret_keys)

        logging.info("Retrieved secret keys successfully, connecting to database.")

        self._connect_to_db(
            user=tenant_id,
            password=secret_keys["db_password"],
            host=credentials["host"],
            port=credentials["port"],
            database=credentials["dbname"],
        )

    def execute(self, query: str, values: Any = None) -> Tuple | None:
        logging.info("Executing query: %s", query)
        self.__cursor.execute(query, values)

        if self.is_select(query):
            return self.__cursor.fetchall()
        else:
            self.__conn.commit()
        return None

    def is_select(self, query: str) -> bool:
        """Check if query is a select query."""
        return query.lower().strip().startswith(("select", "with"))

    def _connect_to_db(self, **kwargs):
        """Database connection."""
        self.__conn = psycopg2.connect(**kwargs)
        logging.info("Connected to database successfully.")
        self.__cursor = self.__conn.cursor(cursor_factory=self.cursor_factory)
        logging.info("Created cursor successfully.")
        self.alchemy_engine = create_engine(
            f"postgresql+psycopg2://{kwargs['user']}:"
            f"{kwargs['password']}@{kwargs['host']}:"
            f"{kwargs['port']}/{kwargs['database']}",
        )
        logging.info("Created engine successfully.")
