import json
import os

from ada.azml_realtime_deployments.intent_model_v2_deployment import (
    init as intent_model_v2_deployment_init,
)
from ada.azml_realtime_deployments.intent_model_v2_deployment import (
    run as intent_model_v2_deployment_run,
)
from ada.utils.azml.azml_utils import set_openai_api_creds
from ada.utils.config.config_loader import read_config

# from ada.utils.format.format import transform_json
from ada.utils.io.function_mapping import function_mapping
from ada.utils.logs.logger import get_logger
from ada.utils.metrics.context_manager import UseCase

conf = read_config("realtime-params.yml")
log = get_logger("endpoint_wrapper")


def call_local_endpoint(endpoint_mapping: dict) -> dict:
    """
    Takes the end_point and function mapping to produce an output locally
    Args:
        endpoint_mapping (dict): The endpoint mapping dict with the name and payload
    Returns:
        (dict) Response from endpoint
    """
    func_mapping = function_mapping()
    func_mapping.update(
        {
            "sps-intent-model-v2": {
                "init": intent_model_v2_deployment_init,
                "run": intent_model_v2_deployment_run,
                "use_case": UseCase.INTENT_CLASSIFY,
            },
        },
    )

    name = endpoint_mapping.get("endpoint", "")
    payload = str(endpoint_mapping.get("payload"))

    # MI:08102024:To handle camelcase payload from realtime-params.yml
    # name = endpoint_mapping.get("endpoint")
    # payload = json.dumps(transform_json(json.loads(endpoint_mapping.get("payload"))))

    set_openai_api_creds(
        {
            "openai_api_key": os.getenv("AZURE_OPENAI_API_KEY"),
        },
    )

    func_mapping[name]["init"]()
    response = func_mapping[name]["run"](payload)

    use_case = (json.loads(payload) or {}).get("use_case", "")
    if use_case:
        name = "-".join([name, use_case])

    log.info("Response from %s endpoint: %s", name, json.dumps(response, indent=2))
    return response


if __name__ == "__main__":
    for mapping in conf["endpoint-mapping"]:
        call_local_endpoint(mapping)
