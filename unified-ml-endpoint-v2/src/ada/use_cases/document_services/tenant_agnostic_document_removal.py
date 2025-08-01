from ada.components.db.pg_connector import COMMON_DB_USER
from ada.use_cases.document_services.base_document_process_request import (
    DocumentProcessRequest,
    NotFoundException,
    PreRequisiteCondition,
)
from ada.utils.logs.logger import get_logger

log = get_logger("DocumentProcessRequest")


class TenantAgnosticKnowledgeDocDeleteRequest(DocumentProcessRequest):
    def __init__(
        self,
        payload: dict,
    ):
        super().__init__(COMMON_DB_USER, payload)

    def validate(self):
        return super().is_all_true(
            [
                PreRequisiteCondition(self.request_body.get("document_name"), "Document Name"),
            ],
        )

    def process(self):
        doc_name = self.request_body.get("document_name")
        document_exists = self.pg_db_conn.document_exists_by_column("document_name", doc_name)
        if document_exists:
            self.pg_db_conn.remove_document_by_column("document_name", doc_name)
            log.info(f"Successfully deleted the document {doc_name}")
        else:
            log.info(f"Document do not exists name: {doc_name}")
            raise NotFoundException(f"Document do not exists name: {doc_name}")
