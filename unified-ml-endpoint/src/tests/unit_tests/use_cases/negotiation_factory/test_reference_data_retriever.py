import os
from unittest.mock import MagicMock, patch

import pandas as pd

from ada.use_cases.negotiation_factory.reference_data_retriever import (
    read_reference_data,
)

os.environ["LOCAL_DB_MODE"] = "0"
os.environ["AZURE_DATABASE_ACCESS"] = "1"


table_data_dict_for_common = {
    "common.negotiation_references": [{"dummy": 1}],
    "common.negotiation_relationship_details": [{"dummy": 2}],
    "common.market_approach_strategy": [{"dummy": 3}],
    "common.email_references": [{"dummy": 4}],
    "common.negotiation_strategy_details": [{"dummy": 5}],
    "common.carrots_and_sticks": [{"dummy": 6}],
}


def select_records_with_filter_mock_for_common(table_name: str):
    if table_name in table_data_dict_for_common.keys():
        return (table_data_dict_for_common)[table_name]


tenant_1 = "test-tenant-1"
tenant_2 = "test-tenant-2"


@patch("ada.use_cases.negotiation_factory.reference_data_retriever.get_secrets")
@patch("ada.use_cases.negotiation_factory.reference_data_retriever.PGConnector")
def test_should_fetch_tenant_specific_and_common_data_fro_the_reference_tables(
    pg_conn_mock_class,
    get_secrets_mock,
):
    pg_connector_instance_mock_for_tenant1 = MagicMock()
    pg_connector_instance_mock_for_tenant2 = MagicMock()
    pg_connector_instance_mock_for_common = MagicMock()
    tenant_mock_dictionary = {
        tenant_1: pg_connector_instance_mock_for_tenant1,
        tenant_2: pg_connector_instance_mock_for_tenant2,
        "common-db-user": pg_connector_instance_mock_for_common,
    }
    nego_strategy_tenant1 = [{"dummy": 6}]
    nego_strategy_tenant2 = [{"dummy": 7}]
    pg_connector_instance_mock_for_tenant1.select_records_with_filter.return_value = (
        nego_strategy_tenant1
    )
    pg_connector_instance_mock_for_tenant2.select_records_with_filter.return_value = (
        nego_strategy_tenant2
    )
    pg_connector_instance_mock_for_common.select_records_with_filter.side_effect = (
        select_records_with_filter_mock_for_common
    )

    def tenant_selector(tenant_id, cursor_type):
        return tenant_mock_dictionary[tenant_id]

    pg_conn_mock_class.side_effect = tenant_selector

    get_secrets_mock.return_value = {"atlas_tenant_ids": f"{tenant_1},{tenant_2}"}

    reference_data = read_reference_data()

    assert_db_call_for_tenant(pg_connector_instance_mock_for_tenant1)
    assert_db_call_for_tenant(pg_connector_instance_mock_for_tenant2)
    assert_db_call_for_common(pg_connector_instance_mock_for_common)

    assert_reference_data(tenant_1, reference_data)
    assert_reference_data(tenant_2, reference_data)


def assert_reference_data(tenant_id, reference_data):
    assert reference_data[tenant_id]["negotiation_references"].equals(
        pd.DataFrame(table_data_dict_for_common["common.negotiation_references"]),
    )
    assert reference_data[tenant_id]["negotiation_relationship_details"].equals(
        pd.DataFrame(table_data_dict_for_common["common.negotiation_relationship_details"]),
    )
    assert reference_data[tenant_id]["market_approach_strategy"].equals(
        pd.DataFrame(table_data_dict_for_common["common.market_approach_strategy"]),
    )
    assert reference_data[tenant_id]["email_references"].equals(
        pd.DataFrame(table_data_dict_for_common["common.email_references"]),
    )

    assert reference_data[tenant_id]["negotiation_strategy_details"].equals(
        pd.DataFrame(table_data_dict_for_common["common.negotiation_strategy_details"]),
    )


def assert_db_call_for_tenant(pg_connector_instance_mock):
    assert (
        pg_connector_instance_mock.select_records_with_filter.call_count == 0
    )  # As tone and tactics uses a different method to fetch its data

    # assert (
    #     pg_connector_instance_mock.select_records_with_filter.call_args_list[0][1]["table_name"]
    #     == "negotiation_strategy_details"
    # )  # For tenant1


def assert_db_call_for_common(pg_connector_instance_mock_for_common):
    assert pg_connector_instance_mock_for_common.select_records_with_filter.call_count == 6
    # common data
    assert (
        pg_connector_instance_mock_for_common.select_records_with_filter.call_args_list[0][1][
            "table_name"
        ]
        == "common.negotiation_references"
    )
    assert (
        pg_connector_instance_mock_for_common.select_records_with_filter.call_args_list[1][1][
            "table_name"
        ]
        == "common.negotiation_relationship_details"
    )
    assert (
        pg_connector_instance_mock_for_common.select_records_with_filter.call_args_list[2][1][
            "table_name"
        ]
        == "common.market_approach_strategy"
    )
    assert (
        pg_connector_instance_mock_for_common.select_records_with_filter.call_args_list[3][1][
            "table_name"
        ]
        == "common.email_references"
    )

    assert (
        pg_connector_instance_mock_for_common.select_records_with_filter.call_args_list[4][1][
            "table_name"
        ]
        == "common.negotiation_strategy_details"
    )

    assert (
        pg_connector_instance_mock_for_common.select_records_with_filter.call_args_list[5][1][
            "table_name"
        ]
        == "common.carrots_and_sticks"
    )
