"""Negotiation factory email generation model"""

import json
from typing import Any

from ada.components.db.pg_connector import PGConnector
from ada.components.llm_models.generic_calls import (
    generate_chat_response_with_chain,
    generate_conversational_rag_agent_response,
    run_conversation_chat,
)
from ada.components.llm_models.model_base import Model
from ada.components.vectorstore.vectorstore import PGRetriever
from ada.use_cases.negotiation_factory.negotiation_factory_utils import (
    convert_to_response_format,
    extract_model_context,
    get_generation_type,
    get_negotiation_model_context,
    identify_negotiation_objective,
    json_regex,
)
from ada.use_cases.negotiation_factory.prompts import email_prompt, summary_email_prompt
from ada.use_cases.negotiation_factory.rag_prompts import email_rag_prompt
from ada.use_cases.negotiation_factory.util_prompts import check_email_prompt
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time
from ada.utils.metrics.similarity import get_best_match_from_list

log = get_logger("Negotiation_factory_email_generation")
negotiation_conf = read_config("use-cases.yml")["negotiation_factory"]


@log_time
def get_emails(chat_history: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Get email chain from chat history
    Args:
       chat_history (list[dict[str, Any]]): chat history list
    Return:
       (list[dict[str, Any]]): email chain
    """
    email_chain = []
    for val in reversed(chat_history):
        if val.get("response_type", "") == "emails":
            email_chain = val.get("response", {}).get("emails", [])
            log.info("email chain %s", json.dumps(email_chain))
            return email_chain
    return email_chain


@log_time
def append_email_to_thread(
    email_thread: list[dict[str, Any]],
    new_email_details: str,
    chat_history: list[dict[str, Any]],
    id_prefix: str = "",
    email_type: str = "ada",
) -> list[dict[str, Any]]:
    """
    Updates the generated emails into email thread.
    Args:
        email_thread: list[dict[str, Any]]: similar elements generated previously
        new_email_details (str): new email to attach
        chat_history (list[dict[str, Any]]): List of previous actions.
        id_prefix (str): ID string for generating the ids
        email_type (str): Type of email, ada generated or supplier
    Returns:
         (list[dict[str, Any]]): the email thread with the newly generated email"""
    email = {
        "id": f"{id_prefix}{1}",
        "details": new_email_details,
        "children": [],
        "type": email_type,
    }
    if not email_thread:
        return [email]
    # update id logic here; the earlier version might give duplicated ids
    if email_thread[0].get("children", []):
        current_id = int(email_thread[0]["children"][-1]["id"].replace(id_prefix, ""))
    else:
        current_id = int(email_thread[0]["id"].replace(id_prefix, ""))
    email["id"] = f"{id_prefix}{current_id + 1}"
    if chat_history and chat_history[-1].get("response_type") == "negotiation_emails_modify":
        log.info("email chain %s", json.dumps(email_thread))
        if email_thread[0].get("children"):
            email_thread[0]["children"][-1] = email
        else:
            email_thread = [email]
    else:
        email_thread[0]["children"].append(email)
    return email_thread


@log_time
def generate_email_thread(
    reference_data: dict[str, Any],
    pg_db_conn: PGConnector,
    category: str,
    user_query: str,
    pinned_elements: dict[str, Any],
    chat_history: list,
    selected_elements: dict[str, Any],
    generation_type: str = "",
    **kwargs: Any,
):
    """
    Chat thread that takes in user-conversation history, arguments, counter-arguments, facts
    and past examples to generate a contextual email thread
    Args:
         reference_data (dict[str, Any]): tenant specific negotiation factory reference data
         pg_db_conn (PGConnector) : Connection object to postgres database
         category (str): user selected category
         user_query (str): User question with key instructions.
         pinned_elements (dict[str, Any]): Pinned elements including insights, objectives
         chat_history (list) : chat history extracted from DB
         selected_elements (dict[str, Any]): selected elements like arguments,
                                        counter-arguments, rebuttals
        generation_type (dict): type of request
        kwargs (Any): Any additional data
     Returns:
         (dict[str, Any]): LLM Generated email thread
    """
    log.info("request_type %s", generation_type)
    log.info(" Generating email %d", len(kwargs))
    cta_email_map = negotiation_conf["cta_email_map"]
    if generation_type not in cta_email_map.keys():
        generation_type = get_generation_type(
            cta_map=cta_email_map,
            user_query=user_query,
            threshold=negotiation_conf["email_cta_threshold"],
            default_str="negotiation_emails_generic",
        )
        previous_response = dict(chat_history[-1]).get("response_type", "") if chat_history else ""
        if "email" not in previous_response and generation_type == "negotiation_emails_generic":
            generation_type = "negotiation_emails_new"

    if generation_type == "negotiation_emails_reply_to_supplier":
        return convert_to_response_format(
            response_type=generation_type,
            message="Can you provide the email from supplier?",
        )
    # if generation_type in [
    #     "negotiation_emails",
    #     "negotiation_emails_continue",
    #     "negotiation_emails_new",
    # ]:
    #     return convert_to_response_format(
    #         response_type=generation_type,
    #         message="Can you provide more context on the purpose of this email?",
    #     )
    if generation_type == "negotiation_emails_modify":
        return convert_to_response_format(
            response_type=generation_type,
            message="Could you please provide details on the modifications needed in the email?",
        )

    # generate email in case of reply to supplier, modify email or new email
    log.info("going into generate email flow %s", generation_type)
    suggested_prompt = [
        {
            "prompt": cta_email_map["negotiation_emails_modify"],
            "intent": "negotiation_emails_modify",
        },
        {
            "prompt": cta_email_map["negotiation_emails_reply_to_supplier"],
            "intent": "negotiation_emails_reply_to_supplier",
        },
        {
            "prompt": cta_email_map["negotiation_emails_continue"],
            "intent": "negotiation_emails_continue",
        },
    ]

    objectives_in_action = identify_negotiation_objective(
        pinned_elements=pinned_elements,
        is_all_objectives_in_action=True,
    )
    objective_types = [
        objective.get("objective_type", "")
        for objective in objectives_in_action
        if objective.get("objective_type", "").lower() != "key facts"
    ]

    # pylint: disable=R0801
    (
        supplier_name,
        supplier_profile,
        objective_descriptions,
    ) = extract_model_context(
        reference_data,
        pg_db_conn,
        category,
        user_query,
        pinned_elements,
        objective_types,
    )
    # pylint: enable=R0801
    
    emails = get_emails(chat_history)
    response = generate_email(
        supplier_name,
        objective_descriptions,
        user_query,
        pinned_elements,
        chat_history,
        selected_elements,
        emails,
        reference_data=reference_data,
        pg_db_conn=pg_db_conn,
    )
    log.info("Generated Response %s", response)

    supplier_email_found = generate_chat_response_with_chain(
        check_email_prompt(user_query),
        negotiation_conf["model"]["model_name"],
    )

    log.info("Supplier email found %s", supplier_email_found)

    if supplier_email_found.lower() == "true":
        emails = append_email_to_thread(
            emails,
            new_email_details=user_query,
            chat_history=chat_history,
            id_prefix="EM_",
            email_type="supplier",
        )

    formatted_email_details = append_email_to_thread(
        emails,
        new_email_details=response.get("emails", "").replace('"', ""),
        id_prefix="EM_",
        email_type="ada",
        chat_history=chat_history,
    )
    default_message = "Please find the draft email below: "
    message = (
        ""
        if get_best_match_from_list(
            ["supplier emails not found", "supplier email found"],
            response.get("message", ""),
            negotiation_conf["model"]["similarity_model"],
            0.9,
        )
        else response.get("message")
    )

    params = {
        "response_type": "emails" if response.get("emails") else "general",
        "message": (message or default_message),
        "supplier_profile": supplier_profile,
        "suggested_prompts": suggested_prompt,
    }
    if response.get("emails"):
        params["emails"] = formatted_email_details
    return convert_to_response_format(**params)


@log_time
def generate_email(
    supplier_name: str,
    objective_descriptions: list[str],
    user_query: str,
    pinned_elements: dict[str, Any],
    chat_history: list,
    selected_elements: dict[str, Any],
    emails: list[dict[str, Any]],
    pg_db_conn: PGConnector,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Chat Model that takes in user-conversation history, arguments, counter-arguments, facts
    and past examples to generate a contextual email
    Args:
         supplier_name (str): supplier name
         objective_descriptions (list[str]): pinned objective descriptions
         user_query (str): User question with key instructions.
         pinned_elements (dict[str, Any]): Pinned elements including insights
         chat_history (list): chat history extracted from DB
         selected_elements (dict[str, Any]): selected elements like arguments,
                                        counter-arguments, rebuttals
         emails (list[dict[str, Any]]): List of previously generated emails in an email chain
         pg_db_conn (PGConnector): Pg database connector objector
         kwargs (Any): Any additional data
     Returns:
         (dict[str, Any]): LLM Generated emails
    """
    log.info("Starting to generate emails, additional data %d", len(kwargs))
    reference_data = kwargs.get("reference_data", {})
    category = pinned_elements.get("supplier_profile", {}).get("category_name", "")

    model_context = get_negotiation_model_context(
        pg_db_conn,
        category,
        user_query,
        pinned_elements,
        generation_type="emails",
        is_all_objectives_in_action=True,
        reference_data=reference_data
    )
    reference_data = reference_data.get("email_references")

    rag_prompt = email_rag_prompt(
        supplier_name,
        pinned_elements,
        selected_elements,
        emails,
        reference_data,
        model_context,
    )

    # prompt = email_prompt(
    #     supplier_name,
    #     pinned_elements,
    #     selected_elements,
    #     emails,
    #     objective_descriptions,
    #     reference_data,
    # )

    # pylint: disable=R0801
    pg_retriever = PGRetriever(
        pg_db_conn=pg_db_conn,
        k=negotiation_conf["model"]["email_retriever_k"],
        table_name=negotiation_conf["tables"]["knowledge_base"],
        embeddings_model=negotiation_conf["model"]["similarity_model"],
        embeddings_column_name="embedding",
        column_names=["chunk_content", "page"],
        conditions=f"category_name in ('{category}', 'ALL', 'all') or category_name is NULL",
    )
    # pylint: enable=R0801

    default_params = {
        "chat_history": chat_history,
        # "prompt": prompt,
        "input_str": user_query,
        "model": negotiation_conf["model"]["model_name"],
        "window_size": negotiation_conf["model"]["conversation_buffer_window"],
        "session_id": kwargs.get("chat_id", ""),
    }

    default_function = run_conversation_chat
    tone = model_context.get("tone", {})

    buffer_win = -1 * negotiation_conf["model"]["conversation_buffer_window"]

    ai_response_dict = generate_conversational_rag_agent_response(
        user_query=user_query,
        prompt=rag_prompt,
        retriever=pg_retriever,
        chat_history=chat_history[buffer_win:],
        model=negotiation_conf["model"]["model_name"],
        fast_model=negotiation_conf["model"]["fast_model_name"],
        default_function=default_function,
        params=default_params,
        max_documents=5,
        temperature = 0.5,
        additional_params={"tone": tone.get("title", "")},
        compressor=Model(name=negotiation_conf["model"]["fast_model_name"]).obj,
    )
    
    # pylint: disable=R0801
    response = (
        ai_response_dict.get("generation", "")
        .replace("\\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n", "\n\n")
        .replace("json", "")
        .replace("`", "")
    )
    # pylint: enable=R0801
    log.info("Response from negotiation email conversation chain: %s", response)
    try:
        response = {"emails":response}
        # response = json.loads(response)
    except json.decoder.JSONDecodeError as json_loads_exception:
        log.info("Json loading exception %s", str(json_loads_exception))
        response = json_regex(response, ["message", "emails"])
    return response


@log_time
def generate_summary_email(
    reference_data: dict[str, Any],
    pg_db_conn: PGConnector,
    category: str,
    user_query: str,
    pinned_elements: dict[str, Any],
    chat_history: list,
    before_update_request_type: str,
    generation_type: str = "",
    **kwargs: Any,
):
    """
    Chat thread that takes in user-conversation history, arguments, counter-arguments, facts
    and past examples to generate a contextual email thread
    Args:
         reference_data (dict[str, Any]): tenant specific negotiation factory reference data
         pg_db_conn (PGConnector) : Connection object to postgres database
         category (str): user selected category
         user_query (str): User question with key instructions.
         pinned_elements (dict[str, Any]): Pinned elements including insights
         chat_history (list) : chat history extracted from DB
         generation_type (dict): type of request
         kwargs (Any): Any additional data
     Returns:
         (dict[str, Any]): LLM Generated email thread
    """
    log.info("Request type %s", generation_type)
    log.info("Generating summary email %d", len(kwargs))
    log.info("Starting to generate summary emails, additional data %d", len(kwargs))

    if before_update_request_type == "":
        msg = (
            "`Generate Summary Email` feature is accessible through awarding section."
            "\nPlease navigate from quick menu to proceed further."
        )
        return convert_to_response_format(
            response_type="negotiation_summary_email",
            message=msg,
            suggested_prompts=[],
        )

    objectives_in_action = identify_negotiation_objective(
        pinned_elements=pinned_elements,
        is_all_objectives_in_action=True,
    )
    objective_types = [
        objective.get("objective_type", "")
        for objective in objectives_in_action
        if objective.get("objective_type", "").lower() != "key facts"
    ]

    # pylint: disable=R0801
    (
        supplier_name,
        supplier_profile,
        objective_descriptions,
    ) = extract_model_context(
        reference_data,
        pg_db_conn,
        category,
        user_query,
        pinned_elements,
        objective_types,
    )

    reference_data = kwargs.get("reference_data", {})
    prompt = summary_email_prompt(supplier_name, pinned_elements, objective_descriptions)
    # pylint: disable=R0801
    response = (
        run_conversation_chat(
            chat_history=chat_history,
            prompt=prompt,
            input_str=user_query,
            model=negotiation_conf["model"]["model_name"],
            window_size=negotiation_conf["model"]["conversation_buffer_window"],
            session_id=kwargs.get("chat_id", ""),
        )
        .replace("\\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n", "\n\n")
        .replace("json", "")
        .replace("`", "")
    )
    # pylint: enable=R0801
    log.info("Response from negotiation email conversation chain: %s", response)
    try:
        response = json.loads(response)
    except json.decoder.JSONDecodeError as json_loads_exception:
        log.info("Json loading exception %s", str(json_loads_exception))
        response = json_regex(response, ["message", "emails"])

    params = {
        "response_type": "negotiation_summary_email",
        "message": "Please find the draft summary email below:",
        "suggested_prompts": [],
        "supplier_profile": supplier_profile,
        "emails": [
            {
                "id": "EM_1",
                "details": response.get("emails", ""),
                "type": "ada",
                "children": [],
            },
        ],
    }

    return convert_to_response_format(**params)
