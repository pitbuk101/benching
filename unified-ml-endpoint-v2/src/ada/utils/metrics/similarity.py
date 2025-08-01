"""
Similarity metric
"""

import re
from typing import List

import numpy as np
import pandas as pd
import spacy
from fuzzywuzzy import fuzz, process
from langchain_core.vectorstores import VectorStore
from sklearn.metrics.pairwise import cosine_similarity

from ada.components.llm_models.generic_calls import (
    generate_chat_response,
    generate_embeddings_from_string,
)
from ada.components.prompts.evaluation_prompts import similarity_prompt
from ada.utils.config.config_loader import read_config
from ada.utils.logs.time_logger import log_time

config = read_config("models.yml")


def get_similarity(
    input1: str,
    input2: str,
    model: str = config["gpt_long"],
    temperature: int = 0,
) -> str:
    """
    This metric will return the similarity between two statements inputted by the user
    Args:
        input1: Phrase 1 to compare
        input2: Phrase 2 to compare
        model: run the model completion which will give a result based on the following

    Returns: similarity, score

    """
    similarity = generate_chat_response(
        messages=similarity_prompt(input1, input2),
        model=model,
        temperature=temperature,
    )
    return similarity


@log_time
def similarity_search_from_vectorstore(
    vectorstore: VectorStore,
    search_string: str,
    no_of_docs_to_return: int,
    is_score_required=False,
) -> List:
    """
    This method will return the similarity search response from a vectorstore given a user input string
    Args:
        vectorstore (Any): Input Vectorstore
        search_string (str): String to be searched with
        no_of_docs_to_return (int): Number of documents to be returned as part of the response
        is_score_required (bool): flag to check if the similarity score is required

    Returns: List

    """
    if is_score_required:
        search_response = vectorstore.similarity_search_with_score(
            search_string,
            k=no_of_docs_to_return,
        )

    else:
        search_response = vectorstore.similarity_search(
            search_string,
            k=no_of_docs_to_return,
        )

    return search_response


@log_time
def get_similarity_score(
    first_string: str,
    second_string: str,
    model: str = "en_core_web_lg",
) -> float:
    """
    Uses a spacy model embeddings to find the similarity between two strings
    Args:
        first_string (str): string 1 to compare
        second_string (str): string 2 to compare
        model (str): name of spacy model
    Returns:
        (float) ratio of the similarity
    """
    if spacy.util.is_package(model):
        first_string = re.sub("[^A-Za-z0-9]+", "", first_string.lower())
        second_string = re.sub("[^A-Za-z0-9]+", "", second_string.lower())
        nlp = spacy.load(
            model,
            disable=[
                "parser",
                "attribute_ruler",
                "lemmatizer",
                "ner",
            ],
        )
        similarity_score = nlp(first_string).similarity(nlp(second_string))
        return similarity_score
    embedding1 = generate_embeddings_from_string(first_string, model)
    embedding2 = generate_embeddings_from_string(second_string, model)
    similarity_score = cosine_similarity(
        np.array(embedding1).reshape(1, -1),
        np.array(embedding2).reshape(1, -1),
    ).squeeze()
    return similarity_score


def remove_special_characters_string(string_val: str) -> str:
    """
    Removed special characters from string which mathcing
    Args:
        string_val (str): Input string value to remove special characters
    Returns:
        (str): Output string with special characters removed
    """
    return re.sub("[^A-Za-z0-9]+", "", string_val)


def partial_match(string_val1: str, string_val2: str) -> float:
    """
    Get partial match between two strings
    Args:
        string_val1 (str): Input string 1 for matching
        string_val2 (str): Input string 2 for matching
    Returns:
        (float): Partial match ratio between two strings
    """
    return fuzz.ratio(string_val1, string_val2)


def compute_spacy_similarity_score_from_list(
    compare_dataframe: pd.DataFrame,
    phrase: str,
    similarity_model: str,
    threshold: float,
    default_value: str = "",
) -> str:
    """
    Computes the similarity score from list using spacy model
    Args:
        compare_dataframe (pd.Dataframe): Dataframe with each row containing
        one item to be compared against the phrase
        phrase (str):phrase to be matched
        similarity_model (str): spacy model to use for generating similarity
        threshold (float): Value below which a similarity is not considered
        default_value (str): default value string
    Returns:
        (str): Best matching key from the given list else default_value
    """
    nlp = spacy.load(
        similarity_model,
        disable=[
            "parser",
            "attribute_ruler",
            "lemmatizer",
            "ner",
        ],
    )
    formatted_list = compare_dataframe["compare"].to_list()
    original_list = compare_dataframe["original"].to_list()
    phrase = nlp(phrase)
    ratios = [val.similarity(phrase) for val in nlp.pipe(formatted_list)]
    matches = np.argmax(ratios)
    return original_list[matches] if ratios[matches] > threshold else default_value


def compute_llm_similarity_score_from_list(
    list_val: list,
    phrase: str,
    similarity_model: str,
    threshold: float,
    default_value: str = "",
) -> str:
    """
    Computes the similarity score from list using spacy model
    Args:
        list_val (list): List to which we need to fuzzy match the phrase
        phrase (str):phrase to be matched
        similarity_model (str): llm model for generating similarity
        threshold (float): Value below which a similarity is not considered
        default_value (str): default value string
    Returns:
        (str): Best matching key from the given list else default_value
    """
    embedding1 = generate_embeddings_from_string(phrase.lower(), similarity_model)
    embedding2 = [generate_embeddings_from_string(x.lower(), similarity_model) for x in list_val]
    ratios = cosine_similarity([embedding1], embedding2).squeeze()
    matches = np.argmax(ratios)
    return list_val[matches] if ratios[matches] > threshold else default_value


def compute_fuzzy_similarity_score_from_list(
    compare_dataframe: pd.DataFrame,
    phrase: str,
    threshold: float,
    default_value: str = "",
) -> str:
    """
    Computes the similarity score from list using spacy model
    Args:
        compare_dataframe (pd.Dataframe): Dataframe with each row comtaining
        one item to be compared against the phrase
        phrase (str):phrase to be matched
        threshold (float): Value below which a similarity is not considered
        default_value (str): default value string
    Returns:
        (str): Best matching key from the given list else default_value
    """
    dataframe_column = pd.DataFrame([phrase], columns=["match"])
    dataframe_column["key"] = 1
    compare_dataframe["key"] = 1
    combined_dataframe = dataframe_column.merge(
        compare_dataframe,
        on="key",
        how="left",
    )
    combined_dataframe = combined_dataframe[
        ~(combined_dataframe.match == combined_dataframe.compare)
    ]
    partial_match_vector = np.vectorize(partial_match)
    combined_dataframe["score"] = partial_match_vector(
        combined_dataframe["match"],
        combined_dataframe["compare"],
    )
    combined_dataframe = combined_dataframe[combined_dataframe.score >= 100 * threshold]
    if len(combined_dataframe) > 0:
        return combined_dataframe.head(1)["original"].values
    return default_value


@log_time
def get_best_match_from_list(
    list_val: list,
    phrase: str,
    similarity_model: str,
    threshold: float,
    default_value: str = "",
) -> str:
    """
    Gets the best match to the given list if greater than a threshold
    else default string
    Args:
        list_val (list): List to which we need to fuzzy match the phrase
        phrase (str):phrase to be matched
        similarity_model (str): fuzzy-wuzzy or spacy model to use for
                                 generating similarity
        threshold (float): Value below which a similarity is not considered
        default_value (str): default value string
    Returns:
        (str): Best matching key from the given list else default_value
    """
    if list_val and phrase:
        compare = pd.DataFrame(
            {"compare": list_val, "original": list_val},
            columns=["compare", "original"],
        )
        compare["compare"] = (
            compare["compare"]
            .str.lower()
            .apply(
                remove_special_characters_string,
            )
        )
        phrase = remove_special_characters_string(phrase.lower())

        if spacy.util.is_package(similarity_model):
            return compute_spacy_similarity_score_from_list(
                compare_dataframe=compare,
                phrase=phrase,
                similarity_model=similarity_model,
                threshold=threshold,
                default_value=default_value,
            )
        elif similarity_model == "text-embedding-ada-002":
            return compute_llm_similarity_score_from_list(
                list_val=list_val,
                phrase=phrase,
                similarity_model=similarity_model,
                threshold=threshold,
                default_value=default_value,
            )
        return compute_fuzzy_similarity_score_from_list(
            compare_dataframe=compare,
            phrase=phrase,
            threshold=threshold,
            default_value=default_value,
        )
    return default_value


def get_fuzzy_match_from_list(
    input_str: str,
    input_list: list[str] = [],
    threshold: int = 85,
    default=None,
) -> str:
    """
    Find the closest matching string from a given list using fuzzy matching.

    Args:
        input_str (str): The raw input string to match against the list.
        input_list (list[str], optional): The list of strings to match against.
        threshold (int, optional): Range is (0-100) required to consider a match. Defaults to 85.

    Returns:
        str | None: The closest matching string if a match exceeds the threshold; otherwise, None.
    """
    if input_list:
        match, score = process.extractOne(input_str, input_list)
        if score > threshold:
            return match
    return default


def get_fuzzy_match_with_custom_comparison(
    input_str: str,
    input_list: list[str] | None = None,
    threshold: int = 80,
) -> list[str]:
    """
    Find the closest matching string from a given list using a custom comparison method.

    This function uses multiple fuzzy matching techniques to find the best match for the input string
    from a list of strings. It calculates the match score using `fuzz.WRatio`, `fuzz.token_set_ratio`,
    and `fuzz.token_sort_ratio` from the `fuzzywuzzy` library and returns the best match if the score
    exceeds the specified threshold.

    Args:
        input_str (str): The raw input string to match against the list.
        input_list (list[str], optional): The list of strings to match against. Defaults to None.
        threshold (int, optional): The minimum score (0-100) required to consider a match. Defaults to 85.

    Returns:
        list[str] | None: The closest matching string if a match exceeds the threshold; otherwise, None.
    """
    if not input_list:
        return []
    score_list = [
        (
            option,
            fuzz.WRatio(option.lower(), input_str.lower()),
            fuzz.token_set_ratio(option.lower(), input_str.lower()),
        )
        for option in input_list
    ]
    sorted_score_list = sorted(score_list, key=lambda x: (x[1], x[2]), reverse=True)

    if sorted_score_list[0][1] < threshold:
        return []

    first_score, second_score = sorted_score_list[0][1], sorted_score_list[0][2]

    return [
        data[0] for data in sorted_score_list if data[1] == first_score and data[2] == second_score
    ]
