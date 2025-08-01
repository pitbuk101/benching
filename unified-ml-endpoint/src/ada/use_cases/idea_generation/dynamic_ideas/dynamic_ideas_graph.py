"""Dynamic Ideas-QnA graph"""

import json
import operator
from typing import Annotated, TypedDict
import datetime

import pandas as pd

from ada.components.db.pg_connector import PGConnector
from ada.components.llm_models.generic_calls import (
    generate_conversational_rag_agent_response,
)
from ada.use_cases.idea_generation.dynamic_ideas.dyn_ideas_prompts import (
    get_question_classifier_prompt, generate_open_world_response_prompt
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
from ada.use_cases.insight_generation.sf_connector import SnowflakeClient
from ada.utils.providers.llm.openai import model, openai_client


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
            "question": state["user_query"],
            "pg_db_conn": state["pg_db_conn"],
            "category": state["category"],
            "chat_history": state["chat_history"],
        },
    )

    log.info("Extracted entities: %s", ner_state["ner_output"])
    return {"ner_output": ner_state["ner_output"]}


def open_world_retriever(state: DynamicIdeasGraphState):
    """
    Retrieves open world data based on the query and chat history

    Args:
        state (DynamicIdeasGraphState): The state dictionary
        containing the input data and extracted entities.

    Returns:
        A dictionary containing the retrieved open world data.
    """

    log.debug(f"Answering question from Open World")

    user_question = state["user_query"]
    history = state["chat_history"]

    prompt = generate_open_world_response_prompt(user_question, history)
    response = openai_client.responses.create(
            model="gpt-4.1",
            tools=[{ "type": "web_search_preview" }],
            input=prompt,
        )

    if response.output[0].type == "message":
        message = response.output[0].content[0].text
        log.info(f"GPT Response: {message}")
    else:
        message = response.output[1].content[0].text
        log.info(f"Internet Based Response: {message}")

    return {"data": [{"open_world_data": message}]}


def supplier_data_retriever(state: DynamicIdeasGraphState):
    """
    Retrieves supplier data based on the extracted entities.

    Args:
        state (DynamicIdeasGraphState): The state dictionary
        containing the input data and extracted entities.

    Returns:
        A dictionary containing the retrieved supplier data.
    """

    supplier_name_list = []
    for ner_data in state["ner_output"]:
        if ner_data["entity"] == "supplier":
            if ner_data["type"] == "name":
                supplier_name_list.extend(ner_data["value"])

    category_name = state["category"]

    sf_conn = SnowflakeClient(tenant_id=state["tenant_id"])

    supplier_data = []

    for supplier in supplier_name_list:

        context = sf_conn.fetch_dataframe(f"""
        SELECT 
            SUPPLIER AS SUPPLIER,
            MAX(KPI_VALUE) AS TOTAL_SAVING_OPPORTUNITY
            FROM (
            SELECT  
                YEAR, 
                CATEGORY AS CATEGORY, 
                SUPPLIER AS SUPPLIER,
                KPI_NAME AS KPI_NAME, 
                SUM(KPI_VALUE) AS KPI_VALUE
            FROM DATA.T_C_TOTAL_SAVINGS_OPPORTUNITY_FRONTEND
            WHERE  KPI_NAME NOT IN ('Spends', 'Total saving opportunity','Supplier Consolidation')
            AND YEAR = (SELECT MAX(YEAR) FROM DATA.T_C_TOTAL_SAVINGS_OPPORTUNITY_FRONTEND)
            AND LOWER(CATEGORY) = '{category_name.lower()}'
            AND LOWER(SUPPLIER) = '{supplier.lower()}'
            GROUP BY YEAR, 
                 CATEGORY, 
                 SUPPLIER,
                 KPI_NAME
            ) AS TS 
            GROUP BY 
            SUPPLIER
            ORDER BY TOTAL_SAVING_OPPORTUNITY DESC
            LIMIT 100;
        """)

        context.columns = [col.replace("'", "").lower() for col in context.columns]    
        
        if len(context) > 0:
            context_dict=context.to_dict(orient='records')
            supplier_data.append(context_dict)

    supplier_data_res = {}
    if len(supplier_data) > 0:
        supplier_data_res["supplier_data"] = supplier_data

    supplier_linked_insights = {}

    for supplier in supplier_name_list:

        linked_context = sf_conn.execute_query(f"""
            SELECT INSIGHT FROM DATA.INSIGHTS_MASTER
            WHERE LOWER(CATEGORY) = '{category_name.lower()}' AND SUPPLIER_INFORMATION ILIKE '%{supplier}%'""")

        supplier_linked_insights[supplier] = linked_context

    if supplier_linked_insights:
        supplier_data_res["supplier_data"] = supplier_data_res.get("supplier_data", []) + [supplier_linked_insights]

    supplier_data_nego = []

    for supplier in supplier_name_list:

        #  MAX(supplier_relationship) AS supplier_relationship,

        context = sf_conn.fetch_dataframe(f"""        
        
        SELECT
        SUPPLIER AS supplier_name,
        YEAR,
        SUM(spend_ytd) AS spend_ytd,
        SUM(last_year_spend) AS last_year_spend,
        ROUND(SUM(percentage_spend_across_category_ytd), 2) AS percentage_spend_across_category_ytd,
        ROUND(SUM(percentage_spend_across_category_last_year), 2) AS percentage_spend_across_category_last_year,
        SUM(single_source_spend_ytd) AS single_source_spend_ytd,
        SUM(multi_source_spend_ytd) AS multi_source_spend_ytd,
        MAX(currency_symbol) AS currency_symbol,
        MAX(early_payment) AS early_payment,
        SUM(spend_without_credit) AS spend_without_credit,
        ROUND(MAX(payment_term_avg), 2) AS payment_term_avg
    FROM
        DATA.NEGO_SUPPLIER_MASTER
    WHERE
        LOWER(category) = '{category_name.lower()}'
        AND YEAR = (
            SELECT MAX(YEAR)
            FROM DATA.NEGO_SUPPLIER_MASTER
        )
        AND LOWER(SUPPLIER) = '{supplier.lower()}'
    GROUP BY
        supplier_name, YEAR;

        """)

        context.columns = [col.replace("'", "").lower() for col in context.columns]    
        
        if len(context) > 0:
            context_dict=context.to_dict(orient='records')
            supplier_data_nego.append(context_dict)

    if supplier_data_nego:
        supplier_data_res["supplier_data"] = supplier_data_res.get("supplier_data", []) + supplier_data_nego


    return {"data": [supplier_data_res]}


def sku_data_retriever(state: DynamicIdeasGraphState):
    """
    Retrieves SKU data based on the extracted entities.

    Args:
        state (DynamicIdeasGraphState): The state dictionary containing the input data and
                                extracted entities.

    Returns:
        dict: A dictionary containing the retrieved SKU data.
    """
    
    sku_name_list = []
    for ner_data in state["ner_output"]:
        if ner_data["entity"] == "sku":
            if ner_data["type"] == "name":
                sku_name_list.extend(ner_data["value"])

    state["skus_list"] = sku_name_list

    category_name = state["category"]
    pg_db_conn = state["pg_db_conn"]

    sf_conn = SnowflakeClient(tenant_id=state["tenant_id"])

    sku_data = []

    for sku in sku_name_list:

        context = sf_conn.fetch_dataframe(f"""
        SELECT 
            MATERIAL AS MATERIAL,
            MAX(KPI_VALUE) AS TOTAL_SAVING_OPPORTUNITY
            FROM (
            SELECT  
                YEAR, 
                CATEGORY AS CATEGORY, 
                MATERIAL AS MATERIAL,
                KPI_NAME AS KPI_NAME, 
                SUM(KPI_VALUE) AS KPI_VALUE
            FROM DATA.T_C_TOTAL_SAVINGS_OPPORTUNITY_FRONTEND
            WHERE  KPI_NAME NOT IN ('Spends', 'Total saving opportunity','Supplier Consolidation')
            AND YEAR = (SELECT MAX(YEAR) FROM DATA.T_C_TOTAL_SAVINGS_OPPORTUNITY_FRONTEND)
            AND LOWER(CATEGORY) = '{category_name.lower()}'
            AND LOWER(MATERIAL) = '{sku.lower()}'
            GROUP BY YEAR, 
                 CATEGORY, 
                 MATERIAL,
                 KPI_NAME
            ) AS TS 
            GROUP BY 
            MATERIAL
            ORDER BY TOTAL_SAVING_OPPORTUNITY DESC
            LIMIT 100;
        """)

        context.columns = [col.replace("'", "").lower() for col in context.columns]    
        
        if len(context) > 0:
            context_dict=context.to_dict(orient='records')
            sku_data.append(context_dict)

    sku_data_res = {}
    if len(sku_data) > 0:
        sku_data_res["sku_data"] = sku_data

    # extract linked insights for each sku

    sku_linked_insights = {}

    for sku in sku_name_list:

        linked_context = sf_conn.execute_query(f"""
            SELECT INSIGHT FROM DATA.INSIGHTS_MASTER
            WHERE LOWER(CATEGORY) = '{category_name.lower()}' AND SKU_INFORMATION ILIKE '%{sku}%'""")

        sku_linked_insights[sku] = linked_context
        
    if sku_linked_insights:
        sku_data_res["sku_data"] = sku_data_res.get("sku_data", []) + [sku_linked_insights]

    return {"data": [sku_data_res]}

def region_data_retriever(state: DynamicIdeasGraphState):
    """
    Retrieves Region data based on the extracted entities.

    Args:
        state (DynamicIdeasGraphState): The state dictionary containing the input data and
                                extracted entities.

    Returns:
        dict: A dictionary containing the retrieved SKU data.
    """
    
    region_name_list = []
    for ner_data in state["ner_output"]:
        if ner_data["entity"] == "region":
            if ner_data["type"] == "name":
                region_name_list.extend(ner_data["value"])

    category_name = state["category"]
    pg_db_conn = state["pg_db_conn"]

    sf_conn = SnowflakeClient(tenant_id=state["tenant_id"])

    region_data = []

    for region in region_name_list:

        context = sf_conn.fetch_dataframe(f"""
        SELECT 
            COUNTRY AS COUNTRY,
            MAX(KPI_VALUE) AS TOTAL_SAVING_OPPORTUNITY
            FROM (
            SELECT  
                YEAR, 
                CATEGORY AS CATEGORY, 
                COUNTRY AS COUNTRY,
                KPI_NAME AS KPI_NAME, 
                SUM(KPI_VALUE) AS KPI_VALUE
            FROM DATA.T_C_TOTAL_SAVINGS_OPPORTUNITY_FRONTEND
            WHERE  KPI_NAME NOT IN ('Spends', 'Total saving opportunity','Supplier Consolidation')
            AND YEAR = (SELECT MAX(YEAR) FROM DATA.T_C_TOTAL_SAVINGS_OPPORTUNITY_FRONTEND)
            AND LOWER(CATEGORY) = '{category_name.lower()}'
            AND LOWER(COUNTRY) = '{region.lower()}' 
            GROUP BY YEAR, 
                 CATEGORY, 
                 COUNTRY,
                 KPI_NAME
            ) AS TS 
            GROUP BY 
            COUNTRY
            ORDER BY TOTAL_SAVING_OPPORTUNITY DESC
            LIMIT 100;""")

        context.columns = [col.replace("'", "").lower() for col in context.columns] 
        if len(context) > 0:
            context_dict=context.to_dict(orient='records')
            region_data.append(context_dict)

                
    region_data_res = {}
    if len(region_data) > 0:
        region_data_res["region_data"] = region_data

    return {"data": [region_data_res]}

def plant_data_retriever(state: DynamicIdeasGraphState):
    """
    Retrieves Region data based on the extracted entities.

    Args:
        state (DynamicIdeasGraphState): The state dictionary containing the input data and
                                extracted entities.

    Returns:
        dict: A dictionary containing the retrieved SKU data.
    """
    
    plant_name_list = []
    for ner_data in state["ner_output"]:
        if ner_data["entity"] == "plant":
            if ner_data["type"] == "name":
                plant_name_list.extend(ner_data["value"])

    category_name = state["category"]
    pg_db_conn = state["pg_db_conn"]

    sf_conn = SnowflakeClient(tenant_id=state["tenant_id"])

    plant_data = []

    for plant in plant_name_list:


        context = sf_conn.fetch_dataframe(f"""        
        SELECT 
            PLANT AS PLANT,
            MAX(KPI_VALUE) AS TOTAL_SAVING_OPPORTUNITY
            FROM (
            SELECT  
                YEAR, 
                CATEGORY AS CATEGORY, 
                PLANT AS PLANT,
                KPI_NAME AS KPI_NAME, 
                SUM(KPI_VALUE) AS KPI_VALUE
            FROM DATA.T_C_TOTAL_SAVINGS_OPPORTUNITY_FRONTEND
            WHERE  KPI_NAME NOT IN ('Spends', 'Total saving opportunity','Supplier Consolidation')
            AND YEAR = (SELECT MAX(YEAR) FROM DATA.T_C_TOTAL_SAVINGS_OPPORTUNITY_FRONTEND)
            AND LOWER(CATEGORY) = '{category_name.lower()}'
            AND LOWER(PLANT) = '{plant.lower()}' 
            GROUP BY YEAR, 
                 CATEGORY, 
                 PLANT,
                 KPI_NAME
            ) AS TS 
            GROUP BY 
            PLANT
            ORDER BY TOTAL_SAVING_OPPORTUNITY DESC
            LIMIT 100;""")

        context.columns = [col.replace("'", "").lower() for col in context.columns] 
        if len(context) > 0:
            context_dict=context.to_dict(orient='records')
            plant_data.append(context_dict)
                
    plant_data_res = {}
    if len(plant_data) > 0:
        plant_data_res["plant_data"] = plant_data

    return {"data": [plant_data_res]}


def get_all_analytics_data_retriever(state: DynamicIdeasGraphState):
    """
    Retrieves all analytics data based on the category.

    Args:
        state (DynamicIdeasGraphState): The state dictionary containing the input data.

    Returns:
        The updated state dictionary with the retrieved analytics data.
    """
    log.info("Started node - Retrieve all analytics data")

    final_result = {}

    category_name = state["category"]
    # pg_db_conn = state["pg_db_conn"]

    sf_conn = SnowflakeClient(tenant_id=state["tenant_id"])

    context = sf_conn.execute_query(
        f"""
        WITH KPI_ANALYTICS AS (
            SELECT  
                YEAR, 
                CATEGORY AS CATEGORY, 
                KPI_NAME AS KPI_NAME, 
                SUM(KPI_VALUE) AS KPI_VALUE
            FROM DATA.T_C_TOTAL_SAVINGS_OPPORTUNITY_FRONTEND
            WHERE KPI_NAME NOT IN ('Total saving opportunity')
                AND YEAR = (SELECT MAX(YEAR) FROM DATA.T_C_TOTAL_SAVINGS_OPPORTUNITY_FRONTEND)
                AND LOWER(CATEGORY) = '{category_name.lower()}'
            GROUP BY YEAR, CATEGORY, KPI_NAME
        ),
        Total_Saving_Opportunity AS (
            SELECT 
                YEAR, 
                CATEGORY AS CATEGORY, 
                'Total saving opportunity' AS KPI_NAME, 
                MAX(KPI_VALUE) AS KPI_VALUE
            FROM (
                SELECT  
                    YEAR, 
                    CATEGORY AS CATEGORY, 
                    KPI_NAME AS KPI_NAME, 
                    SUM(KPI_VALUE) AS KPI_VALUE
                FROM DATA.T_C_TOTAL_SAVINGS_OPPORTUNITY_FRONTEND
                WHERE KPI_NAME NOT IN ('Spends','Total saving opportunity','Supplier Consolidation')
                    AND YEAR = (SELECT MAX(YEAR) FROM DATA.T_C_TOTAL_SAVINGS_OPPORTUNITY_FRONTEND)
                    AND LOWER(CATEGORY) = '{category_name.lower()}'
                GROUP BY YEAR, CATEGORY, KPI_NAME
            )
            GROUP BY YEAR, CATEGORY
        )
        SELECT * FROM KPI_ANALYTICS
        UNION
        SELECT * FROM Total_Saving_Opportunity;
        """
    )


    if len(context) > 0:
        context_dict = context
        log.info("Retrieved opportunity data running get_all_analytics_data_retriever")

    final_result["data"] = context_dict
    
    extra_contexts = sf_conn.execute_query(f"""SELECT INSIGHT FROM DATA.INSIGHTS_MASTER WHERE LOWER(CATEGORY) = '{category_name.lower()}';""")

    final_result["extra_contexts"] = extra_contexts

    final_result["all_analytics_data"] = final_result.get("data", []) + [final_result["extra_contexts"]]
    
    log.info("Finished node - Retrieve all analytics data")

    return {"data": [final_result]}

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
        "idea": "idea_data_retriever",
        "region": "region_data_retriever",
        "plant": "plant_data_retriever",
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
    entity_data_keys = {"supplier_data", "sku_data", "idea_data","region_data","plant_data","open_world_data"}

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
    
    print("Data Sink Output:",json.dumps(data_for_qna))
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
            "ner_output":state["ner_output"]
        },
    )
    state["response_payload"] = response_sub_graph_state["response_payload"]
    return {"response_payload": response_sub_graph_state["response_payload"]}
