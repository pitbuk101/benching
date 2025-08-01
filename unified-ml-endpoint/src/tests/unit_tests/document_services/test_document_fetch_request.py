from unittest.mock import MagicMock, patch

import pytest

from ada.components.db.pg_connector import PGConnector
from ada.use_cases.document_services.base_document_process_request import (
    ValidationFailedException,
)
from ada.use_cases.document_services.document_information_fetch_request import (
    DocumentInformationFetchRequest,
)


@patch("ada.use_cases.document_services.base_document_process_request.PGConnector")
def test_validation_logic_for_document_information_fetch_request(pg_connector_mock_class):
    pg_connector_mock_class.return_value = MagicMock(spec=PGConnector)

    with pytest.raises(
        ValidationFailedException,
        match="Condition failed for: Use case value should be summary",
    ):
        document_fetch = DocumentInformationFetchRequest("123", {})
        document_fetch.validate()

    with pytest.raises(ValidationFailedException, match="Condition failed for: Document Id"):
        document_fetch = DocumentInformationFetchRequest("1", {"use_case": "summary"})
        document_fetch.validate()

    with pytest.raises(ValidationFailedException, match="Condition failed for: Document Id"):
        document_fetch = DocumentInformationFetchRequest(
            "123",
            {"use_case": "summary", "document_id": ""},
        )
        document_fetch.validate()

    with pytest.raises(ValidationFailedException, match="Condition failed for: Tenant Id"):
        document_fetch = DocumentInformationFetchRequest(
            None,
            {"use_case": "summary", "document_id": "123"},
        )
        document_fetch.validate()

    with pytest.raises(
        ValidationFailedException,
        match="Condition failed for: Use case value should be summary",
    ):
        document_fetch = DocumentInformationFetchRequest(
            None,
            {"use_case": "leakage", "document_id": "123"},
        )
        document_fetch.validate()

    with pytest.raises(ValidationFailedException, match="Condition failed for: Document Id"):
        document_fetch = DocumentInformationFetchRequest(
            "123",
            {"use_case": "summary", "document_id": None},
        )
        document_fetch.validate()

    document_fetch = DocumentInformationFetchRequest(
        "123",
        {"use_case": "summary", "document_id": "123"},
    )
    assert document_fetch.validate()


@patch("ada.use_cases.document_services.base_document_process_request.PGConnector")
def test_process_for_document_information_fetch_request(pg_connector_mock_class):
    pg_conn_mock = MagicMock(spec=PGConnector)
    pg_connector_mock_class.return_value = pg_conn_mock
    pg_conn_mock.select_component_column.return_value = [["Some data"]]

    document_fetch = DocumentInformationFetchRequest(
        "123",
        {"use_case": "summary", "document_id": "123"},
    )
    data = document_fetch.process()

    assert data["document_id"] == "123"
    assert data["summary"] == "Some data"
    assert pg_conn_mock.select_component_column.call_args[1]["table_name"] == "document_information"
    assert pg_conn_mock.select_component_column.call_args[1]["column_name"] == "summary"
    assert pg_conn_mock.select_component_column.call_args[1]["key_column"] == "document_id"
    assert pg_conn_mock.select_component_column.call_args[1]["value"] == "123"
