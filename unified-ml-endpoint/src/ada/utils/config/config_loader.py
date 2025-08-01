"""
Reading config files
"""

import argparse
import json
import logging
import os
import pathlib
from pathlib import Path
from typing import Any, Dict

import yaml  # type: ignore

log = logging.getLogger("config_loader")


env_type_storage_account_map = {
    "dev": "storage_config_dev.yml",
    "staging": "storage_config_stage.yml",
    "prod-eu": "storage_config_prod_EU.yml",
    "prod-us": "storage_config_prod_US.yml",
}


def get_tenant_list_for_the_workspace() -> list[str]:
    """
    Fetches the list of tenant IDs for the current workspace based on the environment type.

    Returns:
        list[str]: A list of tenant IDs.
    """
    env_type = 'dev'
    if not env_type:
        raise ValueError("Env type not set")
    storage_accounts_folder_path = Path(Path(__file__).parents[4], "")
    path = Path(storage_accounts_folder_path, env_type_storage_account_map.get(env_type, ""))

    with open(path, encoding="utf8") as storage_account_config_file:
        storage_accounts_conf = yaml.safe_load(storage_account_config_file)
        return storage_accounts_conf.get("ancillary_storage_accounts", [])


def set_component_args(config_file="src/ada/azml_components/azml_conf.json"):
    """
    Parse input arguments from a JSON configuration file.
    Args:
        config_file (str): Path to the JSON configuration file.
    Returns:
        argparse.Namespace: Parsed arguments as an argparse namespace.
    """

    base_path = pathlib.Path(__file__).parents[4]
    conf_path = os.path.join(base_path, config_file)

    with open(conf_path, encoding="utf-8") as config_json:
        config = json.load(config_json)

    parser = argparse.ArgumentParser()

    # Define arguments based on the configuration
    for arg_name, arg_config in config.items():
        parser.add_argument(
            f"--{arg_name}",
            type=arg_config.get("type", str),
            required=arg_config.get("required", False),
            default=arg_config.get("default", None),
            help=arg_config.get("help", None),
        )

    args, _ = parser.parse_known_args()
    return args


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
        raise ValueError("Env type not set")

    conf_folder_path = Path(Path(__file__).parents[4], "conf")
    path = Path(conf_folder_path, env_type, file_path)

    if not path.exists():
        path = Path(conf_folder_path, "common", file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"{file_path} configuration file not found: in {conf_folder_path}/{env_type} or "
                f"{conf_folder_path}/local",
            )

    with open(path, encoding="utf8") as config_file:
        config = yaml.safe_load(config_file)
    return config
