import ast
import datetime
import json
from jinja2 import Template
from src.datamodels.state_model import Text2SQLState
from src.utils.logs import get_custom_logger
from src.providers.prompts import prompt_library
from src.datamodels.openai_response_model import (
    StabiliseQueryResponse,
    RerankedResponse,
    GeneratedSQLResponse,
    SQLCorrectionResponse
)
from src.utils.engine import SQLGenPostProcessorV2
from src.providers.engine.wren_engine import wren_ui_engine
from src.providers.llm.openai import model, openai_embeddings_model
from src.providers.document_store.qdrant_store import qdrant_document_store
from langchain_core.messages import SystemMessage, HumanMessage
from src.utils.custom_callbacks import timed_node_sync
from asgiref.sync import async_to_sync
from src.providers.cache_store.redis_cache import cache

logger = get_custom_logger(__name__)

@timed_node_sync("query_stabilisation")
def query_stabilisation(state: Text2SQLState) -> Text2SQLState:
    """
    Stabilises the query by ensuring it is in a consistent format.
    This function can be extended to include more complex stabilisation logic.
    """
    query = state.user_query
    logger.info(f"Stabilising query: {query}")
    prompt = prompt_library.get_prompts(tenant_id=state.tenant_id, prompt_name="query_stabilisation")
    prompt_rendered = Template(prompt).render( category=state.category)
    if prompt is None:
        logger.error(f"Prompt not found for tenant_id={state.tenant_id,} and prompt_name='query_stabilisation'")
        raise ValueError(f"Prompt not found for tenant_id={state.tenant_id,} and prompt_name='query_stabilisation'")
    structured_llm = model.with_structured_output(StabiliseQueryResponse)
    structured_llm_response = structured_llm.invoke([
        SystemMessage(content=prompt_rendered),
        HumanMessage(content=query)
    ])
    if not structured_llm_response:
        logger.error("No response from structured LLM")
        raise ValueError("No response from structured LLM")
    state.fixed_query = structured_llm_response.fixed_query
    logger.info(f"Stabilised query: {state.fixed_query}")
    return state

@timed_node_sync("check_cache")
def get_cache(state: Text2SQLState) -> Text2SQLState:
    tenant_id = state.tenant_id
    fixed_query = state.fixed_query
    fixed_query = (
            fixed_query
            .replace(" ","")
            .replace("'","")
            .replace("[","")
            .replace("]","")
            .lower()
        )
    key=f"{tenant_id}:{fixed_query}"
    logger.info(f"Retrieving Redis Cache for key: {key}")
    cache_hit = cache.get(key=key)
    if cache_hit:
        logger.info("Cache Hit Found")
        state.cache = json.loads(cache_hit)
    else:
        logger.info("Cache Miss")
        state.cache = {}
    return state

def check_cache_hit(state: Text2SQLState) -> Text2SQLState:
    logger.debug(f"State: {state}")
    if state.cache:
        return "Hit"
    return "Miss"

@timed_node_sync("sql_retriever")
def sql_retriever(state: Text2SQLState) -> Text2SQLState:
    """
    Retrieves SQL queries from the database based on the stabilised query.
    This function can be extended to include more complex retrieval logic.
    """
    fixed_query = state.fixed_query
    tenant_id = state.tenant_id
    logger.info(f"Retrieving SQL for query: {fixed_query}")
    embedded_query = openai_embeddings_model.embed_query(text=fixed_query)
    qdrant_sync_func =  async_to_sync(qdrant_document_store.search_documents)
    results = qdrant_sync_func(collection="sql_examples", embedding=embedded_query, tenant_id=tenant_id, limit=5)
    if not results:
        logger.warning("No SQL examples found for the given query.")
        state.retrieved_sql = "No SQL examples found."
    else:
        sql_samples =  [{ "sample": ind+1, "question":result.payload["content"], "sql": result.payload["solution_example"]} for ind, result in enumerate(results)]
    state.retrieved_sql = sql_samples
    logger.info(f"Retrieved SQL: {state.retrieved_sql}")
    return state

@timed_node_sync("query_reranker")
def query_reranker(state: Text2SQLState) -> Text2SQLState:
    """
    Reranks the retrieved SQL queries based on their relevance to the fixed query.
    This function can be extended to include more complex reranking logic.
    """
    
    retrieved_sql = state.retrieved_sql
    samples = {}
    for element in retrieved_sql:
        samples[element["sample"]] = element["question"]
    logger.info(f"Reranking SQL: {retrieved_sql}")

    # Placeholder for actual reranking logic
    # For now, we just return the first SQL as the best match

    prompt = prompt_library.get_prompts(tenant_id=state.tenant_id, prompt_name="sql_reranker")
    prompt_rendered = Template(prompt).render(user_question=state.fixed_query, samples=samples)
    logger.debug(f"Prompt rendered for reranking: {prompt_rendered}")
    if prompt is None:
        logger.error(f"Prompt not found for tenant_id={state.tenant_id} and prompt_name='sql_reranker'")
        raise ValueError(f"Prompt not found for tenant_id={state.tenant_id} and prompt_name='sql_reranker'")
    structured_llm = model.with_structured_output(RerankedResponse)
    structured_llm_response = structured_llm.invoke([
        HumanMessage(content=prompt_rendered)
    ])
    # state.reranked_sql = structured_llm_response.model_dump()
    temp = []
    reranked_sql = structured_llm_response.model_dump()
    for element in reranked_sql["response"]:
        if element["confidence"] > 0.7:
            question = element["question"]
            for ele in retrieved_sql:
                if ele["question"] == question:
                    temp.append({"question": question, "sql": ele["sql"]}) 
    state.reranked_sql = temp
    logger.info(f"Reranked SQL: {state.reranked_sql}")
    return state

timed_node_sync("db_schema_retriever")
def db_schema_retriever(state: Text2SQLState) -> Text2SQLState:
    qdrant_sync = async_to_sync(qdrant_document_store.get_all_documents)
    schema = qdrant_sync(collection="Document")
    db_schemas = {}
    for document in schema:
        content = ast.literal_eval(document.payload['content'])
        if content["type"] == "TABLE":
            logger.debug(f"Content Type : {content}")
            if content["name"] not in db_schemas:
                db_schemas[content["name"]] = {
                    "description": content.get("comment", "")
                }
            else:
                db_schemas[content["name"]]["description"] = content.get("comment", "")
        elif content["type"] == "TABLE_COLUMNS":
            name = document.payload["name"]
            temp = []
            for col in content.get("columns", []):    
                if col["type"]!= "FOREIGN_KEY":
                    temp.append({
                            "type": col.get("type", ""),
                            "name": col.get("name", ""),
                            "data_type": col.get("data_type", ""),
                            "description": col.get("comment", ""),
                            "is_primary_key": "PRIMARY KEY" if col.get("is_primary_key", "") else ""
                        }
                    )
                else:
                    temp.append({
                        "type": col.get("type", ""),
                        "description": col.get("comment", ""),
                        "constraint": col.get("constraint", ""),
                        "tables": col.get("tables", []),
                    })

            if name not in db_schemas:
                db_schemas[name] = {"columns": temp}
            else:
                db_schemas[name]["columns"] = temp
    logger.debug(f"DB Schema prepared: {db_schemas}")
    db_schema_string = ""
    for table_name, values in db_schemas.items():
        db_schema_string+=f"\nCREATE TABLE { table_name } ("
        db_schema_string+=f"\t{values['description']}\n"
        for column in values['columns']:
            if column['type'] == 'COLUMN':
                db_schema_string+=f"\t{ column['name'] } { column['data_type'] } { column['is_primary_key'] }\n"
            else:
                db_schema_string+=f"\t{column['constraint']}\n"
            db_schema_string+=f"\t{column['description']}"
        db_schema_string+=");\n"
    logger.debug(f"DB Schema String: {db_schema_string}")
    # * This commented code is for trimming the db schemas reqruired to produce sql query
    # * to be implemented in future usecase.
    # logger.debug(f"Final schema retrieved: {db_schemas}")
    # prompt = prompt_library.get_prompts(tenant_id=state.tenant_id, prompt_name='db_schema_retriever')
    # prompt_rendered = Template(prompt).render(category=state["category"], db_schema=final_schema, reranked_sql=reranked_sql)
    # structured_llm = model.with_structured_output(SchemaResponse)
    # structured_llm_response = structured_llm.invoke([
    #     SystemMessage(content=prompt_rendered),
    #     HumanMessage(content=reranked_sql)
    # ])
    state.db_schema = db_schema_string
    # logger.info(f"Retrieved DB schema: {state['db_schema']}")
    return state

@timed_node_sync("sql_generator")
def sql_generator(state: Text2SQLState) -> Text2SQLState:
    reference_sql = state.reranked_sql
    qualified_prompt = []
    for counter, element in enumerate(reference_sql):
        qualified_prompt.append("\n".join([
                                f"#### Sample: {counter}",
                                f"##### Question: {element["question"]}",
                                f"###### SQL Query: {element["sql"]}"
                                ]))
    logger.debug(f"fixed_query: {state.fixed_query}")
    logger.debug(f"category: {state.category}")
    logger.debug(f"tenant_id: {state.tenant_id}")
    logger.info("Generating SQL")
    
    prompt = prompt_library.get_prompts(tenant_id=state.tenant_id, prompt_name="sql_generation")
    prompt_rendered = Template(prompt).render(
        category=state.category, 
        db_schema=state.db_schema, 
        samples="\n".join(qualified_prompt), 
        query=state.fixed_query, 
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    logger.debug(f"Prompt rendered for SQL generation: {prompt_rendered}")
    prompt = prompt_library.get_prompts(tenant_id=state.tenant_id, prompt_name="sql_generation_system_prompt")
    system_prompt_rendered = prompt
    structured_llm = model.with_structured_output(GeneratedSQLResponse)
    structured_llm_response = structured_llm.invoke([
        SystemMessage(content=system_prompt_rendered),
        HumanMessage(content=prompt_rendered)
    ])
    state.generated_sql = structured_llm_response.generated_sql
    logger.info(f"Generated SQL: {state.generated_sql}")
    return state

@timed_node_sync("sql_validation")
def sql_validation(state: Text2SQLState) -> Text2SQLState:
    if state.recursion_depth < 2:
        generated_sql = state.generated_sql
        logger.info("Validating SQL")
        try:
            post_processor = SQLGenPostProcessorV2(engine=wren_ui_engine)
            validated_sql_result, invalid_result = async_to_sync(post_processor.run)(generated_sql)
            logger.debug(f"Invalid SQL Result: {invalid_result}")
            if len(validated_sql_result) == 0:
                logger.debug(f"Invalid SQL Result: {invalid_result}")
                state.validation_result = invalid_result
            else:
                logger.debug(f"Validated SQL Result: {validated_sql_result}")
                state.validation_result = validated_sql_result
        except Exception as e:
            logger.exception(f"Error during SQL validation: {e}")
    else:
        logger.exception(f"Recursion Depth: {state.recursion_depth}")
        raise Exception()
    return state

@timed_node_sync("sql_correction")
def sql_correction(state: Text2SQLState) -> Text2SQLState:
    if state.recursion_depth < 1:
        db_schema = state.db_schema
        category = state.category
        reference_sql = state.reranked_sql
        validation_result=state.validation_result
        prompt = prompt_library.get_prompts(tenant_id=state.tenant_id, prompt_name="sql_correction")
        qualified_prompt = []
        for counter, element in enumerate(reference_sql):
            qualified_prompt.append("\n".join([
                                    f"#### Sample: {counter}",
                                    f"##### Question: {element["question"]}",
                                    f"###### SQL Query: {element["sql"]}"
                                    ]))
        prompt_rendered = Template(prompt).render(
            category=category, 
            db_schema=db_schema, 
            reference_sql=qualified_prompt,
            generated_sql=validation_result[0]['sql'],
            error_in_sql=validation_result[0]['error']
        )
        prompt = prompt_library.get_prompts(tenant_id=state.tenant_id, prompt_name="sql_generation_system_prompt")
        system_prompt_rendered = prompt
        structured_llm = model.with_structured_output(SQLCorrectionResponse)
        structured_llm_response = structured_llm.invoke([
            SystemMessage(content=system_prompt_rendered),
            HumanMessage(content=prompt_rendered)
        ])
        state.generated_sql = structured_llm_response.corrected_sql
        state.recursion_depth+=1
        logger.info(f"Generated SQL: {state.generated_sql}")
    return state


def sql_validation_response_parsing(state: Text2SQLState) -> str:
    validation_result = state.validation_result
    logger.debug(f"SQL Validation Results: {validation_result}")
    if not validation_result:
        logger.warning("No validation results found.")
        return "Invalid"
    if "error" in validation_result[0]:
        logger.error("Error in Validation Results Found")
        return "Invalid"
    if state.recursion_depth >= 1:
        return "Error"
    return "Valid"

def response(state: Text2SQLState)-> Text2SQLState:
    if state.cache:
        state.final_sql = state.cache["sql"]
    else:
        state.final_sql = state.validation_result[0]["sql"]
    return state