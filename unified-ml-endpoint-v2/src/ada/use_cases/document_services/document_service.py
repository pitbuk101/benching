import json

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
from ada.use_cases.document_services.tenant_agnostic_document_removal import (
    TenantAgnosticKnowledgeDocDeleteRequest,
)
from ada.use_cases.document_services.tenant_specific_document_removal import (
    TenantSpecificKnowledgeDocDeleteRequest,
)
from ada.utils.logs.logger import get_logger

log = get_logger("DocumentProcessRequest")


def get_document_process_request(input_json: str) -> DocumentProcessRequest:
    payload = json.loads(input_json)
    request_processor = None
    tenant_id = payload.get("tenant_id", "")
    request_type = getattr(RequestType, payload.get("request_type", ""), RequestType.FETCH)
    request_processor = DocumentProcessRequest(tenant_id, payload)

    if all([request_type == RequestType.FETCH, payload.get("use_case") == "summary"]):
        request_processor = DocumentInformationFetchRequest(tenant_id, payload)
    elif request_type == RequestType.FETCH:
        request_processor = ContractInformationFetchRequest(tenant_id, payload)
    elif all([request_type == RequestType.DELETE, tenant_id]):
        request_processor = TenantSpecificKnowledgeDocDeleteRequest(tenant_id, payload)
    elif all([request_type == RequestType.DELETE, not tenant_id]):
        request_processor = TenantAgnosticKnowledgeDocDeleteRequest(payload)

    return request_processor
