"""Azure ML Endpoint for Negotiation factory deployment."""

import pathlib
import sys
from typing import Any

# pylint: disable=C0413
sys.path.append(str(pathlib.Path(__file__).parents[2]))
from ada.components.db.pg_connector import PGConnector  # noqa: E402
from ada.use_cases.negotiation_factory.negotiation_factory import (  # noqa: E402; noqa: E402
    run_negotiation_factory,
)

# pylint: enable=C0413
from ada.use_cases.negotiation_factory.reference_data_retriever import (  # noqa: E402
    read_reference_data,
)
from ada.utils.config.config_loader import read_config  # noqa: E402
from ada.utils.logs.logger import get_logger  # noqa: E402

conf = read_config("use-cases.yml")
negotiation_conf = conf["negotiation_factory"]
log = get_logger("negotiation_factory_initialization")


def init():
    """Azure Realtime deployment for Idea generation."""
    global ref_data
    ref_data = read_reference_data()


def run(
    json_file: str,
    reference_data: dict,
    pg_db_conn: PGConnector,
    chat_history: list,
) -> dict[str, Any]:
    """
    Entrypoint function.
    Args:
        json_file (str): json dumps version of the input payload
        reference_data (dict): Reference static data
        pg_db_conn (PGConnector) : Postgres connector object
        chat_history (list): Chat history from database
    Returns:
        (dict): Response of negotiation factory
    """
    if reference_data:
        global ref_data
        ref_data = reference_data  # type: ignore

    return run_negotiation_factory(
        input_data_str=json_file,
        reference_data=ref_data,  # type: ignore
        pg_db_conn=pg_db_conn,
        chat_history=chat_history,
    )
