import datetime
import json
import time

import httpx
import qdrant_client
from jinja2 import Template
from langchain_core.messages import HumanMessage, SystemMessage
from src.celery_tasks.redis_task import create_cache
from src.configs.configs_model import config
from src.datamodels.openai_response_model import (
    ClassifyIntentResponse,
    NERResponse,
    OpenWorldResponse
)
from src.providers.cache_store.redis_cache import cache
from src.datamodels.state_model import ChatState
from src.env import QDRANT_HOST, QDRANT_PORT
from src.providers.llm.openai import (
    model, openai_client,
    openai_embeddings_model
)
from src.providers.prompts import prompt_library
from src.utils.apis import execute_api
from src.utils.logs import get_custom_logger
from src.pipelines.threads.chat_thread import Thread
from src.providers.database.snowflake_driver import SnowflakeDatabaseFactory
from src.utils.custom_callbacks import timed_node_sync

logger = get_custom_logger(__name__)


@timed_node_sync("check_history")
def check_history(state: ChatState) -> dict:
    tenant_id = state["tenant_id"]
    session_id = state["session_id"]
    key = f"{tenant_id}:{session_id}:chat_history"
    logger.info(f"Checking History: {key}")
    cache_hit = cache.get(key=key)
    if cache_hit:
        logger.info("Cache History Found")
        history = json.loads(cache_hit)
        logger.debug(f"History: {history}")
    elif state["thread_id"]:
        logger.info("Checking for Thread History")
        thread = Thread(
            tenant_id=tenant_id,
            category=state["category"],
            thread_id=[state["thread_id"]]
        )
        history = []
        for thread_msg in thread.get_thread():
            logger.info(f"Thread: {thread_msg}")
            for msg in thread_msg["chat"]:
                history.append({
                    msg["role"]: msg["content"]
                })
    else:
        logger.info("No History Found")
        history = []
        
    return {"history": history}

@timed_node_sync("classify_intent")
def classify_intent(state: ChatState) -> ChatState:
    query = state["user_input"]
    logger.info(f"Classifying Intent for Query: {query}")
    prompt = prompt_library.get_prompts(tenant_id=state["tenant_id"], prompt_name="intent_classification")
    if prompt is None:
        logger.error(f"Prompt not found for tenant_id={state["tenant_id"]} and prompt_name='intent_classification'")
        raise ValueError(f"Prompt not found for tenant_id={state["tenant_id"]} and prompt_name='intent_classification'")
    structured_llm = model.with_structured_output(ClassifyIntentResponse)
    structured_llm_response =  structured_llm.invoke([SystemMessage(content=prompt),HumanMessage(content=query)])
    logger.info(f"Intent Classified: {structured_llm_response.route}")
    state["route"] = structured_llm_response.route
    return state

@timed_node_sync("ner_tagging")
def ner_tagging(state: ChatState) -> dict:
    query = (
        state["user_input"]
        .replace("'", "")
        .replace('"', "")
        .replace("-", " ")
        .replace("_", " ")
    )
    logger.info(f"Checking for NER Entities: {query}")
    prompt = prompt_library.get_prompts(tenant_id=state["tenant_id"], prompt_name="ner_tagging")
    if prompt is None:
        logger.error(f"Prompt not found for tenant_id={state["tenant_id"]} and prompt_name='ner_tagging'")
        raise ValueError(f"Prompt not found for tenant_id={state["tenant_id"]} and prompt_name='ner_tagging'")
    rendered_prompt = Template(prompt).render(sentence=query)
    structured_llm = model.with_structured_output(NERResponse)
    structured_llm_response =  structured_llm.invoke([HumanMessage(content=rendered_prompt)])
    logger.info(f"Raw LLM response: {structured_llm_response}")
    if not structured_llm_response or not hasattr(structured_llm_response, "entities") or structured_llm_response.entities is None:
        logger.warning("NER LLM response is empty or malformed, setting entities to empty list.")
        entities = []
    else:
        entities = structured_llm_response.entities
    return {"entities": entities}

@timed_node_sync("ner_tag_process")
def ner_tag_process(state: ChatState) -> dict:
    """
    Process the NER tagging response and update the state.
    """
    client = qdrant_client.QdrantClient(QDRANT_HOST, port=QDRANT_PORT)

    if "ludwigshafen" in state["user_input"].lower():
        logger.info("Ludwigshafen detected in user input, skipping NER tagging.")
        # state.ner_tagged_input = state.user_input
        # return state
        return {"ner_tagged_input": state["user_input"]}

    entity_matches = []
    for entity in state["entities"]:
        embedding =  openai_embeddings_model.embed_query(entity)
        result = client.search(
            collection_name="entities",
            query_vector=embedding,
            limit=50,
            score_threshold=0.55
        )
        entity_matches.append((entity, result))

    logger.info(f"Entity matches: {entity_matches}")

    user_query = state["user_input"]
    temp_user_query = user_query
    for entity, result in entity_matches:
        if result:
            if len(result) > 1:
                logger.debug(f"Multiple entities found for {entity}. Using the first match.")
                # type_ = result[0].payload["type"].lower()
                type_counter= {}
                for element in result:
                    type_ = element.payload["type"].lower()
                    type_counter[type_] = type_counter.get(type_, 0) + 1
                max_type = max(type_counter, key=type_counter.get)
                logger.debug(f"Most common type found: {max_type} from {type_counter}")
                temp_user_query = (
                    temp_user_query
                    .replace("'", "")
                    .replace('"', "")
                    .replace(entity, "[entity]")
                    .replace("[entity]", f"{max_type} named like '%{entity}%'")
                )
                return {"ner_tagged_input": temp_user_query}
                # state.ner_tagged_input = temp_user_query
                # return state
            logger.debug(f"Actual Entity: {entity} Mapped Entity: {result[0].payload['name']} of type {result[0].payload['type']}")
            temp = result[0].payload
            entity_name = temp["name"].lower()
            type_ = temp["type"].lower()
            if type_ in entity_name:
                logger.info("Entity is also present in the user query.")
                temp_user_query = (
                    temp_user_query
                    .replace("'", "")
                    .replace('"', "")
                    .replace(entity, "[entity]")
                    .replace("[entity]", f"{type_} named like '%{entity_name}%'")
                )
                # logger.info(f"Entity {entity} is present in the user query.")
            elif type_ in user_query.lower():
                logger.info(f"Entity {type_} is present in the user query.")
                if entity_name in user_query.lower():
                    temp_user_query = (
                        temp_user_query
                        .replace("'", "")
                        .replace('"', "")
                        .replace(entity, "[entity]")
                        .replace("[entity]", f"{type_} named like '%{entity_name}%'")
                    )
            else:
                temp_user_query = user_query.replace(entity, f"{type_} '{entity_name}'")
                logger.info("Simple case changing entity to type + entity")
            user_query = temp_user_query
    # state.ner_tagged_input = user_query
    # return state
    return {"ner_tagged_input": user_query}


@timed_node_sync("api_bridge")
def api_bridge(state: ChatState) -> ChatState:
    """
    Call the API bridge to get the response.
    Args:
        state (BotState): bot state
    """
    logger.info(f"Calling API Bridge")
    final_query = state['ner_tagged_input'] if state.get('ner_tagged_input', None) else state['user_input'] 
    final_query = final_query.replace("?"," ")
    final_query = f"{final_query} for category {state['category']}"
    logger.info(f"Final Query: {final_query}")
    # response = ask_api_bridge(query=final_query, tenant_id=state["tenant_id"])
    with httpx.Client() as client:
        question = final_query
        tenant_id = state['tenant_id']
        region = state['region']
        session_id = state['session_id']
        category = state["category"]
        conn_params = config.conn_params[tenant_id]
        # logger.info(f"Connection Params: {conn_params}")
        temp_tenant_id = conn_params["temp_tenant_id"]
        region = conn_params["region"]
        logger.info(f"Tenant ID: {tenant_id}")
        logger.info(f"Region: {region}")
        logger.info(f"Temp Tenant ID: {temp_tenant_id}")
        # Setting Up the payload for the external api
        json_data = {
            "user_query": question, 
            "tenant_id": tenant_id, 
            "region": region, 
            "session_id": session_id, 
            "category": category
            }
        # Hit the api
        # token = generate_jwt()
        # config.headers["authorization"] = f"Bearer {token}"
        # config.headers["service"] = "api-bridge-service"
        response =  execute_api(client=client,type="post",config=config,api_path="text2sql", payload=json_data)
        # Extract the query_id from the response
        response_json = response.json()
        logger.info(f"Asks API Response: {json.dumps(response_json, indent=4)}")
        task_id = response_json["task_id"]
        # Check the status of the query
        check=True
        while check:
            response =  execute_api(client=client,type="get", config=config, api_path=f"text2sql/{task_id}")
            response_json = response.json()
            logger.info(f"text2sql/{task_id} API Response: {json.dumps(response_json, indent=4)}")
            if response_json['status'].lower() == 'success':
                check=False
            elif response_json['status'].lower() == 'failure':
                return {"kf_response": None, "cache": {}}
            else:
                time.sleep(2)
        state["kf_response"] = {
            "fixed_query": response_json["result"]["fixed_query"],
            "sql": response_json["result"]["sql"]
        }
        state["cache"] = response_json["result"].get("cache", {})
        return state

@timed_node_sync("check_history")
def kf_output_summary(state: ChatState) -> ChatState:
    """
    Summarize the KF output.

    Args:
        state (BotState): bot state
    """
    if state["kf_response"] is None :
        state["kf_summary"]= None
        return state
    logger.info(f"Summarizing KF Output")
    kf_summary_prompt = prompt_library.get_prompts(
        tenant_id=state["tenant_id"],
        prompt_name="kf_summary")
    logger.debug(f"KF Response: {state['kf_response']}")
    kf_output_summary_prompt_render = Template(kf_summary_prompt).render(
        query=state["user_input"],
        preferred_currency=state["preferred_currency"],
        category=state["category"],
        preferred_language=state["language"],
        actual_question=state["user_input"],
        question=state["kf_response"].get("fixed_query", None),
        sql_query=state["kf_response"].get("sql", None),
        time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data=state["kf_data"].get("data", []),
        columns=state["kf_data"].get("columns", []))
    logger.debug(f"KF Output Summary Prompt Rendered: {kf_output_summary_prompt_render}")
    structure_llm = model.with_structured_output(OpenWorldResponse)
    structured_llm_response =  structure_llm.invoke([SystemMessage(content=kf_output_summary_prompt_render)])
    logger.info(f"KF Output Summary: {structured_llm_response.response}")
    state["kf_summary"] = structured_llm_response.response
    return state

@timed_node_sync("check_history")
def open_world(state: ChatState) -> ChatState:
    logger.debug(f"Answering question from Open World")
    user_question = state["user_input"]
    history = state["history"]
    final_message = ""
    if history:
        for element in history:
            for name, value in element.items():
                final_message += f"\n{name}: '{value}'"
    prompt = prompt_library.get_prompts(
        tenant_id=state["tenant_id"], 
        prompt_name="open_world"
    )
    prompt_render = Template(prompt).render(
        preferred_language=state["language"],
        category=state["category"],
        user_question=user_question,
        statement=state.get("kf_response_failure", False),
        history=final_message if final_message else None
    )
    response = openai_client.responses.create(
            model="gpt-4.1",
            tools=[{ "type": "web_search_preview" }],
            input=prompt_render,
        )
    if response.output[0].type == "message":
        message = response.output[0].content[0].text
        logger.info(f"GPT Response: {message}")
    else:
        message = response.output[1].content[0].text
        logger.info(f"Internet Based Response: {message}")
    state["open_world_response"] = message
    return state

@timed_node_sync("check_history")
def query_sql_data(state: ChatState) -> ChatState:
    sql = state["kf_response"]["sql"]
    tenant_id = state["tenant_id"]
    conn_params = config.conn_params[tenant_id]
    temp_tenant_id = conn_params["temp_tenant_id"]
    region = conn_params["region"]
    logger.info(f"Tenant ID: {tenant_id}")
    logger.info(f"Region: {region}")
    logger.info(f"Temp Tenant ID: {temp_tenant_id}")
    sql = (
        sql
        .replace("DATA_", "DATA.")
        .replace('TXT_DATA.POINT', 'TXT_DATA_POINT')
        .replace('"', '')
    )
    sql = f"USE DATABASE \"{temp_tenant_id}\";{sql}"
    logger.info(f"Query: {sql}")
    db = SnowflakeDatabaseFactory(conn_params)
    logger.info("SF Creation Success")
    result =  db.query(sql)
    logger.info(f"Query Result: {result}")
    state["kf_data"] = {
        "data": result["data"],
        "columns": result["columns"]
    }
    return state

@timed_node_sync("check_history")
def final_response(state: ChatState)-> ChatState:
    tenant_id = state["tenant_id"]
    session_id = state["session_id"]
    history_key = f"{tenant_id}:{session_id}:chat_history"
    history_value = state["history"]
    history_value.extend([
        {
            "HumanMessage": state["user_input"]
        }
    ])
    if state.get("cache", False):
        history_value.append({"AIMessage": state["cache"]["kf_summary"]})
        logger.debug(f"Adding To History: {history_key}")
        create_cache.delay(key=history_key, value=json.dumps(history_value), cache_time=60*60*24*30)
        logger.debug("Returing Cache Output")
        return {
            "final_response":{
                "summary": state["cache"]["kf_summary"], 
                "data": list(map(lambda element: list(element), state["cache"].get("kf_data", {}).get("data", []))),
                "columns": state["cache"].get("kf_data", {}).get("columns", []),
                "actual_question": state["user_input"],
                "preferred_language":state["language"],
                "category": state["category"],
                "preferred_currency":state["preferred_currency"],
                "fixed_query": state["kf_response"].get("fixed_query", None)
            }
        }
    if state.get("kf_summary", False):
        history_value.append({"AIMessage": state["kf_summary"]})
        logger.debug(f"Adding To History: {history_key}")
        create_cache.delay(key=history_key, value=json.dumps(history_value), cache_time=60*60*24*30)
        fixed_query = state["kf_response"]["fixed_query"]
        tenant_id = state["tenant_id"]
        value = {
            "sql": state["kf_response"]["sql"],
            "kf_data": state["kf_data"],
            "kf_summary": state["kf_summary"],
            "created_at": str(datetime.datetime.now())
        }
        fixed_query = (
            fixed_query
            .replace(" ","")
            .replace("'","")
            .replace("[","")
            .replace("]","")
            .lower()
        )
        key=f"{tenant_id}:{fixed_query}"
        logger.debug(f"Key: {key} , Value: {json.dumps(value)}")
        create_cache.delay(key=key, value=json.dumps(value))
        return {
            "final_response":{
                "summary": state["kf_summary"], 
                "data": list(map(lambda element: list(element), state["kf_data"].get("data", []))),
                "columns": state["kf_data"].get("columns", []),
                "actual_question": state["user_input"],
                "preferred_language":state["language"],
                "category": state["category"],
                "preferred_currency":state["preferred_currency"],
                "fixed_query": state["kf_response"].get("fixed_query", None)
            }
        }
    history_value.append({"AIMessage": state["open_world_response"]})
    logger.debug(f"Adding To History: {history_key}")
    create_cache.delay(key=history_key, value=json.dumps(history_value), cache_time=60*60*24*30)
    return {
        "final_response":{
            "summary": state["open_world_response"],
            "data": [],
            "columns": [],
            "actual_question": state["user_input"],
            "preferred_language":state["language"],
            "category": state["category"],
            "preferred_currency":state["preferred_currency"],
            "fixed_query": ""
        }
    }