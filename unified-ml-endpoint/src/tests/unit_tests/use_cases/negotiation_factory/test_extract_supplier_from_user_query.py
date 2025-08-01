import re
from unittest.mock import call, patch

import numpy as np
import pytest

from ada.use_cases.negotiation_factory.exception import (
    NegotiationFactoryQueryException,
    NegotiationFactoryUserException,
)
from ada.use_cases.negotiation_factory.extract_supplier_from_user_query import (
    get_supplier_data,
    get_supplier_data_based_on_user_query,
    get_supplier_profiles,
    negotiation_tables,
)
from tests.unit_tests.use_cases.negotiation_factory.test_negotiation_factory_utils import (  # noqa: F401
    insight_data_mock,
    supplier_data_mock,
)


@pytest.fixture
def pg_connector_mock():
    with patch(
        "ada.use_cases.negotiation_factory.extract_supplier_from_user_query.PGConnector",
    ) as mock_obj:
        yield mock_obj.return_value


@pytest.fixture
def all_supplier_data_mock():
    return (
        {
            "supplier_name": "SKF FRANCE",
            "spend": 6770616.584,
            "spend_last_year": 4166189.76,
            "percentage_spend_contribution": 3.22,
            "single_source_spend": 6770616.584,
            "spend_no_po_ytd": 0.0,
            "payment_term_avg": 5,
            "currency_symbol": "EUR",
            "period": [2023],
        },
        {
            "supplier_name": "SKF BV",
            "spend": 33993184.36,
            "spend_last_year": 30197575.85,
            "percentage_spend_contribution": 16.2,
            "single_source_spend": 33993184.4,
            "spend_no_po_ytd": 3399318.46,
            "payment_term_avg": 5,
            "currency_symbol": "EUR",
            "period": [2023],
        },
        {
            "supplier_name": "GBM SARL",
            "spend": 19673657.45,
            "spend_last_year": 20802522.74,
            "percentage_spend_contribution": 9.3,
            "single_source_spend": 19673657.5,
            "spend_no_po_ytd": 2522.7,
            "payment_term_avg": 5,
            "currency_symbol": "EUR",
            "period": [2023],
        },
        {
            "supplier_name": "Havells",
            "spend": 1321.99,
            "spend_last_year": 1000.0,
            "percentage_spend_contribution": 13.0,
            "spend_no_po_ytd": 3399318.5,
            "single_source_spend": 193657.5,
            "payment_term_avg": 5,
            "currency_symbol": "EUR",
            "period": [2023],
        },
    )


def data_for_each_script_type():
    return {
        "highest_single_spend": r"The top \d+ supplier contributes to \d+\.\d{1}% total single source spend and see below the spend break up:",  # noqa: E501
        "top_supplier": r"The top \d+ supplier contributes to \d+\.\d{1}% total spend and see below the spend break up:",
        "largest_gap": r"The top \d+ supplier contributes to \d+\.\d{1}% total spend and see below the spend break up:",
        "spend_without_po": r"The top \d+ supplier contributes to \d+\.\d{1}% total spend without PO and see below the spend break up:",  # noqa: E501
        "top_suppliers_tail_spend": r"The top \d+ supplier contributes to \d+\.\d{1}% total spend and see below the spend break up:",  # noqa: E501
    }


@pytest.fixture
def mock_get_supplier_data():
    """Fixture for patching get_supplier_data function."""
    with patch(
        "ada.use_cases.negotiation_factory.extract_supplier_from_user_query.get_supplier_data",
    ) as mock:
        yield mock


@pytest.mark.parametrize(
    "user_query, script_type, value",
    [
        ("tail suppliers", "top_suppliers_tail_spend", "5"),
        ("suppliers with largest in YOY spend evolution", "largest_gap", "5"),
        ("2 suppliers with missing PO spend", "spend_without_po", "2"),
        ("4 suppliers with largest in YOY spend evolution", "largest_gap", "4"),
        ("top 6 suppliers", "top_supplier", "6"),
    ],
)
def test_patterns(
    pg_connector_mock,
    mock_get_supplier_data,
    all_supplier_data_mock,
    user_query,
    script_type,
    value,
):
    category = "Bearings"
    mock_get_supplier_data.return_value = (all_supplier_data_mock, "some_message")
    result = get_supplier_data_based_on_user_query(pg_connector_mock, category, user_query)
    assert result == (all_supplier_data_mock, "some_message")
    mock_get_supplier_data.assert_called_once_with(pg_connector_mock, category, script_type, value)


def test_no_match(pg_connector_mock):
    category = "Bearings"
    user_query = "some unsupported query"
    with pytest.raises(NegotiationFactoryQueryException):
        get_supplier_data_based_on_user_query(pg_connector_mock, category, user_query)


@pytest.mark.parametrize(
    "script_type, message_pattern",
    [(key, value) for key, value in data_for_each_script_type().items()],
)
def test_get_supplier_data(
    pg_connector_mock,
    all_supplier_data_mock,
    script_type,
    message_pattern,
):
    category = "Bearings"
    value = 5
    mock_total = [{"total_spend_no_po_ytd": 120, "total_single_source_spend": 67706165.8}]
    pg_connector_mock.select_records_with_filter.side_effect = [
        all_supplier_data_mock,
        mock_total,
    ]
    pg_connector_mock.get_tail_spend_supplier_data.return_value = all_supplier_data_mock[3:]
    supplier_data, message = get_supplier_data(pg_connector_mock, category, script_type, value)

    assert not supplier_data.empty
    assert "supplier_name" in supplier_data.columns
    pattern = re.compile(message_pattern)
    assert pattern.match(message)


def test_get_supplier_data_no_data(pg_connector_mock):
    category = "Bearings"
    script_type = "top_supplier"
    value = 5

    pg_connector_mock.select_records_with_filter.return_value = []

    with pytest.raises(NegotiationFactoryQueryException):
        get_supplier_data(pg_connector_mock, category, script_type, value)


def test_get_supplier_data_invalid_request(pg_connector_mock):
    category = "Bearings"
    script_type = "invalid_script_type"
    value = 5

    with pytest.raises(NegotiationFactoryUserException):
        get_supplier_data(pg_connector_mock, category, script_type, value)


def test_get_supplier_profiles(pg_connector_mock, supplier_data_mock):  # noqa: F811
    category = "test_category"
    supplier_names = ["SKF FRANCE", "SKF BV"]
    supplier_name, _, supplier_profile_form_db, supplier_profile, _ = supplier_data_mock
    supplier_profile_form_db.pop("insights")
    supplier_profile_form_db.pop("objectives")

    pg_connector_mock.select_records_with_filter.return_value = [supplier_profile_form_db]
    formatted_supplier_names = ", ".join(f"'{name}'" for name in supplier_names)
    pg_connector_mock.get_condition_string.return_value = (
        f"supplier_name IN ({formatted_supplier_names})"
    )

    actual_supplier_profile = get_supplier_profiles(
        pg_connector_mock,
        category,
        np.array(supplier_names),
    )
    expected_supplier_profile = supplier_profile

    pg_connector_mock.select_records_with_filter.assert_has_calls(
        [
            call(
                table_name=negotiation_tables["supplier_details"],
                filter_condition=f"""category_name = '{category}' AND period = (SELECT MAX(period) """
                f"""FROM {negotiation_tables["supplier_details"]}) AND """
                f"""supplier_name IN ({formatted_supplier_names})""",
            ),
        ],
    )
    pg_connector_mock.get_condition_string.assert_called_once_with(
        ("supplier_name", "in", supplier_names),
    )
    assert actual_supplier_profile.to_dict(orient="records")[0] == expected_supplier_profile
