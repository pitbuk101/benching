"""
Read the reference data from common tenant agnostic tables and tenant specific tables to
run diffeent NEGO models
"""

import json
import os
import pathlib
import sys
from typing import Any

import pandas as pd

# pylint: disable=C0413
sys.path.append(str(pathlib.Path(__file__).parents[2]))
# pylint: enable=C0413

from ada.components.db.pg_connector import PGConnector  # noqa: E402
from ada.utils.config.config_loader import read_config  # noqa: E402
from ada.utils.logs.logger import get_logger  # noqa: E402
from ada.utils.logs.time_logger import log_time  # noqa: E402

conf = read_config("use-cases.yml")
negotiation_conf = conf["negotiation_factory"]
COMMON_DB_USER = "common-db-user"
log = get_logger("negotiation_factory_initialization")

@log_time
def read_reference_data() -> dict[str, Any]:
    """
    Read reference data
    Returns:
        (dict): Static reference data
    """
    log.info("Reading reference data")
    if int(os.getenv("LOCAL_DB_MODE", "0")):
        if not (tenant_id := os.getenv("ATLAS_TENANT_IDS")):
            # pylint: disable=W0719
            raise Exception("Please set ATLAS_TENANT_ID for local testing")
            # pylint: enable=W0719
        tenant_ids = [tenant_id]

    else:
        tenant_ids = os.getenv('ATLAS_TENANT_IDS').split(',')
    extracted_data: dict[str, object] = {}
    retrieve_tenant_specific_reference_data(tenant_ids, extracted_data)
    retrieve_common_reference_data(tenant_ids, extracted_data)
    return extracted_data


@log_time
def retrieve_tenant_specific_reference_data(tenant_ids, extracted_data):
    """
    Retrieves tenant-specific reference data from the database for each tenant in the provided
    `tenant_ids` list. The data for each tenant is fetched from specific tables defined in
    the configuration, with special handling for the "negotiation_strategy_tones_n_tactics"
    table where data is sourced from a YAML file.

    Args:
        tenant_ids (list): A list of tenant IDs for which reference data needs to be retrieved.
        extracted_data (dict): A dictionary where the tenant-specific data will be stored.
        The structure is
                               {tenant_id: {table_name: data}}.

    Returns:
        None: The method modifies the `extracted_data` dictionary in place, adding tenant-specific
          reference data.
    """
    log.info("Retrieving tenant-specific reference data")
    for tenant_id in tenant_ids:
        tenant_specific_data = {}
        pg_connector = PGConnector(tenant_id=tenant_id, cursor_type="real_dict")
        reference_tables = negotiation_conf["reference_tables"]["tenant_specific"].values()
        for table in reference_tables:
            # MI:08102024:Delete below step once we complete the automation for tone & tactics.
            # For now, we are reading the data from use-case.yml file
            data = None
            if table == "negotiation_strategy_tones_n_tactics":
                data = pd.DataFrame(
                    [
                        {
                            **row,
                            "tactics": json.dumps(row["tactics"]),
                            "prioritize": json.dumps(row["prioritize"]),
                        }
                        for row in conf["negotiation_factory"]["tone_n_tactics"]
                    ],
                )
            else:
                data = pg_connector.select_records_with_filter(table_name=table)
            log.info("Data size retrieved for table %s :", len(data))
            tenant_specific_data[table] = pd.DataFrame(data)
        pg_connector.close_connection()
        extracted_data[tenant_id] = tenant_specific_data

@log_time
def retrieve_common_reference_data(tenant_ids, extracted_data):
    """
    Retrieves common reference data from the database for all tenants in the provided
    `tenant_ids` list. The common data is retrieved from predefined common reference tables.

    Args:
        tenant_ids (list): A list of tenant IDs for which the common reference data will be added.
        extracted_data (dict): A dictionary containing tenant-specific data, which will
        be updated with common reference data for each tenant.
          The structure is {tenant_id: {table_name: data}}.

    Returns:
        None: The method modifies the `extracted_data` dictionary in place by adding
        common reference data to each tenant's data.
    """
    log.info("Retrieving common reference data")
    pg_connector = PGConnector(tenant_id=COMMON_DB_USER, cursor_type="real_dict")

    common_reference_tables = negotiation_conf["reference_tables"]["common"].values()
    log.info("Common reference tables: %s", common_reference_tables)
    for table in common_reference_tables:
        data = pg_connector.select_records_with_filter(table_name=f"common.{table}")
        log.info("Data size retrieved for table %s :", len(data))
        for tenant_id in tenant_ids:
            tenant_specific_data = extracted_data[tenant_id]
            tenant_specific_data[table] = pd.DataFrame(data)

    pg_connector.close_connection()
