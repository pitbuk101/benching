"""Module to create a response generator pipeline for dynamic ideas."""

import json
import time
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from ada.components.db.pg_connector import PGConnector
from ada.components.llm_models.generic_calls import (
    generate_conversational_rag_agent_response,
)
from ada.use_cases.idea_generation.dynamic_ideas.dyn_ideas_prompts import (
    create_dynamic_ideas_prompt,
    create_dynamic_qna_prompt,
    create_opportunities_prompt,
    create_objectives_prompt,
)
from ada.use_cases.idea_generation.dynamic_ideas.dynamic_ideas_utils import (
    fetch_linked_insights_with_ids,
    prepare_response_payload,
    extract_category_analytic_data
)
from ada.use_cases.negotiation_factory.negotiation_factory_utils import json_regex
from ada.use_cases.source_ai_knowledge.source_ai_knowledge import (
    run_source_ai_knowledge,
)
from ada.components.llm_models.generic_calls import generate_chat_response_with_chain
from ada.use_cases.insight_generation.sf_connector import SnowflakeClient
from ada.utils.logs.logger import get_logger

log = get_logger("response_generator_workflow")


class ResponseGeneratorState(TypedDict):
    """State for ResponseGenerator processing."""

    question_class: str
    tenant_id: str
    user_query: str
    category: str
    data_for_qna: str
    dynamic_qa_summary: str
    opportunity_summary: str
    dynamic_ideas: list
    insights: list
    response_payload: dict
    chat_history: list
    pg_db_conn: PGConnector
    ner_output:list


def process_ideas_prompt(state: ResponseGeneratorState) -> dict:
    """
    Process the ideas prompt and generate a dynamic response.

    Args:
        state (ResponseGeneratorState): The current state containing context data,
            user query, chat history, and category information.

    Returns:
        dict: A dictionary containing the generated dynamic ideas with the key
        "dynamic_ideas".
    """
    log.info("Executing node: process_ideas_prompt")

    sf_client = SnowflakeClient(tenant_id=state["tenant_id"])
    currency_context = sf_client.execute_query(f"""Select DIM_CURRENCY_DOCUMENT as currency , TXT_CURRENCY_SYMBOL as currency_symbol from data.T_DIM_CURRENCY_SYMBOLS where DIM_CURRENCY_DOCUMENT=(Select TXT_REPORTING_CURRENCY from data.VT_DIM_REPORTINGCURRENCY where NUM_ORDER=1) LIMIT 1;""")
    currency = currency_context[0][0]

    prompt_params = {
        "data_context": state["data_for_qna"],
        "epoch_timestamp": str(int(time.time())),
        "category": state["category"],
        "enable_grader": False,
        "currency": currency,
    }
    response = generate_conversational_rag_agent_response(
        user_query=state["user_query"],
        prompt=create_dynamic_ideas_prompt(),
        chat_history=state["chat_history"],
        additional_params=prompt_params,
    )
    ai_output = response["generation"].replace("json", "").replace("`", "")
    try:
        ideas: list = json.loads(ai_output)
        state["dynamic_ideas"] = ideas
    except json.decoder.JSONDecodeError as ex:
        log.info("Error in processing ideas prompt: %s", ex)
        log.info("Output from LLM: %s", ai_output)
        # todo: implement pydantic parser
        first_index = ai_output.index("[")
        last_index = ai_output.rindex("]")
        json_string = ai_output[first_index : last_index + 1]  # noqa: E203
        try:
            state["dynamic_ideas"] = json.loads(json_string)
        except json.decoder.JSONDecodeError:
            state["dynamic_ideas"] = []
    return {"dynamic_ideas": state["dynamic_ideas"]}


def process_opportunity_prompt(state: ResponseGeneratorState) -> dict:
    """
    Process the opportunity prompt and generate a dynamic response.

    Args:
        state (ResponseGeneratorState): The current state containing context data,
            user query, NER output, and chat history.

    Returns:
        dict:
            - "opportunity_summary" (str): The summary of the opportunity generated
            from the response.
            - "insights" (list): A list of insights extracted from the response.
    """
    log.info("Executing node: process_opportunity_prompt")

    sf_client = SnowflakeClient(tenant_id=state["tenant_id"])
    currency_context = sf_client.execute_query(f"""Select DIM_CURRENCY_DOCUMENT as currency , TXT_CURRENCY_SYMBOL as currency_symbol from data.T_DIM_CURRENCY_SYMBOLS where DIM_CURRENCY_DOCUMENT=(Select TXT_REPORTING_CURRENCY from data.VT_DIM_REPORTINGCURRENCY where NUM_ORDER=1) LIMIT 1;""")
    currency = currency_context[0][0]

    prompt_params = {"data_context": state["data_for_qna"],"currency": currency}
    prompt = create_opportunities_prompt()
    response = generate_conversational_rag_agent_response(
        user_query=state["user_query"],
        prompt=prompt,
        chat_history=state["chat_history"],
        additional_params=prompt_params,
    )
    ai_output = response["generation"].replace("json", "").replace("`", "")
    try:
        json_response = json.loads(ai_output)
        state["opportunity_summary"] = json_response.get("opportunity_summary", "")
        state["insights"] = json_response.get("source_insights", [])
    except json.decoder.JSONDecodeError as ex:
        log.info("Error in processing ideas prompt: %s", ex)
        # todo: improve with pydantic parser
        ai_response = json_regex(ai_output, ["opportunity_summary", "source_insights"])
        state["opportunity_summary"] = ai_response.get(
            "opportunity_summary",
            response["generation"],
        )
        state["insights"] = ai_response.get("source_insights", [])
    return {
        "opportunity_summary": state["opportunity_summary"],
        "insights": state["insights"],
    }


def process_dynamic_qa_prompt(state: ResponseGeneratorState):
    """
    Process a dynamic Q&A prompt and generate a conversational response.

    Args:
        state (ResponseGeneratorState): The current state containing context data,
            user query, chat history, tenant ID, and category.

    Returns:
        dict:
            - "dynamic_qa_summary" (str): The generated summary of the Q&A response.
    """
    log.info("Executing node: process_dynamic_qa_prompt")
    sf_client = SnowflakeClient(tenant_id=state["tenant_id"])

    market_context = sf_client.execute_query(f"""
            SELECT INSIGHT FROM DATA.INSIGHTS_MASTER
            WHERE LOWER(CATEGORY) = '{state["category"].lower()}' AND LOWER(ANALYTICS_NAME) = 'market analysis';""")
    
    currency_context = sf_client.execute_query(f"""Select DIM_CURRENCY_DOCUMENT as currency , TXT_CURRENCY_SYMBOL as currency_symbol from data.T_DIM_CURRENCY_SYMBOLS where DIM_CURRENCY_DOCUMENT=(Select TXT_REPORTING_CURRENCY from data.VT_DIM_REPORTINGCURRENCY where NUM_ORDER=1) LIMIT 1;""")
    currency = currency_context[0][0]
    
    prompt_params = {"data_context": state["data_for_qna"],"market_context":market_context,"currency": currency}
    source_ai_bot_params = {
        "json_file": json.dumps(
            {
                "tenant_id": state["tenant_id"],
                "user_input": state["user_query"],
                "category": state["category"],
                "intent": "source ai knowledge",
            },
        ),
    }
    response = generate_conversational_rag_agent_response(
        user_query=state["user_query"],
        prompt=create_dynamic_qna_prompt(),
        chat_history=state["chat_history"],
        additional_params=prompt_params,
        default_function=run_source_ai_knowledge,
        params=source_ai_bot_params,
    )
    state["dynamic_qa_summary"] = response["generation"]
    return {"dynamic_qa_summary": state["dynamic_qa_summary"]}


def route_based_on_question_class(state: ResponseGeneratorState) -> list:
    """
    Determine the processing route based on the question class.

    Args:
        state (ResponseGeneratorState): The current state containing the `question_class` key,
            which determines the type of question to process.

    Returns:
        list: A list of processing node names to execute. Possible outputs are:
            - ["process_ideas_prompt", "process_dynamic_qa_prompt"] for "ideas" class.
            - ["process_opportunity_prompt", "process_dynamic_qa_prompt"] for "opportunity" class.
            - ["process_dynamic_qa_prompt"] for all other cases.
    """
    if state["question_class"].lower() == "ideas":
        return ["process_ideas_prompt", "process_dynamic_qa_prompt"]
    if state["question_class"].lower() == "opportunity":
        return ["process_opportunity_prompt", "process_dynamic_qa_prompt"]
    if state["question_class"].lower() == "objectives":
        return ["process_objectives_prompt"]
    return ["process_dynamic_qa_prompt"]


def format_response(state: ResponseGeneratorState):
    """
    Format the response payload based on the question class and state data.
    Args:
        state (ResponseGeneratorState): The current state containing keys such as:
            - `question_class` (str): The type of question (e.g., "others", "opportunity", "ideas").
            - `dynamic_qa_summary` (str): The dynamically generated Q&A summary.
            - `opportunity_summary` (str, optional): Summary for opportunity-related questions.
            - `insights` (list, optional): Insights related to the question.
            - `dynamic_ideas` (list, optional): Generated ideas for idea-related questions.
            - `pg_db_conn` (object): Database connection for fetching linked insights.
            - `category` (str): The category of the query.

    Returns:
        dict:
            - "response_payload" (dict): The formatted response payload.

    Notes:
        - For "others" questions, only the dynamic Q&A summary is included.
        - For "opportunity" questions, the summary and any linked insights are included.
        - For "ideas" questions, the dynamic summary and ideas are included if available.
        - An error is raised for invalid `question_class` values.
    """
    log.info("Executing node: format_response")
    response_params: dict[str, Any] = {}

    if state["question_class"] == "others":
        response_params["message"] = state["dynamic_qa_summary"]
    elif state["question_class"] == "objectives":
        if json.loads(state["dynamic_qa_summary"])["objectives"] == {}:
            response_params["message"] = "No objectives can be created."
            response_params["objectives"]= json.loads(state["dynamic_qa_summary"])["objectives"]
        else:
            response_params["message"] = ""
            response_params["objectives"]= json.loads(state["dynamic_qa_summary"])["objectives"]
    elif state["question_class"] == "opportunity":
        response_params["message"] = state["dynamic_qa_summary"]
        if state.get("insights", None):
            # response_params["insights"] = fetch_linked_insights_with_ids(
            #     state["insights"],
            #     state["pg_db_conn"],
            #     state["category"],
            # )
            response_params["insights"] = [value.strip().replace("insight: ", "") for value in state["insights"]]
            # response_params["insights"] = state["insights"]
            
    elif state["question_class"] == "ideas":
        response_params["message"] = state["dynamic_qa_summary"]
        if state.get("dynamic_ideas", None):
            response_params["dynamic_ideas"] = state["dynamic_ideas"]
    else:
        raise ValueError("Invalid question_class")

    if response_params.get("insights", []) or response_params.get("dynamic_ideas", []):
        response_params["message"] += (
            "\n\n" + "Recommended ideas/insights you might be interested in: "
        )
    
    formatted_response = prepare_response_payload(**response_params)

    state["response_payload"] = formatted_response
    log.info("Response Payload created: \n %s", state["response_payload"])
    return {"response_payload": state["response_payload"]}


def process_objectives_prompt(state: ResponseGeneratorState) -> dict:
    """
    Process the objectives prompt and generate a dynamic response.

    Args:
        state (ResponseGeneratorState): The current state containing context data,
            user query, NER output, and chat history.

    Returns:
        dict:
            - "objective_summary" (str): The summary of the objective generated
            from the response.
    """

    log.info("Executing node: process_objectives_prompt")

    sf_client = SnowflakeClient(tenant_id=state["tenant_id"])

    skus_list = []
    supplier = ""

    for ner_data in state["ner_output"]:
        if ner_data["entity"] == "supplier":
            if ner_data["type"] == "name":
                supplier = ner_data["value"][0]
                break
    
    for ner_data in state["ner_output"]:
        if ner_data["entity"] == "sku":
            if ner_data["type"] == "name":
                skus_list = ner_data["value"]

    additional_data = extract_category_analytic_data(supplier,skus_list,state["category"],sf_client)

    print(additional_data)

    if additional_data == None:
        state["dynamic_qa_summary"] = json.dumps({"objectives":{}})
        return {"dynamic_qa_summary": state["dynamic_qa_summary"]} 
    
    currency_context = sf_client.execute_query(f"""Select DIM_CURRENCY_DOCUMENT as currency , TXT_CURRENCY_SYMBOL as currency_symbol from data.T_DIM_CURRENCY_SYMBOLS where DIM_CURRENCY_DOCUMENT=(Select TXT_REPORTING_CURRENCY from data.VT_DIM_REPORTINGCURRENCY where NUM_ORDER=1) LIMIT 1;""")
    currency = currency_context[0][0]

    prompt_params = {"additional_data":additional_data,"category":state["category"],"supplier":supplier,"tenant_id":state["tenant_id"],"currency":currency}


    prompt = create_objectives_prompt()
    response = generate_chat_response_with_chain(prompt,model="gpt-4o",temperature=0.3,prompt_params=prompt_params)

    ai_output = response.replace("json", "").replace("`", "")

    print(ai_output)
    
    try:
        json_response = json.loads(ai_output)
        state["dynamic_qa_summary"] = json.dumps(json_response)
    except json.decoder.JSONDecodeError as ex:
        log.error("Error in processing objectives prompt: %s", ex)
        state["dynamic_qa_summary"] = json.dumps({})

    log.info("Execution complete: process_objectives_prompt")
    return {
        "dynamic_qa_summary": state["dynamic_qa_summary"],
    }



def create_response_generator_pipeline() -> CompiledStateGraph:
    """
    Create and compile the response generator pipeline.

    Returns:
        CompiledStateGraph: The compiled state graph for the response generator pipeline.
    """
    workflow = StateGraph(ResponseGeneratorState)

    workflow.add_node("process_objectives_prompt", process_objectives_prompt)
    workflow.add_node("process_dynamic_qa_prompt", process_dynamic_qa_prompt)
    workflow.add_node("process_opportunity_prompt", process_opportunity_prompt)
    workflow.add_node("process_ideas_prompt", process_ideas_prompt)
    workflow.add_node("format_response", format_response)

    workflow.add_conditional_edges(
        START,
        route_based_on_question_class,
        {
            "process_dynamic_qa_prompt": "process_dynamic_qa_prompt",
            "process_opportunity_prompt": "process_opportunity_prompt",
            "process_ideas_prompt": "process_ideas_prompt",
            "process_objectives_prompt": "process_objectives_prompt"
        },
    )
    workflow.add_edge("process_dynamic_qa_prompt", "format_response")
    workflow.add_edge("process_opportunity_prompt", "format_response")
    workflow.add_edge("process_ideas_prompt", "format_response")
    workflow.add_edge("process_objectives_prompt", "format_response")

    workflow.add_edge("format_response", END)

    return workflow.compile()
