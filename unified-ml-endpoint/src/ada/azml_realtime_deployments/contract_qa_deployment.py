"""Azure ML Endpoint for QnA deployment."""

import pathlib
import sys

# pylint: disable=C0413
sys.path.append(str(pathlib.Path(__file__).parents[2]))
# pylint: enable=C0413

from ada.components.azureml.azml_model import RetrieveModel  # noqa: E402
from ada.use_cases.contract_qa.contract_qa import run_contract_qa  # noqa: E402
# from ada.utils.azml.azml_utils import pop_excess_environment_variables  # noqa: E402
from ada.utils.config.config_loader import read_config  # noqa: E402
from ada.utils.logs.logger import get_logger  # noqa: E402

log = get_logger("contract_qna_deployment")


def init():
    """Azure Realtime deployment for contract qa"""
    global question_classifier_model
    # pop_excess_environment_variables()
    log.info("Retrieving the model")
    model_conf = read_config("azml_deployment.yaml")["models"]["contract_qna_classifier"]
    question_classifier_model = RetrieveModel(model_conf).retrieve_model()
    log.info("classifier model type (%s)", type(question_classifier_model))
    log.info("model config: %s", model_conf)


def run(json_file: str, model: RetrieveModel = None) -> dict:
    """Entrypoint function.
    Args:
        json_file (str): The json dumps str of the input payload
        model (RetrieveModel):  Question classifier model
    Return:
        (dict): Model output response
    """
    if model:
        global question_classifier_model
        question_classifier_model = model  # type: ignore

    return run_contract_qa(
        json_file_str=json_file,
        question_classifier_model=question_classifier_model,  # type: ignore
    )
