"""Intent Classification use-case"""

import json
from typing import Any

from ada.components.db.pg_connector import PGConnector
from ada.use_cases.intent_classification.exception import (
    IntentModelUserException,
    OutOfScopeIntentException,
)
from ada.use_cases.intent_classification.intent_utils import (
    add_nf_specific_suggested_prompts,
    check_key,
    get_chat_history_from_db,
    get_intent,
    get_prerequisites_for_individual_request_payloads,
    get_response_to_save,
    save_conversation_history,
)
from ada.utils.config.config_loader import read_config
from ada.utils.io.function_mapping import function_mapping
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time
from ada.utils.metrics.context_manager import (
    set_intent_flow_context,
    set_tenant_context,
)
from ada.utils.metrics.similarity import get_similarity_score

intent_model_conf = read_config("use-cases.yml")["intent_model_v2"]
log = get_logger("intent_classification_v2")


@log_time
def run_unified_model(json_data: str, **kwargs: dict[str, Any]) -> dict[str, Any]:
    """
    Take the request from the user/ atlas, gets the right intent, and then returns the unified
        response to the user/ atlas
    Args:
        json_file (str): Unified json payload from realtime endpoint
    Returns:
        unified_response (dict[str, Any]): Response from all the models.
    """
    # json_data = json.loads(json_file)
    log.info('run_unified_model')
    try:
        for key in ["tenant_id", "chat_id", "request_id", "category", "page_id"]:
            check_key(key, json_data)
        pg_db_conn = PGConnector(
            tenant_id=json_data["tenant_id"],
            cursor_type="real_dict",
        )

        set_tenant_context(json_data["tenant_id"])

        chat_history_from_db = get_chat_history_from_db(json_data["chat_id"], pg_db_conn)
        chat_history_from_db = chat_history_from_db[-20:]
        if json_data.get("request_type", "") == "key_facts_dashboard":
            json_data["dax_response_code"] = 601
        # intent based on page-id or dax_response key
        intent_type = (
            "key-facts-v2"
            if json_data.get("dax_response_code", "")
            else intent_model_conf["page_id_intent_map"].get(json_data.get("page_id", ""), "")
        )
        log.info(
            "run unified model: The identified intent is %s",
            intent_type,
        )
        log.info('model_router getting called')
        unified_response_payload = model_router(
            intent_type,
            json_data,
            pg_db_conn,
            chat_history_from_db,
            num_hops=0,
            all_reference_data=kwargs["all_reference_data"],
            category_configuration=kwargs["category_configuration"],
            # question_classifier_model=kwargs["question_classifier_model"],
        )
        pg_db_conn.close_connection()
        return unified_response_payload
    except OutOfScopeIntentException as out_of_scope_intent_exception:
        return {
            "chat_id": json_data.get("chat_id"),
            "request_id": json_data.get("request_id"),
            "message": out_of_scope_intent_exception.args[0],
        }
    except IntentModelUserException as intent_model_user_exception:
        return {
            "chat_id": json_data.get("chat_id"),
            "request_id": json_data.get("request_id"),
            "message": intent_model_user_exception.args[0],
        }


@log_time
def model_router(
    intent_type: str,
    json_file: dict,
    pg_db_conn: PGConnector,
    chat_history_from_db: list | None = None,
    num_hops: int = 0,
    **kwargs: Any,
) -> dict:
    """
    Takes the request type as the input and calls the appropriate model and returns the response
    Args;
        intent_type (str): The intent_type which determines which model is to be called
        json_file (dict): The unified_request_payload
        pg_db_conn (PGConnector): PG connector object for writing into database
        chat_history_from_db (list): Chat memory object
        num_hops (int): The number of hops taken by GenAI
    Returns:
        (dict): Unified response from all the models.
    """
    if chat_history_from_db is None:
        chat_history_from_db = []
    if not intent_type:
        log.info("Identifying intent for user query using LLM")
        check_key("user_query", json_file)
        user_query = json_file.get("user_query")
        intent_type = get_intent(
            user_query,
            json_file.get("category", "Category"),
            chat_history=chat_history_from_db,
            chat_id=json_file.get("chat_id", ""),
        )
    log.info("The identified intent is %s", intent_type)
    if intent_type not in intent_model_conf["usecase_scope"]:
        intent_type = "source-ai-knowledge"

    individual_request_payload = get_individual_request_payload(
        json_file,
        intent_type,
    )
    log.info(f"The individual request payload for the intent {individual_request_payload}")


    additional_payload = {
        # "contract-qa": {"model": kwargs["question_classifier_model"]},
        "key-facts-v2": {"configuration_val": kwargs["category_configuration"]},
        "negotiation-factory": {
            "pg_db_conn": pg_db_conn,
            "reference_data": kwargs["all_reference_data"]["negotiation-factory"],
            "chat_history": chat_history_from_db,
        },
        "source-ai-knowledge": {
            "chat_history": chat_history_from_db,
            "pg_db_conn": pg_db_conn,
        },
        "idea-generation-v3": {
            "chat_history": chat_history_from_db,
        },
        "dynamic-ideas": {
            "chat_history": chat_history_from_db,
            "pg_db_conn": pg_db_conn,
        },
    }

    intent_model_mapping = function_mapping()

    set_intent_flow_context(intent_model_mapping[intent_type]["use_case"])

    individual_response_payload = intent_model_mapping[intent_type]["run"](
        json.dumps(individual_request_payload),
        **additional_payload.get(intent_type, {}),
    )
    log.info(f"The individual response payload for the intent {intent_type} is {individual_response_payload}")

    if intent_type == "contract-qa":
        individual_response_payload = individual_response_payload[0]

    unified_response_payload = get_unified_response(
        individual_response_payload,
        json_file,
    )
    log.info(f'the unified response payload for the intent {intent_type} is {unified_response_payload}')

    check_response_val = unified_response_payload.get(
        "message",
        "",
    ).lower() or unified_response_payload.get("response_prerequisite", "")
    if (
        get_similarity_score(check_response_val, "no", model="en_core_web_sm")
        < intent_model_conf["no_threshold"]
    ):
        if (
            json_file.get("dax_response_code", "")
            not in intent_model_conf["allowed_key_fact_codes"]
        ) and (unified_response_payload.get("response_type") != "clear_chat_success"):
            save_response = get_response_to_save(
                individual_response_payload,
                individual_request_payload,
                intent_type,
            )
            log.info(f'The response to save is {save_response}')
            save_conversation_history(
                json_file["chat_id"],
                json_file["request_id"],
                save_response,
                pg_db_conn,
            )
        log.info(
            "The response from the model is %s",
            json.dumps(unified_response_payload),
        )

        nf_specific_suggested_prompts_condition = (
            unified_response_payload.get("response_type") != "dax"
            and json_file.get("page_id") == "negotiation"
            and intent_type != "negotiation-factory"
        )
        if nf_specific_suggested_prompts_condition:
            log.info("Addition of NF specific suggested prompts for intent %s", intent_type)
            unified_response_payload = add_nf_specific_suggested_prompts(
                unified_response_payload,
            )
        return unified_response_payload

    if num_hops < intent_model_conf["num_hops"]:
        intent_type = ""
        return model_router(
            intent_type,
            json_file,
            pg_db_conn=pg_db_conn,
            chat_memory=chat_history_from_db,
            num_hops=num_hops + 1,
            all_reference_data=kwargs["all_reference_data"],
            category_configuration=kwargs["category_configuration"],
            # question_classifier_model=kwargs["question_classifier_model"],
        )

    individual_response_payload["message"] = intent_model_conf["answer_not_found"]
    return get_unified_response(individual_response_payload, json_file)


def get_unified_response(individual_response: dict, request_json: dict) -> dict:
    """
    Takes the individual response payload and returns the unified response payload
    Args:
        individual_response (dict): Individual response payload from the models
        request_json (str): Request dict for the response
    Return:
        (dict): Unified response payload
    """
    individual_response = (
        individual_response[0] if isinstance(individual_response, list) else individual_response
    )
    message = (
        individual_response.get("message", "")
        or individual_response.get("answer", "")
        or individual_response.get("result", [])
        or individual_response.get("response", {}).get("answer", "")
    )

    if len(message) > 0:
        message = (
            message[0].get("insight", [])
            if isinstance(
                message[0],
                dict,
            )
            else message
        )
    
    unified_response = {
        "chat_id": request_json["chat_id"],
        "request_id": request_json.get("request_id", ""),
        "message": message,
        "response_type": individual_response.get("response_type", ""),
        "response_prerequisite": individual_response.get("response_prerequisite", ""),
        "additional_text": individual_response.get("additional_text", ""),
        "links": individual_response.get("links", ""),
        "question": individual_response.get("question", ""),
        "root_causes": individual_response.get("response", {}).get("root_causes", []),
        "ideas": individual_response.get("response", {}).get("ideas", []),
        "linked_insights": individual_response.get("response", {}).get("linked_insights", []),
        "arguments": individual_response.get("arguments", []),
        "counter_arguments": individual_response.get("counter_arguments", []),
        "rebuttals": individual_response.get("rebuttals", []),
        "supplier_profile": individual_response.get("supplier_profile", []),
        "suggested_prompts": individual_response.get("suggested_prompts", []),
        "negotiation_strategy": individual_response.get("negotiation_strategy", {}),
        "negotiation_approach": individual_response.get("negotiation_approach", {}),
        "category_positioning": individual_response.get("category_positioning", []),
        "supplier_positioning": individual_response.get("supplier_positioning", []),
        "buyer_positioning": individual_response.get("buyer_positioning", []),
        "category_positions": individual_response.get("category_positions", []),
        "supplier_positions": individual_response.get("supplier_positions", []),
        "insights": individual_response.get("insights", []),
        "objectives": individual_response.get("objectives", []),
        "emails": individual_response.get("emails", []),
        "additional_data": individual_response.get("additional_data", {}),
        "suppliers_profiles": individual_response.get("suppliers_profiles", []),
        "tones": individual_response.get("tones", []),
        "tone": individual_response.get("tone", {}),
        "carrots": individual_response.get("carrots", []),
        "sticks": individual_response.get("sticks", []),
        "dynamic_ideas": individual_response.get("dynamic_ideas", []),
        "skus": individual_response.get("skus", []),
        "selected_positioning": individual_response.get("selected_positioning", ""),
    }

    unified_response = {key: val for key, val in unified_response.items() if val}
    unified_response["message"] = message or ""
    return unified_response


def get_individual_request_payload(json_file: dict, intent_type: str) -> dict:
    """
    Takes the unified payload and constructs the model-specific payload
    Args:
        json_file (dict): The unified request payload
        intent_type (str): The intent to specify the model type
    Returns:
        (dict): Modified model-specific payload.
    """
    payload_required = get_prerequisites_for_individual_request_payloads(
        json_file,
    )
    update_json_file = {
        key: json_file.get(key, value) for key, value in payload_required[intent_type].items()
    }
    json_file.update(update_json_file)
    return json_file
