"""Argument model used in Negotiation factory"""

# pylint: disable=C0302
import copy
import json
import re
import time
from typing import Any

from ada.components.db.pg_connector import PGConnector
from ada.components.llm_models.generic_calls import (
    generate_chat_response,
    generate_conversational_rag_agent_response,
    run_conversation_chat,
)
from ada.utils.format.format import exception_response
from ada.components.llm_models.model_base import Model
from ada.components.vectorstore.vectorstore import PGRetriever
from ada.use_cases.negotiation_factory.negotiation_factory_utils import (
    convert_to_response_format,
    extract_objective_description,
    extract_qa_context,
    format_details_string,
    get_argument_conversation_history,
    get_argument_section_suggested_prompts,
    get_generation_type,
    get_negotiation_model_context,
    get_section_suggested_prompts,
    get_workflow_suggested_prompts,
    identify_negotiation_objective,
    json_regex,
    perform_argument_prerequisite_check,
    perform_finish_negotiation_prerequisite_check,
    perform_offer_prerequisite_check,
    update_negotiation_details,
)

from ada.use_cases.negotiation_factory.negotiation_factory_utils import extract_supplier_name_from_user_query
from ada.components.llm_models.generic_calls import generate_chat_response_with_chain
from ada.use_cases.negotiation_factory.prompts import create_chatbot_prompt
from ada.use_cases.key_facts_chatbot.call_keyfact_chatbot import fetch
from ada.use_cases.key_facts.key_facts_v3 import summarize_dax_output
from ada.use_cases.negotiation_factory.prompts import (
    argument_prompt,
    counter_argument_rebuttal_prompt,
    user_query_prompt,
)
from ada.use_cases.negotiation_factory.rag_prompts import (
    argument_rag_prompt,
    counter_argument_rebuttal_rag_prompt,
)
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time
from ada.utils.metrics.similarity import get_best_match_from_list

log = get_logger("Negotiation_factory_argument_model")
negotiation_conf = read_config("use-cases.yml")["negotiation_factory"]


@log_time
def get_ctas(
    user_query: str,
    chat_history: list[tuple[str, str]],
    generation_type: str,
    **kwargs: Any,
) -> dict[str, str]:
    """
    Get the CTAs for the given generation type
    Args:
        user_quer (str): User question
        chat_history (list[tuple[str, str]]): Chat history
        generation_type (str): The type of out we are generating
        kwargs (Any): Any additional arguments
    Returns:
        (dict[str, str]): CTAs for the given generation type
    """
    next_step = "rebuttals" if generation_type == "counter_arguments" else "emails"

    suggested_prompts = get_section_suggested_prompts(
        section_name="Generate Arguments",
    )

    if generation_type == "arguments":
        key_if_user_query_found_in_map = ""
        previous_response = ""
        generation_type_before_edit = kwargs.get("generation_type_before_edit", "")
        if user_query != "":
            for key, value in negotiation_conf["cta_argument_map"].items():
                lw_user_query = str(user_query).strip().lower()
                lw_value = str(value).strip().lower()
                if lw_user_query == lw_value:
                    key_if_user_query_found_in_map = key
                    break

        if key_if_user_query_found_in_map == "":
            suffixes = ("_new", "_reply", "_modify")
            for chat in reversed(chat_history):
                previous_response = chat.get("response_type", "")  # type: ignore
                if previous_response.endswith(suffixes):
                    break

        if (
            key_if_user_query_found_in_map == "arguments_new"
            or previous_response == "arguments_new"
            or generation_type_before_edit == "arguments_new"
        ):
            log.info("Current state - arguments_new - Generate new arguments")
            suggested_prompts = get_argument_section_suggested_prompts(
                intent="arguments_new",
            )
        elif (
            key_if_user_query_found_in_map == "arguments_modify"
            or previous_response == "arguments_modify"
            or generation_type_before_edit == "arguments_modify"
        ):
            log.info("Current state - arguments_modify - Modify arguments")
            suggested_prompts = get_argument_section_suggested_prompts(
                intent="arguments_modify",
            )
        elif (
            key_if_user_query_found_in_map == "arguments_reply"
            or previous_response == "arguments_reply"
            or generation_type_before_edit == "arguments_reply"
        ):
            log.info("Current state - arguments_reply - Reply to supplier arguments")
            generation_type = "rebuttals"
            suggested_prompts = get_argument_section_suggested_prompts(
                intent="arguments_reply",
            )
    elif generation_type == "rebuttals":
        suggested_prompts = get_argument_section_suggested_prompts(
            intent="arguments_reply",
        )
    else:
        suggested_prompts = [
            {
                "prompt": negotiation_conf["cta_argument_map"][
                    f"{generation_type}_modify"
                ].capitalize(),
                "intent": f"negotiation_{generation_type}_modify",
            },
            {
                "prompt": "Generate new arguments",
                "intent": "negotiation_arguments_new",
            },
            {
                "prompt": negotiation_conf["cta_argument_map"]["arguments_reply"].capitalize(),
                "intent": "negotiation_arguments_reply",
            },
        ]

    val = (
        {
            "prompt": negotiation_conf["cta_button_map"]["emails"].capitalize(),
            "intent": "negotiation_emails",
        }
        if next_step != "emails"
        else {}
    )

    suggested_prompts.append(val)

    suggested_prompts = [item for item in suggested_prompts if item]

    return suggested_prompts  # type: ignore


@log_time
def generate_arguments(
    reference_data: dict[str, Any],
    pg_db_conn: PGConnector,
    category: str,
    user_query: str,
    pinned_elements: dict[str, Any],
    chat_history: list,
    selected_elements: dict[str, Any],
    generation_type: str = "",
    request_type: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Chat Model that takes in user-conversation history, insights and facts to
    generate a contextual argument counter-argument or a rebuttal
    Args:
        reference_data (dict[str, Any]): tenant specific negotiation factory reference data
        pg_db_conn (PGConnector) : Connection object to postgres database
        category (str): user selected category
        user_query (str) : received user query
        pinned_elements (dict[str, Any]): Pinned elements including insights
        chat_history (list) : chat history object
        selected_elements (dict[str, Any]): Selected elements including argument
        generation_type (str): The type of out we are generating
                                    e.g. arguments, counter-argument
        request_type (str): The actual request_type
        kwargs (Any): Any additional arguments
    Returns:
        (dict[str, Any]): Generated arguments, counter-arguments or rebuttals
            with suggested prompts in proper response format
    """
    log.info("Argument model %d", len(kwargs))
    generation_type = generation_type.replace("negotiation_", "")
    user_query = user_query.replace(negotiation_conf["cta_button_map"][generation_type], "")

    # pylint: disable=R0801
    
    model_context = get_negotiation_model_context(
        pg_db_conn,
        category,
        user_query,
        pinned_elements,
        generation_type=generation_type,
        current_round=kwargs.get("current_round", 1),
        reference_data=reference_data,
    )
    
    # pylint: enable=R0801

    tone = model_context.get("tone", {})
    log.info("TONE %s", tone)

    chat_prompt = argument_prompt(
        model_context,
        user_query=user_query,
        generation_type=generation_type,
        selected_values=selected_elements.get(generation_type, []),
        request_type=request_type,
    )

    rag_prompt = argument_rag_prompt(
        model_context,
        pinned_elements,
        user_query=user_query,
        generation_type=generation_type,
        selected_values=selected_elements.get(generation_type, []),
        request_type=request_type,
    )

    argument_history = get_argument_conversation_history(chat_history, generation_type)
    messages = chat_prompt + argument_history

    if "modify" in request_type:
        value = pinned_elements.get(generation_type) or selected_elements.get(generation_type, [])
        previous_ids = [item.get("id") for item in value]
        value = {
            f"argument{i+1}": item.get("details", "")
            for i, item in enumerate(value)
            if isinstance(item, dict) and item.get("details")
        }
        rag_query = (
            "\n Note modify the each of following arguments as follows: \n"
            + user_query
            + "\n Arguments to be modified: \n"
            + "```json\n"
            + json.dumps(value, indent=4)
            + f"\n``` NOTE: only generate {len(value)} arguments"
        )

        user_query = (
            user_query
            + "\n"
            + "Note please modify the following arguments"
            + "\n"
            + "```json\n"
            + json.dumps(value, indent=4)
            + "\n```"
        )
    else:
        target_list = model_context.get("target_list", [])
        previous_ids = []
        prev_step = "objective"
        value = model_context.get("filtered_objectives", [])
        value = {
            f"""{prev_step}{i+1} - {item.get("objective_type")}""": f"""{target_list[i]}\n"""
            for i, item in enumerate(value)
            if isinstance(item, dict) and item.get(prev_step)
        }

        log.info("VALUE %s", value)

        rag_query = (
            f"\n Note please generate the 1-3 {generation_type} to achieve targets for each"
            + f" {prev_step} below: \n"
            + f"\n {prev_step}: \n"
            + json.dumps(value, indent=4)
        )

        user_query = (
            user_query
            + "\n"
            + f"Note generate {generation_type} based on {prev_step} below:"
            + (f"""Use tone {tone.get("title")}""" if tone.get("title") else "")
            + "\n"
            + "```json\n"
            + json.dumps(value, indent=4)
            + "\n```"
        )

    messages.append({"role": "user", "content": user_query})

    default_params = {
        "messages": messages,
        "model": negotiation_conf["model"]["model_name"],
    }

    pg_retriever = PGRetriever(
        pg_db_conn=pg_db_conn,
        k=negotiation_conf["model"]["arg_retriever_k"],
        table_name=negotiation_conf["tables"]["knowledge_base"],
        embeddings_model=negotiation_conf["model"]["similarity_model"],
        embeddings_column_name="embedding",
        column_names=["chunk_content", "page"],
        conditions=f"category_name in ('{category}', 'ALL', 'all') or category_name is NULL",
    )

    buffer_win = -1 * negotiation_conf["model"]["conversation_buffer_window"]

    # pylint: disable=R0801
    ai_response_dict = generate_conversational_rag_agent_response(
        user_query=rag_query,
        prompt=rag_prompt,
        retriever=None,#pg_retriever,
        chat_history=chat_history[buffer_win:],
        model=negotiation_conf["model"]["model_name"],
        fast_model=negotiation_conf["model"]["fast_model_name"],
        default_function=generate_chat_response,
        params=default_params,
        max_documents=5,
        additional_params={"tone": f"""{tone.get("title", "")}: {tone.get("description", "")}"""},
        temperature = 0.3
    )
    # pylint: enable=R0801

    ai_response_str = (
        ai_response_dict.get("generation", "")
        .replace("json", "")
        .replace("`", "")
        .replace("\n", "")
    )
    try:
        ai_response = json.loads(ai_response_str)
    except json.JSONDecodeError:
        ai_response = json_regex(
            ai_response_str,
            ["message", "argument1", "argument2", "argument3", "argument4", "argument5"],
        )
    if ai_response.get("arguments") and isinstance(ai_response.get("arguments"), list):
        ai_response_list = [
            item.get("details") for item in ai_response.get("arguments") if item.get("details")
        ]
    else:
        ai_response_list = [item for _, item in ai_response.items()]

    formatted_details = update_negotiation_details(
        generated_details=ai_response_list,
        previous_ids=previous_ids,
    )
    message = ai_response.get("message", "")

    suggested_prompts = get_ctas(
        user_query=user_query,
        chat_history=chat_history,
        generation_type=generation_type,
        **kwargs,
    )

    params = {
        "response_type": generation_type,
        "message": (
            message
            if message
            else f"Arguments generated for supplier {model_context.get('supplier_name')}"
        ),
        "suggested_prompts": suggested_prompts,
        f"{generation_type}": formatted_details,
    }
    return convert_to_response_format(**params)


@log_time
def generate_counter_argument_rebuttal(
    reference_data: dict[str, Any],
    pg_db_conn: PGConnector,
    category: str,
    user_query: str,
    pinned_elements: dict[str, Any],
    chat_history: list,
    selected_elements: dict[str, Any],
    generation_type: str = "",
    request_type: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Chat Model that takes in user-conversation history, insights and facts to
    generate a contextual argument counter-argument or a rebuttal
    Args:
        reference_data (dict[str, Any]): tenant specific negotiation factory reference data
        pg_db_conn (PGConnector) : Connection object to postgres database
        category (str): user selected category
        user_query (str) : received user query
        pinned_elements (dict[str, Any]): Pinned elements including insights
        chat_history (list) : chat history object
        selected_elements (dict[str, Any]): Selected elements including argument
        generation_type (str): The type of out we are generating e.g. arguments, counter-argument
        request_type (str): The actual request_type
        kwargs (Any): Any additional arguments
    Returns:
        (dict[str, Any]): Generated arguments, counter-arguments or rebuttals
            with suggested prompts in proper response format
    """
    generation_type = generation_type.replace("negotiation_", "")
    prev_step = "objectives" if generation_type == "rebuttals" else "arguments"
    user_query = user_query.replace(
        negotiation_conf["cta_button_map"][generation_type],
        "",
    ).replace(
        negotiation_conf["cta_argument_map"].get(request_type, ""),
        "",
    )
    user_query_original = copy.deepcopy(user_query)
    tone = pinned_elements.get("tone_and_tactics", {})
    matched_val = "test"
    if user_query_original:
        matched_val = get_best_match_from_list(
            list(negotiation_conf["cta_argument_map"].values()),
            user_query_original,
            similarity_model=negotiation_conf["model"]["similarity_model"],
            threshold=negotiation_conf["argument_cta_threshold"],
        )

        # pylint: disable=R0801
    model_context = get_negotiation_model_context(
        pg_db_conn,
        category,
        user_query,
        pinned_elements,
        generation_type=generation_type,
        reference_data=reference_data
    )
    # pylint: enable=R0801

    if "modify" in request_type:
        value = pinned_elements.get(generation_type) or selected_elements.get(generation_type, [])
        previous_ids = [item.get("id") for item in value]
        value = {
            f"{generation_type}{i+1}": f"""{item.get("details", "")}"""
            for i, item in enumerate(value)
            if isinstance(item, dict) and item.get("details")
        }
        rag_query = (
            f"\n Note please modify the following {generation_type} as follows: \n"
            + user_query
            + f"\n {generation_type}: \n"
            + "```json\n"
            + json.dumps(value, indent=4)
            + f"\n``` NOTE: only generate {len(value)} {generation_type}"
        )

        user_query = (
            f"Note please modify the following {generation_type} as follows:"
            + "\n"
            + user_query
            + "\n"
            + "```json\n"
            + json.dumps(value, indent=4)
            + "\n```"
        )

    else:
        previous_ids = []
        target_list = model_context.get("target_list", [])
        value = pinned_elements.get(prev_step) or selected_elements.get(prev_step, [])
        value = {
            f"{prev_step}{i+1}": f"""{item.get("details", "")}"""
            for i, item in enumerate(value)
            if isinstance(item, dict) and item.get("details")
        }
        instruction = ""
        if not matched_val and user_query_original and generation_type == "rebuttals":
            value.update({f"{prev_step}{len(value)+1}": user_query_original})
        if not matched_val and user_query_original and generation_type == "counter_arguments":
            instruction = f"User instruction: {user_query_original}"

        rag_query = (
            f"\n Note please generate the {generation_type} as for each {prev_step}:"
            + "\n"
            + (
                f"""Use tone {tone.get("title")}"""
                if tone.get("title") and generation_type == "rebuttals"
                else ""
            )
            + "\n"
            + instruction
            + f"\n {prev_step}: \n"
            + "```json\n"
            + json.dumps(value, indent=4)
            + f"""Target list: {json.dumps(target_list, indent=4)}\n"""
            + f"\n``` NOTE: only generate {len(value)} {generation_type}"
        )

        user_query = (
            f"Note generate {generation_type} for each {prev_step} below "
            + (
                f"""Use tone {tone.get("title")}"""
                if tone.get("title") and generation_type == "rebuttals"
                else ""
            )
            + "\n"
            + "```json\n"
            + json.dumps(value, indent=4)
            + "\n```"
        )

    prompt = counter_argument_rebuttal_prompt(  # type: ignore
        model_context,
        user_query=user_query,
        generation_type=generation_type,
        selected_values=selected_elements.get(generation_type, []),
        request_type=request_type,
        selected_elements=selected_elements,
    )
    rag_prompt = counter_argument_rebuttal_rag_prompt(  # type: ignore
        model_context,
        user_query=user_query,
        generation_type=generation_type,
        selected_values=selected_elements.get(generation_type, []),
        request_type=request_type,
        selected_elements=selected_elements,
    )

    message = ""
    # pylint: disable=R0801
    buffer_win = (
        -1 * negotiation_conf["model"]["conversation_buffer_window_counter_arguments_rebuttals"]
    )
    default_params = {
        "chat_history": chat_history,
        "prompt": prompt,
        "input_str": user_query,
        "model": negotiation_conf["model"]["model_name"],
        "memory_type": "window",
        "window_size": negotiation_conf["model"]["conversation_buffer_window"],
        "temperature": 0,
        "input_message_key": "input",
        "history_message_key": "history",
        "session_id": kwargs.get("chat_id", ""),
    }
    default_function = run_conversation_chat
    pg_retriever = PGRetriever(
        pg_db_conn=pg_db_conn,
        k=negotiation_conf["model"]["arg_retriever_k"],
        table_name=negotiation_conf["tables"]["knowledge_base"],
        embeddings_model=negotiation_conf["model"]["similarity_model"],
        embeddings_column_name="embedding",
        column_names=["chunk_content", "page"],
        conditions=f"category_name in ('{category}', 'ALL', 'all') or category_name is NULL",
    )

    ai_response_dict = generate_conversational_rag_agent_response(
        user_query=rag_query,
        prompt=rag_prompt,
        retriever=pg_retriever,
        chat_history=chat_history[buffer_win:],
        model=negotiation_conf["model"]["model_name"],
        fast_model=negotiation_conf["model"]["fast_model_name"],
        default_function=default_function,
        params=default_params,
        max_documents=5,
        compressor=Model(name=negotiation_conf["model"]["fast_model_name"]).obj,
    )
    # pylint: enable=R0801
    ai_response = ai_response_dict.get("generation", "")
    log.info("AI response, %s", ai_response)
    ai_response_list = [val for val in ai_response.split("|") if val and val not in rag_query]

    formatted_details = update_negotiation_details(
        generated_details=ai_response_list,
        previous_ids=previous_ids,
    )

    header_string = (
        "** Arguments ** \n"
        if generation_type == "counter_arguments"
        else ("** Supplier argument ** \n" if (not matched_val) and user_query_original else "")
    )
    selected_or_pinned = selected_elements.get(generation_type, []) or pinned_elements.get(
        generation_type,
        [],
    )
    if "modify" not in request_type:
        selected_or_pinned = pinned_elements.get(prev_step) or selected_elements.get(prev_step, [])

    if (not matched_val) and user_query_original and "modify" not in request_type:
        selected_or_pinned.append(
            {
                "id": f"{time.time()}",
                "reference_raw": user_query_original,
                "details": user_query_original,
                "raw": user_query_original,
            },
        )

    selected_or_pinned = [
        item for item in selected_or_pinned if item.get("details") or item.get("reference_raw")
    ]

    formatted_details = [
        {
            "id": current_step_item["id"],
            "raw": current_step_item["raw"],
            "reference_id": (
                prev_step_item.get("reference_id", None) or prev_step_item.get("id", None)
            ),
            "reference_raw": (
                prev_step_item.get("reference_raw", "") or prev_step_item.get("details", "")
            ),
            "details": format_details_string(prev_step_item, current_step_item, header_string),
        }
        for prev_step_item, current_step_item in zip(selected_or_pinned, formatted_details)
    ]

    suggested_prompts = get_ctas(
        user_query=user_query,
        chat_history=chat_history,
        generation_type=generation_type,
        **kwargs,
    )

    params = {
        "response_type": generation_type,
        "message": (
            message
            if message
            else (
                (
                    f"""{generation_type.replace("_", " ").capitalize()} generated"""
                    if generation_type != "rebuttals"
                    else "Reply to supplier argument"  # they want to remove the wording of rebuttal
                )
                + f""" for supplier {model_context.get("supplier_name")} """
            )
        ),
        "suggested_prompts": suggested_prompts,
        f"{generation_type}": formatted_details,
    }
    return convert_to_response_format(**params)


@log_time
def generate_user_answers(
    reference_data: dict[str, Any],
    pg_db_conn: PGConnector,
    category: str,
    user_query: str,
    pinned_elements: dict[str, Any],
    chat_history: list,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Model that takes in user-conversation history,
    and generate response for user query from the context
    Args:
        reference_data (dict[str, Any]): tenant specific negotiation factory reference data
        pg_db_conn (PGConnector): Connection object to postgres database
        category (str): The selected category
        user_query (str): user_query
        pinned_elements (dict[str, Any]): List of pinned elements from the UI
        chat_history (list) : chat history extracted from database
        negotiation_objective (str): Negotiation objective
        kwargs (Any): Any additional arguments
    Returns:
        (dict[str, Any]) : Model response to the user input
    """
    try:
        supplier_profile = pinned_elements.get("supplier_profile", {})

        negotiation_objectives_description = ""
        
        if "objectives" in pinned_elements.keys():
            objectives_in_action = identify_negotiation_objective(
                pinned_elements=pinned_elements,
                is_all_objectives_in_action=True,
            )
            goals: list[str] = []
            for i, objective in enumerate(objectives_in_action):
                if objective.get("objective_type", "").lower() != "key facts":
                    # pylint: disable=R0801
                    holder = extract_objective_description(
                        reference_data,
                        objective.get("objective_type", ""),
                    )
                    # pylint: enable=R0801
                    goals.append(f"{i}. {objective.get('objective_type', '')}: {holder}\n")
            negotiation_objectives_description = ", ".join(goals)

        selected_elements = kwargs.get("selected_elements", {}) or pinned_elements


        import asyncio
        supplier_name = pinned_elements.get("supplier_profile", {}).get(
            "supplier_name",
        ) or extract_supplier_name_from_user_query(user_query)
        
        prompt = create_chatbot_prompt(user_query=user_query, supplier_name=supplier_name, category=category)
        question = generate_chat_response_with_chain(
                    prompt=prompt,
                    temperature=0.3
                )
        
        data, sql, fixed_query = asyncio.run(fetch(question))
        answer = summarize_dax_output(
                data,
                user_query,
                category,
                preferred_currency="EUR",
                # sql_query=sql,
                fixed_query=fixed_query
            )

        

        
        # sku_list = supplier_profile.get("sku_list", [])
        # category_qna, supplier_qna, sku_qna = extract_qa_context(
        #     pg_db_conn,
        #     category,
        #     supplier_name,
        #     sku_list,
        # )

        negotiation_factory_help = negotiation_conf["negotiation_factory_description"]

        # prompt = user_query_prompt(
        #     category,
        #     category_qna,
        #     supplier_profile,
        #     supplier_qna,
        #     sku_qna,
        #     negotiation_objectives_description,
        #     negotiation_factory_help,
        #     selected_elements,
        # )
        # ai_response = run_conversation_chat(
        #     chat_history=chat_history,
        #     prompt=prompt,
        #     input_str=user_query,
        #     model=negotiation_conf["model"]["model_name"],
        #     memory_type="window",
        #     window_size=negotiation_conf["model"]["conversation_buffer_window"],
        #     temperature=0,
        #     input_message_key="input",
        #     history_message_key="history",
        #     session_id=kwargs.get("chat_id", ""),
        # )

        log.info("User Query model response %s", answer)
        lst_suggested_promts: list[dict[str, str]] = []
        if (
            kwargs.get("generation_type", "") == "negotiation_user_questions"
            or user_query == "Learn more about supplier"
        ):
            lst_suggested_promts = get_section_suggested_prompts(
                section_name="Select Supplier",
            )
        else:
            lst_suggested_promts = get_workflow_suggested_prompts(
                pinned_elements,
                include_insights=False,
                strategy_flow=True,
            ) + get_workflow_suggested_prompts(
                pinned_elements,
            )

        remove_list = []
        remove_list.append(
            f"{'Set' if 'objectives' in pinned_elements.keys() else 'Change'} negotiation objectives",
        )
        remove_list.append("Learn more about supplier")
        lst_suggested_promts = [
            prompt for prompt in lst_suggested_promts if (prompt["prompt"] not in remove_list)
        ]

        return convert_to_response_format(
            response_type="user_questions",
            message=answer,
            suggested_prompts=lst_suggested_promts,
        )
    except Exception:  # pylint: disable=broad-exception-caught
        log.exception("Exception in fetch")
        return exception_response(
            response_type="exception",
            message="Ada was unable to answer this question, "
            "can you rephrase the question or be more specific?",
        )


@log_time
def generate_arguments_counter_argument_rebuttal_workflow(
    reference_data: dict[str, Any],
    pg_db_conn: PGConnector,
    category: str,
    user_query: str,
    pinned_elements: dict[str, Any],
    chat_history: list,
    selected_elements: dict[str, Any],
    generation_type: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Chat Model that takes in user-conversation history, insights and facts to
    get the correct argument counter argument and rebuttal workflow
    Args:
        reference_data (dict[str, Any]): tenant specific negotiation factory reference data
        pg_db_conn (PGConnector) : Connection object to postgres database
        category (str): user selected category
        user_query (str) : received user query
        pinned_elements (dict[str, Any]): Pinned elements including insights
        chat_history (list) : chat history object
        selected_elements (dict[str, Any]): Selected elements including argument
        generation_type (str): The type of out we are generating
                                    e.g. arguments, counter-argument
        kwargs (Any): Any additional arguments
    Returns:
        (dict[str, Any]): Generated arguments, counter-arguments or rebuttals
            with suggested prompts in proper response format
    """
    log.info("request_type %s", generation_type)
    log.info(" Generating  %d", len(kwargs))

    generation_type = generation_type.replace("negotiation_", "")

    kwargs["generation_type_before_edit"] = (
        generation_type if (generation_type == "") else generation_type.replace("negotiation_", "")
    )

    suggested_prompt = get_section_suggested_prompts(
        section_name="Generate Arguments",
    )

    # Check pre-requisites are met or not - objective is mandatory
    check_keys = [key for key, value in pinned_elements.items() if value]
    check_keys.extend([key for key, value in selected_elements.items() if value])
    flag, message, suggested_prompt = perform_argument_prerequisite_check(
        key="objectives",
        suggested_prompt=suggested_prompt,
        pinned_keys=list(set(check_keys)),
    )

    if not flag and "counter" in generation_type:
        flag, message, suggested_prompt = perform_argument_prerequisite_check(
            key="arguments",
            suggested_prompt=suggested_prompt,
            pinned_keys=list(set(check_keys)),
        )

    if flag:  # pre-requisite failed
        argument_state = kwargs["generation_type_before_edit"].replace("_generic", "")
        return convert_to_response_format(
            response_type=f"negotiation_{argument_state}",
            message=message,
            suggested_prompts=suggested_prompt,
        )

    cta_arg_map = negotiation_conf["cta_argument_map"]

    # CTA - Generate negotiation arguments
    if generation_type not in cta_arg_map:
        generation_type = get_generation_type(
            cta_map=cta_arg_map,
            user_query=user_query,
            threshold=negotiation_conf["argument_cta_threshold"],
            default_str="arguments_generic",
        )

    if generation_type in ["negotiation_arguments", "arguments", "arguments_round"]:
        return convert_to_response_format(
            response_type=generation_type,
            message="What type of arguments would you like to create?",
            suggested_prompts=suggested_prompt,
        )

    generation_type = (
        generation_type.replace("_generic", "")
        if "counter_arguments" in generation_type
        else generation_type
    )
    generation_vals = [val for val in negotiation_conf["new_workflow"] if val in generation_type]
    generation_vals = (
        ["counter_arguments"] if "counter_arguments" in generation_type else generation_vals
    )

    current_step = next(iter(generation_vals)) if generation_vals else generation_type.split("_")[0]
    log.info("Current step in arguments flow %s", current_step)

    suggested_prompt = [
        {
            "prompt": cta_arg_map["arguments_new"],
            "intent": "negotiation_arguments_new",
        },
        {
            "prompt": cta_arg_map["arguments_reply"],
            "intent": "negotiation_arguments_reply",
        },
    ]

    if generation_type in ["rebuttals", "counter_arguments"]:
        cta_map = {
            generation_type: cta_arg_map.get(generation_type, ""),
            f"{generation_type}_modify": cta_arg_map.get(f"{generation_type}_modify", ""),
        }
        if generation_type == "rebuttals":
            additional_key = "arguments_reply"
            cta_map.update({additional_key: cta_arg_map.get(additional_key, "")})
        generation_type = get_generation_type(
            cta_map=cta_map,
            user_query=user_query,
            threshold=negotiation_conf["argument_cta_threshold"],
            default_str=generation_type,
        )
    reply_match = re.match(r"^(.+)_reply$", generation_type)
    if reply_match:
        match_string = reply_match.group(1)
        return convert_to_response_format(
            response_type=generation_type,
            message=f"""Can you provide the {" ".join(match_string.split("_"))} from supplier?""",
        )

    if generation_type in ["arguments_modify", "rebuttals_modify", "counter_arguments_modify"]:
        message = "Could you please provide details on the modifications needed in the " + (
            f"""{current_step.replace("_", " ")}?"""
            if current_step != "rebuttals"
            else "reply to supplier argument"  # they want to remove the wording of rebuttal
        )

        if not bool(pinned_elements.get(current_step)):
            display_str = (
                f"""{current_step.replace("_", " ")}"""
                if current_step != "rebuttals"
                else "reply to supplier argument"
            )
            message = (
                f"""To effectively modify {display_str}, it's imperative to have """
                f"""{display_str} pinned/selected. Please select {display_str} or click """
                f"""`{negotiation_conf["cta_button_map"][current_step]}` to proceed further. """
            )

            suggested_prompts = [
                {
                    "prompt": cta_arg_map[generation_type],
                    "intent": f"negotiation_{generation_type}",
                },
                {
                    "prompt": negotiation_conf["cta_button_map"][current_step],
                    "intent": f"negotiation_{current_step}",
                },
            ]
            generation_type = generation_type.replace("_modify", "")

        params: dict[str, Any] = {
            "response_type": generation_type,
            "message": message,
            "suggested_prompts": (
                suggested_prompts if not bool(pinned_elements.get(current_step)) else []
            ),
        }

        output_params = {key: value for key, value in params.items() if value}

        return convert_to_response_format(**output_params)  # type: ignore

    generation_vals = [val for val in negotiation_conf["new_workflow"] if val in generation_type]
    # pylint: disable=R0801
    generation_vals = (
        ["counter_arguments"] if "counter_arguments" in generation_type else generation_vals
    )
    generation_type = next(iter(generation_vals)) if generation_vals else generation_type
    request_type = dict(chat_history[-1]).get("response_type", "") if chat_history else ""
    if generation_type == "arguments":
        return generate_arguments(
            reference_data,
            pg_db_conn,
            category,
            user_query,
            pinned_elements,
            chat_history,
            selected_elements,
            generation_type,
            request_type,
            **kwargs,
        )
    return generate_counter_argument_rebuttal(
        reference_data,
        pg_db_conn,
        category,
        user_query,
        pinned_elements,
        chat_history,
        selected_elements,
        generation_type,
        request_type,
        **kwargs,
    )
    # pylint: enable=R0801


@log_time
def save_negotiation_latest_offer(
    pinned_elements: dict[str, Any],
    user_query: str,
    generation_type: str,
    before_update_request_type: str,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    This function  is executed when user wants to save latest offer they got
    Args:
        pinned_elements (dict[str, Any]): Pinned elements including insights
        user_query (str) : received user query
        generation_type (str): The type of out we are generating e.g. arguments, counter-argument
        before_update_request_type (str): request_type before front end
        kwargs (Any): Any additional arguments
    Returns:
        (dict[str, Any]): Generated response for front end
    """
    log.info(kwargs)
    flag: bool = False
    message: str = ""
    suggested_prompts: list[dict[str, Any]] = []
    if before_update_request_type == "":
        generation_type = before_update_request_type
    user_query = "Save latest offer" if (user_query == "") else user_query
    flag, msg, prompts = perform_offer_prerequisite_check(
        generation_type=generation_type,
        pinned_keys=list(pinned_elements.keys()),
    )
    if flag:  # pre-requisite failed
        message = msg
        suggested_prompts = prompts
    else:
        message = (
            "**Offer Added**\nLatest offer added and progress towards objectives updated"
            "\n\nHow would you like to proceed?"
        )
        suggested_prompts = [
            {"prompt": "Start new round", "intent": "negotiation_arguments"},
            {"prompt": "Finish negotiation", "intent": "negotiation_finished"},
        ]
    return convert_to_response_format(
        response_type="negotiation_offer",
        message=message,
        suggested_prompts=suggested_prompts,
    )


@log_time
def finish_negotiation(
    pinned_elements: dict[str, Any],
    **kwargs: Any,
) -> dict[str, Any]:
    """
    This function  is executed when user wants to finish the negotiation
    Args:
        pinned_elements (dict[str, Any]): Pinned elements including insights
        kwargs (Any): Any additional arguments
    Returns:
        (dict[str, Any]): Generated response for front end
    """
    log.info(kwargs)
    flag: bool = False
    message: str = ""
    suggested_prompts: list[dict[str, Any]] = []
    flag, msg = perform_finish_negotiation_prerequisite_check(
        pinned_keys=list(pinned_elements.keys()),
    )
    if flag:  # pre-requisite failed
        message = msg
    else:  # pre-requisite passed
        message = msg
        is_broken_once = False
        for objective in pinned_elements["objectives"]:
            for key, value in objective.items():
                if key == "current_offer" and value != "":
                    is_broken_once = True
                    message = (
                        "Well done!!!.\nYou successfully finished the negotiation, "
                        "\nlets redirect you to awarding section for negotiation summary email."
                    )
                    break
            if is_broken_once:
                break

    return convert_to_response_format(
        response_type="negotiation_finished",
        message=message,
        suggested_prompts=suggested_prompts,
    )
