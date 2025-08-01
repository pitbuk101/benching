"""Azure ML Endpoint for preprocessing pipeline deployment."""

# flake8: noqa: E402

import json
import os
import pathlib
import sys

# from azure.ai.ml import MLClient
# from azure.ai.ml.dsl import pipeline
from dotenv import load_dotenv

load_dotenv()

# pylint: disable=C0413,
sys.path.append(str(pathlib.Path(__file__).parents[2]))
# pylint: enable=C0413

# from ada.components.azureml.workspace import get_workspace
# from ada.utils.authorization.credentials import get_workspace_client_secret_credential
from ada.utils.config.config_loader import read_config
from ada.utils.io.misc import clean_string, get_deployment_name
from ada.utils.logs.logger import get_logger
from ada.utils.migrations.utils import pop_excess_environment_variables

log = get_logger("preprocess-deploy")
pop_excess_environment_variables()


def init():
    """Azure Real time deployments for preprocessing"""


def assemble_pipeline(client: MLClient, component_conf: dict):
    """Assemble the pipeline using the components registered in the workspace."""

    preprocessing_pipe = client.components.get(
        component_conf[f"preprocessing_{os.environ['ENV_TYPE']}"]["component_name"],
    )

    @pipeline()
    def contract_preprocessing_pipeline(
        tenant_id: str,
        document_id: int,
        input_data_filename: str,
        sku_list: str,
        document_type: str,
        region: str,
        category: str,
        supplier: str,
        azure_client_secret: str,
        azure_client_secret_secondary: str,
        input_container: str = ".",
        output_container: str = "./outputs",
    ):
        # pylint: disable=unused-variable
        read_node = preprocessing_pipe(
            tenant_id=tenant_id,
            input_data_filename=input_data_filename,
            sku_list=sku_list,
            document_id=document_id,
            document_type=document_type,
            region=region,
            category=category,
            supplier=supplier,
            input_container=input_container,
            output_container=output_container,
            azure_client_secret=azure_client_secret,
            azure_client_secret_secondary=azure_client_secret_secondary,
        )

    return contract_preprocessing_pipeline


def run(inputs):
    """Entrypoint function"""
    inputs = json.loads(inputs)
    log.info("Received inputs: \n%s", inputs)
    conf = read_config("azml_deployment.yaml")
    workspace = get_workspace(conf)
    tenant_id = workspace.get_details()["identity"]["tenant_id"]
    client_id = conf["global"]["sp_client_id"]

    azml_client = MLClient(
        credential=get_workspace_client_secret_credential(client_id=client_id, tenant_id=tenant_id),
        subscription_id=workspace.subscription_id,
        resource_group_name=workspace.resource_group,
        workspace_name=workspace.name,
    )

    contract_preprocessing_pipeline = assemble_pipeline(
        client=azml_client,
        component_conf=conf["components"],
    )

    preprocessing_job = contract_preprocessing_pipeline(
        tenant_id=inputs.get("tenant_id"),
        document_id=inputs.get("document_id"),
        input_data_filename=inputs.get("input_data_filename"),
        sku_list=json.dumps(json.dumps(inputs.get("sku_list"))),
        document_type=inputs.get("document_type"),
        region=inputs.get("region"),
        category=inputs.get("category"),
        supplier=inputs.get("supplier"),
        azure_client_secret=os.getenv("AZURE_CLIENT_SECRET"),
        azure_client_secret_secondary=os.getenv("AZURE_CLIENT_SECRET_SECONDARY", ""),
    )

    deployment_name = get_deployment_name("contract-preprocessing")
    # Extracts the job_params from config file
    job_params = [
        endpoint["job_params"]
        for endpoint in conf["endpoints"]
        if endpoint["name"] == deployment_name
    ][0]

    experiment_file_name = clean_string(inputs.get("input_data_filename"))

    preprocessing_job.settings.default_datastore = job_params["datastore"]
    preprocessing_job.settings.default_compute = job_params["compute"]

    job_run = azml_client.jobs.create_or_update(
        job=preprocessing_job,
        experiment_name=experiment_file_name,
    )

    return {
        "document_id": inputs.get("document_id"),
        "job_status": job_run.status,
        "experiment_name": experiment_file_name,
    }
