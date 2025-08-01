import os

# from azure.core.exceptions import ClientAuthenticationError
# from azure.identity import ClientSecretCredential
# from azureml._vendor.azure_cli_core.azclierror import AuthenticationError
# from azureml.core.authentication import ServicePrincipalAuthentication
from dotenv import load_dotenv

load_dotenv()

from ada.utils.logs.logger import get_logger

logging = get_logger("Credentials")


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


def get_workspace_client_secret_credential(
    client_id: str,
    tenant_id: str,
    primary_secret: str,
    secondary_secret: str,
) -> ClientSecretCredential:
    """
    Get a ClientSecretCredential for Azure authentication.

    This function attempts to create a `ClientSecretCredential` using the provided primary secret.
    If the primary secret is invalid or expired, it falls back to using the secondary secret.

    Args:
        client_id (str): The client ID for the Azure service principal.
        tenant_id (str): The tenant ID for the Azure service principal.
        primary_secret (str | None): The primary client secret for the Azure service principal. Defaults to None.
        secondary_secret (str | None): The secondary client secret for the Azure service principal. Defaults to None.

    Returns:
        ClientSecretCredential: An authenticated `ClientSecretCredential` object for Azure.

    Raises:
        ClientAuthenticationError: If both the primary and secondary secrets are invalid or expired.
    """
    if not primary_secret:
        primary_secret = os.getenv("AZURE_CLIENT_SECRET")
    if not secondary_secret:
        secondary_secret = os.getenv("AZURE_CLIENT_SECRET_SECONDARY")

    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=primary_secret,
    )
    try:
        credential.get_token("https://vault.azure.net/.default")
    except ClientAuthenticationError as e:
        logging.warning(f"Primary secret has expired: {e}, using secondary secret")
        credential_secondary = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=secondary_secret,
        )
        credential_secondary.get_token("https://vault.azure.net/.default")
        return credential_secondary

    return credential
