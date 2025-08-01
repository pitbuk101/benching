"""Leakage extraction component for preprocessing pipeline"""

import json
from json import JSONDecodeError
from typing import Any, Optional

import pandas as pd
from fuzzywuzzy import fuzz
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.vectorstores import VectorStore

from ada.components.llm_models.generic_calls import (
    create_qa_chain,
    generate_chat_response,
    run_qa_chain,
)
from ada.components.vectorstore.vectorstore import VectorStoreFactory
from ada.use_cases.leakage.prompts import (
    find_sku_id_prompts,
    search_currency_code_prompts,
    search_currency_code_query,
    table_analyzation_prompts,
)
from ada.use_cases.negotiation_factory.negotiation_factory_utils import json_regex
from ada.utils.config.config_loader import read_config
from ada.utils.format.format import format_price
from ada.utils.io.misc import fetch_string_within_triple_quote
from ada.utils.logs.logger import get_logger
from ada.utils.metrics.context_manager import (
    UseCase,
    set_tenant_and_intent_flow_context,
)

log = get_logger("leakage")
leakage_conf = read_config("use-cases.yml")["leakage"]


def extract_currency_code(
    vector_store: VectorStore,
    chain_config: dict[str, Any],
) -> Any | str | None:
    """
    It runs Retrieval QA chain on the vector store
    and extracts the transaction currency code from the document.
    Args:
        vector_store (VectorStore): vectorstore used for document search
        chain_config (dict[str, Any]): configuration with details
                                like model name, search type, temperature etc
    Returns:
        (Any | str | None): extracted currency code from the document

    """
    retriever = vector_store.as_retriever(
        search_type=chain_config["search_type"],
        search_kwargs=chain_config["search_kwargs"],
    )
    prompt = search_currency_code_prompts()
    qa_chain = create_qa_chain(
        retriever=retriever,
        prompt=prompt,
        model=chain_config["model_name"],
        temperature=chain_config["temperature"],
    )
    probable_currencies = []
    for query in search_currency_code_query():
        qa_chain_output = run_qa_chain(qa_chain, query)
        log.info("Entity Output from AI: %s", qa_chain_output)
        try:
            currency_code = json.loads(qa_chain_output).get("currency_code", "")
        except JSONDecodeError:
            currency_code = json_regex(qa_chain_output, ["currency_code"]).get("currency_code", "")

        probable_currencies.append(currency_code or "")

    currency_code_from_contract = max(
        (currency for currency in probable_currencies if currency.strip()),
        key=probable_currencies.count,
        default=None,
    )
    log.info("extracted currency code: %s", currency_code_from_contract)
    currency_code_from_contract = (
        currency_code_from_contract
        if currency_code_from_contract is None or currency_code_from_contract == ""
        else "USD"
    )
    return currency_code_from_contract


def analyze_table_using_llm(
    doc_tables_df: list[pd.DataFrame],
    sku_list: list[dict[str, str]],
    retries: int = 2,
) -> list[dict]:
    """
    This function matches table metadata and sample rows with specified columns,
    and extracts additional relevant information such as price, transaction type, and currency.

    Args:
        doc_tables_df (list[pd.DataFrame]): A list of tables ( in form of dataframe)
                                        extracted from the document.
        sku_list (list[dict[str, str]]):  A list of SKU related to the document,
                    containing information such as SKU ID, code, and description
        retries (int): number of retry to get proper output

    Returns:
        (list[dict]): A list of dictionaries containing the required information,
                derived from the output of the LLM by analyzing the tables.

    """
    log.info("Starting analyzation table")
    table_analyzer_prompt = table_analyzation_prompts(
        doc_tables_df,
        leakage_conf["columns_of_interest"],
        original_codes=[
            sku_detail.get("code", sku_detail.get("id", "")) for sku_detail in sku_list
        ],
    )
    log.info("generating response with Retry count: %s", retries)
    while retries > 0:
        ai_response = generate_chat_response(
            table_analyzer_prompt,
            model=leakage_conf["model"],
            parser=JsonOutputParser(),
        )

        log.info("AI response after analyzing tables: %s", ai_response)
        if ai_response:
            analyzed_tables = ai_response
            log.info("Extracted table details: %s", analyzed_tables)
            return analyzed_tables
        log.error("AI response has failed for ai response: \n%s", ai_response)
        log.info("Retrying to analyze tables")
        retries -= 1
    return []


def find_sku_id_without_llm(
    index: int,
    original_code: Optional[str],
    description: str,
    sku_list: list[dict[str, str]],
) -> tuple[str, Optional[int], dict[str, str]]:
    """
    This function compares the original code with the code from a SKU list.
    If a match is found, it returns the corresponding SKU ID.
    If no match is found or original code is None,
    it performs a fuzzy match between the input description \
    and the description from the SKU details.
    If the fuzzy match score is more than 95, it returns the SKU ID.
    Else it returns NA
    Also for all sku_id with match score more than 70 added to filtered sku

    Args:
        index (int): index of the row
        original_code (Optional[str]): The code obtained from the contract table.
        description (str):  The description obtained from the contract table.
        sku_list (list[dict[str, str]]): A list of SKU details,
                including SKU ID, code, and description, retrieved from the SpendsAcme database.
        filtered_sku (dict[str, Any]): Dict to update
        unmatched_rows_index (list[int]): index of the row if there is no match in sku id

    Returns:
        (tuple[str, Optional[int], dict[str, str]]): The matched SKU ID if a match is found,
        otherwise None, index or none and probable sku details

    """
    if original_code is not None:
        if ( # NOSONAR
            sku_id := next(
                (
                    sku_details["id"]
                    for sku_details in sku_list
                    if sku_details.get("code", sku_details.get("id", "")) == original_code
                ),
                None,
            )
        ) is not None:
            return sku_id, None, {}
    fuzzy_match_output = [
        (
            fuzz.ratio(sku_details["description"].lower(), description.lower()),
            sku_details["id"],
            sku_details["description"],
        )
        for sku_details in sku_list
    ]
    top_score, closest_sku_id, sku_description = max(fuzzy_match_output)

    if top_score > 95:
        log.info(
            "description from contract: '%s', best match description: '%s' with score '%s'",
            description,
            sku_description,
            top_score,
        )
        return closest_sku_id, None, {}
    probable_sku_details = {
        sku_id: description for score, sku_id, description in fuzzy_match_output if score > 70
    }
    return "No Match Found", index, probable_sku_details


def find_sku_id_with_llm(
    unmatched_rows_df: pd.DataFrame,
    filtered_sku_for_unmatched_rows: dict[str, Any],
    retries: int,
) -> dict[str, str]:
    """
    This function attempts to find the SKU ID using LLM method.
    If no match returns a blank dict

    Args:
        unmatched_rows_df (pd.DataFrame): A DataFrame containing rows of descriptions
                    where no SKU ID match was found.
        filtered_sku_for_unmatched_rows (dict[str, Any]):  A dictionary of SKUs that have the
                        highest probability of matching with the descriptions in the DataFrame.
        retries (int): number of retry to avoid failure

    Returns:
        (dict[str, str]): dict with index of df along with matched sku id from LLM
    """
    while retries > 0:
        find_sku_id_prompt = find_sku_id_prompts(
            unmatched_rows_df=unmatched_rows_df,
            filtered_sku_df=pd.DataFrame(
                list(filtered_sku_for_unmatched_rows.items()),
                columns=["sku_id", "description"],
            ),
        )

        ai_response = generate_chat_response(find_sku_id_prompt, model=leakage_conf["long_model"])
        log.info("Ai response for the description matching: %s", ai_response)
        try:
            matched_sku_dict = json.loads(fetch_string_within_triple_quote(ai_response))
            return matched_sku_dict
        except JSONDecodeError:
            retries -= 1
    return {}


def run_leakage( # NOSONAR
    document_id: int,
    document_type: str,
    sku_list: list[dict[str, str]],
    df_doc_tables: list[pd.DataFrame],
    df_doc_chunks: pd.DataFrame,
    tenant_id: str,
) -> pd.DataFrame:
    """
    Extracts leakage information from a list of tables and constructs a DataFrame
    that includes the document_id, description, price, and quantity.

    Args:
        document_id (int): id of the given document
        document_type (str): type of the given document
        sku_list (list[dict[str, str]]): list of sku id along with their description and code
        df_doc_tables (list[pd.DataFrame]): list of pandas dataframe
                                    which are tables extracted from given document
        df_doc_chunks (pd.DataFrame): DataFrame containing document chunks
    Returns:
        (pd.DataFrame): pandas dataframe consist of leakage information
    """
    set_tenant_and_intent_flow_context(tenant_id, UseCase.CONTRACT_LEAKAGE)

    log.info("Initializing leakage")
    vector_store_factory = VectorStoreFactory()
    vector_store = vector_store_factory.faiss_from_embeddings(doc_chunk=df_doc_chunks)
    leakage_df = pd.DataFrame(columns=leakage_conf["contract_sku_details_table_columns"])
    if document_type.lower() != "contract":
        log.info("Not running Leakage extraction as document type is %s ", document_type)
    elif not df_doc_tables:
        log.info("Nothing to process in given doc . Empty list of tables received. ")
    elif analyzed_tables := analyze_table_using_llm(df_doc_tables, sku_list):
        log.info("Tables received from OCR: %s", df_doc_tables)
        log.info("Analyzed table details: %s", analyzed_tables)
        currency_code_from_contract = extract_currency_code(
            vector_store=vector_store,
            chain_config=leakage_conf["chain_model"],
        )

        for analyzed_table in analyzed_tables:
            table = df_doc_tables[analyzed_table.get("index", "")]
            log.info("processing Leakage information in table \n%s", table.to_markdown())
            subset_leakage_df = pd.DataFrame()
            for leakage_column, matched_column in analyzed_table["column_match"].items():
                subset_leakage_df[leakage_column] = (
                    None if matched_column is None else table[matched_column]
                )
            subset_leakage_df = subset_leakage_df.dropna(subset=["description", "price"])
            # https://github.com/pylint-dev/pylint/issues/4577
            # pylint: disable=E1136
            subset_leakage_df = subset_leakage_df[
                subset_leakage_df["price"].str.contains(r"\d", na=False)
            ]
            # pylint: enable=E1136
            log.info("Table after Filtering required rows and column\n%s", table.to_markdown())
            subset_leakage_df["sku_id"], unmatched_rows_index, filtered_skus = zip(
                *subset_leakage_df.apply(
                    lambda row: find_sku_id_without_llm(
                        row.name,
                        row["original_code"],
                        row["description"],
                        sku_list=sku_list,
                    ),
                    axis=1,
                ),
            )
            unmatched_rows_index = [
                index for index in unmatched_rows_index if index != ""
            ]  # type: ignore
            log.info("Unmatched rows index: %s", unmatched_rows_index)
            filtered_sku_for_unmatched_rows = {}
            for skus in filtered_skus:
                filtered_sku_for_unmatched_rows.update(skus)
            log.info(
                "Filtered sku to find match of unmatched rowa: \n%s",
                filtered_sku_for_unmatched_rows,
            )
            if unmatched_rows_index and filtered_sku_for_unmatched_rows:
                unmatched_rows_df = table[table.index.isin(unmatched_rows_index)]
                log.info("Unmatched rows after Sku id match: \n%s", unmatched_rows_df)
                log.info(
                    "Filtered Sku details for unmatched Rows: %s",
                    filtered_sku_for_unmatched_rows,
                )

                matched_sku_dict = find_sku_id_with_llm(
                    unmatched_rows_df,
                    filtered_sku_for_unmatched_rows,
                    retries=4,
                )
                for index, matched_sku_id in matched_sku_dict.items():
                    if matched_sku_id is not None:
                        subset_leakage_df.at[int(index), "sku_id"] = matched_sku_id

            subset_leakage_df["price_type"] = analyzed_table["price_type"]
            subset_leakage_df["currency"] = (
                currency_code_from_contract
                if analyzed_table["currency"] is None
                or analyzed_table["currency"].lower() == "unknown"
                else analyzed_table["currency"]
            )
            log.info(
                "Table after Sku & description match with price type and currency, \n%s",
                subset_leakage_df,
            )
            leakage_df = pd.concat([leakage_df, subset_leakage_df])

        leakage_df["document_id"] = document_id
        leakage_df["price"] = leakage_df["price"].apply(format_price)

        log.info("Leakage DF from Contracts info: \n%s", leakage_df)

        leakage_df.drop_duplicates(
            subset=["document_id", "description", "sku_id", "price"],
            inplace=True,
        )
        log.info("leakage df after matching with spendscape data: \n%s", leakage_df)
    log.info("COMPLETED: leakage")
    return leakage_df
