"""All functions which are used to create pipeline steps
Like creating embeddings of string column, train model with different classifier
"""
from typing import Callable

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

from ada.components.vectorstore.embedding import Embedding


def generate_pipeline(
    classifier: Callable, processing_function: Callable, model_params: dict
) -> Pipeline:
    """create classifier model for intent classification of main user question.

    Args:
        classifier: estimator of the pipeline
        processing_function: transformer function that changes input according to estimator need
        model_params: dictionary of model parameters like embeddings, rf_params, svc_params, etc
    Returns:
        Random Forest Model set with model param
    """
    return Pipeline( # NOSONAR
        steps=[
            ("transformed_column", processing_function(model_params["embedding"])),
            ("classifier", classifier(model_params)),
        ]
    ) 


def voting_classifier(model_params: dict) -> object:
    """create classifier model for contract qna question classification

    Args:
        model_params: dictionary of model parameters like n_estimators, max_depth, etc

    Returns:
        Random Forest Model set with model param
    """
    rf_classifier = RandomForestClassifier(**model_params["rf_params"]) # NOSONAR
    svm_classifier = SVC(**model_params["svc_params"]) # NOSONAR

    return VotingClassifier(
        estimators=[("rf", rf_classifier), ("svm", svm_classifier)],
        voting="soft",
        weights=model_params.get("weights", [1, 1]),
    )


class BertEmbeddingsTransformer(BaseEstimator, TransformerMixin):
    """Transforms input text data into BERT embeddings.

    Args:
        embedding_param (dict): Dictionary of embedding parameters, including
            'embedding_model_type', 'tokenizer', and 'embedding_model'.

    Attributes:
        embedding_param (dict): Dictionary of embedding parameters.

    Methods:
        fit(X, y=None): Fit the transformer.
        transform(X: pd.Series): Transform the input text data into BERT embeddings.

    Returns:
        np.array: Array of BERT embeddings.
    """

    def __init__(self, embedding_param: dict):
        self.embedding_param = embedding_param

    # pylint: disable=W0613
    def fit(self, train_x, train_y=None): # NOSONAR
        """Fit the transformer.
        This method is a part of the scikit-learn transformer interface and is
        implemented as a no-op since BERT embeddings are not learned from the data.

        Args:
            train_x: Input data.
            train_y: Target labels (ignored).

        Returns:
            BertEmbeddingsTransformer: The fitted transformer.
        """
        return self

    def transform(self, text_input: pd.Series):
        """Transform the input text data into BERT embeddings.

        Args:
            text_input (pd.Series): Input text data.

        Returns:
            np.array: Array of BERT embeddings.
        """
        max_len = text_input.str.len().max()
        embedder = Embedding(
            self.embedding_param["embedding_model_type"],
            tokenizer=self.embedding_param["tokenizer"],
            bert_model=self.embedding_param["embedding_model"],
            max_length=max_len,
        )
        embeddings = text_input.apply(lambda x: np.squeeze(embedder.create_embeddings(x)))
        return np.array(embeddings.tolist())


def predict(model_pipeline: Pipeline, input_questions: pd.Series) -> pd.Series:
    """
    Predicts the question type based on the provided classifier pipeline.

    Args:
        model_pipeline (Pipeline): The pipeline object containing the classifier.
        input_questions (pd.Series): A pandas Series containing the list of questions to predict
                                    the type.

    Returns:
        pd.Series: A pandas Series with the predicted question types.
    """
    return model_pipeline.predict(input_questions)
