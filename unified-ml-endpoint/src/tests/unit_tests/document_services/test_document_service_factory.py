import json
from unittest.mock import MagicMock, patch

from ada.use_cases.document_services.base_document_process_request import (
    DocumentProcessRequest,
    RequestType,
)
from ada.use_cases.document_services.contract_information_fetch_request import (
    ContractInformationFetchRequest,
)
from ada.use_cases.document_services.document_information_fetch_request import (
    DocumentInformationFetchRequest,
)
from ada.use_cases.document_services.document_service import (
    get_document_process_request,
)
from ada.use_cases.document_services.tenant_agnostic_document_removal import (
    TenantAgnosticKnowledgeDocDeleteRequest,
)
from ada.use_cases.document_services.tenant_specific_document_removal import (
    TenantSpecificKnowledgeDocDeleteRequest,
)


@patch("ada.use_cases.document_services.document_service.DocumentProcessRequest")
@patch("ada.use_cases.document_services.document_service.TenantAgnosticKnowledgeDocDeleteRequest")
@patch("ada.use_cases.document_services.document_service.TenantSpecificKnowledgeDocDeleteRequest")
@patch("ada.use_cases.document_services.document_service.ContractInformationFetchRequest")
@patch("ada.use_cases.document_services.document_service.DocumentInformationFetchRequest")
def test_get_document_fetch_request_based_on_request_type_and_use_case(
    document_info_fetch_mock_class,
    contract_info_fetch_mock_class,
    tenant_kd_delete_mock_class,
    tenant_agnostic_kd_delete_mock_class,
    default_document_process_request_mock_class,
):
    document_info_fetch_mock_class.return_value = MagicMock(spec=DocumentInformationFetchRequest)
    contract_info_fetch_mock_class.return_value = MagicMock(spec=ContractInformationFetchRequest)
    tenant_kd_delete_mock_class.return_value = MagicMock(
        spec=TenantSpecificKnowledgeDocDeleteRequest,
    )
    tenant_agnostic_kd_delete_mock_class.return_value = MagicMock(
        spec=TenantAgnosticKnowledgeDocDeleteRequest,
    )
    default_document_process_request_mock_class.return_value = MagicMock(
        spec=DocumentProcessRequest,
    )

    input_dict: dict = {"request_type": RequestType.FETCH.value, "use_case": "summary"}
    assert isinstance(
        get_document_process_request(json.dumps(input_dict)),
        DocumentInformationFetchRequest,
    )

    input_dict: dict = {"request_type": RequestType.FETCH.value, "use_case": "other_than_summary"}
    assert isinstance(
        get_document_process_request(json.dumps(input_dict)),
        ContractInformationFetchRequest,
    )

    input_dict: dict = {"request_type": RequestType.DELETE.value, "tenant_id": "123"}
    assert isinstance(
        get_document_process_request(json.dumps(input_dict)),
        TenantSpecificKnowledgeDocDeleteRequest,
    )

    input_dict: dict = {"request_type": RequestType.DELETE.value, "tenant_id": ""}
    assert isinstance(
        get_document_process_request(json.dumps(input_dict)),
        TenantAgnosticKnowledgeDocDeleteRequest,
    )

    input_dict: dict = {"request_type": RequestType.DELETE.value, "document_name": "doc1.pdf"}
    assert isinstance(
        get_document_process_request(json.dumps(input_dict)),
        TenantAgnosticKnowledgeDocDeleteRequest,
    )

    input_dict: dict = {"request_type": "unknown", "document_name": "doc1.pdf"}
    assert isinstance(get_document_process_request(json.dumps(input_dict)), DocumentProcessRequest)
