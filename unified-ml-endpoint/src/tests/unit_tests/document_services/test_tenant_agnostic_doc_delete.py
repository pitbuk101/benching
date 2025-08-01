from unittest.mock import MagicMock, patch

import pytest

from ada.components.db.pg_connector import COMMON_DB_USER, PGConnector
from ada.use_cases.document_services.base_document_process_request import (
    NotFoundException,
    ValidationFailedException,
)
from ada.use_cases.document_services.tenant_agnostic_document_removal import (
    TenantAgnosticKnowledgeDocDeleteRequest,
)


@patch("ada.use_cases.document_services.base_document_process_request.PGConnector")
def test_validation_logic_for_tenant_agnostic_kd_doc_delete_request(pg_connector_mock_class):
    pg_connector_mock_class.return_value = MagicMock(spec=PGConnector)

    tenant_specific_doc_delete = TenantAgnosticKnowledgeDocDeleteRequest({"document_name": "1.pdf"})
    assert tenant_specific_doc_delete.validate()

    tenant_specific_doc_delete = TenantAgnosticKnowledgeDocDeleteRequest({"document_name": "1.pdf"})
    assert tenant_specific_doc_delete.validate()

    with pytest.raises(ValidationFailedException, match="Condition failed for: Document Name"):
        tenant_specific_doc_delete = TenantAgnosticKnowledgeDocDeleteRequest({"document_name": ""})
        tenant_specific_doc_delete.validate()

    with pytest.raises(ValidationFailedException, match="Condition failed for: Document Name"):
        tenant_specific_doc_delete = TenantAgnosticKnowledgeDocDeleteRequest(
            {"document_name": None},
        )
        tenant_specific_doc_delete.validate()

    with pytest.raises(ValidationFailedException, match="Condition failed for: Document Name"):
        tenant_specific_doc_delete = TenantAgnosticKnowledgeDocDeleteRequest({})
        tenant_specific_doc_delete.validate()


@patch("ada.use_cases.document_services.base_document_process_request.PGConnector")
def test_process_for_tenant_agnostic_kd_doc_delete_request(pg_connector_mock_class):
    pg_conn_mock = MagicMock(spec=PGConnector)
    pg_connector_mock_class.return_value = pg_conn_mock

    pg_conn_mock.document_exists_by_column.return_value = True
    tenant_specific_doc_delete = TenantAgnosticKnowledgeDocDeleteRequest({"document_name": "1.pdf"})
    tenant_specific_doc_delete.process()

    assert pg_connector_mock_class.call_args[0][0] == COMMON_DB_USER
    assert pg_conn_mock.remove_document_by_column.call_args[0][0] == "document_name"
    assert pg_conn_mock.remove_document_by_column.call_args[0][1] == "1.pdf"


@patch("ada.use_cases.document_services.base_document_process_request.PGConnector")
def test_process_for_tenant_agnostic_kd_doc_delete_should_fail_when_document_do_not_exists_request(
    pg_connector_mock_class,
):
    pg_conn_mock = MagicMock(spec=PGConnector)
    pg_connector_mock_class.return_value = pg_conn_mock

    pg_conn_mock.document_exists_by_column.return_value = False
    tenant_specific_doc_delete = TenantAgnosticKnowledgeDocDeleteRequest({"document_name": "1.pdf"})
    with pytest.raises(NotFoundException, match="Document do not exists name: 1.pdf"):
        tenant_specific_doc_delete.process()
        assert pg_conn_mock.call_args[0][0] == COMMON_DB_USER
        assert pg_conn_mock.remove_document_by_column.assert_not_called()
