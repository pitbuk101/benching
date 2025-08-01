import os
from pathlib import Path

import pandas as pd
import yaml  # type: ignore
from azure.core.exceptions import ResourceNotFoundError
from azure.keyvault.secrets import SecretClient
from azureml.core import Workspace

from ada.components.azureml.workspace import get_workspace
# from ada.utils.authorization.credentials import get_workspace_client_secret_credential
from ada.utils.azml.azml_utils import (
    get_keyvault_name,
    is_secret_expired,
    is_secret_valid,
)
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger

conf = read_config("azml_deployment.yaml")
secrets_from_config = read_config("secrets.yml")
log = get_logger("secrets_validations")

email_message_template = """
Dear All,
<br>
<br>
Please find the secrets details used in SourceAI and take the necessary action,
if you see any secret is missing/expired or about to expire.
<br><br>
******************* Missing Secrets (key-vault) ******************
<br><br>
{secret_not_found_content}
<br><br>
******************* Expired Secrets **********************
<br><br>
{expired_secrets_content}
<br><br><br>
******************* Expiring in next 15 days **********************
<br>
{near_expiry_secrets_content}
<br><br>
To ensure continuous access and avoid any disruptions,
please take the necessary steps to renew or replace your secrets before the expiry date.<br>
If you need any assistance, feel free to contact our support team at <b>support@mckinsey.com</b> or visit our help center.
<br><br>
Thank you for your prompt attention to this matter.
<br><br>
Best regards,<br>
The SourceAI Team
"""

env_type_storage_account_map = {
    "dev": "storage_config_dev.yml",
    "staging": "storage_config_stage.yml",
    "prod-eu": "storage_config_prod_EU.yml",
    "prod-us": "storage_config_prod_US.yml",
}


def get_storage_account_secrets() -> list[str]:
    """
    Get storage accounts secrete names.

    Returns:
        list[str]: Returns storage accounts secret names list for configured env type.
    """

    env_type = os.environ.get("ENV_TYPE")
    if not env_type:
        raise ValueError("Env type not set")

    storage_accounts_folder_path = Path(Path(__file__).parents[2], "")
    path = Path(storage_accounts_folder_path, env_type_storage_account_map.get(env_type, ""))

    storage_account_secret_names = list([])
    with open(path, encoding="utf8") as storage_account_config_file:
        storage_accounts_conf = yaml.safe_load(storage_account_config_file)
        for tenant_id in storage_accounts_conf.get("ancillary_storage_accounts", []):
            tenant_id_part = tenant_id.replace("-", "")[:17]
            workspace_part = conf["global"]["workspace_name"].split("-")[-1]
            storage_account_name = tenant_id_part + workspace_part
            storage_account_secret_names.append(storage_account_name + "-service-account-secret-1")
            storage_account_secret_names.append(storage_account_name + "-service-account-secret-2")
    return storage_account_secret_names


def get_secrets_expiry_details(secret_client: SecretClient) -> dict:
    """
    Get secrets list about to expire configured in secrets.yml.

    Args:
        secret_client (SecretClient): SecretClient to get the secret properties.

    Returns:
        dict: secrets with expiry and near expiry details.
    """

    secret_expiry_details: dict = {"not_found": [], "expired": [], "near_expiry": []}
    secrets_to_validate = list(secrets_from_config.values())
    secrets_to_validate.extend(get_storage_account_secrets())
    for secret_name in secrets_to_validate:
        try:
            secret = secret_client.get_secret(secret_name)
            secret_properties = secret.properties
            if secret_properties:
                if secret_properties.expires_on:
                    expiry_date = secret_properties.expires_on.strftime("%Y-%m-%d %H:%M:%S")
                    secret_details = {"Expiry Date": expiry_date}

                    if is_secret_expired(secret_properties):
                        expired = secret_expiry_details["expired"]
                        expired.append(secret_details)
                        secret_expiry_details["expired"] = expired

                    elif not is_secret_valid(secret_properties, days=15):
                        near_expiry = secret_expiry_details["near_expiry"]
                        near_expiry.append(secret_details)
                        secret_expiry_details["near_expiry"] = near_expiry
        except ResourceNotFoundError as e:
            secret_expiry_details["not_found"].append("secret not found")
            log.error(f"Error: {e.message}")

    return secret_expiry_details


def validate_secrets(workspace: Workspace) -> dict:
    """
    Validate the secrets expiration from azure keyvault.

    Args:
        workspace (Workspace): The workspace to validate secrets.

    Returns:
        dict: secrets with expiry and near expiry details.
    """
    log.info("Starting secrets validations....")
    tenant_id = workspace.get_details()["identity"]["tenant_id"]
    client_id = conf["global"]["sp_client_id"]
    credential = get_workspace_client_secret_credential(
        client_id=client_id,
        tenant_id=tenant_id,
    )
    secret_client = SecretClient(
        vault_url=f"https://{get_keyvault_name(workspace)}.vault.azure.net/",
        credential=credential,
    )
    return get_secrets_expiry_details(secret_client=secret_client)


if __name__ == "__main__":
    if not os.environ.get("AZURE_CLIENT_SECRET"):
        raise ValueError("AZURE_CLIENT_SECRET is not set")
    else:
        log.info("AZURE_CLIENT_SECRET is set")

    workspace = get_workspace(conf)
    secret_expiry_details = validate_secrets(workspace)

    secrets_not_found_df = pd.DataFrame(secret_expiry_details["not_found"], columns=["Secrets"])
    secrets_expired_df = pd.DataFrame(secret_expiry_details["expired"])
    secrets_near_expiry_df = pd.DataFrame(secret_expiry_details["near_expiry"])

    log.info("Creating workspace to share output..")
    Path("/tmp/workspace").mkdir(parents=True, exist_ok=True) #NOSONAR

    file_path = "/tmp/workspace/secret_expiry_details.json" #NOSONAR
    try:
        file_content = email_message_template.format(
            secret_not_found_content=(
                "No missing secret found"
                if secrets_not_found_df.empty
                else secrets_not_found_df.to_html()
            ),
            expired_secrets_content=(
                "No secrets are expired"
                if secrets_expired_df.empty
                else secrets_expired_df.to_html()
            ),
            near_expiry_secrets_content=(
                "No secrets are expiring in next 15 days"
                if secrets_near_expiry_df.empty
                else secrets_near_expiry_df.to_html()
            ),
        )
        with open(file_path, "x") as file:
            file.write(file_content)
    except FileExistsError:
        print(f"The file '{file_path}' already exists.")
        file.write(file_content)
