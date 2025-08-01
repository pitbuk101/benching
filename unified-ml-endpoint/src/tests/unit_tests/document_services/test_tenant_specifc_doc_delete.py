from unittest.mock import MagicMock, patch

import pytest

from ada.components.db.pg_connector import PGConnector
from ada.use_cases.document_services.base_document_process_request import (
    NotFoundException,
    ValidationFailedException,
)
from ada.use_cases.document_services.tenant_specific_document_removal import (
    TenantSpecificKnowledgeDocDeleteRequest,
)


@patch("ada.use_cases.document_services.base_document_process_request.PGConnector")
def test_validation_logic_for_tenant_specific_kd_doc_delete_request(pg_connector_mock_class):
    pg_connector_mock_class.return_value = MagicMock(spec=PGConnector)

    tenant_specific_doc_delete = TenantSpecificKnowledgeDocDeleteRequest(
        "123",
        {"document_id": "12345"},
    )
    assert tenant_specific_doc_delete.validate()

    with pytest.raises(ValidationFailedException, match="Condition failed for: Tenant Id"):
        tenant_specific_doc_delete = TenantSpecificKnowledgeDocDeleteRequest(
            None,
            {"document_id": "12345"},
        )
        tenant_specific_doc_delete.validate()

    with pytest.raises(ValidationFailedException, match="Condition failed for: Tenant Id"):
        tenant_specific_doc_delete = TenantSpecificKnowledgeDocDeleteRequest(
            "",
            {"document_id": "12345"},
        )
        tenant_specific_doc_delete.validate()

    with pytest.raises(ValidationFailedException, match="Condition failed for: Document Id"):
        tenant_specific_doc_delete = TenantSpecificKnowledgeDocDeleteRequest(
            "123",
            {"document_id": ""},
        )
        tenant_specific_doc_delete.validate()

    with pytest.raises(ValidationFailedException, match="Condition failed for: Document Id"):
        tenant_specific_doc_delete = TenantSpecificKnowledgeDocDeleteRequest(
            "123",
            {"document_id": None},
        )
        tenant_specific_doc_delete.validate()

    with pytest.raises(ValidationFailedException, match="Condition failed for: Document Id"):
        tenant_specific_doc_delete = TenantSpecificKnowledgeDocDeleteRequest(
            "123",
            {},
        )
        tenant_specific_doc_delete.validate()


@patch("ada.use_cases.document_services.base_document_process_request.PGConnector")
def test_process_for_tenant_specific_kd_doc_delete_request(pg_connector_mock_class):
    pg_conn_mock = MagicMock(spec=PGConnector)
    pg_connector_mock_class.return_value = pg_conn_mock

    pg_conn_mock.document_exists_by_column.return_value = True
    tenant_specific_doc_delete = TenantSpecificKnowledgeDocDeleteRequest(
        "123",
        {"document_id": "123456"},
    )
    tenant_specific_doc_delete.process()

    assert pg_connector_mock_class.call_args[0][0] == "123"
    assert pg_conn_mock.remove_document_by_column.call_args[0][0] == "document_id"
    assert pg_conn_mock.remove_document_by_column.call_args[0][1] == "123456"


@patch("ada.use_cases.document_services.base_document_process_request.PGConnector")
def test_process_for_tenant_specific_kd_doc_delete_should_fail_when_document_do_not_exists_request(
    pg_connector_mock_class,
):
    pg_conn_mock = MagicMock(spec=PGConnector)
    pg_connector_mock_class.return_value = pg_conn_mock

    pg_conn_mock.document_exists_by_column.return_value = False
    tenant_specific_doc_delete = TenantSpecificKnowledgeDocDeleteRequest(
        "123",
        {"document_id": "1123456"},
    )
    with pytest.raises(NotFoundException, match="Document do not exists with id: 1123456"):
        tenant_specific_doc_delete.process()
        assert pg_conn_mock.call_args[0][0] == "123"
        assert pg_conn_mock.remove_document_by_column.assert_not_called()
