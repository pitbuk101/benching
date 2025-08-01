"""Endpoints E2E integration test in Azure"""

import os
import time

import pytest
from azureml.core.experiment import Experiment

from ada.components.azureml.azml_connector import AzureMLConnector
from ada.components.azureml.workspace import get_workspace
from ada.utils.config.config_loader import read_config
from ada.utils.io.misc import get_deployment_name, get_endpoint_url
from tests.unit_tests.use_cases.intent_classification.test_intent_classification import (
    get_unified_response_keys,
)

conf = read_config("azml_deployment.yaml")


@pytest.fixture()
def azml_key_vault():
    """
    Set azml endpoint key as environment variable
    """
    work_space = get_workspace(conf)

    default_key_vault = work_space.get_default_keyvault()

    return default_key_vault


@pytest.fixture()
def azml_endpoint_payloads():
    """
    Creates request payloads for endpoints
    """
    input_filename = "Contract 4 - Faber Industrietechnik GmbH.pdf"
    tenant_id = os.getenv("ATLAS_TENANT_ID")
    contract_preprocessing_payload = {
        "tenant_id": tenant_id,
        "document_id": "9999",
        "input_data_filename": input_filename,
        "sku_list": [
            {
                "id": "POR001.000000000010017347",
                "code": "10017347",
                "description": "Deep groove ball bearings 6304 / C3 DIN625",
            },
            {
                "id": "POR001.000000000010017349",
                "code": "10017349",
                "description": "Deep groove ball bearings 6305 / C3 DIN625",
            },
            {
                "id": "POR001.000000000010017350",
                "code": "10017350",
                "description": "Deep groove ball bearings 6306 / C3 DIN625",
            },
            {
                "id": "POR001.000000000010017351",
                "code": "10017351",
                "description": "Deep groove ball bearings 6308 / C3 DIN625",
            },
            {
                "id": "POR001.000000000010017352",
                "code": "10017352",
                "description": "Angular contact ball bearing 3305 A TN9 / C3 DIN628",
            },
        ],
        "document_type": "contract",
        "region": "Region Test",
        "category": "Category Test",
        "supplier": "Supplier Test",
    }

    summary_retrieval_payload = {
        "tenant_id": tenant_id,
        "document_id": "9999",
        "use_case": "summary",
    }
    ee_retrieval_payload = {
        "tenant_id": tenant_id,
        "document_id": "9999",
        "use_case": "entity_extraction",
    }
    benchmarking_retrieval_payload = {
        "tenant_id": tenant_id,
        "document_id": "9999",
        "use_case": "benchmarking",
    }
    clauses_retrieval_payload = {
        "tenant_id": tenant_id,
        "document_id": "9999",
        "use_case": "clauses",
    }
    leakage_extraction_payload = {
        "tenant_id": tenant_id,
        "document_id": "9999",
    }

    top_ideas_payload = {
        "tenant_id": tenant_id,
    }

    unified_model_payload = {
        "tenant_id": tenant_id,
        "category": "Bearings",
        "page_id": "negotiation",
        "chat_id": "123_KB",
        "request_id": "1",
        "user_query": "Define Net Sales terms in the cotext of agreements.",
        "request_type": "",
        "pinned_elements": {},
    }

    data_retrieval_service_payload = {
        "tenant_id": tenant_id,
        "date_int": 20241219,
        "request_type": "news_insights",
    }

    payload_map = {
        "summary": summary_retrieval_payload,
        "entity_extraction": ee_retrieval_payload,
        "benchmarking": benchmarking_retrieval_payload,
        "clauses": clauses_retrieval_payload,
        "leakage_extraction": leakage_extraction_payload,
        "contract_preprocessing": contract_preprocessing_payload,
        "top_ideas": top_ideas_payload,
        "unified_intent_model": unified_model_payload,
        "data_retrieval_service": data_retrieval_service_payload,
    }

    return payload_map


@pytest.fixture()
def azml_endpoint_connections(azml_key_vault):
    """
    Creates azml connections for respective endpoints
    """
    base_url = conf["base_endpoint_url"]

    contract_preprocessing_deployment = get_deployment_name("contract-preprocessing")
    azml_conn_preprocess = AzureMLConnector(
        azml_url=get_endpoint_url(base_url, contract_preprocessing_deployment),
        azml_deployment=contract_preprocessing_deployment,
        azml_api_key=azml_key_vault.get_secret(contract_preprocessing_deployment),
    )

    document_service_deployment = get_deployment_name("data-retrieval")
    azml_conn_retrieval = AzureMLConnector(
        azml_url=get_endpoint_url(base_url, document_service_deployment),
        azml_deployment=document_service_deployment,
        azml_api_key=azml_key_vault.get_secret(document_service_deployment),
    )

    leakage_extraction_deployment = get_deployment_name("leakage-extraction")
    azml_conn_leakage_extraction = AzureMLConnector(
        azml_url=get_endpoint_url(base_url, leakage_extraction_deployment),
        azml_deployment=leakage_extraction_deployment,
        azml_api_key=azml_key_vault.get_secret(leakage_extraction_deployment),
    )

    unified_intent_model_deployment = get_deployment_name("unified-model")
    azml_conn_unified_intent_model = AzureMLConnector(
        azml_url=get_endpoint_url(base_url, unified_intent_model_deployment),
        azml_deployment=unified_intent_model_deployment,
        azml_api_key=azml_key_vault.get_secret(unified_intent_model_deployment),
    )

    top_ideas_deployment = get_deployment_name("top-ideas")
    azml_conn_top_ideas = AzureMLConnector(
        azml_url=get_endpoint_url(base_url, top_ideas_deployment),
        azml_deployment=top_ideas_deployment,
        azml_api_key=azml_key_vault.get_secret(top_ideas_deployment),
    )

    data_retrieval_service_deployment = get_deployment_name("data-retrieval-service")
    azml_conn_data_retrieval_service = AzureMLConnector(
        azml_url=get_endpoint_url(base_url, data_retrieval_service_deployment),
        azml_deployment=data_retrieval_service_deployment,
        azml_api_key=azml_key_vault.get_secret(data_retrieval_service_deployment),
    )

    azml_conn_map = {
        "contract_preprocessing": azml_conn_preprocess,
        "document_service_deployment": azml_conn_retrieval,
        "leakage_extraction_deployment": azml_conn_leakage_extraction,
        "unified_intent_model": azml_conn_unified_intent_model,
        "top_ideas": azml_conn_top_ideas,
        "data_retrieval_service": azml_conn_data_retrieval_service,
    }

    return azml_conn_map


@pytest.mark.e2e_azure
def test_contract_preprocessing(azml_endpoint_connections, azml_endpoint_payloads):
    """
    Testing contract preprocessing endpoint
    """

    azml_conn = azml_endpoint_connections["contract_preprocessing"]
    test_payload = azml_endpoint_payloads["contract_preprocessing"]

    workspace = get_workspace(conf)

    # sending request for preprocessing
    response = azml_conn.azml_post(payload=test_payload)
    job_status = response.get("job_status")
    job_experiment_name = response.get("experiment_name")

    # Sleeping to wait for azure metadata update.
    time.sleep(5)
    exp = Experiment(workspace=workspace, name=job_experiment_name)

    run_status = None
    if job_status in ["Preparing", "NotStarted"]:
        exp_runs = exp.get_runs(type="azureml.PipelineRun")
        # __next__() for getting latest experiment run status
        run_status = exp_runs.__next__().wait_for_completion()

    assert run_status is not None


@pytest.mark.e2e_azure
def test_summary(azml_endpoint_connections, azml_endpoint_payloads):
    """
    Testing summary retrieval endpoint
    """
    azml_conn = azml_endpoint_connections["document_service_deployment"]
    test_payload = azml_endpoint_payloads["summary"]

    response = azml_conn.azml_post(payload=test_payload)

    keys_to_check = ["document_id", "summary"]

    assert (
        (keys_to_check == list(response.keys()))
        and (isinstance(response.get("summary"), str))
        and (len(response.get("summary")) > 0)
    ), "Incorrect data retrieval response for summary"


@pytest.mark.e2e_azure
def test_entity_extraction(azml_endpoint_connections, azml_endpoint_payloads):
    """
    Testing entity extraction retrieval endpoint
    """
    azml_conn = azml_endpoint_connections["document_service_deployment"]
    test_payload = azml_endpoint_payloads["entity_extraction"]

    response = azml_conn.azml_post(payload=test_payload)

    keys_to_check = ["document_id", "entity_extraction"]

    assert (
        (keys_to_check == list(response.keys()))
        and (isinstance(response.get("entity_extraction"), dict))
        and (len(response.get("entity_extraction")) > 0)
    ), "Incorrect data retrieval response for entity extraction"


@pytest.mark.e2e_azure
def test_benchmarking(azml_endpoint_connections, azml_endpoint_payloads):
    """
    Testing benchmarking retrieval endpoint
    """
    azml_conn = azml_endpoint_connections["document_service_deployment"]
    test_payload = azml_endpoint_payloads["benchmarking"]

    response = azml_conn.azml_post(payload=test_payload)

    keys_to_check = ["document_id", "benchmarking"]

    assert (
        (keys_to_check == list(response.keys()))
        and (isinstance(response.get("benchmarking"), dict))
        and (len(response.get("benchmarking")) > 0)
    ), "Incorrect data retrieval response for benchmarking"


@pytest.mark.e2e_azure
def test_clauses(azml_endpoint_connections, azml_endpoint_payloads):
    """
    Testing clauses retrieval endpoint
    """
    azml_conn = azml_endpoint_connections["document_service_deployment"]
    test_payload = azml_endpoint_payloads["clauses"]

    response = azml_conn.azml_post(payload=test_payload)

    keys_to_check = ["document_id", "clauses"]

    assert (
        (keys_to_check == list(response.keys()))
        and (isinstance(response.get("clauses"), list))
        and (len(response.get("clauses")) > 0)
    ), "Incorrect data retrieval response for clauses"


@pytest.mark.e2e_azure
def test_leakage_extraction(azml_endpoint_connections, azml_endpoint_payloads):
    """
    Testing leakage extraction endpoint
    """
    azml_conn = azml_endpoint_connections["leakage_extraction_deployment"]
    test_payload = azml_endpoint_payloads["leakage_extraction"]

    response = azml_conn.azml_post(payload=test_payload)

    keys_to_check = [
        "document_id",
        "sku_id",
        "original_code",
        "description",
        "price",
        "price_type",
        "currency",
    ]

    assert (
        (["contract_sku_details"] == list(response.keys()))
        and (isinstance(response.get("contract_sku_details"), list))
        and keys_to_check == list(response.get("contract_sku_details")[0])
    ), "Incorrect data retrieval response for benchmarking"


@pytest.mark.e2e_azure
def test_unified_model(azml_endpoint_connections, azml_endpoint_payloads):
    """Test unified Intent classification use case."""
    azml_conn = azml_endpoint_connections["unified_intent_model"]
    test_payload = azml_endpoint_payloads["unified_intent_model"]

    response = azml_conn.azml_post(payload=test_payload)
    assert (
        isinstance(response, dict)
        and len(response) > 0
        and set(get_unified_response_keys()).issubset(response.keys())
    ), "Incorrect response for unified intent model"


@pytest.mark.e2e_azure
def test_top_ideas(azml_endpoint_connections, azml_endpoint_payloads):
    """Test top ideas use case."""
    azml_conn = azml_endpoint_connections["top_ideas"]
    test_payload = azml_endpoint_payloads["top_ideas"]

    response = azml_conn.azml_post(payload=test_payload)

    keys_to_check = {
        "top_ideas",
        "response_type",
        "message",
    }

    assert (
        isinstance(response, dict)
        and len(response) > 0
        and set(response.keys()).issubset(keys_to_check)
    ), "Incorrect response for top ideas"


@pytest.mark.e2e_azure
def test_data_retrieval_service_for_news_insights(
    azml_endpoint_connections,
    azml_endpoint_payloads,
):
    """Test news insights use case."""
    azml_conn = azml_endpoint_connections["data_retrieval_service"]
    test_payload = azml_endpoint_payloads["data_retrieval_service"]

    response = azml_conn.azml_post(payload=test_payload)

    keys_to_check = {
        "curated_news_insights",
    }

    assert (
        isinstance(response, dict)
        and len(response) > 0
        and set(response.keys()).issubset(keys_to_check)
    ), "Incorrect response for news insights"
