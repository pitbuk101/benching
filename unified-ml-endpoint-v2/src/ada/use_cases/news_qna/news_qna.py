"""News QnA use case."""

import json
import os
import pathlib
from datetime import date, datetime, timedelta
from typing import Any

import pandas as pd

from ada.components.db.pg_connector import PGConnector
from ada.components.llm_models.generic_calls import generate_chat_response_with_chain
from ada.use_cases.news_qna.exception import (
    CategoryNotMatchedException,
    NoNewsFoundException,
    SupplierNotFoundException,
)
from ada.use_cases.news_qna.prompts import (
    context_analyzation_prompts,
    generate_summary_for_supplier_news_prompts,
    generate_summary_news_prompts,
)
from ada.utils.config.config_loader import read_config
from ada.utils.format.format import exception_response
from ada.utils.logs.logger import get_logger

log = get_logger("news_qna")
news_conf = read_config("use-cases.yml")["news"]


def get_analyzed_context_from_user_query(user_query: str, category: str) -> dict[str, Any]:
    """
    Analyze user query and using GenAi extract context
    like category name, number of news requested etc
    Return the extracted context

    Args:
        user_query: User query
        category:  user selected query

    Returns: extracted context from user query

    """
    # Todo: As of now , hard coded. Need to receive from TCME backend
    available_categories = ["Bearings"]

    # Todo: needs to replaced with a table from DB
    log.info("fetching suppler details for the category")
    data_dir = os.path.join(pathlib.Path(__file__).parents[4], "data")
    supplier_mapping_df = pd.read_csv(
        f"{data_dir}/{news_conf['files']['category_supplier_mapping']}",
    )
    supplier_mapping_df = supplier_mapping_df[
        supplier_mapping_df.category_name.str.upper() == category.upper()
    ]
    suppliers_dict = pd.Series(
        supplier_mapping_df.dim_supplier.values,
        index=supplier_mapping_df.supplier_name,
    ).to_dict()
    log.info(suppliers_dict)

    context_analyzer_prompts = context_analyzation_prompts(
        user_query,
        available_categories,
        list(suppliers_dict),
    )
    ai_response = generate_chat_response_with_chain(
        context_analyzer_prompts,
        model="gpt-35-turbo",
        # response_format="json_mode",
    )
    analyzed_query_context = json.loads(ai_response)

    if "category" in analyzed_query_context:
        analyzed_query_context = modify_query_context_for_category(category, analyzed_query_context)
    if "supplier" in analyzed_query_context:
        analyzed_query_context = modify_query_context_for_supplier(
            analyzed_query_context,
            suppliers_dict,
        )
    log.info(analyzed_query_context)
    return analyzed_query_context


def modify_query_context_for_category(
    category: str,
    analyzed_query_context: dict[str, Any],
) -> dict[str, Any]:
    """
    Modify query context if query is specific to category

    Args:
        category:  user selected category
        analyzed_query_context: context of user query

    Returns: modified query context

    Raise:
     CategoryNotMatchedException:
        if user selected query and query in analyzed_query_context does not match

    """
    if analyzed_query_context["category"] in [None, "None", "NONE"]:
        analyzed_query_context["category"] = category

    # Todo: news for all available category
    if (
        category != "All Categories"
        and analyzed_query_context["category"].lower() != category.lower()
    ):
        log.error("category not matched")
        raise CategoryNotMatchedException(category, analyzed_query_context["category"])

    return analyzed_query_context


def modify_query_context_for_supplier(
    analyzed_query_context: dict[str, Any],
    suppliers_dict: dict[str, Any],
) -> dict[str, Any]:
    """
    Modify query context if its specific to supplier

    Args:
        analyzed_query_context: context of user query
        suppliers_dict: supplier name with  id mapping

    Returns: modified query context

    Raise:
     SupplierNotFoundException: if user does not mention any supplier name in user query

    """
    if analyzed_query_context["supplier"] in [None, "None", "NONE"]:
        log.error("supplier name not found")
        raise SupplierNotFoundException()
    suppliers_in_user_query = analyzed_query_context["supplier"]
    allowed_supplier_for_user = [
        supplier for supplier in suppliers_in_user_query if supplier in suppliers_dict.keys()
    ]
    not_allowed_supplier_for_user = [
        supplier
        for supplier in suppliers_in_user_query
        if supplier not in allowed_supplier_for_user
    ]
    allowed_supplier_for_user_dict = {
        supplier: suppliers_dict[supplier] for supplier in allowed_supplier_for_user
    }
    analyzed_query_context.update(
        {
            "allowed_supplier": allowed_supplier_for_user_dict,
            "not_allowed_supplier": not_allowed_supplier_for_user,
        },
    )

    return analyzed_query_context


def extract_filter_details(analyzed_query_context: dict[str, Any]) -> tuple:
    """
    extract start date, end date and num of records for Db query
    Args:
        analyzed_query_context: query context

    Returns: start date, end date and num of records in tuple

    """
    start_date = analyzed_query_context["date_range"][0]
    start_date = (
        date.today() - timedelta(days=15)
        if start_date == "None"
        else datetime.strptime(start_date, "%d/%m/%Y").date()
    )

    end_date = analyzed_query_context["date_range"][1]
    end_date = (
        date.today() if end_date == "None" else datetime.strptime(end_date, "%d/%m/%Y").date()
    )

    num_docs = (
        analyzed_query_context["news_count"]
        if isinstance(analyzed_query_context["news_count"], int)
        else None
    )
    log.info("start date: %s, end_date: %s, number of news: %s", start_date, end_date, num_docs)
    return start_date, end_date, num_docs


def get_news_data(
    tenant_id: str,
    analyzed_query_context: dict[str, Any],
    category: str = "",
) -> tuple:
    """
    Identify filters from analyzed_query_context and
    extract category or supplier news from DB related with required fileter

    Args:
        analyzed_query_context: query context details
        category: user selected category

    Returns: tuple of news extracted from DB

    Raise:
     NoNewsFoundException: if no nws found related to user query

    """
    pg_db_conn = PGConnector(tenant_id=tenant_id, cursor_type="dict")

    news_data: tuple = tuple()

    start_date, end_date, num_records = extract_filter_details(analyzed_query_context)
    date_filter = f"publication_date::date BETWEEN '{start_date}' AND '{end_date}'"

    if analyzed_query_context["type"] == "category":
        filtered_columns = [
            "news_id",
            "title",
            "news_content",
            "image_url",
            "url",
            "publication_date",
            "description",
            "bullet_points_summary",
        ]
        category_filter = f"category_name = '{category.upper()}'"
        news_data = pg_db_conn.select_records_with_filter(
            table_name=news_conf["tables"]["category_table_name"],
            filtered_columns=filtered_columns,
            filter_condition=" AND ".join([date_filter, category_filter]),
            num_records=num_records,
        )
    elif analyzed_query_context["type"] == "supplier":
        filtered_columns = [
            "supplier_name",
            "news_id",
            "title",
            "news_content",
            "image_url",
            "url",
            "publication_date",
            "description",
            "bullet_points_summary",
        ]
        suppliers = (
            "("
            + ",".join([f"'{sup}'" for sup in analyzed_query_context["allowed_supplier"].values()])
            + ")"
        )
        supplier_filter = f"supplier_id in {suppliers}"
        news_data = pg_db_conn.select_records_with_filter(
            table_name=news_conf["tables"]["supplier_table_name"],
            filtered_columns=filtered_columns,
            filter_condition=" AND ".join([date_filter, supplier_filter]),
            num_records=num_records,
        )
    if len(news_data) == 0:
        log.error("No news found")
        raise NoNewsFoundException()
    return news_data


def convert_to_response_format(
    response_type: str,
    *,
    news_data: list | tuple | Any = None,
    message: str = "",
) -> dict[str, Any]:
    """
    Convert acquired data to specified endpoint output format dict

    Args:
        response_type: type of response i.e. exception , individual  or summary
        news_data: list of news with details such as title, url , description etc
        message: exception message or summary message from genAI needs to add

    Returns: formatted dict object
    """

    if response_type == "exception":
        return exception_response("news qna", message)

    links = [
        {
            "type": "news",
            "details": {
                "title": news["title"],
                "description": news["description"],
                "link": news["url"],
                "imageUrl": news["image_url"],
            },
        }
        for news in news_data[::9]
    ]
    output = {
        "owner": "ai",
        "additional_text": "For additional info, please visit the links....",
        "response_type": "summary",
        "response_prerequisite": "",
        "links": links,
    }
    if response_type == "summary":
        output["message"] = message
    elif response_type == "individual":
        output["message"] = [
            {
                "title": news["title"],
                "summary": news["bullet_points_summary"],
                "publicationDate": news["publication_date"].strftime("%d %B %Y"),
            }
            for news in news_data[::9]
        ]
    return output


def run_news_qna(json_file_str: str) -> dict[str, Any]:
    """
    Fetch News from DB related to user query and Generate Answer using Genai from that news

    Args:
        json_file: json payload from realtime endpoint

    Returns:
        Answer to user query
    """
    json_file = json.loads(json_file_str)
    user_query = json_file.get("user_query", "")
    category = json_file["category"]
    tenant_id = json_file["tenant_id"]

    log.info("Analyzing user query")
    analyzed_query_context = get_analyzed_context_from_user_query(user_query, category)

    try:
        news_data = get_news_data(tenant_id, analyzed_query_context, category)
        log.info(news_data)

        if analyzed_query_context["mode"] == "individual":
            return convert_to_response_format(response_type="individual", news_data=news_data)

        # if mode is other or combined
        if (
            analyzed_query_context["type"] == "supplier"
            and (
                len(analyzed_query_context["allowed_supplier"])
                + len(analyzed_query_context["not_allowed_supplier"])
            )
            > 1
        ):
            log.info("Summarizing the news using openAI")
            summary_prompts = generate_summary_for_supplier_news_prompts(
                user_query,
                analyzed_query_context["allowed_supplier"],
                analyzed_query_context["not_allowed_supplier"],
                news_data,
            )
        else:
            log.info("Summarizing the news using openAI")
            summary_prompts = generate_summary_news_prompts(
                user_query,
                news_data,
                analyzed_query_context,
            )

        ai_response = generate_chat_response_with_chain(summary_prompts)
        return convert_to_response_format(
            response_type="summary",
            news_data=news_data,
            message=ai_response,
        )

    except NoNewsFoundException as no_news_found_exception:
        return convert_to_response_format(
            response_type="exception",
            message=no_news_found_exception.message,
        )
    except SupplierNotFoundException as supplier_name_not_found_exception:
        return convert_to_response_format(
            response_type="exception",
            message=supplier_name_not_found_exception.message,
        )
    except CategoryNotMatchedException as category_not_matched_exception:
        return convert_to_response_format(
            response_type="exception",
            message=category_not_matched_exception.message,
        )
