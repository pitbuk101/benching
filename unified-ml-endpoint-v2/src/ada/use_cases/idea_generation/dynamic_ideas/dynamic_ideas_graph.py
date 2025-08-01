"""Dynamic Ideas-QnA graph"""

import json
import operator
from typing import Annotated, TypedDict

import pandas as pd

from ada.components.db.pg_connector import PGConnector
from ada.components.llm_models.generic_calls import (
    generate_conversational_rag_agent_response,
)
from ada.use_cases.idea_generation.dynamic_ideas.dyn_ideas_prompts import (
    get_question_classifier_prompt,
)
from ada.use_cases.idea_generation.dynamic_ideas.dynamic_ideas_utils import (
    fetch_linked_insights_for_suppliers,
    filter_supplier_data_for_max_period,
    prepare_analytics_json,
    update_ner_format,
)
from ada.use_cases.idea_generation.dynamic_ideas.ner_graph import create_ner_pipeline
from ada.use_cases.idea_generation.dynamic_ideas.response_generator_graph import (
    create_response_generator_pipeline,
)
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger

log = get_logger("dynamic_ideas")

dynamic_ideas_conf = read_config("use-cases.yml")["dynamic_ideas"]


class DynamicIdeasGraphState(TypedDict):
    """TypedDict for Dynamic Ideas Graph state."""

    chat_history: list[tuple[str, str]]
    tenant_id: str
    user_query: str
    request_type: str
    page_id: str
    category: str
    question_class: str
    ner_output: list
    data: Annotated[list, operator.add]
    data_for_qna: str
    generated_response: str
    response_payload: dict
    pg_db_conn: PGConnector


def dynamic_quest_classifier(state: DynamicIdeasGraphState):
    """
    Classifies the user's query into a specific question class.

    This function uses a pre-defined prompt to generate a response that classifies the user's query.
    The classification is based on the context of the user's query and chat history.

    Args:
        state (DynamicIdeasGraphState): The state dictionary containing
        the input data and chat history.

    Returns:
        The updated state dictionary with the classified question.
    """
    log.info("Executing node : dynamic_quest_classifier")
    prompt = get_question_classifier_prompt()
    # TODO: rename to hybrid agent
    response = generate_conversational_rag_agent_response(
        user_query=state["user_query"],
        prompt=prompt,
        chat_history=state["chat_history"],
        additional_params={"enable_grader": False},
        fast_llm_for_rag_chain=True,
    )
    log.info("Predicted Question class : %s", response["generation"])
    log.info("Completed Executing node : dynamic_quest_classifier")
    return {"question_class": response["generation"].strip('"')}


# TODO: address rephrase node post func testing
# def rephrase_question_based_on_history(state: DynamicIdeasGraphState) -> DynamicIdeasGraphState:
#     prompt = question_rephraser_prompt()
#     fast_llm = (
#         Model(name=fast_model, temp=temperature).obj
#         if isinstance(fast_model, str) else fast_model
#     )
#     ner_chain = prompt | fast_llm
#     params = {
#         "question": state["user_query"],
#         "chat_history": state["chat_history"],
#     }
#     llm_response = ner_chain.invoke(params)
#     response = parse_llm_json_response(llm_response.content, ["rephrased_question"])
#     state["rephrased_user_query"] = response.get("rephrased_question")
#     return state


def call_ner_sub_graph(state: DynamicIdeasGraphState):
    """
    Executes the Named Entity Recognition (NER) sub-graph.

    This function invokes the NER pipeline to extract entities from the user's query.

    Args:
        state (DynamicIdeasGraphState): The state dictionary containing the input data.

    Returns:
        dict: A dictionary containing the extracted entities.
    """
    log.info("Executing node: call_ner_sub_graph")
    ner_sub_graph = create_ner_pipeline()
    ner_state = ner_sub_graph.invoke(
        {
            # "question": state["rephrased_user_query"],
            "question": state["user_query"],
            "pg_db_conn": state["pg_db_conn"],
            "category": state["category"],
            "chat_history": state["chat_history"],
        },
    )
    log.info("Extracted entities: %s", ner_state["corrected_ner_output"])
    return {"ner_output": ner_state["corrected_ner_output"]}


def analytics_data_retriever(state: DynamicIdeasGraphState):
    """
    Retrieves analytics data based on the extracted entities and category.

    Args:
        state (DynamicIdeasGraphState): The state dictionary containing the input data
                                    and extracted entities.

    Returns:
        The updated state dictionary with the retrieved analytics data.
    """
    category_name = state["category"]
    ner_output = [ner_data for ner_data in state["ner_output"] if ner_data["entity"] == "analytics"]
    analytics_name = update_ner_format(ner_output)
    pg_db_conn = state["pg_db_conn"]

    column_list = dynamic_ideas_conf["columns"]["analytics_retriever_cols"]
    table_name = dynamic_ideas_conf["tables"]["analytics_list_tbl"]
    filter_condition = (
        f"LOWER(category_name) = '{category_name.lower()}' "
        f"AND analytics_name IN {analytics_name} "
        f"AND CAST(file_timestamp AS BIGINT) = "
        f"(SELECT MAX(CAST(file_timestamp AS BIGINT)) "
        f"FROM {table_name})"
    )

    analytics_view_df = pd.DataFrame(
        pg_db_conn.select_records_with_filter(
            table_name=table_name,
            filtered_columns=column_list,
            filter_condition=filter_condition,
        ),
    )
    context = {}
    if len(analytics_view_df) > 0:
        context["analytics_data"] = prepare_analytics_json(analytics_view_df, category_name)
    return {"data": [context]}


def idea_data_retriever(state: DynamicIdeasGraphState):
    """
    Retrieves idea data based on the extracted entities.

    Args:
        state (DynamicIdeasGraphState): The state dictionary containing the input data
                            and extracted entities.

    Returns:
        The updated state dictionary with the retrieved idea data.
    """
    category_name = state["category"]
    ner_output = [ner_data for ner_data in state["ner_output"] if ner_data["entity"] == "idea"]
    idea_id = update_ner_format(ner_output)
    pg_db_conn = state["pg_db_conn"]

    table_name = dynamic_ideas_conf["tables"]["analytics_list_tbl"]
    column_list = dynamic_ideas_conf["columns"]["idea_retriever_cols"]
    filter_condition = (
        f"LOWER(category_name) = '{category_name.lower()}' "
        f"AND (category_name || '_' || file_timestamp || idea_number) IN {idea_id} "
        f"AND CAST(file_timestamp AS BIGINT) = "
        f"(SELECT MAX(CAST(file_timestamp AS BIGINT)) "
        f"FROM {table_name})"
    )

    ideas_view_df = pd.DataFrame(
        pg_db_conn.select_records_with_filter(
            table_name=table_name,
            filtered_columns=column_list,
            filter_condition=filter_condition,
        ),
    )
    context = {}
    if len(ideas_view_df) > 0:
        context["idea_data"] = prepare_analytics_json(ideas_view_df, category_name)
    return {"data": [context]}


def supplier_data_retriever(state: DynamicIdeasGraphState):
    """
    Retrieves supplier data based on the extracted entities.

    Args:
        state (DynamicIdeasGraphState): The state dictionary
        containing the input data and extracted entities.

    Returns:
        A dictionary containing the retrieved supplier data.
    """
    supplier_id_list = []
    supplier_name_list = []
    for ner_data in state["ner_output"]:
        if ner_data["entity"] == "supplier":
            if ner_data["type"] == "id":
                supplier_id_list.extend(ner_data["value"])
            elif ner_data["type"] == "name":
                supplier_name_list.extend(ner_data["value"])

    category_name = state["category"]
    pg_db_conn = state["pg_db_conn"]

    supplier_name_condition = (
        pg_db_conn.get_condition_string(
            cond=("supplier_name", "in", supplier_name_list),
        )
        if supplier_name_list
        else ""
    )
    supplier_id_condition = (
        pg_db_conn.get_condition_string(
            cond=("supplier_id", "in", supplier_id_list),
        )
        if supplier_id_list
        else ""
    )

    filter_condition = f"LOWER(category_name) = '{category_name.lower()}'"
    if supplier_name_condition and supplier_id_condition:
        filter_condition += f"AND ({supplier_name_condition} OR {supplier_id_condition})"
    elif supplier_name_condition:
        filter_condition += f"AND {supplier_name_condition}"
    elif supplier_id_condition:
        filter_condition += f"AND {supplier_id_condition}"

    kwargs = {
        "table_name": dynamic_ideas_conf["tables"]["supplier_profile_view"],
        "filter_condition": filter_condition,
        "filtered_columns": dynamic_ideas_conf["columns"]["supplier_profile_view_cols"],
    }
    extracted_supplier_data = pg_db_conn.select_records_with_filter(**kwargs)
    context = {}

    if len(extracted_supplier_data) > 0:
        log.info("received supplier data from supplier profile")
        supplier_data = [dict(row) for row in extracted_supplier_data]
        # Todo: needs to be removed once period is available for all
        context["supplier_data"] = filter_supplier_data_for_max_period(supplier_data)

    # extract linked insights for each supplier
    supplier_linked_insights = {}
    for supplier in supplier_name_list:
        supplier_linked_insights[supplier] = fetch_linked_insights_for_suppliers(
            pg_db_conn,
            category_name,
            supplier_name=supplier,
        )
    for supplier in supplier_id_list:
        supplier_linked_insights[supplier] = fetch_linked_insights_for_suppliers(
            pg_db_conn,
            category_name,
            supplier_id=supplier,
        )
    if supplier_linked_insights:
        context["supplier_data"] = context.get("supplier_data", []) + [supplier_linked_insights]
    return {"data": [context]}


def sku_data_retriever(state: DynamicIdeasGraphState):
    """
    Retrieves SKU data based on the extracted entities.

    Args:
        state (DynamicIdeasGraphState): The state dictionary containing the input data and
                                extracted entities.

    Returns:
        dict: A dictionary containing the retrieved SKU data.
    """
    sku_id_list = []
    sku_name_list = []
    for ner_data in state["ner_output"]:
        if ner_data["entity"] == "sku":
            if ner_data["type"] == "id":
                sku_id_list.extend(ner_data["value"])
            elif ner_data["type"] == "name":
                sku_name_list.extend(ner_data["value"])

    category_name = state["category"]
    pg_db_conn = state["pg_db_conn"]

    sku_name_condition = (
        pg_db_conn.get_condition_string(
            cond=("entity_name", "in", sku_name_list),
        )
        if sku_name_list
        else ""
    )
    sku_id_condition = (
        pg_db_conn.get_condition_string(
            cond=("entity_id", "in", sku_id_list),
        )
        if sku_id_list
        else ""
    )

    filter_condition = f"LOWER(category_name) = '{category_name.lower()}'"
    if sku_name_condition and sku_id_condition:
        filter_condition += f"AND ({sku_name_condition} OR {sku_id_condition})"
    elif sku_name_condition:
        filter_condition += f"AND {sku_name_condition}"
    elif sku_id_condition:
        filter_condition += f"AND {sku_id_condition}"

    kwargs = {
        "table_name": dynamic_ideas_conf["tables"]["sku_profile_view"],
        "filter_condition": filter_condition,
        "filtered_columns": dynamic_ideas_conf["columns"]["sku_profile_view_cols"],
    }
    extracted_sku_data = pg_db_conn.select_records_with_filter(**kwargs)

    context = {}
    if len(extracted_sku_data) > 0:
        context["sku_data"] = [dict(row) for row in extracted_sku_data]

    # Todo: Add linked insights for each sku
    # # extract linked insights for each sku
    # sku_linked_insights = {}
    # for sku in sku_name_list:
    #     sku_linked_insights[sku] = fetch_linked_insights_for_suppliers(
    #         pg_db_conn,
    #         category_name,
    #         sku_name=sku,
    #     )
    # for sku in sku_id_list:
    #     sku_linked_insights[sku] = fetch_linked_insights_for_suppliers(
    #         pg_db_conn,
    #         category_name,
    #         sku_id=sku,
    #     )
    # context["sku_data"] = context.get("sku_data", []).append(sku_linked_insights)

    return {"data": [context]}


def get_all_analytics_data_retriever(state: DynamicIdeasGraphState):
    """
    Retrieves all analytics data based on the category.

    Args:
        state (DynamicIdeasGraphState): The state dictionary containing the input data.

    Returns:
        The updated state dictionary with the retrieved analytics data.
    """
    log.info("Started node - Retrieve all analytics data")
    category_name = state["category"]
    pg_db_conn = state["pg_db_conn"]

    column_list = [
        "idea_number",
        "idea",
        "analytics_name",
        "impact",
        "linked_insight",
        "opportunity_insight",
        "file_timestamp",
        "expert_inputs",
    ]
    table_name = dynamic_ideas_conf["tables"]["analytics_list_tbl"]
    filter_condition = (
        f"LOWER(category_name) = '{category_name.lower()}' "
        f"AND CAST(file_timestamp AS BIGINT) = "
        f"(SELECT MAX(CAST(file_timestamp AS BIGINT)) "
        f"FROM {table_name})"
    )

    analytics_view_df = pd.DataFrame(
        pg_db_conn.select_records_with_filter(
            table_name=table_name,
            filtered_columns=column_list,
            filter_condition=filter_condition,
        ),
    )

    context = {}
    if len(analytics_view_df) > 0:
        context["all_analytics_data"] = prepare_analytics_json(analytics_view_df, category_name)
    log.info("Completed node - Retrieve all analytics data : %s", len([context]))
    return {"data": [context]}


def decide_retrieval_nodes(state: DynamicIdeasGraphState):
    """
    Determines the retrieval nodes to be executed based on the extracted entities.

    Args:
        state (DynamicIdeasGraphState): The state dictionary containing
        the input data and extracted entities.

    Returns:
        A list of retrieval node names to be executed.
    """
    ner_output = state.get("ner_output", [])
    # routes = ["get_all_analytics_data_retriever"] if ner_output == [] else []
    routes = ["get_all_analytics_data_retriever"]  # we always add this retriever
    entity_to_route_map = {
        "sku": "sku_data_retriever",
        "supplier": "supplier_data_retriever",
        "analytics": "analytics_data_retriever",
        "idea": "idea_data_retriever",
    }
    for entity, route in entity_to_route_map.items():
        if any(item["entity"] == entity for item in ner_output):
            routes.append(route)
    log.info("Routes identified: %s", routes)
    return routes


def data_sink(state: DynamicIdeasGraphState):
    """
    Processes and stores the retrieved data for further use.

    This function collects the available data keys from the state dictionary,
    filters the data based on the presence of 'all_analytics_data', and prepares
    the data for QnA processing.

    Args:
        state (DynamicIdeasGraphState): The state dictionary containing the input data
                                and retrieved data.

    Returns:
        A dictionary containing the prepared data for QnA processing.
    """

    log.info("Starting node Data sink")
    entity_data_keys = {"supplier_data", "sku_data", "idea_data", "analytics_data"}

    data_keys_available = []
    for data_item in state["data"]:
        data_keys_available += data_item.keys()

    log.info("Available data keys during data sink: %s", data_keys_available)
    if entity_data_keys & set(data_keys_available):
        data_for_qna = [
            data_item for data_item in state["data"] if "all_analytics_data" not in data_item
        ]
    else:
        data_for_qna = [
            data_item for data_item in state["data"] if "all_analytics_data" in data_item.keys()
        ]
    return {"data_for_qna": json.dumps(data_for_qna)}


def call_response_generator_graph(state: DynamicIdeasGraphState):
    """
    Invoke the response generator graph with the provided state.

    Args:
        state (DynamicIdeasGraphState)

    Returns:
        dict: A dictionary containing the key:
            - "response_payload" (dict): The formatted response payload generated
              by the response generator graph.

    Notes:
        - The `response_payload` in the state is updated with the result of the
          response generator graph.
    """
    log.info("Executing node: call_response_generator_graph")
    response_sub_graph = create_response_generator_pipeline()
    response_sub_graph_state = response_sub_graph.invoke(
        {
            "question_class": state["question_class"],
            "tenant_id": state["tenant_id"],
            "user_query": state["user_query"],
            "category": state["category"],
            "data_for_qna": state["data_for_qna"],
            "chat_history": state["chat_history"],
            "pg_db_conn": state["pg_db_conn"],
        },
    )
    state["response_payload"] = response_sub_graph_state["response_payload"]
    return {"response_payload": response_sub_graph_state["response_payload"]}
