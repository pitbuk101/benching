import json
from jinja2 import Template
from datetime import datetime
from src.utils.logs import get_custom_logger
from src.providers.database.snowflake_driver import SnowflakeConnection
from src.celery_tasks.pg_status_task import update_pg_status
from src.celery_tasks.contract_summary_task import update_snowflake_contracts

logger = get_custom_logger(__name__)


def fetch_rows_for_entity_update(sf_conn, database, schema, table, upload_id):

    with open(f"{sf_conn.sql_template_path}/fetch_rows_for_entity_update.sql", 'r') as file:
        template = Template(file.read())

    query = template.render(
        database=database,
        schema=schema,
        table=table,
        upload_id=upload_id
    )
    logger.info(f"Entity extraction query: {query}")
    rows = sf_conn.execute_query(query)
    return rows

def fetch_invoice_spend(sf_conn, sku, start_date, end_date, database, schema, table, sql_template_path):
    # Query the DB for the sum of MES_SPEND_CURR_1 for this SKU and date range
    with open(f"{sql_template_path}/fetch_invoice_spend.sql", 'r') as file:
        template = Template(file.read())

    query = template.render(
        database=database,
        schema=schema,
        table=table,
        sku=sku,
        start_date=start_date,
        end_date=end_date
    )
    logger.info(f"Fetch Invoice Spend Query: {query}")
    result = sf_conn.execute_query(query)
    logger.info(f"Invoice spend query: {query}")
    return float(result[0][0]) if result and result[0][0] is not None else 0.0

def update_entity_json(sf_conn, upload_id, entity_json, database, schema, table, sql_template_path):
    try:
        with open(f"{sql_template_path}/update_entity_json.sql", 'r') as file:
            template = Template(file.read())

        query = template.render(
            database=database,
            schema=schema,
            table=table,
            updated_json=json.dumps(entity_json),
            upload_id=upload_id
        )

        logger.info(f"Executing query to insert UPDATED_JSON for UPLOAD_ID={upload_id}: {query}")
        
        sf_conn.cur.execute(query)
        sf_conn.conn.commit()
        logger.info(f"Inserted UPDATED_JSON for UPLOAD_ID={upload_id}")
    except Exception as e:
        logger.error(f"Failed to insert UPDATED_JSON for UPLOAD_ID={upload_id}: {e}")

def parse_contract_date(date_str):
    # Converts "01/09/2022" to "20220901"
    return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y%m%d")

def add_leakage_to_json(contract_json, sf_conn, database, schema, table, category, sql_template_path):
    start_date = parse_contract_date(contract_json["contract_start_date"])
    end_date = parse_contract_date(contract_json["contract_expiry_date"])
    total_spend = 0.0
    total_leakage = 0.0
    for sku in contract_json.get("skus", []):
        sku_id = sku["product_id"]
        contract_spend = sku["quantity_per_sku"] * sku["unit_price"]
        invoice_spend = fetch_invoice_spend(sf_conn, sku_id, start_date, end_date, database, schema, table, sql_template_path)
        leakage = invoice_spend - contract_spend
        sku["contract_spend"] = contract_spend
        sku["invoice_spend"] = invoice_spend
        sku["leakage"] = leakage
        total_spend += contract_spend
        total_leakage += leakage
    contract_json["total_spend"] = total_spend
    contract_json["total_leakage"] = total_leakage
    contract_json["category"] = category
    contract_json["leakage_percentage"] = '0'
    return contract_json

def update_leakage_in_json(conn_params, database, schema, upload_id, tenant_id, category, sql_template_path):
    try:
        sf_conn = SnowflakeConnection(conn_params)
        row = fetch_rows_for_entity_update(sf_conn, database, schema, "DOCUMENT_AI_EXTRACTED_DATA", upload_id, sql_template_path)
        entity_json = json.loads(row[0][1]) if row else {}
        updated_json = add_leakage_to_json(entity_json, sf_conn, database, schema, "VT_C_FACT_INVOICEPOSITION_MULTIPLIED", category, sql_template_path) # finding leakage

        # Update the Snowflake table with the new JSON
        update_entity_json(sf_conn, upload_id, updated_json, database, schema, "DOCUMENT_AI_EXTRACTED_DATA", sql_template_path)

        update_snowflake_contracts.delay(
            conn_params=conn_params,
            database=database,
            schema=schema,
            upload_id=upload_id,
            entity_json=updated_json,
            tenant_id=tenant_id,
            sql_template_path=sql_template_path
        )

        update_pg_status.delay(table='doc_ai_document', upload_id=upload_id, status="Update Leakage in Progress", schema=tenant_id)

        return {"status": "success", "message": f"Leakage updated for UPLOAD_ID={upload_id}"}
    except Exception as e:
        logger.error(f"Error updating leakage for UPLOAD_ID={upload_id}: {e}")
        update_pg_status.delay(table='doc_ai_document', upload_id=upload_id, status="ERROR", schema=tenant_id)
        return {"status": "error", "message": str(e)}
    finally:
        if sf_conn:
            sf_conn.close()