"""Conftest for tests"""

import os
from dotenv import load_dotenv
from ada.components.azureml.workspace import get_workspace
from ada.utils.config.config_loader import read_config

load_dotenv()
component_conf = read_config("models.yml")


def pytest_sessionstart(session):
    """
    Set openai configuration from config
    """

    model_conf = read_config("models.yml")
    secrets_conf = read_config("secrets.yml")
    conf = read_config("azml_deployment.yaml")

    openai_api_key_not_exists = os.getenv("AZURE_OPENAI_API_KEY") is None
    if openai_api_key_not_exists:
        print("\033[31mFetching OPENAI_KEY to perform tests\033[0m")
        print(
            """
              \033[31m
              If you are seeing this message in local development environment, it means that you do not have AZURE_OPENAI_API_KEY
              set in your environment variable. Please get the key from the dev vault and store it, else every test run which
              from local will access key vault for the open ai key. This feature is implemented to avoid maintaining
              the azure endpoint and key in the circle CI contexts
               \033[0m
              """,
        )
        workspace = get_workspace(conf)
        key_vault = workspace.get_default_keyvault()
        openai_api_key = key_vault.get_secret(secrets_conf["openai_api_key"])
        os.environ["AZURE_OPENAI_API_KEY"] = openai_api_key
        print("\033[31mOPENAI_KEY: Fetched successfully\033[0m")

    os.environ["OPENAI_API_VERSION"] = model_conf["openai_api_version"]
    os.environ["AZURE_OPENAI_ENDPOINT"] = model_conf["open_api_base_url"]
