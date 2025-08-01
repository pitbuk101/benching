"""Negotiation factory use-case."""

from __future__ import annotations

import copy
import json
from typing import Any

from ada.components.db.pg_connector import PGConnector
from ada.components.db.sf_connector import SnowflakeClient

# pylint: disable=W0611
from ada.components.llm_models.generic_calls import run_conversation_chat
from ada.use_cases.negotiation_factory.email_generation import (  # noqa: F401
    generate_email_thread,
    generate_summary_email,
)
from ada.use_cases.negotiation_factory.exception import (
    NegotiationFactoryException,
    NegotiationFactoryQueryException,
    NegotiationFactoryUserException,
)
from ada.use_cases.negotiation_factory.extract_supplier_from_user_query import (  # noqa: F401
    generate_carrots_and_sticks,
    generate_scoping,
    negotiation_init,
)
from ada.use_cases.negotiation_factory.intent_prompts import intent_prompt
from ada.use_cases.negotiation_factory.negotiation_factory_utils import (  # noqa: F401
    clear_chat_history,
    convert_to_response_format,
    ensure_key_exist,
    get_probable_intent,
)
from ada.use_cases.negotiation_factory.negotiation_gameplan_components import (  # noqa: F401
    generate_csb_positioning,
    generate_insights,
    generate_objectives,
    generate_strategy,
    generate_tones_n_tactics,
)
from ada.use_cases.negotiation_factory.negotiation_models import (  # noqa: F401
    finish_negotiation,
    generate_arguments_counter_argument_rebuttal_workflow,
    generate_user_answers,
    save_negotiation_latest_offer,
)
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time
from ada.use_cases.negotiation_factory.insight_generation import (  # noqa: F401
    generate_nego_insights)
# pylint: enable=W0611

log = get_logger("Negotiation_factory")
negotiation_conf = read_config("use-cases.yml")["negotiation_factory"]


@log_time
def get_intent(
    chat_history: list,
    category: str,
    user_query: str,
    selected_elements: dict,
    chat_id: str = "",
) -> tuple[str, str]:
    """
    Model that takes in user-conversation history, user query to get intent
    Args:
        chat_history (list) : chat history details from database
        category (str): user selected category
        user_query (str): user query
        selected_elements (dict): The selected elements dict
        chat_id (str): Chat id for the session
    Returns:
        (tuple[str, str]) : Identified intent and the user query
    """
    log.info("get_intent called for category '%s' and chat_id '%s'", category, chat_id)
    log.info("User query: %s", user_query)
    log.debug("Selected elements keys: %s", list(selected_elements.keys()))

    previous_response = dict(chat_history[-1]).get("response_type", "") if chat_history else ""
    log.info("Previous response from chat history: %s", previous_response)

    intent_value = get_probable_intent(previous_response)
    log.info("Probable intent based on previous response: %s", intent_value)

    if not intent_value:
        prompt = intent_prompt(
            category_name=category,
            selected_elements=selected_elements,
            previous_response_type=previous_response,
            likely_current_intent=intent_value,
        )
        log.info("Intent prompt generated, calling LLM for response")

        ai_response = run_conversation_chat(
            chat_history=chat_history,
            prompt=prompt,
            input_str=user_query,
            memory_type="window",
            model=negotiation_conf["model"]["model_name"],
            window_size=negotiation_conf["model"]["conversation_buffer_window"],
            temperature=0,
            input_message_key="input",
            history_message_key="history",
            session_id=chat_id,
        )
        log.info("AI model raw response for intent: %s", ai_response)
        intent_value = ai_response.replace('"', "").strip()
        if intent_value != "summary_email":
            intent_value = (
                f"{intent_value}_generic"
                if ("email" in intent_value or "arguments" in intent_value)
                else intent_value
            )
        log.info("Final intent value after generic adjustment: %s", intent_value)

    intent_value = f"""negotiation_{intent_value}"""
    log.info("Final intent to be returned: %s", intent_value)

    return intent_value, user_query

@log_time
def run_negotiation_factory(
    input_data_str: str,
    reference_data: dict[str, Any],
    pg_db_conn: PGConnector,
    chat_history: list,
) -> dict[str, Any]:
    """
    Runs the negotiation factory and its different use cases based on user request.
    Args:
        input_data_str (str): Payload received for negotiation model from API call
        reference_data( dict[str, Any]): tenant specific reference data
        pg_db_conn (PGConnector): Connection object to postgres database
        chat_history (list): history of the conversation
    Returns:
        (dict[str, Any]): the output from the model in the required format
    """
    log.info("run_negotiation_factory called")
    log.debug("Raw input data string: %s", input_data_str)

    input_data = json.loads(input_data_str)
    request_type = ""
    try:
        required_fields = [
            "tenant_id",
            "category",
            "negotiation_id",
            "user_query",
            "pinned_elements",
            "request_type",
        ]
        (
            tenant_id,
            category,
            negotiation_id,
            user_query,
            pinned_elements,
            request_type,
        ) = (ensure_key_exist(field, input_data, return_element=True) for field in required_fields)

        log.info("Tenant ID: %s | Category: %s | Negotiation ID: %s", tenant_id, category, negotiation_id)
        log.info("Request type from payload: %s", request_type)

        if not (isinstance(negotiation_id, str) and negotiation_id):
            error_message = "Negotiation Id is not correct."
            log.error(error_message)
            raise NegotiationFactoryException(error_message)

        pg_db_conn = pg_db_conn or PGConnector(tenant_id=tenant_id, cursor_type="real_dict")
        sf_client = SnowflakeClient(tenant_id=tenant_id)

        if request_type.startswith("supplier_name"):
            log.info("Supplier name present in user query. Replacing in pinned elements.")
            input_data["pinned_elements"]["supplier_name"] = user_query
            request_type = (
                request_type.split("|")[1] if "|" in request_type else "negotiation_begin"
            )

        selected_elements = input_data.get("selected_elements", {})
        before_update_request_type = copy.deepcopy(request_type)

        if not request_type:
            log.info("No request_type found. Calling intent model to predict.")
            request_type, user_query = get_intent(
                chat_history=chat_history,
                category=category,
                user_query=user_query,
                selected_elements=selected_elements,
            )
            log.info("Predicted request_type: %s", request_type)

        skus = input_data.get("pinned_elements", {}).get("skus", [])
        log.info("Total SKUs provided: %d", len(skus) if skus else 0)
        log.info("Reference data keys: %s", reference_data.keys())
        log.info("Tenant-specific reference keys: %s", reference_data.get(tenant_id, {}).keys())

        params = {
            "sf_client": sf_client,
            "pg_db_conn": pg_db_conn,
            "skus": skus,
            "category": category,
            "user_query": user_query,
            "pinned_elements": pinned_elements,
            "reference_data": reference_data.get(tenant_id, {}),
            "chat_history": chat_history,
            "selected_elements": selected_elements,
            "generation_type": request_type,
            "chat_id": negotiation_id,
            "before_update_request_type": before_update_request_type,
            "current_round": input_data.get("current_round", 1),
            "tenant_id": tenant_id,
        }

        if request_type.startswith("negotiation_emails"):
            log.info("Email use case detected. Normalizing request type.")
            request_type = "negotiation_emails_generic"

        if (
            request_type.startswith("negotiation_arguments")
            or request_type.startswith("negotiation_rebuttals")
            or request_type.startswith("negotiation_counter_arguments")
        ):
            log.info("Argument-related use case detected. Normalizing request type.")
            request_type = "negotiation_arguments_generic"
        
        if request_type in negotiation_conf["function_map"]:
            log.info("Found matching function for request type: %s", request_type)
            negotiation_function = globals()[negotiation_conf["function_map"][request_type]]
            response = negotiation_function(**params)
            log.info("Generated response successfully for request type: %s", request_type)
            log.info("Response: %s", response)
            return response

        log.info("Calling generic user answer generation function")
        ai_response = generate_user_answers(**params)
        return ai_response

    except (
        NegotiationFactoryException,
        NegotiationFactoryQueryException,
    ) as negotiation_factory_exception:
        log.error("NegotiationFactory error: %s", negotiation_factory_exception)
        suggested_prompts = (
            (chat_history[-1] if chat_history else {})
            .get("response", {})
            .get("suggested_prompts", [])
        )
        return convert_to_response_format(
            response_type="exception",
            message=negotiation_factory_exception.args[0],
            suggested_prompts=suggested_prompts,
        )

    except NegotiationFactoryUserException as negotiation_factory_user_exception:
        message, *prompts = negotiation_factory_user_exception.args
        log.warning("User exception: %s", message)
        suggested_prompts = (prompts[0] if prompts else []) or (
            chat_history[-1] if chat_history else {}
        ).get("response", {}).get("suggested_prompts", [])

        for prompt in suggested_prompts:
            if prompt["intent"] == "supplier_name" and request_type:
                prompt["intent"] = f"supplier_name|{request_type}"

        return convert_to_response_format(
            response_type="general",
            message=message,
            suggested_prompts=suggested_prompts,
        )
