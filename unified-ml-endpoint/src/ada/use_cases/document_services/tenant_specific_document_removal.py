from ada.use_cases.document_services.base_document_process_request import (
    DocumentProcessRequest,
    NotFoundException,
    PreRequisiteCondition,
)
from ada.utils.logs.logger import get_logger

log = get_logger("DocumentProcessRequest")


class TenantSpecificKnowledgeDocDeleteRequest(DocumentProcessRequest):
    def __init__(
        self,
        tenant_id: str,
        payload: dict,
    ):
        super().__init__(tenant_id, payload)

    def validate(self):
        return super().is_all_true(
            [
                PreRequisiteCondition(self.request_body.get("document_id"), "Document Id"),
                PreRequisiteCondition(self.tenant_id, "Tenant Id"),
            ],
        )

    def process(self):
        doc_id = self.request_body.get("document_id")
        document_exists = self.pg_db_conn.document_exists_by_column("document_id", doc_id)
        if document_exists:
            self.pg_db_conn.remove_document_by_column("document_id", doc_id)
            log.info(f"Successfully deleted the document {doc_id}")
        else:
            log.info(f"Document do not exists name: {doc_id}")
            raise NotFoundException(f"Document do not exists with id: {doc_id}")
