"""Utilities for azure ML."""

import json
import os
import pathlib
from datetime import datetime
from io import BytesIO
from typing import Dict
from dotenv import load_dotenv
# from azure.ai.ml import MLClient, load_component
# from azure.identity import ClientSecretCredential
# from azure.keyvault.secrets import SecretClient, SecretProperties
# from azure.storage.blob import BlobServiceClient
# from azureml.core import Environment, Workspace

# from ada.components.azureml.workspace import get_workspace
# from ada.components.extractors.text_extractors import azure_ocr
# from ada.utils.authorization.credentials import get_workspace_client_secret_credential
from ada.utils.config.config_loader import read_config
from ada.utils.io.misc import is_difference_greater_than_n_days
from ada.utils.logs.logger import get_logger

load_dotenv()

log = get_logger("azml_utils")
conf = read_config("azml_deployment.yaml")
openai_conf = read_config("models.yml")


def get_keyvault_name(workspace: Workspace) -> str:
    """
    Get keyvault name from workspace.

    Args:
        workspace (Workspace): Workspace to get the keyvault.

    Returns:
        string: keyvault name configured in given workspace.
    """
    workspace_name = workspace.get_details()["name"]
    workspace_part = str(workspace_name).split("-")[-1]
    return "keyvault-" + workspace_part


def is_secret_expired(secret_properties: SecretProperties) -> bool:
    """
    Checks if a secret is expired.

    Args:
        secret_properties (SecretProperties): Secret properties of the configured secret.

    Returns:
        bool: True if the secret is expired else False
    """
    if secret_properties.expires_on:
        log.info(f"Checking if Secret: {secret_properties.name} is expired.")
        expiry_date = secret_properties.expires_on.strftime("%Y-%m-%d %H:%M:%S")
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return expiry_date < current_date
    else:
        log.info(f"Secret {secret_properties.name} has not set any expiry date.")
        return False


def is_secret_valid(secret_properties: SecretProperties, days: int = 0) -> bool:
    """
    Checks if a secret is valid by comparing its expiry date with the current date.

    Args:
        secret_properties (SecretProperties): Secret properties of the configured secret.
        days (int): Number of day to look in secret expiry.

    Returns:
        bool: True if the secret is valid (expiry date is more than given days from the current date), False otherwise.
    """
    log.info(f"Checking if Secret: {secret_properties.name} is valid.")
    if secret_properties.expires_on:
        date_str1 = secret_properties.expires_on.strftime("%Y-%m-%d %H:%M:%S")
        date_str2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if is_difference_greater_than_n_days(date_str1, date_str2, days=days):
            log.info(
                f"Secret {secret_properties.name} is valid. Sufficent time left before expiry.",
            )
            return True
        else:
            log.warning(
                f"Secret {secret_properties.name} is not valid. < {days} days left in expiry.",
            )
            return False
    else:
        log.info(f"Secret {secret_properties.name} has not set any expiry date.")
        return True


def get_valid_secrets(
    secret_names: dict,
) -> dict:
    """
    Retrieve secrets from Azure Key Vault using user-assigned managed identity.

    Args:
        global_conf (dcit): Dictionary containing config details to connect to workspace
        secret_names (List[str]): List of secret names to retrieve.

    Returns:
        dict[str, str]: A dictionary containing secret names as keys and their values.
    """

    # Authenticate using user-assigned managed identity
    # We should use DefaultAzureCredential going ahead since we intend to use a local setup.
    # credential = DefaultAzureCredential(client_id=identity_config_client_id)
    workspace = get_workspace(conf)
    tenant_id = workspace.get_details()["identity"]["tenant_id"]
    client_id = conf["global"]["sp_client_id"]
    secret_client = SecretClient(
        vault_url=f"https://{get_keyvault_name(workspace=workspace)}.vault.azure.net/",
        credential=get_workspace_client_secret_credential(
            client_id=client_id,
            tenant_id=tenant_id,
        ),
    )

    valid_secrets = {}
    for secret_key, secret_name in secret_names.items():
        secret = secret_client.get_secret(secret_name)
        secret_properties = secret.properties
        if secret_properties and is_secret_valid(secret_properties, days=0):
            valid_secrets[secret_key] = secret.value
    return valid_secrets


def get_secrets(
    secret_names: dict,
) -> dict:
    """
    Retrieve secrets from Azure Key Vault using user-assigned managed identity.

    Args:
        global_conf (dict): Dictionary containing config details to connect to workspace
        secret_names (List[str]): List of secret names to retrieve.

    Returns:
        dict : A dictionary containing secret names as keys and their values.
    """

    # Authenticate using user-assigned managed identity
    # We should use DefaultAzureCredential going ahead since we intend to use a local setup.
    # credential = DefaultAzureCredential(client_id=identity_config_client_id)
    workspace = get_workspace(conf)

    # Get the default Azure Key Vault associated with the workspace
    keyVaultName = workspace.get_default_keyvault()

    secret_keys = {}
    for k, v in secret_names.items():
        log.info("Retrieving secret %s", v)
        secret_keys[k] = keyVaultName.get_secret(v)
    return secret_keys


def set_openai_api_creds(secret_keys: dict):
    """
    Set OpenAI api credentials.

    Args:
        secret_keys: A dictionary containing secret names as keys and their values.

    """
    os.environ["AZURE_OPENAI_API_KEY"] = secret_keys.get("openai_api_key", "")
    os.environ["AZURE_OPENAI_ENDPOINT"] = openai_conf["open_api_base_url"]
    os.environ["OPENAI_API_VERSION"] = openai_conf["openai_api_version"]

    log.info("Setting OpenAI API credentials")
    pop_excess_environment_variables()


def pop_excess_environment_variables():
    """
    Pop excess environment variables.
    """
    if os.getenv("OPENAI_API_BASE"):
        os.environ.pop("OPENAI_API_BASE")


def azure_download_pdf(
    storage_account_name: str,
    credential: ClientSecretCredential,
    filename: str,
    container: str,
    vision_endpoint: str,
    vision_key: str,
) -> dict:
    """
    Download PDF contract from Azure Blob Storage for given account
    Args:
        storage_account_name: tenant specific storage account name
        credential: credential of the tenant
        filename: name of the file to download
        container: name of the container inside storage account
        vision_endpoint: endpoint url for azure ocr
        vision_key: key for azure ocr
    """
    blob_service_client = BlobServiceClient(
        f"https://{storage_account_name}.blob.core.windows.net/upload",
        credential=credential,
    )
    blob_client = blob_service_client.get_blob_client(container=container, blob=filename)
    with BytesIO() as input_blob:
        blob_client.download_blob().readinto(input_blob)
        input_blob.seek(0)
        response = azure_ocr(input_blob, vision_endpoint, vision_key)
        return response


def get_latest_env(azml_client: MLClient, env_name: str) -> Environment:
    """
    Retrieve the latest version of a specified Azure Machine Learning environment.

    Args:
        azml_client: The Azure Machine Learning client for accessing ML resources.
        env_name: The name of the Azure Machine Learning environment.

    Returns:
        azureml.core.Environment: The latest version of the specified environment.

    Raises:
        Exception: If the latest version is not found for the specified environment or if the environment is archived.
    """
    envs = azml_client.environments.list(name=env_name)
    latest_env = None

    for env in envs:
        if env.properties["azureml.labels"] == "latest":
            latest_env = env
            break

    if latest_env is None:
        raise Exception(
            f"Latest environment named {env_name} not found. Check if the environment exists or is archived.",
        )
    else:
        return latest_env


def azure_download_json(
    storage_account_name: str,
    credential: ClientSecretCredential,
    filename: str,
    container: str,
) -> dict:
    """
    Download dict from Azure Blob Storage for given account
    Args:
        storage_account_name: tenant specific storage account name
        credential: credential of the tenant
        filename: name of the file to download
        container: name of the container inside storage account
    Return:
        (dict): json of contraining the contents of the file on Azure blobfile
    """
    blob_service_client = BlobServiceClient(
        f"https://{storage_account_name}.blob.core.windows.net/upload",
        credential=credential,
    )
    container_client = blob_service_client.get_container_client(container=container)
    downloaded_blob = container_client.download_blob(filename)
    return json.loads(downloaded_blob.readall())


def get_azml_client():
    """
    Get azure ml client
    Return:
        azure ml client object
    """

    workspace = get_workspace(conf)
    tenant_id = workspace.get_details()["identity"]["tenant_id"]
    client_id = conf["global"]["sp_client_id"]

    azml_client = MLClient(
        credential=get_workspace_client_secret_credential(client_id=client_id, tenant_id=tenant_id),
        subscription_id=conf["global"]["subscription_id"],
        resource_group_name=conf["global"]["resource_group"],
        workspace_name=conf["global"]["workspace_name"],
    )
    return azml_client


def register_component(ml_client: MLClient, component_config: Dict[str, str]):
    """Register a component to the workspace."""
    repo_root = pathlib.Path(__file__).parents[4]
    name = component_config["component_name"]
    if component_config["register"]:
        log.info("Registering component %s", name)
        component = load_component(
            source=os.path.join(repo_root, component_config["source"]),
            relative_origin=os.path.join(repo_root, "src"),
        )
        ml_client.create_or_update(component)
        log.info("Successfully registered component %s", name)
