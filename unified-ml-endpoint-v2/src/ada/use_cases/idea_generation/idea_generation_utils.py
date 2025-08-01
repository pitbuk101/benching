"""Methods for idea generation v2 - std and chat models"""

from typing import Any

from langchain_core.prompts import PromptTemplate

from ada.components.db.pg_connector import PGConnector
from ada.components.llm_models.generic_calls import (
    generate_chat_response_with_chain,
    run_conversation_chat,
)
from ada.use_cases.idea_generation.exception import IdeaGenException
from ada.use_cases.idea_generation.prompts import (
    generate_ideas_prompt,
    generate_rca_prompt,
    get_selected_idea_prompt,
    prompt_with_chat_history_v3,
)
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time
import json
import re
from ada.use_cases.insight_generation.sf_connector import SnowflakeClient

idea_generation_conf = read_config("use-cases.yml")["idea_generation_chat"]
intent_model_conf = read_config("use-cases.yml")["intent_model_v2"]
pg_config = idea_generation_conf["tables"]
model_config = idea_generation_conf["model"]
log = get_logger("idea_generation_v2_utils")


@log_time
def extract_pinned_elements(
    data: dict[str, Any],
    main_insight_mandatory: bool = True,
) -> dict[str, Any]:
    """
    Extract pinned elements from the provided data dictionary.


    Args:
        data (dict[str, Any]): Dictionary containing ideation-tab data.
        main_insight_mandatory (bool): Flag to decide if main_inights is mandatory

    Returns:
        dict[str, Any]: Dictionary with keys "pinned_main_insight," "pinned_related_insight,"
        "pinned_root_causes," "pinned_ideas," and "insight_id" containing the extracted information.

    Raises:
        IdeaGenException: Raised if no main insight is selected for ideation.
    """
    pinned_elements = data.get("pinned_elements", {})
    pinned_insights = pinned_elements.get("pinned_insights", [])

    # TODO : Multiple main insights user journey is part of next version
    pinned_main_insight, insight_id = next(
        (
            (insight.get("insight", ""), insight.get("insight_id", ""))
            for insight in pinned_insights
            if insight.get("is_main") == "1"
        ),
        ("", ""),
    )

    if main_insight_mandatory and not (pinned_main_insight and insight_id):
        err_msg = "Please select an insight to continue ideating!"
        log.error(err_msg)
        raise IdeaGenException(err_msg)

    pinned_related_insight = "\n".join(
        insight.get("insight", "") for insight in pinned_insights if insight.get("is_main") != "1"
    )

    pinned_root_causes = "\n".join(
        pinned_elements.get("pinned_root_causes", ""),
    )
    pinned_ideas = "\n".join(pinned_elements.get("pinned_ideas", ""))

    return {
        "pinned_main_insight": pinned_main_insight,
        "pinned_related_insight": pinned_related_insight.strip(),
        "pinned_root_causes": pinned_root_causes.strip(),
        "pinned_ideas": pinned_ideas.strip(),
        "insight_id": insight_id.strip(),
    }


@log_time
def get_precomputed_response(
    insight_id: str,
    pg_db_conn: PGConnector,
    request_type: str,
) -> list[Any]:
    """
    Retrieve precomputed responses based on the specified insight ID and request type.
    Args:
        insight_id (str): Identifier for the insight.
        pg_db_conn (PGConnector): PostgresSQL database connection object.
        request_type (str): Type of request, such as "rca," "ideas," or "linked_insights."

    Returns:
        (list[Any]): List containing precomputed responses based on the provided request type.

    Raises:
        IdeaGenException: Raised if an invalid request type is provided.

    Note: If the response is not generated, returns empty list
    """
    if request_type == "rca":
        response_col_name = "recommended_rca"
    elif request_type == "ideas":
        response_col_name = "recommended_ideas"
    elif request_type == "linked_insights":
        response_col_name = "linked_insight"
    else:
        err_msg = "invalid request type for precomputed response"
        log.error(err_msg)
        raise IdeaGenException(err_msg)

    pre_computed_response = pg_db_conn.select_records_with_filter(
        table_name=pg_config["idea_generation_context_table"],
        filtered_columns=[response_col_name],
        filter_condition=f"insight_id = '{insight_id}'",
    )
    try:
        if pre_computed_response[0][0]:
            if request_type in ["rca", "ideas"]:
                return list(filter(lambda x: len(x) > 0, pre_computed_response[0][0].split("|")))
            return pre_computed_response[0][0]
    except IdeaGenException as exception:
        log.info("Pre-computed responses not available in IG context table: %s", exception)
    return []


@log_time
def get_insight_context(insight_id: str, pg_db_conn: PGConnector) -> dict[str, Any]:
    """
    Retrieve context information for a given insight ID from the PostgresSQL database.

    Args:
        insight_id (str): Identifier for the insight.
        pg_db_conn (PGConnector): PostgresSQL database connection object.

    Returns:
        (dict[str, Any]): Dictionary containing context information with keys -
            "linked_insight"
            "category_name",
            "sku_qna",
            "supplier_qna",
            "category_qna",
            "definitions",
            "alert_type."

    Raises:
        IdeaGenException: Raised if the insight is not found in the database.

    """
    context_col_names = [
        "linked_insight",
        "category_name",
        "sku_qna",
        "supplier_qna",
        "category_qna",
        "definitions",
        "alert_type",
    ]
    context_data_tuple = pg_db_conn.select_records_with_filter(
        table_name=pg_config["idea_generation_context_table"],
        filtered_columns=context_col_names,
        filter_condition=f"insight_id = '{insight_id}'",
    )

    if not context_data_tuple:
        err_msg = "Insight not found in the database, please check."
        log.error(err_msg)
        raise IdeaGenException(err_msg)

    context_dict = {}
    for i, col_name in enumerate(context_col_names):
        context_dict[col_name] = context_data_tuple[0][i] if context_data_tuple[0][i] else None
    return context_dict


@log_time
def generate_response_dict(
    chat_id: str,
    response_type: str,
    rca_list: list | None = None,
    ideas_list: list | None = None,
    answer_str: str | None = None,
    linked_insights_list: list | None = None,
) -> dict[str, Any]:
    """
    Generate a response dictionary based on the provided parameters.

    Args:
        chat_id (str): The identifier for the chat session.
        response_type (str): The type of response.
        rca_list (list | None): List of root causes (optional).
        ideas_list (list | None): List of ideas (optional).
        answer_str (str | None): String containing the answer (optional).
        linked_insights_list (list | None): List of linked insights (optional).

    Returns:
        Dict[str, Any]: A dictionary representing the generated response.
    """
    return {
        "chat_id": chat_id,
        "response_type": response_type,
        "response": {
            "root_causes": rca_list if rca_list is not None else [],
            "ideas": ideas_list if ideas_list is not None else [],
            "answer": answer_str if answer_str is not None else "",
            "linked_insights": linked_insights_list if linked_insights_list is not None else [],
        },
    }


@log_time
def get_chat_history_context(table_name: str, chat_id: str, pg_db_conn: PGConnector) -> dict:
    """
    Retrieve chat history context from the specified table in the PostgresSQL database.

    Args:
        table_name (str): Name of the table containing chat history.
        chat_id (str): Identifier for the chat session.
        pg_db_conn (PGConnector): PostgresSQL database connection object.

    Returns:
        dict: Dictionary containing chat history context.

    Note:
        If the chat history data is not available in the database, an empty dictionary is returned.
    """
    chat_context_data = pg_db_conn.select_records_with_filter(
        table_name=table_name,
        filter_condition=f"chat_id = '{chat_id}'",
    )
    if chat_context_data:
        return map_data_to_columns(chat_context_data)
    return {}


@log_time
def write_response_to_db(
    table_name: str,
    col_name: str,
    response: str,
    chat_id: str,
    pg_db_conn: PGConnector,
):
    """
    Write the response to the specified column in the PostgresSQL database.

    Args:
        table_name (str): Name of the table containing chat history.
        col_name (str): Name of the column to be updated.
        response (str): Response value to be written.
        chat_id (str): Identifier for the chat session.
        pg_db_conn (PGConnector): PostgresSQL database connection object.
    """
    chat_id_from_db = pg_db_conn.select_component_column(
        table_name=table_name,
        column_name="chat_id",
        key_column="chat_id",
        value=f"'{chat_id}'",
    )
    if chat_id_from_db:
        new_value = {"column_name": col_name, "value": response}
        condition = {"column_name": "chat_id", "value": str(chat_id)}
        pg_db_conn.update_component_column(
            table_name=pg_config["chat_history_table_name"],
            new_value=new_value,
            condition=condition,
        )
        log.info(
            "Chat Id %s found in Database and updated the response for : %s ",
            chat_id,
            col_name,
        )
    else:
        pg_db_conn.insert_values_into_columns(
            tuple_with_columns=("chat_id", "recommended_ideas"),
            list_with_values=(chat_id, response),
            table_name=pg_config["chat_history_table_name"],
        )


@log_time
def map_data_to_columns(data: tuple) -> dict:
    """
    Map tuple data to a dictionary with specific keys.
    Args:
        data (Tuple): A tuple containing structured data as below
                    chat_id text,
                    recommended_rca jsonb,
                    recommended_ideas jsonb,
                    chat_message_history jsonb
    Returns:
        Dict[str, Any]: A dictionary mapping specific keys to corresponding values.
    """
    return {
        "recommended_rca": data[0][1],
        "recommended_ideas": data[0][2],
        "chat_message_history": data[0][3],
    }


@log_time
def input_data_validation(chat_id: str, request_type: str):
    """
    Validate input data from a JSON dictionary.

    Args:
        chat_id (str): Identifier for the chat session.
        request_type (str): "linked_insights", "rca", "ideas", "user_input" and "clear_chat_history"

    Raises:
        IdeaGenException: Raised if the validation fails.
    """
    if not chat_id or not isinstance(chat_id, str):
        err_msg = "chat_id retrieved from realtime params is either None or not a string!"
        log.error(err_msg)
        raise IdeaGenException(err_msg)
    log.info("Chat ID retrieved from the realtime params : %s", chat_id)

    if request_type not in ["linked_insights", "rca", "ideas", "user_input", "clear_chat_history"]:
        err_msg = f"Invalid request_type retrieved from the realtime params: {request_type}"
        log.error(err_msg)
        raise IdeaGenException(err_msg)
    log.info("Request type retrieved from the realtime params : %s", request_type)


@log_time
def delete_chat_history(chat_id: str, pg_db_conn: PGConnector, **kwargs: Any) -> dict[str, Any]:
    """
    Delete chat history for a specific chat_id and generate a response indicating success.

    Args:
        chat_id : The identifier of the chat whose history is to be deleted.
        pg_db_conn : An instance of PGConnector for connecting to the PostgresSQL database.
        kwargs (Any): Any additional data
    Returns:
        (dict[str, Any]): Returns response to the user.
    """
    log.info("Len of additonal data %d", len(kwargs))
    pg_db_conn.delete_values(
        table_name=pg_config["chat_history_table_name"],
        conditions={"chat_id": chat_id},
    )
    pg_db_conn.delete_values(
        table_name=intent_model_conf["tables"]["chat_history_table"],
        conditions={"chat_id": chat_id},
    )
    pg_db_conn.close_connection()
    return generate_response_dict(chat_id=chat_id, response_type="clear_chat_success")


@log_time
def generate_rca(insight_context: dict, pinned_elements: dict) -> list[str]:
    """
    Generate root cause analysis based on user pinned elements and insight's context.

    Args:
        insight_context (dict): Data dictionary containing insight context.
        pinned_elements (dict): Dictionary containing pinned elements.

    Returns:
        list[str]: List of root causes.
    """
    prompt = generate_rca_prompt(insight_context, pinned_elements)

    response = generate_chat_response_with_chain(prompt, model=model_config["model_name"])
    return list(filter(lambda x: len(x) > 0, response.split("|")))


@log_time
def generate_ideas(insight_context: dict, pinned_elements: dict) -> list[str]:
    """
    Generate ideas as response based on user pinned elements and insight's context.

    Args:
        insight_context (dict): Data dictionary containing insight context.
        pinned_elements (dict): Dictionary containing pinned elements.

    Returns:
        list[str]: List of strings representing ideas.
    """
    prompt = generate_ideas_prompt(insight_context, pinned_elements)
    response = generate_chat_response_with_chain(prompt, model=model_config["model_name"])
    return list(filter(lambda x: len(x) > 0, response.split("|")))


@log_time
def generate_chat_model_response(
    json_data: dict[str, Any],
    chat_history: list[dict[str, Any]],
    pg_db_conn: PGConnector,
    sf_client: SnowflakeClient,
    insight_context: dict,
    # pinned_elements: dict,
) -> str:
    """
    Chat Model that takes in user-conversation history and domain context and generates
    contextual response
    Args:
        json_data (dict[str, Any]): Data dictionary containing chat id and context
        chat_history (list[dict[str, Any]]): chat history extracted from db
        pg_db_conn (PGConnector): Postgres connection instance
        insight_context (dict): Data dictionary containing insight context.
        pinned_elements (dict): Dictionary containing pinned elements.
    Returns:
        (str) : Model response to the user input
    """
    chat_id = json_data["chat_id"]
    user_input = json_data["user_input"]
    selected_idea = json_data.get("general_info",{}).get("idea")
    selected_idea_description = json_data.get("general_info",{}).get("idea_description")

    retrieved_context = get_chat_history_context(
        table_name=pg_config["chat_history_table_name"],
        chat_id=chat_id,
        pg_db_conn=pg_db_conn,
    )
    
    if selected_idea:
        return generate_selected_idea_prompt_response(
            retrieved_context,
            insight_context,
            # pinned_elements,
            user_input,
            selected_idea,
            selected_idea_description
        )

    if not user_input:
        err_msg = "I did not get your question. Please input again!"
        log.error(err_msg)
        raise IdeaGenException(err_msg)
    
    prompt = prompt_with_chat_history_v3(
        user_input,
        retrieved_context,
        insight_context,
        # pinned_elements,
    )
    response = generate_chat_response_with_chain(prompt, model=model_config["model_name"])
    
    return response


@log_time
def generate_user_intent(
    intent_prompt: PromptTemplate,
    chat_history: list[Any],
    user_query: str,
    chat_id: str = "",
) -> str:
    """
    generate the user's intent based on the provided intent prompt and JSON data.
    Args:
        intent_prompt (PromptTemplate): System Prompt for generating intent from below list
        ["rca", "ideas", "user_input", "linked_insight]
        chat_history (list[Any]): Chat history from database
        user_query (str): User query string
        chat_id (str): Chat id for the session
    Returns:
        dict: Generated chat response based on the user's intent and model configuration.
    """
    return run_conversation_chat(
        chat_history=chat_history,
        prompt=intent_prompt,
        input_str=user_query,
        model=model_config["model_name"],
        window_size=idea_generation_conf["context"]["conversation_buffer_window"],
        session_id=chat_id,
    )


@log_time
def generate_selected_idea_prompt_response(
    retrieved_context: dict,
    insight_context: dict,
    # pinned_elements: dict,
    user_input: str,
    selected_idea: str,
    selected_idea_description:str
) -> str:
    """
    Generate a response for a selected idea prompt (commenting /reply action)

    Args:
        retrieved_context (dict): The retrieved context for generating the prompt.
        insight_context (dict): Contextual insights related to the prompt.
        pinned_elements (dict): Elements that are pinned or prioritized.
        user_input (str): User's input or query.
        selected_idea (str): The selected idea for which the response is generated.

    Returns:
        str: Generated response based on the provided inputs.

    """

    prompt = get_selected_idea_prompt(
        retrieved_context=retrieved_context,
        insight_context=insight_context,
        # pinned_elements=pinned_elements,
        user_query=user_input,
        selected_idea=selected_idea,
        selected_idea_description=selected_idea_description
    )
    response = generate_chat_response_with_chain(prompt, model=model_config["model_name"])
    return response


def extract_json(text):
    """
    Extracts all JSON arrays from the given text and merges them into a single list.

    :param text: The input text containing JSON data.
    :return: A list of extracted JSON objects.
    """

    json_pattern = r'\[\s*\{.*?\}\s*\]'  
    matches = re.findall(json_pattern, text, re.DOTALL)

    extracted_list = []
    for match in matches:
        try:
            json_data = json.loads(match)  
            if isinstance(json_data, list):
                extracted_list.extend(json_data)  
        except json.JSONDecodeError:
            print("Invalid JSON extracted!")
            return []

    return extracted_list