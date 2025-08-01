"""Idea generation module to assist users in inferring insights better"""

import json
from typing import Any

from ada.components.db.pg_connector import PGConnector
from ada.use_cases.idea_generation.exception import IdeaGenException

# pylint: disable=W0611
from ada.use_cases.idea_generation.idea_generation_utils import (  # noqa: F401
    extract_pinned_elements,
    generate_chat_model_response,
    generate_ideas,
    generate_rca,
    generate_response_dict,
    generate_user_intent,
    get_insight_context,
    get_precomputed_response,
    input_data_validation,
    write_response_to_db,
    extract_json
)
from ada.components.llm_models.generic_calls import generate_chat_response_with_chain
from ada.use_cases.insight_generation.sf_connector import SnowflakeClient

# pylint: enable=W0611
from ada.use_cases.idea_generation.prompts import get_intent_prompt,generate_top_ideas_prompt,generate_rca_prompt
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time
import re
import ast

idea_generation_conf = read_config("use-cases.yml")["idea_generation_chat"]
pg_config = idea_generation_conf["tables"]
insight_generation_conf = read_config("use-cases.yml")["insight_generation"]
insight_model_conf = read_config("use-cases.yml")["insight_generation"]["model"]
analytics_conf = insight_generation_conf["analytics"]
log = get_logger("idea_generation_v2")


@log_time
def get_linked_insights_rca_idea_model(
    chat_id: str,
    pinned_elements: dict[str, Any],
    pg_db_conn: PGConnector,
    sf_client: SnowflakeClient,
    request_type: str,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Computes or retrieves the linked_insights/ ideas/ rca based on the provided inputs.

    This function first checks if a pre-computed values are available for the given `chat_id`.
    If a pre-computed value is not found, it will compute it from the  provided `pinned_elements`
    and store it for future use. The function then returns the values to the user.
    Args:
        chat_id (str): A unique identifier for the chat or session
        pinned_elements (dict[str, Any]): Dictionary  of elements that are pinned by user
        pg_db_conn (PGConnector): A database connection object used to interact with PostgreSQL
        request_type (str): request type made
        kwargs: Additional arguments
    Returns:
        dict[str, Any]: A dictionary containing the ideas
    """
    log.info("len of additional arguments %d", len(kwargs))
    value_list = []
    context_dict = {}


    if any(pinned_elements[key] for key in pinned_elements):

        if request_type =='rca':
            value_list = sf_client.execute_query(f"""
                SELECT RCA_HEADING, RCA_DESCRIPTION FROM SAI_770ABBC_PROD_DB.DATA.INSIGHTS_MASTER
                WHERE ID = '{pinned_elements.get("insight_id")}'
                AND RCA_HEADING!= 'NULL';
            """)

        elif request_type == 'ideas':
            value_list = sf_client.execute_query(f"""
                SELECT TOP_IDEAS FROM SAI_770ABBC_PROD_DB.DATA.INSIGHTS_MASTER
                WHERE ID = '{pinned_elements.get("insight_id")}'
                AND TOP_IDEAS != 'NULL';
            """)


        elif request_type == 'linked_insights':
            value_list = sf_client.execute_query(f"""
                SELECT LINKED_INSIGHTS FROM SAI_770ABBC_PROD_DB.DATA.INSIGHTS_MASTER
                WHERE ID = '{pinned_elements.get("insight_id")}'
            """)

        if not value_list and request_type != "linked_insights":

            context = sf_client.execute_query(f"""
                SELECT ANALYTICS_NAME, SEGMENT, CATEGORY, INSIGHT, OBJECTIVE ,LINKED_INSIGHTS, 
                RELATED_INSIGHTS FROM SAI_770ABBC_PROD_DB.DATA.INSIGHTS_MASTER
                WHERE ID = '{pinned_elements.get("insight_id")}'""")
            
            context_col_names = [
            "analytics_name",
            "segment",
            "category",
            "insight",
            "objective",
            "linked_insights",
            "related_insights"
            ]
                

            for i, col_name in enumerate(context_col_names):
                context_dict[col_name] = context[0][i] if context[0][i] else None
            
            if request_type == 'ideas':
                prompt = generate_top_ideas_prompt(context_dict['insight'],context_dict['linked_insights'],context_dict['analytics_name'])
                response = generate_chat_response_with_chain(prompt,temperature=insight_model_conf["temperature"],model=insight_model_conf["model_name"])
                value_list = extract_json(response)
                message = sf_client.execute_query(f"""
                UPDATE SAI_770ABBC_PROD_DB.DATA.INSIGHTS_MASTER
                SET TOP_IDEAS = '{json.dumps(value_list)}', 
                WHERE ID = '{pinned_elements.get("insight_id")}';""")

            elif request_type == 'rca':
                prompt = generate_rca_prompt(context_dict['analytics'],context_dict['insight'],context_dict['linked_insights'],context_dict['related_insights'])
                response = generate_chat_response_with_chain(prompt,temperature=insight_model_conf["temperature"],model=insight_model_conf["model_name"])
                match = re.search(r"```dict(.*?)```", response, re.DOTALL)
                if match:
                    dict_str = match.group(1).strip()  
                    data_dict = ast.literal_eval(dict_str)
                    value_list.append(data_dict)
                    message = sf_client.execute_query(f"""
                    UPDATE SAI_770ABBC_PROD_DB.DATA.INSIGHTS_MASTER
                    SET RCA_HEADING = '{data_dict.get("heading", "NULL")}',
                    RCA_DESCRIPTION = {json.dumps(data_dict.get("description", []))}'
                    WHERE ID = '{pinned_elements.get("insight_id")}';""")

            write_response_to_db(
                table_name=pg_config["chat_history_table_name"],
                col_name=f"recommended_{request_type}",
                response=json.dumps(value_list),
                chat_id=chat_id,
                pg_db_conn=pg_db_conn,
            )
            pg_db_conn.close_connection()

    return_params = {
        "chat_id": chat_id,
        "response_type": (
            request_type if request_type != "linked_insights" else "linked_insights_response"
        ),
        f"{request_type}_list": value_list,
        "answer_str": (
            "Sorry! I am unable to find any relevant insights." if not value_list else None
        ),
    }
    return_params = {key: value for key, value in return_params.items() if value}
    return generate_response_dict(**return_params)


@log_time
def run_idea_generation_v2(
    json_file: str,
    chat_history: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Idea Generation model to generate RCA, Ideas, Linked Insights and user input responses

    Args:
        json_file (str): json payload from realtime endpoint
        chat_history (list[dict[str, Any]]): list of previous chat history from db
    Returns:
        dict : Dictionary consists chat_id, response_type and the model response
    """

    json_data = json.loads(json_file)
    chat_id = json_data.get("chat_id")
    request_type = json_data.get("request_type")

    try:

        input_data_validation(chat_id, request_type)

        if request_type == "user_input":
            intent_prompt = get_intent_prompt()
            request_type = generate_user_intent(
                intent_prompt,
                chat_history,
                json_data.get("user_input", ""),
                json_data.get("chat_id", ""),
            ).replace('"', "")
            log.info("request type from intent classifier : %s", request_type)

        pg_db_conn = PGConnector(tenant_id=json_data["tenant_id"])
        sf_client = SnowflakeClient()

        log.info("Identified request type %s", request_type)

        if json_data.get("pinned_elements").get("pinned_insights")!=[]:

            context_dict = {}

            pinned_elements = extract_pinned_elements(json_data, request_type != "user_input")

            context = sf_client.execute_query(f"""
                    SELECT ANALYTICS_NAME, SEGMENT, CATEGORY, INSIGHT, OBJECTIVE ,LINKED_INSIGHTS, 
                    RELATED_INSIGHTS,RCA_HEADING, RCA_DESCRIPTION,TOP_IDEAS FROM SAI_770ABBC_PROD_DB.DATA.INSIGHTS_MASTER
                    WHERE ID = '{pinned_elements.get("insight_id")}'""")
                
            context_col_names = [
            "analytics_name",
            "segment",
            "category",
            "insight",
            "objective",
            "linked_insights",
            "related_insights",
            "rca_heading",
            "rca_description",
            "top_ideas"
            ]

            for i, col_name in enumerate(context_col_names):
                context_dict[col_name] = context[0][i] if context[0][i] else None

            
        elif json_data.get("general_info",{}).get("idea") != "":

            context_dict = {}

            general_info = json_data.get("general_info",{})
            idea_description = general_info.get("idea_description","") if general_info else ""

            # if idea_description:
            context = sf_client.execute_query(f"""
                    SELECT ANALYTICS_NAME, SEGMENT, CATEGORY, INSIGHT, OBJECTIVE ,LINKED_INSIGHTS, 
                    RELATED_INSIGHTS,RCA_HEADING, RCA_DESCRIPTION,TOP_IDEAS FROM SAI_770ABBC_PROD_DB.DATA.INSIGHTS_MASTER
                    WHERE TOP_IDEAS ILIKE '%{idea_description}%'
                    LIMIT 1;""")
                
            context_col_names = [
            "analytics_name",
            "segment",
            "category",
            "insight",
            "objective",
            "linked_insights",
            "related_insights",
            "rca_heading",
            "rca_description",
            "top_ideas"
            ]

            for i, col_name in enumerate(context_col_names):
                context_dict[col_name] = context[0][i] if context[0][i] else None

        else:
            err_msg = "Please select an insight or top idea to continue ideating!"
            log.error(err_msg)
            raise IdeaGenException(err_msg)


        insight_context = context_dict
        
        user_input_response = generate_chat_model_response(
            json_data=json_data,
            chat_history=chat_history,
            pg_db_conn=pg_db_conn,
            sf_client = sf_client,
            insight_context=insight_context,
            # pinned_elements=pinned_elements,
        )
        pg_db_conn.close_connection()
        return generate_response_dict(
            chat_id=chat_id,
            response_type="user_input_response",
            answer_str=user_input_response,
        )
    
    except IdeaGenException as err:
        return generate_response_dict(
            chat_id=chat_id,
            response_type="exception",
            answer_str=f"Error : {err.args[0]}",
        )