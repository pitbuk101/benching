from enum import Enum

from ada.components.db.pg_connector import PGConnector


class RequestType(Enum):
    FETCH = "FETCH"
    DELETE = "DELETE"


class NotFoundException(Exception):
    """Raised when queried entity do not exists"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ValidationFailedException(Exception):
    """Raised when required arguments are missing"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class PreRequisiteCondition:
    def __init__(self, condition, description: str):
        self.condition = condition
        self.description = description

    def is_failed(self):
        return not self.condition


class DocumentProcessRequest:
    def __init__(self, tenant_id: str, payload: dict):
        self.request_type = getattr(RequestType, payload.get("request_type", ""), RequestType.FETCH)
        self.request_body = payload
        self.tenant_id = tenant_id if (tenant_id is not None) else ""
        self.pg_db_conn: PGConnector = PGConnector(self.tenant_id)

    def is_all_true(self, conditions: list[PreRequisiteCondition]):
        for prerequisite_condition in conditions:
            if prerequisite_condition.is_failed():
                raise ValidationFailedException(
                    f"Condition failed for: {str(prerequisite_condition.description)}",
                )

        return True

    def validate(self):
        pass

    def process(self):
        pass
