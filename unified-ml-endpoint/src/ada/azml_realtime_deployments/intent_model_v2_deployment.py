"""Azure ML Endpoint for Intent Model v2 deployment."""

# flake8: noqa: E402

import os
import pathlib
import sys
from typing import Any

# pylint: disable=C0413
sys.path.append(str(pathlib.Path(__file__).parents[2]))
# pylint: enable=C0413


from ada.azml_realtime_deployments.key_facts_deployment_v2 import read_context
from ada.azml_realtime_deployments.negotiation_factory_deployment import (
    read_reference_data,
)
from ada.components.azureml.azml_model import RetrieveModel
from ada.use_cases.intent_classification.intent_classification_v2 import (
    run_unified_model,
)

from ada.utils.migrations.utils import pop_excess_environment_variables
from ada.use_cases.key_facts.configuration import Configuration
# from ada.utils.azml.azml_utils import pop_excess_environment_variables
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger

conf = read_config("use-cases.yml")
intent_model_conf = conf["intent_model_v2"]
data_dir = os.path.join(pathlib.Path(__file__).parents[3], "data")

contract_qa_question_classifier_model: Any
category_configuration: Configuration
all_reference_data: dict[str, Any]
log = get_logger("intent_model_v2_deployment")

def init():
    """AWS Realtime deployment for Idea generation."""
    # To handle library upgrades
    log.info('intent_model_v2_deployment init')

    log.info("Populating environment variables")
    pop_excess_environment_variables()

    # pylint: disable=global-statement
    global contract_qa_question_classifier_model, category_configuration, all_reference_data
    # pylint: enable=global-statement

    model_conf = read_config("azml_deployment.yaml")["models"]["contract_qna_classifier"]
    log.info(f"Model configuration: {model_conf}")
    # contract_qa_question_classifier_model = RetrieveModel(model_conf).retrieve_model()
    category_configuration = read_context()
    log.info(f"Category configuration: {category_configuration}")
    all_reference_data = {"negotiation-factory": read_reference_data()}


def run(json_data: str):
    """Entrypoint function."""
    log.info("Running intent model v2 deployment through run_unified_model")
    try:
        log.info(f"Input data: {json_data}")
        log.info(f"Category configuration: {category_configuration}")
        return run_unified_model(
            json_data=json_data,
            category_configuration=category_configuration,
            # question_classifier_model=contract_qa_question_classifier_model,
            all_reference_data=all_reference_data,
        )
    except Exception:
        log.info("Error running intent model v2 deployment")
        raise
        