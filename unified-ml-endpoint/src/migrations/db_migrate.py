import os
import sys
from dotenv import load_dotenv
from alembic import command
from alembic.config import Config
from constants import (
    DB_HOST,
    DB_NAME,
    DB_PORT,
    DB_SECRET,
    DB_USER,
    TENANT_LIST,
)
load_dotenv()
# flake8: noqa: E402


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

# !! This code is commented out since we are not calling any azure postgres server
# from azure.keyvault.secrets import SecretClient

from ada.components.azureml.workspace import get_workspace
# from ada.utils.authorization.credentials import get_workspace_client_secret_credential
# from ada.utils.azml.azml_utils import get_keyvault_name
from ada.utils.config.config_loader import read_config, set_component_args

conf = read_config("azml_deployment.yaml")
if os.getenv("LOCAL_DB_MODE") == "1":
    pg_credentials = {"host": "0.0.0.0", "user": "postgres", "dbname": "postgres", "port": "5432"}
else:
    pg_credentials = read_config("pg_credentials.yml")

# !! This code is commented out since we are not calling any azure postgres server
# secrets_conf = read_config("secrets.yml")
# admin_password_key = secrets_conf["psql_admin_password"]

# !! Removing this code from here since we are not calling any azure postgres server
# def get_db_secret():
#     if os.getenv("LOCAL_DB_MODE") == "1":
#         return "postgres"
#     workspace = get_workspace(conf)
#     tenant_id = workspace.get_details()["identity"]["tenant_id"]
#     client_id = conf["global"]["sp_client_id"]
#     credential = get_workspace_client_secret_credential(
#         client_id=client_id,
#         tenant_id=tenant_id,
#     )
#     secret_client = SecretClient(
#         vault_url=f"https://{get_keyvault_name(workspace)}.vault.azure.net/",
#         credential=credential,
#     )
#     secret = secret_client.get_secret(admin_password_key).value
#     secret = secret.replace("@", "%40")
#     secret = secret.replace("%", "%%")
#     return secret


def run_migrations():
    """
    Start running DB migrations
    """
    alembic_cfg = Config("./src/migrations/common_migrations/alembic.ini")
    command.upgrade(alembic_cfg, "head")

    alembic_cfg = Config("./src/migrations/tenant_migrations/alembic.ini")
    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    args = set_component_args("src/migrations/migrate_pipeline_conf.json")
    os.environ[TENANT_LIST] = args.tenant_list

    # !! This code is commented out since we are not calling any azure postgres server
    # os.environ[AZURE_CLIENT_SECRET] = args.azure_client_secret
    # os.environ[AZURE_CLIENT_SECRET_SECONDARY] = args.azure_client_secret_secondary

    os.environ[DB_HOST] = pg_credentials["host"]
    os.environ[DB_PORT] = str(pg_credentials["port"])
    os.environ[DB_SECRET] = os.getenv('PGPASSWORD')
    os.environ[DB_NAME] = pg_credentials["dbname"]
    os.environ[DB_USER] = pg_credentials["user"]

    run_migrations()
