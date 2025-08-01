"""Module to create a NER pipeline for dynamic ideas."""

import json
from typing import TypedDict

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from ada.components.db.pg_connector import PGConnector
from ada.components.llm_models.generic_calls import generate_embeddings_from_string
from ada.components.llm_models.model_base import Model
from ada.use_cases.idea_generation.dynamic_ideas.dyn_ideas_prompts import (
    get_history_based_ner_prompt,
)
from ada.use_cases.idea_generation.dynamic_ideas.dynamic_ideas_utils import (
    get_analytics_values,
)
from ada.use_cases.idea_generation.exception import DynamicQnAException
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger
from ada.components.llm_models.generic_calls import generate_chat_response_with_chain

dynamic_ideas_conf = read_config("use-cases.yml")["dynamic_ideas"]
model = dynamic_ideas_conf["models"]["llm"]
fast_model = dynamic_ideas_conf["models"]["fast_llm"]
analytics_list = dynamic_ideas_conf["analytics"]

log = get_logger("ner_graph_workflow")


class NERState(TypedDict):
    """State for NER processing."""

    question: str
    ner_output: list
    corrected_ner_output: list
    category: str
    pg_db_conn: PGConnector
    chat_history: list


def extract_entities(state: NERState) -> NERState:
    """
    Extracts entities from the given state using a language model.

    Args:
        state (NERState): The state containing the question,
                pg connector, category, and chat history.

    Returns:
        NERState: The updated state with extracted entities.
    """
    
    question = state["question"]
    prompt = get_history_based_ner_prompt(question)
    
    llm = Model(name=model).obj if isinstance(model, str) else model

    llm_response = generate_chat_response_with_chain(prompt,model=llm)
    
    ai_output = llm_response.replace("json", "").replace("`", "")

    log.info(f"NER response: {ai_output}")
    try:
        state["ner_output"] = json.loads(ai_output)
    except json.decoder.JSONDecodeError:
        first_index = ai_output.index("[")
        last_index = ai_output.rindex("]")
        json_string = ai_output[first_index : last_index + 1]  # noqa: E203
        try:
            state["ner_output"] = json.loads(json_string)
        except json.decoder.JSONDecodeError:
            state["ner_output"] = []
    return state


def get_closest_matching_supplier(
    pg_db_conn: PGConnector,
    category: str,
    raw_value: str,
    entity_type="name",
) -> str:
    """
    Retrieves the closest matching supplier based on the given raw value and category.

    Args:
        pg_db_conn (PGConnector): Post gress connection object.
        category (str): The category name.
        raw_value (str): The raw value to match against supplier names.
        entity_type (str, optional): The type of entity to match. Defaults to "name".

    Returns:
        str: The closest matching supplier name.

    Raises:
        DynamicQnAException: If the entity type is not supported.
    """
    if entity_type == "name":
        supplier_data = pg_db_conn.search_by_vector_similarity(
            table_name=dynamic_ideas_conf["tables"]["supplier_profile_view"],
            query_emb=generate_embeddings_from_string(raw_value),
            emb_column_name="supplier_name_embedding",
            num_records=5,
            conditions={"LOWER(category_name)": category.lower()},
        )
        if supplier_data:
            filtered_supplier_data = [
                {
                    "supplier_name": supplier["supplier_name"],
                    "cosine_distance": supplier["cosine_distance"],
                }
                for supplier in supplier_data
                if supplier["cosine_distance"] < 0.15
            ]
            # Todo: if need to return multiple suppliers
            if filtered_supplier_data:
                return filtered_supplier_data[0]["supplier_name"]
        return raw_value

    err_msg = "Entity Type not supported"
    log.error(err_msg)
    raise DynamicQnAException(err_msg)


def get_closest_matching_sku(
    pg_db_conn: PGConnector,
    category: str,
    raw_value: str,
    entity_type="name",
) -> str:
    """
    Retrieves the closest matching SKU based on the given raw value and category.

    Args:
        pg_db_conn (PGConnector): Postgres connection object.
        category (str): The category name.
        raw_value (str): The raw value to match against SKU names.
        entity_type (str, optional): The type of entity to match. Defaults to "name".

    Returns:
        str: The closest matching SKU name.

    Raises:
        DynamicQnAException: If the entity type is not supported.
    """
    if entity_type == "name":
        sku_data = pg_db_conn.search_by_vector_similarity(
            table_name=dynamic_ideas_conf["tables"]["sku_profile_view"],
            query_emb=generate_embeddings_from_string(raw_value),
            emb_column_name="entity_embedding",
            num_records=1,
            conditions={"LOWER(category_name)": category.lower(), "entity_type": "SKU"},
        )
        if sku_data and sku_data[0]["cosine_distance"] and sku_data[0]["cosine_distance"] < 0.15:
            return sku_data[0]["entity_name"]
        return raw_value

    err_msg = "Entity Type not supported"
    log.error(err_msg)
    raise DynamicQnAException(err_msg)


def get_corrected_entities(state: NERState) -> NERState:
    """
    Corrects the extracted entities in the given state.

    Args:
        state (NERState): The state containing the extracted entities,
        pg_db_conn, category, and chat history.

    Returns:
        NERState: The updated state with corrected entities.
    """
    state["corrected_ner_output"] = []
    for item in state["ner_output"]:
        if item["entity"] == "supplier" and item["type"] == "name":
            corrected_values = [
                get_closest_matching_supplier(
                    state["pg_db_conn"],
                    state["category"],
                    value,
                )
                for value in item["value"]
            ]
            item["value"] = corrected_values

        elif item["entity"] == "sku" and item["type"] == "name":
            corrected_values = [
                get_closest_matching_sku(
                    state["pg_db_conn"],
                    state["category"],
                    value,
                )
                for value in item["value"]
            ]
            item["value"] = corrected_values
        elif item["entity"] == "idea" and item["type"] == "id":
            corrected_values = [str(value) for value in item["value"]]
            item["value"] = corrected_values

        state["corrected_ner_output"].append(item)
    return state


def create_ner_pipeline() -> CompiledStateGraph:
    """
    Creates and compiles the NER pipeline workflow.

    This function sets up the workflow for processing Named Entity Recognition (NER) tasks.
    It defines the nodes and edges of the workflow, specifying the sequence of operations
    to be performed on the input data.

    Returns:
        CompiledStateGraph: The compiled workflow for NER processing.
    """
    workflow = StateGraph(NERState)
    workflow.add_node("extract_entities", extract_entities)

    workflow.set_entry_point("extract_entities")

    workflow.add_edge("extract_entities", END)
    ner_app = workflow.compile()
    return ner_app
