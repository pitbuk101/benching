"""Prompts for Leakage extraction"""

from typing import Any

import pandas as pd
from langchain_core.prompts import PromptTemplate


def table_analyzation_prompts(
    doc_tables_df: list[pd.DataFrame],
    columns_of_interest: dict[str, Any],
    original_codes: list[str],
) -> list[dict[str, str]]:
    """
    Prompts that will be submitted to LLM model to analyze table
    to retrieve data such matched column, price type, currency etc

    Args:
        doc_tables_df (list[pd.DataFrame]): list of tables
                            ( in form of pandas dataframe) extracted from contract
        columns_of_interest (dict[str, Any]): Columns for which we need to find the matched column ,
                            it includes both mandatory and optional columns
        original_codes (list[str]): List of codes received in  sku details from Spendscape data

    Returns:
        (list[dict[str, str]]): Prompt message for llm model
    """
    table_data = ""
    for index, table in enumerate(doc_tables_df):
        table_data += f"""
            Index: {index}
            Columns: {list(table.columns)}
            Sample records:
            {
            table.loc[:2, ~table.columns.duplicated()].to_json(orient='records') +
            table.loc[table.index[-1:], ~table.columns.duplicated()].to_json(orient='records')
        }


            """
    return [
        {
            "role": "system",
            "content": "You are an expert in interpreting column headers for tables "
            "and giving relevant information",
        },
        {
            "role": "user",
            "content": f"""
            COLUMN_OF_INTEREST:
                {columns_of_interest}

            sample ORIGINAL_CODE : {original_codes}

            TABLES:
            {table_data}

            Filter out tables which is containing similar information \
            about all of the MANDATORY_COLUMN_OF_INTEREST
            NOTE: Its good to have OPTIONAL_COLUMN_OF_INTEREST
            NOTE: We may get match with multiple tables

            RETURN FORMAT:
            ONLY LIST of JSON objects or blank [] if no match in ``` quote [ DONT mention json inside triple quote]

            SAMPLE OUTPUT IF NO MATCH:
            ```[]```

            SAMPLE OUTPUT IF MATCH:
            ```
            [{{{{
                "index": int // matched table index
                "column_match": {{{{
                    "price" : "col_ab", // prefer to get `unit price` column
                    "description" : "col_xy",
                    "original_code" : "col_qw" // null, if no match
                }}}}
                "price_type": str // unit or total, null if no match
                "currency": str // CURRENCY CODE like EUR , INR etc. NOT currency name. OR `null` If no match then
            }}}}
            ]
            ```

            IMPORTANT:
                1. ALWAYS check Sample records with FULL ATTENTION to identify the column
                2. currency: sometimes It can be with symbol only , check CAREFULLY
                3. match column for ORIGINAL_CODE: it can be with different Column names,
                       - compare SAMPLE RECORDS with sample ORIGINAL_CODE with ATTENTION to FIND OUT the column
                       - It may not be exact match with sample records but similar one only

            """,
        },
    ]


def search_currency_code_prompts() -> PromptTemplate:
    """
    Generate prompt to find the currency code from document using QA chain

    Returns:
        (PromptTemplate): Langchain `PromptTemplate` object with the specified prompt.

    """
    prompt = """
    You are an experienced lawyer who is specialized in analyzing commercial contracts.

    Transaction Currency: Variable to represent the currency on which \
    financial transaction such as deal, settlement, transfer of money, payment  etc happened
    between parties such as Buyers and suppliers

    Find the currency code of the contract signed in the contract.

    Output must strictly follow the format. Always return your answer in JSON format.[WITHOUT word 'json']

    {{{{
        "currency_code": str // Remember Currency code not currency name
    }}}}

    Example:
    {{{{
        "currency_code": "EUR"
    }}}}

    TEXT: {context}
    """
    return PromptTemplate(
        template=prompt,
        input_variables=["context"],
    )


def search_currency_code_query() -> list[str]:
    """
    Generate query to find the currency code from document using QA chain

    Returns:
        list[str] : a str object with the specified query.

    """

    currency_code_queries = [
        "Contract sealed for * monetary value",
        "Transaction finalized for * cash amount",
        "deal signed for * amount of money",
        "product purchased / sale with amount",
    ]

    return currency_code_queries


def find_sku_id_prompts(
    unmatched_rows_df: pd.DataFrame,
    filtered_sku_df: pd.DataFrame,
) -> list[dict[str, str]]:
    """
    Generate Prompt to find sku id by matching
    description from spendscape data and contract data

    Args:
        unmatched_rows_df (pd.DataFrame):  df with rows without sku id match
        filtered_sku_df (pd.DataFrame): df with filter sku list with high probability to match

    Returns:
        (list[dict[str, str]]): prompt message for llm model
    """
    return [
        {
            "role": "system",
            "content": "You are an expert in interpreting column headers for tables "
            "and giving relevant information",
        },
        {
            "role": "user",
            "content": f"""
            ACTUAL_DATA:
                {filtered_sku_df.to_json(orient='records')}


            CONTRACT_DATA:
                {unmatched_rows_df.loc[:, ~unmatched_rows_df.columns.duplicated()].reset_index().to_json(orient='records')}

            TRY to match the records of ACTUAL_DATA & CONTRACT_DATA.
            and for each index of CONTRACT_DATA , identify the sku id .
            If there is not match retun the value of that index an null

            OUTPUT_FORMAT:
            STRICTLY JSON DICT inside triple quote [WITHOUT word 'json']
            ```
            {{{{
                index_num : matched sku_id // null if no match
            }}}}
            ```

            NOTE: DONT provide SCRIPT , give output in JSON format
            """,
        },
    ]
