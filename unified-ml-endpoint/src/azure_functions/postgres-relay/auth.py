"""Utilities for azure function."""

import logging
import os
import pathlib
from typing import Any, Dict
from dotenv import load_dotenv
import yaml  # type: ignore
from azureml._vendor.azure_cli_core.azclierror import AuthenticationError
from azureml.core import Workspace
# from azureml.core.authentication import ServicePrincipalAuthentication

load_dotenv()

def get_authorized_service_principle(conf: dict) -> ServicePrincipalAuthentication:
    """
    Get authorized service principle to authorize azure account.

    Args:
        conf (dict): configurations dictionary having tenant and client details.

    Returns:
        ServicePrincipalAuthentication: Service principle to authenticate with client id and secret.
    """

    svc_pr = ServicePrincipalAuthentication(
        tenant_id=conf["global"]["azure_tenant_id"],
        service_principal_id=conf["global"]["sp_client_id"],
        service_principal_password=os.getenv("AZURE_CLIENT_SECRET"),
    )
    try:
        svc_pr.get_token()
    except AuthenticationError as e:
        logging.warning(f"Primary secret has expired: {e.error_msg}, using secondary secret")
        svc_pr = ServicePrincipalAuthentication(
            tenant_id=conf["global"]["azure_tenant_id"],
            service_principal_id=conf["global"]["sp_client_id"],
            service_principal_password=os.getenv("AZURE_CLIENT_SECRET_SECONDARY"),
        )
        svc_pr.get_token()
    return svc_pr


def read_config(file_path: str) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.

    Args:
        file_path (str): Path to the YAML configuration file.

    Returns:
        Dict[str, Any]: Loaded configuration as a dictionary.
    """
    env_type = os.getenv("ENV_TYPE")

    if not env_type:
        env_type = "dev"
        logging.warning("ENV_TYPE is not set, defaulting to 'dev'.")

    conf_folder_path = "conf"
    path = pathlib.Path(conf_folder_path, env_type, file_path)

    if not path.exists():
        path = pathlib.Path(conf_folder_path, "common", file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"{file_path} configuration file not found: in {conf_folder_path}/{env_type} or "
                f"{conf_folder_path}/local",
            )
    with open(path, encoding="utf8") as config_file:
        config = yaml.safe_load(config_file)
    return config


def get_workspace(conf: Dict) -> Workspace:
    """Reusable method for retrieving the Azure ML workspace."""

    svc_pr = get_authorized_service_principle(conf=conf)
    workspace = Workspace(
        workspace_name=conf["global"]["workspace_name"],
        subscription_id=conf["global"]["subscription_id"],
        resource_group=conf["global"]["resource_group"],
        auth=svc_pr,
    )

    return workspace


def get_secrets(
    secret_names: Dict,
) -> Dict[str, str]:
    """
    Retrieve secrets from Azure Key Vault using user-assigned managed identity.

    Args:
        global_conf (Dict): Dictionary containing config details to connect to workspace
        secret_names (List[str]): List of secret names to retrieve.

    Returns:
        Dict[str, str]: A dictionary containing secret names as keys and their values.
    """

    # Authenticate using user-assigned managed identity
    # We should use DefaultAzureCredential going ahead since we intend to use a local setup.
    # credential = DefaultAzureCredential(client_id=identity_config_client_id)
    logging.info("Authenticating using Service Principal")

    conf = read_config("azml_deployment.yaml")

    # Connect to the Azure ML workspace
    logging.info(
        "Connecting to Azure ML workspace with tenant id: %s, service principal id: %s, service principal password: %s",
        conf["global"]["azure_tenant_id"],
        conf["global"]["sp_client_id"],
        os.getenv("AZURE_CLIENT_SECRET"),
    )

    workspace = get_workspace(conf)

    # Get the default Azure Key Vault associated with the workspace
    logging.info("Getting default key vault")
    keyVaultName = workspace.get_default_keyvault()
    secret_keys = {}
    for k, v in secret_names.items():
        logging.info("Getting secret %s from key vault", v)
        secret_keys[k] = keyVaultName.get_secret(v)

    return secret_keys
