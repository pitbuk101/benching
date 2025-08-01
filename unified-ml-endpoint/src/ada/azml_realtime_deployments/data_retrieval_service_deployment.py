"""Azure ML Endpoint for data retrieval service deployment."""

import pathlib
import sys

# pylint: disable=C0413
sys.path.append(str(pathlib.Path(__file__).parents[2]))
# pylint: enable=C0413

# flake8: noqa: E402
from ada.use_cases.data_retrieval_services.data_retrieval_service import (
    run_data_retrieval_service,
)


def init():
    """Azure Realtime deployment for data retrieval service"""


def run(inputs):
    """Entrypoint function"""
    return run_data_retrieval_service(inputs)
