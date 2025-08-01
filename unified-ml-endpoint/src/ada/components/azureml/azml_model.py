"""Module to Use Azure ML model for intent classification."""
import logging
import os
from pathlib import Path
from typing import Any, Dict

import joblib
# from azureml.core import Model

from ada.components.azureml.create import get_local_model
# from ada.components.azureml.workspace import get_workspace
from ada.utils.config.config_loader import read_config

conf = read_config("azml_deployment.yaml")
log = logging.getLogger("azml_model_deployment")


# pylint: disable=too-few-public-methods
class RetrieveModel:
    """Represents an interface for interacting with  OPENAI's Machine Learning models.

    This class provides methods to retrieve and generate machine learning models
    either locally or via cloud services, based on a provided configuration.
    It supports operations like retrieving a pre-trained model from AWS or generating
    a new model from local training data.

    Attributes:
        model_config (Dict[str, Any]): Configuration dictionary containing model specifications.
        root_dir (Path): The root directory path for the model operations.
    """

    def __init__(self, model_config: Dict[str, Any]):
        """Initializes the RetrieveModel instance with provided model configuration.

        The constructor sets up the model configuration and determines the root directory
        for model-related operations, which is a few levels up from the current file's directory.

        Args:
            model_config (Dict[str, Any]): A dictionary containing configuration details such as
                                           model name, version, local paths, and training data
                                           information.
        """
        self.model_config = model_config
        self.root_dir = Path(__file__).parents[4]

    def retrieve_model(self) -> object:
        """Retrieves a machine learning model based on the current environment configuration.

        If running in a local model mode (determined by an environment variable), the method
        tries to load the model from a local path. If the local model doesn't exist, it triggers
        its generation. In a cloud environment, it authenticates with Azure and retrieves the
        model from the Azure ML workspace.

        Returns:
            object: The loaded machine learning model.

        Raises:
            FileNotFoundError: If the model file does not exist in the expected path.
            EnvironmentError: If there is an issue with Azure environment setup.
        """
        # print(os.getenv("LOCAL_MODEL_MODE"))
        if os.getenv("LOCAL_MODEL_MODE"):
            print(self.model_config)
            model_path = get_local_model(self.model_config)
        # ** Disabling this flow since we are moving to AWS now. This is Azure flow, will look into this going forward. if required **
        # else:
        #     workspace = get_workspace(conf)
        #     model_path = Model.get_model_path(
        #         self.model_config["model_name"],
        #         version=self.model_config["version"],
        #         _workspace=workspace,
        #     )
        # print(model_path)
        return joblib.load(model_path)
