from ada.use_cases.document_services.base_document_process_request import (
    DocumentProcessRequest,
    PreRequisiteCondition,
)
from ada.utils.logs.logger import get_logger

log = get_logger("DocumentInformationFetchRequest")


class DocumentInformationFetchRequest(DocumentProcessRequest):
    def __init__(
        self,
        tenant_id: str,
        payload: dict,
    ):
        super().__init__(tenant_id, payload)

    def validate(self):
        return super().is_all_true(
            [
                PreRequisiteCondition(
                    self.request_body.get("use_case") == "summary",
                    "Use case value should be summary",
                ),
                PreRequisiteCondition(self.request_body.get("document_id"), "Document Id"),
                PreRequisiteCondition(self.tenant_id, "Tenant Id"),
            ],
        )

    def process(self):
        doc_id = self.request_body["document_id"]
        data = self.pg_db_conn.select_component_column(
            table_name="document_information",
            column_name="summary",
            key_column="document_id",
            value=str(doc_id),
        )
        self.pg_db_conn.close_connection()
        return {"document_id": doc_id, self.request_body["use_case"]: data[0][0]}
