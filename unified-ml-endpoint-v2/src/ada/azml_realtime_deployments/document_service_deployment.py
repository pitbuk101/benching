"""Azure ML Endpoint for data retrieval deployment."""

import pathlib
import sys

# pylint: disable=C0413
sys.path.append(str(pathlib.Path(__file__).parents[2]))
# pylint: enable=C0413

# flake8: noqa: E402

from ada.use_cases.document_services.base_document_process_request import (
    NotFoundException,
    ValidationFailedException,
)
from ada.use_cases.document_services.document_service import (
    get_document_process_request,
)
from ada.utils.logs.logger import get_logger

log = get_logger("Document service deployment")

log = get_logger("Document service deployment")


def init():
    """Azure Realtime deployment for data retrieval"""


def run(inputs):
    """Entrypoint function"""
    try:
        document_request = get_document_process_request(inputs)
        document_request.validate()
        return document_request.process()
    except ValidationFailedException as validation_exception:
        return {
            "error": f"A validation error occurred: {str(validation_exception)}",
            "http_status_code": 412,
        }
    except NotFoundException as not_found_exception:
        return {
            "error": f"A validation error occurred: {str(not_found_exception)}",
            "http_status_code": 404,
        }
