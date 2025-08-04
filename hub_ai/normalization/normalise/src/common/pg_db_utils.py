import psycopg2
from psycopg2.extras import RealDictCursor
import os
import logging
import normalise.env as env

POSTGRES_HOST = os.getenv('PGHOST')
POSTGRES_PORT = os.getenv('PGPORT')
POSTGRES_DB = os.getenv('PGDATABASE')
POSTGRES_USER = os.getenv('PGUSER')
POSTGRES_PASSWORD = os.getenv('PGPASSWORD')
POSTGRES_SCHEMA = "idp"

class PostgresConnector:
    def __init__(self, logger: logging.Logger):
        self.host = POSTGRES_HOST
        self.port = POSTGRES_PORT
        self.database = POSTGRES_DB
        self.user = POSTGRES_USER
        self.password = POSTGRES_PASSWORD
        self.schema = POSTGRES_SCHEMA
        self.connection = None
        self.logger = logger

    def connect(self):
        self.logger.info(
            f"Connecting to PostgreSQL with params: host='{self.host}', port='{self.port}', db='{self.database}', user='{self.user}', schema='{self.schema}'"
        )
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                cursor_factory=RealDictCursor
            )
            self.logger.info("PostgreSQL connection established successfully.")

            # Set schema
            with self.connection.cursor() as cursor:
                self.logger.info(f"Setting search_path to schema: {self.schema}")
                cursor.execute(f"SET search_path TO {self.schema};")
            self.logger.info(f"Schema '{self.schema}' set successfully.")
        except Exception as e:
            self.logger.error(f"Error connecting to PostgreSQL: {e}", exc_info=True)
            self.connection = None

    def execute_query(self, query, params=None):
        if not self.connection:
            self.logger.error("No active PostgreSQL connection. Query not executed.")
        try:
            with self.connection.cursor() as cursor:
                self.logger.debug(f"Executing query: {query}")
                if params:
                    self.logger.debug(f"With parameters: {params}")

                # Detect write operations and log
                if query.strip().lower().startswith(("insert", "update", "delete")):
                    self.logger.info("Executing a write operation (INSERT/UPDATE/DELETE)")

                cursor.execute(query, params)
                if cursor.description:
                    result = cursor.fetchall()
                    self.logger.info(f"Query executed successfully. Rows fetched: {len(result)}")
                    return result
                else:
                    self.connection.commit()
                    self.logger.info("Query executed successfully. No rows to fetch (committed).")
        except Exception as e:
            self.rollback()
            self.logger.error(f"Error executing query: {query}", exc_info=True)

    def mark_status(self, table_name, where_clause="", status=""):
        """
        Marks the status of a record in the specified table.
        """
        self.logger.info(
            f"Attempting to update status to '{status}' in table {table_name} where {where_clause}"
        )
        query = f"UPDATE {table_name} SET status = %s WHERE {where_clause}"
        result = self.execute_query(query, (status,))
        if result is not None or (self.connection and self.connection.status == psycopg2.extensions.STATUS_READY):
            self.logger.info(
                f"Status successfully updated to '{status}' in table {table_name} where {where_clause}"
            )
        else:
            self.logger.warning(
                f"Status update failed. Rolling back. Table: {table_name}, Where: {where_clause}"
            )
            self.rollback()

    def rollback(self):
        """Roll back the current transaction if connection is active."""
        if self.connection:
            try:
                self.connection.rollback()
                self.logger.info("Rolled back the transaction.")
            except Exception as e:
                self.logger.error(f"Failed to rollback transaction: {e}", exc_info=True)
