"""Unit test for usecases."""

import json
import os
import pathlib

import pandas as pd
import pytest
import yaml  # type: ignore
from pandas._testing import assert_frame_equal

from ada.components.azureml.azml_model import RetrieveModel
from ada.components.db.pg_operations import get_content_from_db
from ada.components.vectorstore.vectorstore import VectorStoreFactory
from ada.use_cases.clauses.clauses import run_clauses
from ada.use_cases.contract_qa.contract_qa import run_contract_qa
from ada.use_cases.entity_extraction.entity_extraction import run_entity_extraction
from ada.use_cases.intent_classification.intent_classification_v2 import (
    run_unified_model,
)
from ada.use_cases.key_facts.configuration import Configuration
from ada.use_cases.key_facts.key_facts_v3 import run_key_facts
from ada.use_cases.leakage.leakage import run_leakage
from ada.use_cases.news_qna.news_qna_v2 import run_news_qna
from ada.use_cases.summary.summary_generator import run_summary_generator
from ada.utils.azml.azml_utils import set_openai_api_creds
from ada.utils.config.config_loader import read_config
from ada.utils.metrics.similarity import get_similarity
from tests.integration_tests.test_unified_intent_model_input_data import (
    get_uniformed_input_json,
)
from tests.unit_tests.use_cases.intent_classification.test_intent_classification import (
    get_unified_response_keys,
)

component_conf = read_config("models.yml")
deployment_conf = read_config("azml_deployment.yaml")

set_openai_api_creds(
    {
        "openai_api_key": os.getenv("AZURE_OPENAI_API_KEY"),
    },
)


@pytest.fixture()
def usecase_expected_outputs():
    """
    Set usecase expected outputs.
    """
    path = os.path.join(
        pathlib.Path(
            __file__,
        ).parents[1],
        "fixtures",
        "test_endpoints_local.yml",
    )
    with open(path, encoding="utf8") as config_file:
        config = yaml.safe_load(config_file)

    expected_outputs = {
        "summary": config["expected-output-mapping"]["summary"],
        "entity_extraction": config["expected-output-mapping"]["entity_extraction"],
        "clauses": config["expected-output-mapping"]["clauses"],
        "contract_qa": config["expected-output-mapping"]["contract_qa"],
    }
    return expected_outputs


@pytest.mark.e2e_local
def test_summary(set_env_variables, usecase_expected_outputs):
    """
    Test summary generator usecase.
    """
    document_id = 1002
    tenant_id = "920a2f73-c7db-405f-98ea-f768c6da864f"
    df_doc_chunks = get_content_from_db(
        tenant_id=tenant_id,
        document_id=document_id,
    )
    document_type = "document"
    actual_output = run_summary_generator(
        document_id,
        document_type,
        df_doc_chunks,
    )

    similarity_level, similarity_score = get_similarity(
        usecase_expected_outputs,
        actual_output,
    ).split(",")

    assert (similarity_level in ("similar", "perfect")) and float(similarity_score) >= 0.8


@pytest.mark.e2e_local
def test_leakage_extraction(set_env_variables, usecase_expected_outputs):
    """
    Test leakage extraction usecase.
    """
    document_id = 1002
    document_type = "contract"
    tenant_id = "920a2f73-c7db-405f-98ea-f768c6da864f"
    df_doc_chunks = get_content_from_db(
        tenant_id=tenant_id,
        document_id=document_id,
    )
    vector_store_factory = VectorStoreFactory()
    vectorstore = vector_store_factory.faiss_from_embeddings(
        doc_chunk=df_doc_chunks,
    )
    test_df_1 = pd.DataFrame(
        {
            "Sr. No": [1],
            "SKU Code": ["100020428"],
            "SKU Description": ["FAN BEARING ASSEMBLY"],
            "Unit price (Per Piece)": ["3055.5"],
            "Quantity(Annual)": ["3"],
        },
    )
    df_doc_tables = [test_df_1]
    sku_list = [
        {
            "id": "POR004.000000000100020428",
            "code": "100020428",
            "description": "Fan Bearings assembly",
        },
    ]
    expected_output = pd.DataFrame(
        {
            "document_id": [1002],
            "sku_id": ["POR004.000000000100020428"],
            "original_code": ["100020428"],
            "description": ["FAN BEARING ASSEMBLY"],
            "price": [3055.5],
            "price_type": "unit",
            "currency": ["USD"],
        },
    )
    actual_output = run_leakage(
        document_id,
        document_type,
        sku_list,
        df_doc_tables,
        vectorstore,
    )
    assert_frame_equal(actual_output, expected_output, check_dtype=False)


@pytest.mark.e2e_local
def test_entity_extraction(set_env_variables, usecase_expected_outputs):
    """
    Test entity extraction usecase.
    """
    tenant_id = "920a2f73-c7db-405f-98ea-f768c6da864f"
    document_id = 1002
    df_doc_chunks = get_content_from_db(
        tenant_id=tenant_id,
        document_id=document_id,
    )
    vector_store_factory = VectorStoreFactory()
    vectorstore = vector_store_factory.faiss_from_embeddings(
        doc_chunk=df_doc_chunks,
    )
    actual_output = run_entity_extraction(vectorstore)

    assert isinstance(actual_output, dict) and (
        actual_output == usecase_expected_outputs["entity_extraction"]
    )


@pytest.mark.e2e_local
def test_clauses(set_env_variables):
    """
    Test clauses usecase.
    """
    document_id = 1002
    tenant_id = "920a2f73-c7db-405f-98ea-f768c6da864f"
    df_doc_chunks = get_content_from_db(
        tenant_id=tenant_id,
        document_id=document_id,
    )
    vector_store_factory = VectorStoreFactory()
    vectorstore = vector_store_factory.faiss_from_embeddings(
        doc_chunk=df_doc_chunks,
    )
    clauses_result = run_clauses(vectorstore)
    keys_to_check = ["Clause/section", "Answer", "Most Similar Sections"]

    assert (
        (isinstance(clauses_result, list))
        and (len(clauses_result) > 0)
        and (list(clauses_result[0].keys()) == keys_to_check)
        and clauses_result[0]["Clause/section"]
        and clauses_result[0]["Answer"]
        and clauses_result[0]["Most Similar Sections"]
    )


@pytest.mark.e2e_local
def test_contract_qa(set_env_variables, usecase_expected_outputs):
    """
    Test contract qa usecase.
    """
    expected_answer = usecase_expected_outputs["contract_qa"]
    input_json_string = json.dumps(
        {
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "document_id": 1002,
            "question": ["What are the main parties of the contract?"],
        },
    )

    model_conf = deployment_conf["models"]["contract_qna_classifier"]
    question_classifier_model = RetrieveModel(model_conf).retrieve_model()

    contract_qa_answer = run_contract_qa(
        json_file=input_json_string,
        question_classifier_model=question_classifier_model,
    )[0]["answer"]

    similarity_level, similarity_score = get_similarity(expected_answer, contract_qa_answer).split(
        ",",
    )

    assert (similarity_level in ("similar", "perfect")) and float(similarity_score) >= 0.8


# @pytest.mark.e2e_local
# def test_key_facts_v2(set_env_variables):
#     """Test key facts v2 usecase."""
#     input_json_string = json.dumps(
#         {
#             "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
#             "user_id": "dummy",
#             "user_query": "What is spend break down across "
#             "different sub-categories for last 12 months?",
#             "category": "Bearings",
#             "dax_response_code": None,
#             "dax_response": "dummy",
#             "request_id": "dummy",
#         },
#     )

#     category_configuration = Configuration(
#         required_configuration_keys={
#             "data_model",
#             "table_model",
#             "measures_description",
#             "filters_description",
#             "reports_description",
#             "format_description",
#         },
#     )

#     key_facts_result = run_key_facts_v2(
#         json_file=input_json_string,
#         category_configuration=category_configuration,
#     )

#     keys_to_check = {
#         "response_type",
#         "response_prerequisite",
#         "owner",
#         "additional_text",
#         "message",
#         "links",
#     }

#     assert (
#         isinstance(key_facts_result, dict)
#         and len(key_facts_result) > 0
#         and set(key_facts_result.keys()) == keys_to_check
#     )


@pytest.mark.e2e_local
def test_key_facts(set_env_variables):
    """Test key facts usecase."""
    input_json_string = json.dumps(
        {
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "user_id": "dummy",
            "user_query": "What is spend break down across different sub-categories for last 12 months?",
            "category": "Bearings",
            "dax_response_code": None,
            "dax_response": "dummy",
        },
    )

    data_dir = os.path.join(pathlib.Path(__file__).parents[3], "data")
    key_facts_query_report_mapping = pd.read_excel(
        os.path.join(data_dir, "key_facts/query_report_mapping.xlsx"),
    ).to_json(orient="records")
    key_facts_query_report_mapping = (
        json.dumps(
            json.loads(key_facts_query_report_mapping),
            ensure_ascii=False,
        )
        .replace("{", "{{{{")
        .replace("}", "}}}}")
    )

    dax_map_df = pd.read_excel(
        os.path.join(
            data_dir,
            "key_facts/query_dax_mapping.xlsx",
        ),
    )
    key_facts_query_dax_mapping = dax_map_df.to_json(orient="records")
    key_facts_query_dax_mapping = (
        json.dumps(json.loads(key_facts_query_dax_mapping), ensure_ascii=False)
        .replace("{", "{{{{")
        .replace("}", "}}}}")
    )

    key_facts_result = run_key_facts(
        json_file=input_json_string,
        query_dax_mapping=key_facts_query_dax_mapping,
        query_report_mapping=key_facts_query_report_mapping,
    )

    keys_to_check = [
        "response_type",
        "response_prerequisite",
        "owner",
        "additional_text",
        "message",
        "links",
    ]

    assert (
        isinstance(key_facts_result, dict)
        and len(key_facts_result) > 0
        and list(key_facts_result.keys()) == keys_to_check
    )


# NOTE: There are future changes to benchmarking usecase, unit tests for benchmarking usecase need
# to be implemented in the future.
@pytest.mark.e2e_local
def test_benchmarking():
    """
    Test for benchmarking usecase.
    """
    pass


@pytest.mark.e2e_local
def test_news_qna(set_env_variables):
    """Test news qna usecase."""
    news_conf = read_config("use-cases.yml")["news"]["context"]
    input_json_string = json.dumps(
        {
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "user_query": "Where are the key players of the engines bearings market located?",
            "category": "Bearings",
        },
    )
    news_qna_result = run_news_qna(json_file_str=input_json_string)
    keys_to_check = {
        "message",
        "response_type",
        "links",
        "additional_text",
    }

    assert (
        isinstance(news_qna_result, dict)
        and (len(news_qna_result) in news_conf["response_len"])
        and set(news_qna_result.keys()).issubset(keys_to_check)
    ), "Incorrect response for news qna"


intent_model_scope = read_config(
    "use-cases.yml",
)[
    "intent_model_v2"
]["intent_model_scope"]


@pytest.mark.e2e_local
@pytest.mark.parametrize(
    "input_json",
    [
        item
        for use_case, item in get_uniformed_input_json().items()
        if use_case in intent_model_scope
    ],
)
def test_unified_model(set_env_variables, input_json):
    """Test unified Intent classification use case."""

    category_configuration = Configuration(
        required_configuration_keys={
            "data_model",
            "table_model",
            "measures_description",
            "filters_description",
            "reports_description",
            "format_description",
        },
    )
    model_conf = deployment_conf["models"]["contract_qna_classifier"]
    question_classifier_model = RetrieveModel(model_conf).retrieve_model()

    unified_response_payload = run_unified_model(
        json.dumps(input_json),
        category_configuration=category_configuration,
        question_classifier_model=question_classifier_model,
    )

    assert isinstance(unified_response_payload, dict) and set(get_unified_response_keys()).issubset(
        set(unified_response_payload.keys()),
    )
