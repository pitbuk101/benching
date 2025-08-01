from unittest.mock import MagicMock, patch

import pytest

from ada.components.db.pg_connector import PGConnector
from ada.use_cases.document_services.base_document_process_request import (
    ValidationFailedException,
)
from ada.use_cases.document_services.contract_information_fetch_request import (
    ContractInformationFetchRequest,
)


@patch("ada.use_cases.document_services.base_document_process_request.PGConnector")
def test_validation_logic_for_contract_information_fetch_request(pg_connector_mock_class):
    pg_connector_mock_class.return_value = MagicMock(spec=PGConnector)

    contract_info_fetch = ContractInformationFetchRequest(
        "123",
        {"use_case": "leakage", "document_id": "123"},
    )
    assert contract_info_fetch.validate()

    with pytest.raises(ValidationFailedException, match="Condition failed for: Tenant Id"):
        contract_info_fetch = ContractInformationFetchRequest(
            "",
            {"use_case": "leakage", "document_id": "123"},
        )
        contract_info_fetch.validate()

    with pytest.raises(ValidationFailedException, match="Condition failed for: Tenant Id"):
        contract_info_fetch = ContractInformationFetchRequest(
            None,
            {"use_case": "leakage", "document_id": "123"},
        )
        assert contract_info_fetch.validate()

    with pytest.raises(ValidationFailedException, match="Condition failed for: Use case"):
        contract_info_fetch = ContractInformationFetchRequest(
            "123",
            {"use_case": "", "document_id": "123"},
        )
        assert contract_info_fetch.validate()

    with pytest.raises(ValidationFailedException, match="Condition failed for: Document Id"):
        contract_info_fetch = ContractInformationFetchRequest(
            "123",
            {"use_case": "leakage", "document_id": ""},
        )
        assert contract_info_fetch.validate()

    with pytest.raises(ValidationFailedException, match="Condition failed for: Document Id"):
        contract_info_fetch = ContractInformationFetchRequest(
            "123",
            {"use_case": "leakage", "document_id": None},
        )
        assert contract_info_fetch.validate()

    with pytest.raises(ValidationFailedException, match="Condition failed for: Document Id"):
        contract_info_fetch = ContractInformationFetchRequest("123", {"use_case": "leakage"})
        assert contract_info_fetch.validate()


@patch("ada.use_cases.document_services.base_document_process_request.PGConnector")
def test_process_for_contract_information_fetch_request(pg_connector_mock_class):
    pg_conn_mock = MagicMock(spec=PGConnector)
    pg_connector_mock_class.return_value = pg_conn_mock
    pg_conn_mock.select_component_column.return_value = [["Some data"]]
    contract_info_fetch = ContractInformationFetchRequest(
        "123",
        {"use_case": "leakage", "document_id": "123"},
    )
    data = contract_info_fetch.process()

    assert data["document_id"] == "123"
    assert data["leakage"] == "Some data"
    assert pg_conn_mock.select_component_column.call_args[1]["table_name"] == "contract_details"
    assert pg_conn_mock.select_component_column.call_args[1]["column_name"] == "leakage"
    assert pg_conn_mock.select_component_column.call_args[1]["key_column"] == "document_id"
    assert pg_conn_mock.select_component_column.call_args[1]["value"] == "123"
