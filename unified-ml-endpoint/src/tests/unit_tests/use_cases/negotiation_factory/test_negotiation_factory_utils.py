from __future__ import annotations

import json
from unittest.mock import ANY, MagicMock, call, patch

import pandas as pd
import pytest

from ada.use_cases.negotiation_factory.exception import (
    NegotiationFactoryException,
    NegotiationFactoryUserException,
)
from ada.use_cases.negotiation_factory.negotiation_factory_utils import (
    convert_qna_to_string,
    convert_to_response_format,
    create_supplier_profile,
    enrich_supplier_profile,
    ensure_key_exist,
    extract_model_context,
    extract_objective_description,
    extract_qa_context,
    extract_supplier_details,
    extract_supplier_name_from_user_query,
    filter_insight_by_reinforcement,
    get_modified_insights,
    get_negotiation_model_context,
    get_negotiation_strategy_data,
    get_samples,
    get_supplier_profile,
    get_supplier_profile_insights_objectives,
    get_workflow_suggested_prompts,
    json_regex,
    update_negotiation_details,
)
from ada.utils.config.config_loader import read_config

negotiation_conf = read_config("use-cases.yml")["negotiation_factory"]


@pytest.fixture
def insight_data_mock():
    insight_db_data = [
        {
            "insight_id": "I1",
            "label": "label_1",
            "objective": "objective_1",
            "reinforcements": ["reinforcements_1", "reinforcements_2"],
            "analytics_name": "test analytics 1",
        },
        {
            "insight_id": "I2",
            "label": "label_2",
            "objective": "objective_2",
            "reinforcements": ["reinforcements_1", "reinforcements_3"],
            "analytics_name": "test analytics 1",
        },
        {
            "insight_id": "I3",
            "label": "label_3",
            "objective": "objective_1",
            "reinforcements": ["reinforcements_4", "reinforcements_3"],
            "analytics_name": "test analytics 2",
        },
    ]
    modified_insights = [
        {
            "id": "I1",
            "insight": "label_1",
            "insight_objective": "objective_1",
            "insight_reinforcements": ["reinforcements_1", "reinforcements_2"],
            "analytics_name": "test analytics 1",
            "list_of_skus": [],
        },
        {
            "id": "I2",
            "insight": "label_2",
            "insight_objective": "objective_2",
            "insight_reinforcements": ["reinforcements_1", "reinforcements_3"],
            "analytics_name": "test analytics 1",
            "list_of_skus": [],
        },
        {
            "id": "I3",
            "insight": "label_3",
            "insight_objective": "objective_1",
            "insight_reinforcements": ["reinforcements_4", "reinforcements_3"],
            "analytics_name": "test analytics 2",
            "list_of_skus": [],
        },
    ]
    return insight_db_data, modified_insights


@pytest.fixture
def supplier_data_mock(insight_data_mock):
    supplier_name = "dummy_supplier_name"
    supplier_relationship = "dummy relationship"
    insight_db_data, _ = insight_data_mock
    supplier_profile_from_db = {
        "category_name": "test_category",
        "supplier_name": supplier_name,
        "sku_list": ["sku_1", "sku_2", "sku_3", "sku_4", "sku_5", "sku_6"],
        "spend_ytd": 1321.987,
        "spend_last_year": 1000.0,
        "percentage_spend_across_category_ytd": 13.0,
        "supplier_relationship": supplier_relationship,
        "supplier_name_embedding": "mocked_embedding",
        "cosine_distance": 0,
        "number_of_supplier_in_category": 500,
        "sku_list_name": ["sku_1", "sku_2", "sku_3", "sku_4", "sku_5", "sku_6"],
        "single_source_spend_ytd": 1000,
        "spend_no_po_ytd": 500,
        "insights": insight_db_data,
        "objectives": insight_db_data,
        "reporting_currency": "€",
        "payment_term_avg": 5,
        "period": [2022, 2023],
    }
    supplier_profile = {
        "category_name": "test_category",
        "supplier_name": supplier_name,
        "number_of_sku": 6,
        "sku_list": ["sku_1", "sku_2", "sku_3"],
        "spend_ytd": 1321.99,
        "spend_last_year": 1000.0,
        "currency_symbol": "€",
        "currency_position": "prefix",
        "percentage_spend_across_category_ytd": 13.0,
        "number_of_supplier_in_category": 500,
        "supplier_relationship": supplier_relationship,
        "single_source_spend_ytd": 1000,
        "spend_no_po_ytd": 500,
        "percentage_spend_which_is_single_sourced": 0.8,
        "percentage_spend_without_po": 0.4,
        "target_savings": 0,
        "payment_term_avg": 5,
        "period": [2022, 2023],
    }
    user_query = f"start Negotiation with {supplier_name}"
    return (
        supplier_name,
        supplier_relationship,
        supplier_profile_from_db,
        supplier_profile,
        user_query,
    )


@pytest.fixture
def all_supplier_data_db_mock():
    all_supplier_data = [
        {
            "supplier_name": "SKF FRANCE",
            "category_name": "Bearings",
            "spend_ytd": 6770616.584,
            "spend_last_year": 4166189.76,
            "cosine_distance": 0.07,
            "sku_list": ["sku_1", "sku_2", "sku_3", "sku_4", "sku_5", "sku_6"],
            "sku_list_name": ["sku_1", "sku_2", "sku_3", "sku_4", "sku_5", "sku_6"],
            "percentage_spend_across_category_ytd": 3.22,
            "percentage_spend_across_category_last_year": 1.59,
            "supplier_relationship": "core",
            "supplier_name_embedding": "mocked_embedding",
            "single_source_spend_ytd": 6770616.584,
            "spend_no_po_ytd": 0.0,
            "payment_term_avg": 5,
            "reporting_currency": "€",
        },
        {
            "supplier_name": "SKF BV",
            "category_name": "Bearings",
            "spend_ytd": 33993184.36,
            "spend_last_year": 30197575.85,
            "sku_list": ["sku_1", "sku_2", "sku_3", "sku_4", "sku_5", "sku_6"],
            "sku_list_name": ["sku_1", "sku_2", "sku_3", "sku_4", "sku_5", "sku_6"],
            "percentage_spend_across_category_ytd": 16.2,
            "cosine_distance": 0.06,
            "percentage_spend_across_category_last_year": 11.5,
            "supplier_relationship": "core",
            "supplier_name_embedding": "mocked_embedding",
            "single_source_spend_ytd": 33993184.36,
            "spend_no_po_ytd": 33993184.36,
            "payment_term_avg": 4,
            "reporting_currency": "€",
        },
        {
            "supplier_name": "GBM SARL",
            "category_name": "Bearings",
            "spend_ytd": 19673657.45,
            "spend_last_year": 20802522.74,
            "sku_list": ["sku_1", "sku_2", "sku_3", "sku_4", "sku_5", "sku_6"],
            "sku_list_name": ["sku_1", "sku_2", "sku_3", "sku_4", "sku_5", "sku_6"],
            "percentage_spend_across_category_ytd": 9.3,
            "percentage_spend_across_category_last_year": 7.8,
            "supplier_relationship": "core",
            "supplier_name_embedding": "mocked_embedding",
            "cosine_distance": 0.8,
            "single_source_spend_ytd": 19673657.45,
            "spend_no_po_ytd": 0.0,
            "payment_term_avg": 5,
            "reporting_currency": "€",
        },
        {
            "supplier_name": "Havells",
            "category_name": "Bearings",
            "sku_list": ["sku_1", "sku_2", "sku_3", "sku_4", "sku_5", "sku_6"],
            "spend_ytd": 1321.987,
            "spend_last_year": 1000.0,
            "percentage_spend_across_category_ytd": 13.0,
            "supplier_relationship": "leverage",
            "supplier_name_embedding": "mocked_embedding",
            "cosine_distance": 0.5,
            "number_of_supplier_in_category": 500,
            "sku_list_name": ["sku_1", "sku_2", "sku_3", "sku_4", "sku_5", "sku_6"],
            "payment_term_avg": 5,
            "reporting_currency": "€",
        },
    ]
    return all_supplier_data


@pytest.fixture
def negotiation_strategy_data_mock():
    data = {
        "category": "dummy category",
        "category_positioning": "leverage",
        "pricing_methodology": ["pr method 1", "pr method 2", "pr method 3"],
        "contract_methodology": ["ct method 1", "ct method 2", "ct method 3"],
    }
    return data


@pytest.fixture
def pg_connector_mock():
    with patch(
        "ada.use_cases.negotiation_factory.negotiation_factory_utils.PGConnector",
    ) as mock_obj:
        yield mock_obj.return_value


@pytest.fixture
def reference_data():
    relationship_data = {
        "relationship": ["test_relationship"],
        "expert_input": ["test_expert_input"],
        "general_information": ["test data"],
        "argument_strategy": ["test argument strategy"],
        "negotiation_strategy": ["test negotiation strategy"],
    }
    ref_data = {
        "l1_objective": ["test_objective"],
        "l1_objective_description": ["test description"],
        "samples": [
            [
                {
                    "argument": "test argument",
                    "rebuttal": "test rebuttal",
                    "counter_argument": "test counter argument",
                },
            ],
        ],
    }
    strategy_data = {
        "category_name": ["test_category"],
        "is_auctionable": [True],
        "category_positioning": ["leverage"],
        "pricing_methodology": [["Market based pricing", "Index based pricing", "Cost plus model"]],
        "contract_methodology": [
            ["Framework agreement approach", "Long term contract", "Indefinite delivery"],
        ],
    }
    data = {
        "negotiation_relationship_details": pd.DataFrame(relationship_data),
        "negotiation_references": pd.DataFrame(ref_data),
        "negotiation_strategy_details": pd.DataFrame(strategy_data),
    }
    return data


@patch(
    "ada.use_cases.negotiation_factory.negotiation_factory_utils.generate_chat_response_with_chain",
)
def test_extract_supplier_name_from_user_query(chat_response_mock, supplier_data_mock):
    supplier_name, _, _, _, user_query = supplier_data_mock

    chat_response_mock.return_value = json.dumps(
        {"supplier_name": supplier_name},
    )

    actual_output = extract_supplier_name_from_user_query(user_query)
    assert actual_output == supplier_name


@patch(
    "ada.use_cases.negotiation_factory.negotiation_factory_utils.generate_chat_response_with_chain",
)
def test_extract_supplier_name_from_user_query_without_supplier_name(chat_response_mock):
    user_query = "Start negotiation"
    chat_response_mock.return_value = json.dumps({"supplier_name": ""})

    with pytest.raises(NegotiationFactoryUserException) as negotiation_exception:
        extract_supplier_name_from_user_query(user_query)
    assert (
        str(
            negotiation_exception.value,
        )
        == "Before we proceed with negotiations, please provide the name of the supplier"
    )


# Place holder : negotiation_objective_from_user_query


@patch(
    "ada.use_cases.negotiation_factory.negotiation_factory_utils.generate_embeddings_from_string",
)
def test_create_supplier_profile(
    embeddings_from_string_mock,
    pg_connector_mock,
    supplier_data_mock,
    insight_data_mock,
):
    category = "test_category"
    supplier_name, _, supplier_profile_form_db, supplier_profile, _ = supplier_data_mock
    pg_connector_mock.search_by_vector_similarity.return_value = [supplier_profile_form_db]

    embeddings_from_string_mock.return_value = "mocked_embedding"
    expected_supplier_profile = supplier_profile
    _, expected_insights = insight_data_mock
    supplier_details = extract_supplier_details(category, pg_connector_mock, supplier_name)
    actual_supplier_profile, actual_insights, _ = create_supplier_profile(
        supplier_details,
        category,
        supplier_name,
    )

    condition_str = (
        f"category_name = '{category}' AND period = (SELECT MAX(period)"
        f""" FROM {negotiation_conf["tables"]["supplier_details"]})"""
    )

    pg_connector_mock.search_by_vector_similarity.assert_has_calls(
        [
            call(
                table_name=negotiation_conf["tables"]["supplier_details"],
                query_emb="mocked_embedding",
                emb_column_name="supplier_name_embedding",
                num_records=negotiation_conf["num_similar_suppliers"],
                conditions=condition_str,
            ),
        ],
    ),
    assert expected_supplier_profile == actual_supplier_profile.to_dict()
    assert expected_insights == actual_insights


def test_enrich_supplier_profile(supplier_data_mock):
    supplier_name, _, supplier_profile_form_db, expected_supplier_profile, _ = supplier_data_mock
    actual_supplier_profile = enrich_supplier_profile(
        pd.DataFrame([supplier_profile_form_db]),
    )
    actual_supplier_profile.pop("insights")
    actual_supplier_profile.pop("objectives")
    assert actual_supplier_profile.to_dict() == expected_supplier_profile


@patch(
    "ada.use_cases.negotiation_factory.negotiation_factory_utils.generate_embeddings_from_string",
)
def test_extract_supplier_details(
    embeddings_from_string_mock,
    pg_connector_mock,
    supplier_data_mock,
):
    category = "test_category"
    supplier_name, _, supplier_profile_form_db, supplier_profile, _ = supplier_data_mock
    pg_connector_mock.search_by_vector_similarity.return_value = (supplier_profile_form_db,)

    embeddings_from_string_mock.return_value = "mocked_embedding"
    expected_supplier_profile = supplier_profile_form_db

    actual_supplier_details = extract_supplier_details(category, pg_connector_mock, supplier_name)
    print(actual_supplier_details.to_json(orient="records"))
    print(actual_supplier_details.columns)

    condition_str = (
        f"category_name = '{category}' AND period = (SELECT MAX(period)"
        f""" FROM {negotiation_conf["tables"]["supplier_details"]})"""
    )

    pg_connector_mock.search_by_vector_similarity.assert_has_calls(
        [
            call(
                table_name=negotiation_conf["tables"]["supplier_details"],
                query_emb="mocked_embedding",
                emb_column_name="supplier_name_embedding",
                num_records=negotiation_conf["num_similar_suppliers"],
                conditions=condition_str,
            ),
        ],
    ),
    expected_columns = [
        "category_name",
        "supplier_name",
        "sku_list",
        "spend_ytd",
        "spend_last_year",
        "percentage_spend_across_category_ytd",
        "supplier_relationship",
        "supplier_name_embedding",
        "cosine_distance",
        "number_of_supplier_in_category",
        "sku_list_name",
        "single_source_spend_ytd",
        "spend_no_po_ytd",
        "insights",
        "objectives",
        "reporting_currency",
        "payment_term_avg",
        "period",
    ]
    assert all(expected_supplier_profile == actual_supplier_details)
    assert set(expected_columns) == set(actual_supplier_details.columns)


@patch(
    "ada.use_cases.negotiation_factory.negotiation_factory_utils.generate_embeddings_from_string",
)
def test_extract_supplier_details_without_supplier_data_in_db(
    embeddings_from_string_mock,
    pg_connector_mock,
):
    category = "test_category"
    supplier_name = "unknown_supplier_name"
    embeddings_from_string_mock.return_value = "mocked_embedding"

    pg_connector_mock.search_by_vector_similarity.return_value = []

    with pytest.raises(NegotiationFactoryUserException) as negotiation_exception:
        extract_supplier_details(category, pg_connector_mock, supplier_name)

    assert str(negotiation_exception.value) == (
        f"Apologies, but the data for supplier {supplier_name} in category {category} "
        "is not available at the moment. If you'd like, you can check for other suppliers"
    )

    condition_str = (
        f"category_name = '{category}' AND period = (SELECT MAX(period)"
        f""" FROM {negotiation_conf["tables"]["supplier_details"]})"""
    )

    pg_connector_mock.search_by_vector_similarity.assert_has_calls(
        [
            call(
                table_name=negotiation_conf["tables"]["supplier_details"],
                query_emb="mocked_embedding",
                emb_column_name="supplier_name_embedding",
                num_records=negotiation_conf["num_similar_suppliers"],
                conditions=condition_str,
            ),
        ],
    ),


@patch(
    "ada.use_cases.negotiation_factory.negotiation_factory_utils.generate_embeddings_from_string",
)
def test_create_supplier_profile_with_approximate_name(
    embeddings_from_string_mock,
    pg_connector_mock,
    all_supplier_data_db_mock,
):
    category = "test_category"
    supplier_name = "SKF"
    embeddings_from_string_mock.return_value = "mocked_embedding"

    pg_connector_mock.search_by_vector_similarity.return_value = all_supplier_data_db_mock

    with pytest.raises(NegotiationFactoryUserException) as negotiation_supplier_not_exact_exception:
        supplier_details = extract_supplier_details(category, pg_connector_mock, supplier_name)
        create_supplier_profile(supplier_details, category, supplier_name)

    assert str(
        negotiation_supplier_not_exact_exception.value,
    ) == (
        f"('We could not find the exact SKF in {category}, "
        "is the supplier you are looking for one of these?', "
        "[{'prompt': 'SKF FRANCE', 'intent': 'supplier_name'},"
        " {'prompt': 'SKF BV', 'intent': 'supplier_name'}])"
    )

    condition_str = (
        f"category_name = '{category}' AND period = (SELECT MAX(period)"
        f""" FROM {negotiation_conf["tables"]["supplier_details"]})"""
    )

    pg_connector_mock.search_by_vector_similarity.assert_has_calls(
        [
            call(
                table_name=negotiation_conf["tables"]["supplier_details"],
                query_emb="mocked_embedding",
                emb_column_name="supplier_name_embedding",
                num_records=negotiation_conf["num_similar_suppliers"],
                conditions=condition_str,
            ),
        ],
    ),


@patch("ada.use_cases.negotiation_factory.negotiation_factory_utils.extract_supplier_details")
@patch("ada.use_cases.negotiation_factory.negotiation_factory_utils.create_supplier_profile")
def test_get_supplier_profile_insights_objectives(
    create_supplier_profile_mock,
    extract_supplier_details_mock,
    pg_connector_mock,
    supplier_data_mock,
):
    category = "test_category"
    supplier_name, _, _, supplier_profile, user_query = supplier_data_mock
    pinned_elements = {"supplier_profile": supplier_profile}

    insights = MagicMock()
    objectives = MagicMock()
    supplier_details = extract_supplier_details_mock(category, pg_connector_mock, supplier_name)
    create_supplier_profile_mock.return_value = (pd.Series(supplier_profile), insights, objectives)

    actual_data = get_supplier_profile_insights_objectives(
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
    )
    assert actual_data == (supplier_name, supplier_profile, insights, objectives)
    create_supplier_profile_mock.assert_called_once_with(supplier_details, category, supplier_name)


def test_get_supplier_profile_when_available_in_pinned_elements(
    pg_connector_mock,
    supplier_data_mock,
):
    category = "test_category"
    supplier_name, _, _, supplier_profile, user_query = supplier_data_mock
    pinned_elements = {"supplier_profile": supplier_profile}
    actual_data = get_supplier_profile(
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
    )
    assert (supplier_name, supplier_profile) == actual_data


@patch(
    "ada.use_cases.negotiation_factory.negotiation_factory_utils.extract_supplier_name_from_user_query",
)
def test_get_supplier_profile_when_not_available_in_pinned_elements_and_element_required(
    extract_supplier_mock,
    pg_connector_mock,
):
    category = "test_category"
    user_query = "Start Negotiation"
    pinned_elements = {}

    exception_message = "Dummy exception message"
    extract_supplier_mock.side_effect = NegotiationFactoryUserException(
        exception_message,
    )

    with pytest.raises(NegotiationFactoryUserException) as negotiation_exception:
        get_supplier_profile(
            pg_connector_mock,
            category,
            user_query,
            pinned_elements,
        )

    assert str(negotiation_exception.value) == exception_message


@patch(
    "ada.use_cases.negotiation_factory.negotiation_factory_utils.extract_supplier_name_from_user_query",
)
def test_get_supplier_profile_when_not_available_in_pinned_elements_and_element_not_required(
    extract_supplier_mock,
    pg_connector_mock,
):
    category = "test_category"
    user_query = "Start Negotiation"
    pinned_elements = {}

    exception_message = "Dummy exception message"
    extract_supplier_mock.side_effect = NegotiationFactoryUserException(
        exception_message,
    )

    actual_data = get_supplier_profile(
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
        elements_required=False,
    )

    assert ("", {}) == actual_data


@patch(
    "ada.use_cases.negotiation_factory.negotiation_factory_utils.get_supplier_profile_insights_objectives",
)
def test_get_supplier_profile_when_supplier_details_available_in_user_query(
    get_supplier_profile_insights_objectives_mock,
    pg_connector_mock,
    supplier_data_mock,
):
    category = "test_category"
    supplier_name, _, _, supplier_profile, user_query = supplier_data_mock
    pinned_elements = {}

    get_supplier_profile_insights_objectives_mock.return_value = (
        supplier_name,
        supplier_profile,
        MagicMock(),
        MagicMock(),
    )

    actual_data = get_supplier_profile(
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
    )

    assert (supplier_name, supplier_profile) == actual_data
    get_supplier_profile_insights_objectives_mock.assert_called_once_with(
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
    )


def test_extract_objective_description(reference_data):
    expected_data = "test description"
    actual_data = extract_objective_description(
        reference_data=reference_data,
        objective="test_objective",
    )

    assert expected_data == actual_data


def test_extract_objective_description_when_description_not_available(reference_data):
    actual_data = extract_objective_description(
        reference_data=reference_data,
        objective="unknown_objective",
    )

    assert actual_data is None


def test_get_samples(reference_data):
    objective = ["test_objective"]
    expected_data = [
        {"example": "test argument"},
        {"example": "test argument"},
        {"example": "test argument"},
    ]
    actual_data = get_samples(
        reference_data=reference_data,
        objective_types=objective,
        generation_type="arguments",
    )
    assert actual_data == expected_data


def test_get_samples_when_no_data_available(reference_data):
    objective = ["unknown_objective"]

    expected_data = [{"example": ""}]
    actual_data = get_samples(
        reference_data=reference_data,
        objective_types=objective,
        generation_type="arguments",
    )
    assert actual_data == expected_data


def test_update_negotiation_details():
    generated_details = ["data_3", "data_4", "data_5"]

    expected_data = [
        {"id": ANY, "details": "data_3", "raw": "data_3"},
        {"id": ANY, "details": "data_4", "raw": "data_4"},
        {"id": ANY, "details": "data_5", "raw": "data_5"},
    ]

    actual_data = update_negotiation_details(
        generated_details,
    )

    assert actual_data == expected_data


def test_get_modified_insights(insight_data_mock):
    insight_data, modified_insights = insight_data_mock

    expected_output = modified_insights
    actual_output = get_modified_insights(insight_data)

    assert expected_output == actual_output


def test_filter_insight_by_reinforcement():
    insights = [
        {
            "id": "I1",
            "insight": "label_1",
            "insight_objective": "objective_1",
            "insight_reinforcements": ["reinforcements_1", "reinforcements_2"],
            "list_of_skus": [],
        },
        {
            "id": "I2",
            "insight": "label_2",
            "insight_objective": "objective_2",
            "insight_reinforcements": ["reinforcements_1", "reinforcements_3"],
            "list_of_skus": [],
        },
        {
            "id": "I3",
            "insight": "label_3",
            "insight_objective": "objective_1",
            "insight_reinforcements": ["reinforcements_4", "reinforcements_3"],
            "list_of_skus": [],
        },
    ]
    reinforcement = "reinforcements_3"

    expected_data = [
        {
            "id": "I2",
            "insight": "label_2",
            "insight_objective": "objective_2",
            "insight_reinforcements": ["reinforcements_1", "reinforcements_3"],
            "list_of_skus": [],
        },
        {
            "id": "I3",
            "insight": "label_3",
            "insight_objective": "objective_1",
            "insight_reinforcements": ["reinforcements_4", "reinforcements_3"],
            "list_of_skus": [],
        },
    ]
    actual_data = filter_insight_by_reinforcement(insights, reinforcement)

    assert expected_data == actual_data


def test_ensure_key_exist():
    required_key = "key_1"
    source_dict = {"key_1": "data_1"}

    assert ensure_key_exist(required_key, source_dict) is None


def test_ensure_key_exist_when_need_to_return_element():
    required_key = "key_1"
    source_dict = {"key_1": "data_1"}

    assert (
        ensure_key_exist(
            required_key,
            source_dict,
            return_element=True,
        )
        == "data_1"
    )


def test_ensure_key_exist_when_key_does_not_exist():
    required_key = "key_1"
    source_dict = {"key_2": "data_1"}

    with pytest.raises(NegotiationFactoryException) as negotiation_exception:
        ensure_key_exist(required_key, source_dict)

    assert (
        str(
            negotiation_exception.value,
        )
        == f"{required_key} is missing in the Payload"
    )


def test_ensure_key_exist_when_key_does_not_exist_but_cannot_inform_user():
    required_key = "key_1"
    source_dict = {"key_2": "data_1"}

    with pytest.raises(NegotiationFactoryUserException) as negotiation_exception:
        ensure_key_exist(required_key, source_dict, can_inform_user=True)

    assert (
        str(
            negotiation_exception.value,
        )
        == f"{required_key} is Not available."
    )


def test_convert_qna_to_string():
    qna_list = [[{"question": "dummy question.", "answer": "dummy answer"}]]
    expected_output = "answer: dummy answer question: dummy question."

    actual_output = convert_qna_to_string(qna_list)
    assert expected_output == actual_output


def test_extract_qa_context(pg_connector_mock):
    category_name = "test_category"
    supplier_name = "test supplier name"
    sku_list = ["test sku 1", "test sku 2"]

    data = (
        {
            "category_name": category_name,
            "supplier_name": None,
            "sku_id": None,
            "qna": [{"question": "dummy category question.", "answer": "dummy category answer"}],
        },
        {
            "category_name": category_name,
            "supplier_name": supplier_name,
            "sku_id": None,
            "qna": [{"question": "dummy supplier question.", "answer": "dummy supplier answer"}],
        },
        {
            "category_name": category_name,
            "supplier_name": None,
            "sku_id": "test sku 1",
            "qna": [{"question": "dummy sku question.", "answer": "dummy sku answer"}],
        },
    )
    pg_connector_mock.select_records_with_filter.return_value = data
    pg_connector_mock.get_condition_string.side_effect = [
        f"category_name = '{category_name}'",
        f"supplier_name = '{supplier_name}'",
        f"sku_id in ('{' , '.join(sku_list)}')",
    ]

    expected_data = (
        "answer: dummy category answer question: dummy category question.",
        "answer: dummy supplier answer question: dummy supplier question.",
        "answer: dummy sku answer question: dummy sku question.",
    )
    actual_data = extract_qa_context(
        pg_connector_mock,
        category_name,
        supplier_name,
        sku_list,
    )

    assert expected_data == actual_data
    pg_connector_mock.select_records_with_filter.assert_called_once_with(
        table_name=negotiation_conf["tables"]["qna_view"],
        filter_condition=(
            "supplier_name = 'test supplier name' or sku_id in "
            "('test sku 1 , test sku 2') or category_name = 'test_category'"
        ),
    )


def test_extract_qa_context_without_supplier_name_sku_list(
    pg_connector_mock,
):
    category_name = "test_category"
    supplier_name = ""
    sku_list = []

    data = (
        {
            "category_name": category_name,
            "supplier_name": None,
            "sku_id": None,
            "qna": [{"question": "dummy category question.", "answer": "dummy category answer"}],
        },
    )
    pg_connector_mock.select_records_with_filter.return_value = data
    pg_connector_mock.get_condition_string.return_value = "category_name = 'test_category'"

    expected_data = ("answer: dummy category answer question: dummy category question.", "", "")
    actual_data = extract_qa_context(
        pg_connector_mock,
        category_name,
        supplier_name,
        sku_list,
    )

    assert expected_data == actual_data


@patch("ada.use_cases.negotiation_factory.negotiation_factory_utils.extract_objective_description")
@patch("ada.use_cases.negotiation_factory.negotiation_factory_utils.get_supplier_profile")
def test_extract_model_context(
    get_supplier_profile_mock,
    extract_objective_description_mock,
    reference_data,
    pg_connector_mock,
    supplier_data_mock,
):
    category = "test_category"
    supplier_name, _, _, supplier_profile, user_query = supplier_data_mock
    pinned_elements = {"supplier_profile": supplier_profile}

    negotiation_objective = ["test_objective"]
    negotiation_objective_description = ["test objective description"]

    get_supplier_profile_mock.return_value = (supplier_name, supplier_profile)
    extract_objective_description_mock.return_value = negotiation_objective_description

    expected_output = (
        supplier_name,
        supplier_profile,
        negotiation_objective_description,
    )

    actual_output = extract_model_context(
        reference_data,
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
        negotiation_objective,
    )

    assert expected_output == actual_output
    get_supplier_profile_mock.assert_called_with(
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
        elements_required=True,
    )

    extract_objective_description_mock.assert_called_once_with(
        reference_data=reference_data,
        objective=negotiation_objective[0],
    )


@patch("ada.use_cases.negotiation_factory.negotiation_factory_utils.extract_objective_description")
@patch("ada.use_cases.negotiation_factory.negotiation_factory_utils.get_supplier_profile")
def test_extract_model_context_with_optional_relationship_description(
    get_supplier_profile_mock,
    extract_objective_description_mock,
    reference_data,
    pg_connector_mock,
    supplier_data_mock,
):
    category = "test_category"
    supplier_name, supplier_relationship, _, supplier_profile, user_query = supplier_data_mock
    pinned_elements = {"supplier_profile": supplier_profile}

    negotiation_objective = ["test_objective"]
    negotiation_objective_description = ["test objective description"]

    get_supplier_profile_mock.return_value = (supplier_name, supplier_profile)
    extract_objective_description_mock.return_value = negotiation_objective_description

    expected_output = (
        supplier_name,
        supplier_profile,
        negotiation_objective_description,
    )

    actual_output = extract_model_context(
        reference_data,
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
        negotiation_objective,
        elements_required=False,
    )

    assert expected_output == actual_output


def test_convert_to_response_format():
    response_type = "dummy response"
    message = "dummy message"
    suggested_prompts = [{"prompt": "dummy prompt", "intent": "dummy intent"}]
    other_kwrags = {"key_1": "data_1", "key_2": 2}

    expected_data = {
        "response_type": response_type,
        "message": message,
        "suggested_prompts": suggested_prompts,
        "key_1": "data_1",
        "key_2": 2,
    }
    actual_data = convert_to_response_format(
        response_type,
        message,
        suggested_prompts,
        **other_kwrags,
    )
    assert expected_data == actual_data


def test_convert_to_response_format_without_suggested_prompt():
    response_type = "dummy response"
    message = "dummy message"
    other_kwrags = {"key_1": "data_1", "key_2": 2}

    expected_data = {
        "response_type": response_type,
        "message": message,
        "suggested_prompts": [],
        "key_1": "data_1",
        "key_2": 2,
    }
    actual_data = convert_to_response_format(
        response_type,
        message,
        **other_kwrags,
    )
    assert expected_data == actual_data


def test_get_negotiation_strategy_data(reference_data):
    category = "test_category"
    expected_data = {
        "category_name": category,
        "is_auctionable": True,
        "category_positioning": "leverage",
        "pricing_methodology": ["Market based pricing", "Index based pricing", "Cost plus model"],
        "contract_methodology": [
            "Framework agreement approach",
            "Long term contract",
            "Indefinite delivery",
        ],
    }
    actual_data = get_negotiation_strategy_data(reference_data, category)

    assert expected_data == actual_data


@patch("ada.use_cases.negotiation_factory.negotiation_factory_utils.extract_model_context")
def test_get_negotiation_model_context(
    extract_model_context_mock,
    pg_connector_mock,
):
    supplier_name = "test_supplier"
    supplier_profile = ""
    negotiation_objective = ["test_objective"]
    reference_data = {
        "negotiation_references": pd.DataFrame(
            {
                "l1_objective": "spend",
                "l1_objective_description": "test description",
                "samples": [],
            },
        ),
    }
    extract_model_context_mock.return_value = (
        supplier_name,
        supplier_profile,
        negotiation_objective,
    )

    # fetch_insights_for_supplier_mock.return_value = supplier_carrot_insights
    actual_data = get_negotiation_model_context(
        reference_data,
        pg_connector_mock,
        category="test_category",
        user_query="test_query",
        pinned_elements={"objectives": [{"objective": "test_objective", "objective_type": "l1"}]},
        generation_type="negotiation_arguments",
        is_all_objectives_in_action=True,
    )

    expected_data = {
        "supplier_name": supplier_name,
        "supplier_profile": supplier_profile,
        "objective_descriptions": negotiation_objective,
        "objective_types": ["l1"],
        "filtered_objectives": [{"objective": "test_objective", "objective_type": "l1"}],
        "filtered_insights": [],
        "sourcing_approach": [],
        "category_positioning": " ",
        "supplier_positioning": " ",
        "buyer_attractiveness": {},
        "tone": {},
        "past_examples": [],
        "target_list": ["For the objective l1: "],
        "Selected SKUs": "",
        "carrots": [],
        "sticks": [],
        "priority": {},
    }
    assert actual_data == expected_data


def test_json_regex():
    test_json_string = """AI Assistant: "supplier_name":"ABC""supplier_val":'BMW'"""
    expected_output = {
        "supplier_name": "ABC",
        "supplier_val": "BMW",
    }
    actual_output = json_regex(test_json_string, ["supplier_name", "supplier_val"])
    assert expected_output == actual_output


def test_get_negotiation_approach_suggested_prompts():
    pinned_elements = {"supplier_profile": MagicMock()}

    expected_prompts = [
        {
            "prompt": negotiation_conf["cta_button_map"]["approach_cp"],
            "intent": "negotiation_approach_cp",
        },
    ]
    actual_prompts = get_workflow_suggested_prompts(
        pinned_elements,
        need_supplier_profile_check=False,
        include_insights=False,
        strategy_flow=True,
    )

    assert expected_prompts == actual_prompts


def test_get_workflow_suggested_prompts():
    pinned_elements = {
        "supplier_profile": MagicMock(),
    }

    expected_prompts = [
        {
            "prompt": negotiation_conf["cta_button_map"]["objective"],
            "intent": "negotiation_objective",
        },
        {
            "prompt": negotiation_conf["cta_button_map"]["insights"],
            "intent": "negotiation_insights",
        },
    ]
    actual_prompts = get_workflow_suggested_prompts(pinned_elements)

    assert expected_prompts == actual_prompts


def test_get_workflow_suggested_prompts_with_arguemnets_pinned():
    pinned_elements = {
        "supplier_profile": MagicMock(),
        "arguments": {},
    }

    expected_prompts = [
        {
            "prompt": negotiation_conf["cta_button_map"]["counter_arguments"],
            "intent": "negotiation_counter_arguments",
        },
    ]
    actual_prompts = get_workflow_suggested_prompts(pinned_elements)

    assert expected_prompts == actual_prompts
