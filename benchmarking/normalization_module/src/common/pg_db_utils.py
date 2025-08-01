import psycopg2
from psycopg2.extras import RealDictCursor
import os
import logging
class PostgresConnector:
    def __init__(self, config,logger: logging.Logger):
        self.postgres = config.postgres
        self.host = self.postgres.host_env_var
        self.port = self.postgres.port_env_var
        self.database = self.postgres.database_env_var
        self.user = self.postgres.user_env_var
        self.password = self.postgres.password_env_var
        self.schema = self.postgres.schema_env_var
        self.connection = None
        self.logger = logger
    def connect(self):
        self.logger.info(f"Connecting to PostgreSQL database: {self.database} at {self.host}:{self.port}")
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                cursor_factory=RealDictCursor
            )
            # Set the search_path to the desired schema
            with self.connection.cursor() as cursor:
                cursor.execute(f"SET search_path TO {self.schema};")
            self.logger.info(f"PostgreSQL connection established. Using schema: {self.schema}")
        except Exception as e:
            self.logger.info(f"Error connecting to PostgreSQL: {e}")
            self.connection = None
    

    def execute_query(self, query, params=None):
        if not self.connection:
            self.logger.info("No active PostgreSQL connection.")
            return None
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                if cursor.description:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
                    return None
        except Exception as e:
            self.connection.rollback()  # <== This is critical
            self.logger.info(f"Error executing query: {e}")
            return None


    def mark_status_inprogress(self,table_name,where_clause=""):
        """
        Marks the status of a record in the specified table.
        """
        query = f"UPDATE {table_name} SET status = 'In Progress' WHERE {where_clause}"
        self.execute_query(query)
        self.logger.info(f"Status updated in table {table_name} where {where_clause}")
        


    def mark_status_ended(self, table_name, where_clause=""):
        """
        Marks the status of a record in the specified table.
        """
        query = f"UPDATE {table_name} SET status = 'Completed' WHERE {where_clause}"
        self.execute_query(query)
        self.logger.info(f"Status updated in table {table_name} where {where_clause}")
        
        




