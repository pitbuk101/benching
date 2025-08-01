from unittest.mock import MagicMock, patch

from ada.components.db.pg_connector import PGConnector
from ada.components.db.pg_operations import fuzzy_search_contract_content


@patch("ada.components.db.pg_operations.PGConnector")
def test_document_search_query_should_execute_with_vectorised_user_queries(pg_connector_mock_class):
    pg_conn_instance = MagicMock(spec=PGConnector)
    pg_connector_mock_class.return_value = pg_conn_instance

    pg_conn_instance.search_contract_doc_content_user_query.return_value = 12345

    user_questions = ["What is the leakage"]
    doc_id = fuzzy_search_contract_content(user_questions, "123")

    pg_conn_instance.search_contract_doc_content_user_query.assert_called_once()
    assert pg_conn_instance.search_contract_doc_content_user_query.call_args[0][0] == user_questions
    assert doc_id == 12345
