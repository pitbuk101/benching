"""All methods relating to creating and updating local and online models."""

import os
import pickle
from pathlib import Path

import pandas as pd

from ada.components.azureml import pipeline_steps
from ada.components.azureml.pipeline_steps import BertEmbeddingsTransformer
from ada.utils.logs.logger import get_logger

log = get_logger("create_upload_model")


def create_versioned_model_name(model_config: dict[str, str]) -> str:
    """Creates a versioned model in the Azure ML workspace.

    Args:
        model_config: The config settings for the model
    """
    model_version = model_config["version"]
    model_file_name = model_config["source"]
    return f"v{model_version}_{model_file_name}"


def get_local_model(model_config: dict) -> Path:
    """Generates and saves a machine learning model locally.

    This method reads training data from a specified file, generates embeddings,
    trains a new model, and saves it to the provided model path. It is typically
    called when a local model is not found during retrieval.

    Args:
        model_config: The config settings for the model
    Returns:
        model_path: The path to the saved model.
    """
    root_dir = Path(__file__).parents[4]

    model_dir = os.path.join(root_dir, "models")
    version_local_file_name = create_versioned_model_name(model_config)
    model_path = Path(model_dir, version_local_file_name)
    log.info("Model expected at %s", model_path)

    if not model_path.exists():
        log.info("Model not found locally, creating ...")
        train_model(model_path=model_path, root_dir=root_dir, **model_config)
    return model_path


def train_model(
    model_path: Path,
    root_dir: Path,
    training_data: str,
    encoding: str,
    training_column: str,
    class_column: str,
    model_function_name: str,
    **kwargs,
):
    """
    Create a local model based on the configurations of the model in the config file.
    Args:
        model_path: The path to the model file.
        root_dir: The root directory of the project.
        training_data: The name of the training data file.
        training_column: input column name that is used to train a model
        class_column: class column name that is used to train a model
        model_function_name: The name of the model function.
        **kwargs: Additional arguments to be passed to the model function.
    Raises:
        FileExistsError: If the training data file does not exist.
        IOError: If there is an issue in reading the training data or saving the model.

    """
    training_data_file = Path(root_dir, training_data)

    if not training_data_file.exists():
        raise FileExistsError(
            "Could not find the training set for the creation of the intent model.",
        )

    log.info("Extracting input data from %s", training_data_file)
    input_data = pd.read_csv(training_data_file, encoding=encoding)
    # train classifier model
    model_function = getattr(pipeline_steps, model_function_name)
    model_pipeline = pipeline_steps.generate_pipeline(
        model_function,
        BertEmbeddingsTransformer,
        kwargs,
    )
    trained_model = model_pipeline.fit(input_data[training_column], input_data[class_column])

    log.info("Finished training classifier model, storing to %s file", model_path)

    # save model
    with open(model_path, "wb") as path:
        pickle.dump(trained_model, path)
