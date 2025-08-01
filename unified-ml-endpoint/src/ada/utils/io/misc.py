"""Utils for knowledge extraction application."""

import os
import re
from datetime import datetime, timedelta
from typing import Dict, List
from dotenv import load_dotenv
import pandas as pd
import tiktoken

from ada.utils.logs.logger import get_logger


load_dotenv()
log = get_logger("utils")


def sort_dict_by_key(dictionary):
    """
    Sort a dictionary alphabetically by its keys and return the sorted dictionary.
    """
    sorted_dict = dict(sorted(dictionary.items()))
    return sorted_dict


def move_dict_key_to_top(key, my_dict):
    """
    Move the specified key to the top of the dictionary.
    """
    if key in my_dict:
        value = my_dict.pop(key)
        my_dict = {key: value, **my_dict}
    return my_dict


def num_tokens_from_messages(
    messages: List[Dict],
    model: str = "gpt-3.5-turbo-0301",
) -> int:
    """
    Returns the number of tokens used by a list of messages.
    Args:
        messages (List[Dict]): The list of messages to count tokens in.
        model (str): The OpenAI model to use. Defaults to gpt-3.5-turbo-0301.
    Returns:
        num_tokens (int): The number of tokens used by the messages.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        log.info("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        gpt_model = "gpt-3.5-turbo-0301"
        log.info(f"Warning:{model} may change over time. Returning num tokens assuming {gpt_model}")
        return num_tokens_from_messages(messages, model=gpt_model)
    if model == "gpt-4o":
        log.info(
            "Warning: gpt-4o may change over time. Returning num tokens assuming gpt-4o.",
        )
        return num_tokens_from_messages(messages, model="gpt-4o")
    if model == "gpt-3.5-turbo-0301":
        # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_message = 4
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4o":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(
            f"num_tokens_from_messages() is not implemented for model {model}. "
            f"See https://github.com/openai/openai "
            f"-python/blob/main/chatml.md for information on how messages are converted to tokens.",
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def synthesize_clauses_question(
    clause: str,
    alternative_clause: str,
    clause_definition: str,
    clause_typical_terms: str,
    clause_additional_explaination: str,
):
    """
    Synthesize the full clauses question based on the given definition elements

    Args:
        clause (str): clause name
        alternative_clause (str): clause alternative name
        clause_definition (str): clause definition
        clause_typical_terms (str): clause typical terms
        clause_additional_explaination (str): clause additional explaination

    Returns:
        A full question regarding the clause
    """
    question = f"Does the contract contain {clause}"
    if alternative_clause:
        question += f", alternatively known as {alternative_clause}"
    if clause_definition:
        question += f" which specifies {clause_definition}?"
    if clause_typical_terms:
        question += f" This clause typically contains terms like {clause_typical_terms}."
    if clause_additional_explaination:
        question += f" To elaborate further, this clause {clause_additional_explaination}."

    return question


def import_csv_sheet_for_clauses(question_file: str):
    """
    Importing a csv file containing the definitions of clauses

    Args:
        question_file (str): file path to the csv file

    Returns:
        list of clauses and respective questions extracted from the csv file
    """
    df_questions = pd.read_csv(question_file, keep_default_na=False)
    df_questions["question"] = df_questions.apply(
        lambda x: synthesize_clauses_question(
            x["Clause/section"],
            x["Alternative names for clause/section"],
            x["Definition"],
            x["Typical terms"],
            x["Additional Explaination"],
        ),
        axis=1,
    )
    list_clauses = df_questions["Clause/section"].to_list()
    list_questions = df_questions["question"].to_list()

    return list_clauses, list_questions


def import_csv_sheet_for_term_extraction(question_file):
    """Importing the excel sheet."""
    df_questions = pd.read_csv(question_file, header=0)
    df_questions["index_and_description"] = df_questions["Benchmark"].astype(
        str,
    )  # + "= Usually " + df["Value"].astype(str)
    numerical_factors = (
        str(
            df_questions.loc[
                df_questions["Qualitative or quantitative?"] == "Quantitative",
                "index_and_description",
            ].to_list(),
        )
        .lstrip("[")
        .rstrip("]")
        .replace("'", "")
    )

    trend_factors = (
        str(
            df_questions.loc[
                df_questions["Qualitative or quantitative?"] != "Quantitative",
                "index_and_description",
            ].to_list(),
        )
        .lstrip("[")
        .rstrip("]")
        .replace("'", "")
    )

    return [numerical_factors, trend_factors]


def clean_string(input_string: str, size_limit: int = 255) -> str:
    """Clean string to be used as a filename."""
    filename, _ = os.path.splitext(input_string)
    filename = re.sub("[^0-9a-zA-Z]+", "-", filename)
    return filename.lower()[:size_limit]


def fetch_string_within_triple_quote(text: str) -> str:
    """
    identify and return the  content within ```
    """
    pattern = r"```(.*?)```"
    # Use re.search to find the first match of the pattern in the text
    match = re.search(pattern, text, re.DOTALL)

    # Extract the matched text if a match is found
    if match:
        extracted_text = match.group(1)
        return extracted_text.strip()
    return text


def get_tenant_key_name(tenant_id: str) -> str:
    """
    Converts hyphen separated, alpha-numeric tenant_id to key_name
    """
    # Append "psql-" and truncating tenant_id as keyvault has 24 character
    # limit
    key_name = "psql-" + tenant_id[:19]
    return key_name


def get_storage_account_name_for_tenant(tenant_id: str, workspace: str) -> str:
    """
    Generates storage account name for a tenant.

    Args:
        tenant_id (str): The tenant ID.
        workspace (str): The workspace name.

    Returns:
        str: The generated storage account name.
    """
    tenant_id_part = tenant_id.replace("-", "")[:17]
    workspace_part = workspace.split("-")[-1]
    storage_account_name = tenant_id_part + workspace_part
    return storage_account_name


def get_storage_details(workspace: str, tenant_id: str) -> tuple:
    """
    Uses tenant_id, workspace name and constant suffix to generate storage key and client id
    """
    storage_account_name = get_storage_account_name_for_tenant(tenant_id, workspace)

    service_account_constant = "-service-account-secret-1"
    service_account_constant_secondary = "-service-account-secret-2"
    storage_sp_key = storage_account_name + service_account_constant
    storage_sp_key_secondary = storage_account_name + service_account_constant_secondary

    client_id_key = storage_account_name + "-client-id"
    return storage_account_name, storage_sp_key, storage_sp_key_secondary, client_id_key


def get_deployment_name(use_case: str) -> str:
    """
    Returns deployment name for use cases based on environment type
    Args:
        use_case: name of the use case

    Returns:
        Name of the deployment
    """
    env_type = os.getenv("ENV_TYPE")

    if env_type == "dev":
        deployment_name = f"sps-{use_case}-{env_type}"
    else:
        deployment_name = f"{use_case}-{env_type}"

    return deployment_name


def get_endpoint_url(base_url: str, deployment_name: str) -> str:
    """
    Returns endpoint name for use cases based on deployment_name
    Args:
        base_url: Url of the endpoint
        deployment_name: Name of the deployment

    Returns:
        Url of the endpoint
    """
    endpoint_url = base_url.replace("endpoint-name", deployment_name)
    return endpoint_url


def is_difference_greater_than_n_days(
    date1: str,
    date2: str,
    days: int = 15,
) -> bool:
    """
    Checks if difference between date1 and date2 is greater than number of days passed.

    Args:
        date1 (str): The first date in the format "%Y-%m-%d %H:%M:%S".
        date2 (str): The second date in the format "%Y-%m-%d %H:%M:%S".
        days (int, optional): The number of days to compare the difference against. Defaults to 15.
    Returns:
        bool: True if the difference between given dates is greater than days passed as arg.
    """
    first_date = datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
    second_date = datetime.strptime(date2, "%Y-%m-%d %H:%M:%S")
    return abs(first_date - second_date) > timedelta(days=days)
