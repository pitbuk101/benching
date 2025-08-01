import os
import unittest
from unittest.mock import MagicMock, patch
from ada.components.db.pg_connector import PGConnector


class TestPGConnector(unittest.TestCase):
    @patch("ada.components.db.pg_connector.psycopg2")
    @patch("ada.components.db.pg_connector.read_config")
    @patch("ada.components.db.pg_connector.get_secrets")
    @patch("ada.components.db.pg_connector.get_tenant_key_name")
    def setUp(self, mock_get_tenant_key_name, mock_get_secrets, mock_read_config, mock_psycopg2):
        self._tenant_id = "tenant1"
        self._cursor = MagicMock()
        mock_get_tenant_key_name.return_value = "tenant_key"
        mock_get_secrets.return_value = {
            "db_password": os.getenv("test_password"),
            "azfa_url": "https://azure-url",
        }
        mock_read_config.return_value = {
            "user": "test_user",
            "password": os.environ['testpassword'],
            "host": "localhost",
            "port": "5432",
            "dbname": "test_db",
            "global": {},
        }
        mock_psycopg2.connect.return_value = MagicMock()
        with patch.dict("os.environ", {"LOCAL_DB_MODE": "1"}):
            self.connector = PGConnector(tenant_id=self._tenant_id)
            self.connector._submit_query = MagicMock()
            self.connector._retrieve_query = MagicMock()

    @patch("ada.components.db.pg_connector.read_config")
    @patch("ada.components.db.pg_connector.psycopg2.connect")
    def test_db_local_mode(self, mock_connect, mock_read_config):
        mock_read_config.return_value = {
            "user": "test_user",
            "password": "test_password",
            "host": "localhost",
            "port": "5432",
            "dbname": "test_db",
        }
        with patch.dict("os.environ", {"LOCAL_DB_MODE": "1"}):
            connector = PGConnector(tenant_id=self._tenant_id)
            self.assertEqual(connector._tenant_id, self._tenant_id)
            mock_connect.assert_called_once_with(
                user="test_user",
                password="test_password",
                host="localhost",
                port="5432",
                database="test_db",
            )

    @patch("ada.components.db.pg_connector.AzureConnector")
    @patch("ada.components.db.pg_connector.psycopg2.connect")
    @patch("ada.components.db.pg_connector.read_config")
    @patch("ada.components.db.pg_connector.get_secrets")
    def test_db_azure_mode(
        self,
        mock_get_secrets,
        mock_read_config,
        mock_psycopg2_connect,
        mock_azure_connector,
    ):
        mock_get_secrets.return_value = {
            "db_password": os.getenv['secret_password'],
            "azfa_url": "https://example.com",
        }
        mock_read_config.return_value = {
            "user": "test_user",
            "password": "test_password",
            "host": "localhost",
            "port": "5432",
            "dbname": "test_db",
            "global": {},
        }
        with patch.dict("os.environ", {"LOCAL_DB_MODE": "0", "AZURE_DATABASE_ACCESS": "0"}):
            connector = PGConnector(tenant_id=self._tenant_id)
            self.assertEqual(connector._tenant_id, self._tenant_id)
            mock_psycopg2_connect.assert_not_called()
            mock_azure_connector.assert_called_once()

    def test_update_values(self):
        table_name = "table_name"
        values = {"key1": "value1", "key2": 1}
        conditions = {"cond1": 2}
        self.connector.update_values(table_name, values, conditions)
        expected_query = "UPDATE table_name SET key1 = %s, key2 = %s WHERE cond1 = %s"
        expected_values = ["value1", 1, 2]
        self.connector._submit_query.assert_called_once_with(
            query=expected_query,
            values=expected_values,
        )

    def test_delete_values(self):
        table_name = "table_name"
        conditions = {"cond1": 2, "cond2": "value1"}

        expected_query = """DELETE FROM table_name WHERE cond1 = %s AND cond2 = %s"""

        self.connector.delete_values(table_name, conditions)
        self.connector._submit_query.assert_called_once_with(
            query=expected_query,
            values=[2, "value1"],
        )

    def test_search_by_vector_similarity_cosine_distance(self):
        table_name = "table_name"
        query_emb = [0.1, 0.2, 0.3]
        emb_column_name = "embedding"
        num_records = 10
        search_type = "cosine_distance"
        conditions = {"column1": "value1", "column2": 123}
        expected_query = f"""
                SELECT *, {emb_column_name} <=> '{str(query_emb)}' AS cosine_distance
                FROM {table_name}
                WHERE column1 = %s AND column2 = %s
                ORDER BY cosine_distance
                LIMIT {num_records or 'ALL'};
            """

        self.connector.search_by_vector_similarity(
            table_name=table_name,
            query_emb=query_emb,
            emb_column_name=emb_column_name,
            num_records=num_records,
            search_type=search_type,
            conditions=conditions,
        )

        self.connector._retrieve_query.assert_called_once_with(
            query=expected_query,
            values=list(conditions.values()),
        )

    def test_search_by_psq_vs_vector(self):
        expected_query = """SELECT document_id from document_information
        WHERE  lower(document_type)='contract' AND
        to_tsvector('english', content) @@ to_tsquery('What|is|the|leakages|values|Contract|motors') limit 1;"""
        user_questions = ["What is the leakage's values", "Contract motors"]

        self.connector.search_contract_doc_content_user_query(user_questions)
        assert self.connector._retrieve_query.call_args[1]["query"].strip() == expected_query
