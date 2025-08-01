import json
import os
import re
import asyncio
import copy
from pathlib import Path

from jinja2 import Template
from src.providers.database.snowflake_driver import SnowflakeConnection
from src.env import OPENAI_API_KEY, OPENAI_BASE_URL
from lightrag import LightRAG
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed
from src.configs.configs_model import config
from src.utils.logs import get_custom_logger
from src.datamodels.doc_ai_model import ExtractedEntities
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag import QueryParam
from src.providers.llm.openai import model_mini
from src.celery_tasks.doc_ai_task import update_leakage
from src.celery_tasks.pg_status_task import update_pg_status
from src.celery_tasks.contract_summary_task import update_snowflake_invoice

logger = get_custom_logger(__name__)

def find_project_root(
  start: Path = Path(__file__).resolve(),
  markers: set = {"pyproject.toml", "setup.py", ".git"}
) -> Path:
    p = start
    while p.parent != p:
        if any((p / m).exists() for m in markers):
            return p
        p = p.parent
    raise FileNotFoundError(f"no project root found from {start}")

PROJECT_ROOT = find_project_root()
logger.info(f"Project root: {PROJECT_ROOT}")

def clean_json_result(result):
    if isinstance(result, dict):
        return result
    if isinstance(result, str):
        match = re.search(r"```json\s*(\{.*\})\s*```", result, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            match = re.search(r"(\{.*\})", result, re.DOTALL)
            if match:
                json_str = match.group(1)
            else:
                json_str = result
        try:
            return json.loads(json_str)
        except Exception:
            return {"raw": result}
    return {"raw": result}

async def fetch_rows_for_entity_extraction(sf_conn, database, schema, table, upload_ids, sql_template_path):
    # Prepare the SQL IN clause with the upload_ids
    upload_ids_str = ', '.join([f"'{uid}'" for uid in upload_ids])
    with open(f"{sql_template_path}/fetch_rows_for_entity_extraction.sql", "r") as f:
        sql_template = Template(f.read())
    # Render the query with provided variables
    query = sql_template.render(database=database, schema=schema, table=table, upload_ids_str=upload_ids_str)
    logger.info(f"Executing query to fetch rows for entity extraction: {query}")
    rows = sf_conn.execute_query(query)
    return rows

async def insert_entity_json(sf_conn, upload_id, entity_json, database, schema, table, sql_template_path):
    try:
        # Load the template
        with open(f"{sql_template_path}/insert_entity_json.sql", "r") as f:
            sql_template = Template(f.read())
        # Render the query with provided variables
        query = sql_template.render(database=database, schema=schema, table=table, entity_json=json.dumps(entity_json), upload_id=upload_id)

        logger.info(f"Executing query to insert ENTITY_JSON for UPLOAD_ID={upload_id}: {query}")
        sf_conn.cur.execute(query)
        sf_conn.conn.commit()
        logger.info(f"Updated ENTITY_JSON for UPLOAD_ID={upload_id}")
    except Exception as e:
        logger.error(f"Failed to update ENTITY_JSON for UPLOAD_ID={upload_id}: {e}")


def load_template(template_path):
    with open(template_path, "r") as f:
        return json.load(f)

def load_prompt(prompt_path):
    with open(prompt_path, "r") as f:
        return f.read()


async def extract_entities_from_pdf(text, rag, template_path, prompt_txt_path):
    logger.info(f"Initializing RAG with working directory: {rag.working_dir}")
    await rag.initialize_storages()
    await initialize_pipeline_status()
    await rag.ainsert(text)
    await rag.finalize_storages()

    template = load_template(template_path)

    # Define field groups and their prompt keys
    field_groups = {
        "extract_generic_fields": [
            "Supplier", "Region","Payment terms", "Supplier termination (convenience) period",
            "Buyer termination (convenience) period", "Buyer termination (cause) period",
            "Prices", "Specific terms agreed", "Incoterms/shipping", "Payment/invoicing terms",
            "Jurisdiction/compliance", "Vendor name and address/region", "Title for the contract",
            "Volume commitment", "Contract start date", "Contract expiry date", "Contract duration",
            "Renewal clause and notice period"
        ],
        "extract_skus": ["SKUs"],
        "extract_insurance": ["Insurance"],
        "extract_performance_penalties": ["Performance penalties"],
        "extract_pricing_and_partnership": ["Pricing Value, Drivers & Commercial Sustainability", "Partnership & Contract Governance"],
        "extract_contract_digest": ["Contract Digest"]
    }

    # Map field group to prompt txt key
    prompt_keys = {
        "extract_generic_fields": "node_extract_generic_fields",
        "extract_skus": "node_extract_skus",
        "extract_insurance": "node_extract_insurance",
        "extract_performance_penalties": "node_extract_performance_penalties",
        "extract_pricing_and_partnership": "node_extract_pricing_and_partnership",
        "extract_contract_digest": "node_extract_contract_digest"
    }

    results = {}
    for key, fields in field_groups.items():
        sub_template = {k: template[k] for k in fields if k in template}
        prompt_file = prompt_txt_path[prompt_keys[key]]
        prompt_template = load_prompt(prompt_file)
        prompt = Template(prompt_template).render(TEMPLATE_JSON=json.dumps(sub_template, indent=2))
        await rag.initialize_storages()
        logger.info(f"Starting entity extraction query for {key}...")
        result = await rag.aquery(prompt, param=QueryParam(mode="mix"))
        await rag.finalize_storages()
        results[key] = clean_json_result(result)

    # Combine all results using OpenAI model and combine prompt
    combine_prompt_template = load_prompt(prompt_txt_path["combine_results"])
    combine_prompt = (
        combine_prompt_template
        .replace("{{TEMPLATE_JSON}}", json.dumps(template, indent=2))
        .replace("{{NODE_EXTRACT_GENERIC_FIELDS_JSON}}", json.dumps(results["extract_generic_fields"], indent=2))
        .replace("{{NODE_EXTRACT_SKUS_JSON}}", json.dumps(results["extract_skus"], indent=2))
        .replace("{{NODE_EXTRACT_INSURANCE_JSON}}", json.dumps(results["extract_insurance"], indent=2))
        .replace("{{NODE_EXTRACT_PERFORMANCE_PENALTIES_JSON}}", json.dumps(results["extract_performance_penalties"], indent=2))
        .replace("{{NODE_EXTRACT_PRICING_AND_PARTNERSHIP_JSON}}", json.dumps(results["extract_pricing_and_partnership"], indent=2))
        .replace("{{NODE_EXTRACT_CONTRACT_DIGEST_JSON}}", json.dumps({"contract_digest": text}, indent=2))
    )
    messages = [
        {"role": "system", "content": "You are a helpful assistant that combines JSON outputs."},
        {"role": "user", "content": combine_prompt}
    ]
    response = model_mini.invoke(messages)
    final_json = clean_json_result(response.content)
    return final_json

async def process_single_row(upload_id, data_content, working_dir, rag, template_path, prompt_txt_path, sf_conn, database, schema, table, sql_template_path):
    logger.info(f"Processing upload_id: {upload_id} with data_content length: {len(data_content.split(" "))}...")  # Log first 100 char
    os.makedirs(working_dir, exist_ok=True)
    extracted = await extract_entities_from_pdf(data_content, rag, template_path, prompt_txt_path)
    logger.info(f"Entities extracted for upload_id {upload_id}")
    validated = ExtractedEntities.parse_obj(extracted)
    output_json = os.path.join(working_dir, "entities_extracted.json")
    with open(output_json, "w") as f:
        json.dump(validated.dict(), f, indent=2)

    await insert_entity_json(sf_conn, upload_id, validated.dict(), database, schema, table, sql_template_path)
    return 1  # for counting updated rows

async def process_snowflake_entities(tenant_id, upload_ids):
    conn_params = config.conn_params.get(tenant_id)
    if not conn_params:
        raise ValueError(f"No Snowflake credentials found for tenant_id: {tenant_id}")

    #TODO Fix improve
    user = conn_params["user"]
    password = conn_params["password"]
    account = conn_params["account"]
    warehouse = conn_params["warehouse"]
    role = conn_params["role"]
    database = conn_params["database"]
    schema = "DATA"
    table = "DOCUMENT_AI_EXTRACTED_DATA"
    temp_tenant_id = conn_params["temp_tenant_id"]
    base_dir = f"{Path(PROJECT_ROOT)}/src/source_ai/{temp_tenant_id}/bearings"
    template_path = f"{base_dir}/templates/entity_prompt_template.json"
    sql_template_path = f"{base_dir}/sql"

    logger.info(f"Processing Snowflake entities for {temp_tenant_id}.{schema}.{table} using template {template_path}")

    prompt_txt_path = {
        "node_extract_generic_fields": f"{base_dir}/templates/prompt_extract_generic_fields.txt",
        "node_extract_skus": f"{base_dir}/templates/prompt_extract_skus.txt",
        "node_extract_insurance": f"{base_dir}/templates/prompt_extract_insurance.txt",
        "node_extract_performance_penalties": f"{base_dir}/templates/prompt_extract_performance_penalties.txt",
        "node_extract_pricing_and_partnership": f"{base_dir}/templates/prompt_extract_pricing_and_partnership.txt",
        "node_extract_contract_digest": f"{base_dir}/templates/prompt_extract_contract_digest.txt",
        "combine_results": f"{base_dir}/templates/prompt_with_examples_combine.txt"
    }

    conn_params = {
        "user": user,
        "password": password,
        "account": account,
        "database": database,
        "warehouse": warehouse,
        "role": role,
    }
    sf_conn = SnowflakeConnection(conn_params)

    updated_rows = 0
    rows = await fetch_rows_for_entity_extraction(sf_conn, temp_tenant_id, schema, table, upload_ids, sql_template_path)

    for upload_id, data_content, category, doc_type in rows:
        if doc_type == "Contracts":
            try:
                #TODO - Path Should be mounted of efs
                update_pg_status.delay(table='doc_ai_document', upload_id=upload_id, status="processing", schema=tenant_id)
                working_dir = f"{base_dir}/data/data_light_rag/data_{upload_id}"
                logger.info(f"Processing upload_id: {upload_id} with working_dir: {working_dir}")
                os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
                os.environ["OPENAI_API_BASE"] = OPENAI_BASE_URL
                rag = LightRAG(
                    working_dir=working_dir,
                    embedding_func=openai_embed,
                    llm_model_func=gpt_4o_mini_complete,
                    llm_model_kwargs={
                        "api_key": OPENAI_API_KEY,
                        "base_url": OPENAI_BASE_URL,
                    }
                )
                logger.info(f"Checking Variables: Upload ID: {upload_id}, Data Content Length: {len(data_content.split(' '))}, Working Dir: {working_dir}, Template Path: {template_path}")
                logger.info(f"temp_tenant_id: {temp_tenant_id}, schema: {schema}, table: {table}")
                updated_rows += await process_single_row(
                    upload_id,
                    data_content,
                    working_dir,
                    rag,
                    template_path,
                    prompt_txt_path,
                    sf_conn,
                    temp_tenant_id,
                    schema,
                    table,
                    sql_template_path
                )
                input_parms = {
                    "conn_params": conn_params,
                    "database": temp_tenant_id,
                    "schema": schema,
                    "upload_id": upload_id,
                    "tenant_id": tenant_id,
                    "category": category,
                    "sql_template_path": sql_template_path
                }

                update_pg_status.delay(table='doc_ai_document', upload_id=upload_id, status="entity_extracted", schema=tenant_id)

                update_leakage.delay(**input_parms)
            except Exception as e:
                logger.exception(f"Error processing upload_id {upload_id}: {e}")
                update_pg_status.delay(table='doc_ai_document', upload_id=upload_id, status="ERROR", schema=tenant_id)
                continue
        elif doc_type == "Invoices":
            try:
                invoice_prompt_txt_path =  f"{base_dir}/templates/invoice_extraction_prompt.txt"
                invoice_prompt = load_prompt(invoice_prompt_txt_path)
                messages = [
                    {"role": "system", "content": invoice_prompt},
                    {"role": "user", "content": f"Invoice Text to Process: {data_content}"}
                ]
                response = model_mini.invoke(messages)
                final_json = clean_json_result(response.content)
                await insert_entity_json(sf_conn, upload_id, final_json, database, schema, table, sql_template_path)
                update_pg_status.delay(table='doc_ai_document', upload_id=upload_id, status="invoice_extracted", schema=tenant_id)
                update_snowflake_invoice.delay(
                    conn_params=conn_params,
                    database=database,
                    schema=schema,
                    upload_id=upload_id,
                    entity_json=final_json,
                    tenant_id=tenant_id,
                    sql_template_path=sql_template_path
                )
                updated_rows += 1
            except Exception as e:
                logger.exception(f"Error processing upload_id {upload_id}: {e}")
                update_pg_status.delay(table='doc_ai_document', upload_id=upload_id, status="ERROR", schema=tenant_id)
                continue
        else:
            logger.warning(f"Unsupported document type '{doc_type}' for upload_id {upload_id}. Skipping entity extraction.")
    sf_conn.cur.close()
    sf_conn.conn.close()
    return updated_rows