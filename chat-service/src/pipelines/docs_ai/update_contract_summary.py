import json
from jinja2 import Template
from datetime import datetime
from src.utils.logs import get_custom_logger
from src.providers.database.snowflake_driver import SnowflakeConnection
from src.celery_tasks.pg_status_task import update_pg_status

logger = get_custom_logger(__name__)

def get_benchmarks() -> dict:
    """
    Returns the hard-coded benchmark values.
    """
    return {
        'PAYMENT_TERMS_BENCHMARK': 45,
        'CONTRACT_DURATION_BENCHMARK': 24,
        'SUPPLIER_TERMINATION_CONVENIENCE_PERIOD_BENCHMARK': 30,
        'BUYER_TERMINATION_CONVENIENCE_PERIOD_BENCHMARK': 30,
        'BUYER_TERMINATION_CAUSE_PERIOD_BENCHMARK': 7
    }

def prepare_summary_record(entity: dict) -> dict:
    """
    Flattens the input JSON to a single dict of column -> value,
    and merges in the benchmark columns.
    """
    record = {
        'SUPPLIER':                                   entity.get('supplier'),
        'REGION':                                     entity.get('region'),
        'CONTRACT_DIGEST':                            json.dumps(entity.get('contract_digest', {})),
        'PAYMENT_TERMS':                              json.dumps(entity.get('payment_terms', {})),
        'SUPPLIER_TERMINATION_CONVENIENCE_PERIOD':    entity.get('supplier_termination_convenience_period'),
        'BUYER_TERMINATION_CONVENIENCE_PERIOD':       entity.get('buyer_termination_convenience_period'),
        'BUYER_TERMINATION_CAUSE_PERIOD':             entity.get('buyer_termination_cause_period'),
        'PRICES':                                     json.dumps(entity.get('prices', {})),
        'SKUS':                                       json.dumps(entity.get('skus', [])),
        'SPECIFIC_TERMS_AGREED':                      entity.get('specific_terms_agreed'),
        'INCOTERMS_SHIPPING':                         entity.get('incoterms_shipping'),
        'PAYMENT_INVOICING_TERMS':                    json.dumps(entity.get('payment_invoicing_terms', {})),
        'INSURANCE':                                  json.dumps(entity.get('insurance', {})),
        'JURISDICTION_COMPLIANCE':                    entity.get('jurisdiction_compliance'),
        'VENDOR_NAME_ADDRESS_REGION':                 json.dumps(entity.get('vendor_name_address_region', {})),
        'CONTRACT_TITLE':                             entity.get('contract_title'),
        'VOLUME_COMMITMENT':                          entity.get('volume_commitment'),
        'CONTRACT_START_DATE':                        entity.get('contract_start_date'),
        'CONTRACT_EXPIRY_DATE':                       entity.get('contract_expiry_date'),
        'CONTRACT_DURATION':                          entity.get('contract_duration'),
        'RENEWAL_CLAUSE_NOTICE_PERIOD':               json.dumps(entity.get('renewal_clause_and_notice_period', {})),
        'PERFORMANCE_PENALTIES':                      json.dumps(entity.get('performance_penalties', [])),
        'PRICING_VALUE_DRIVERS_COMM_SUSTAINABILITY':  json.dumps(entity.get('pricing_value_drivers_commercial_sustainability', [])),
        'PARTNERSHIP_CONTRACT_GOVERNANCE':            json.dumps(entity.get('partnership_contract_governance', [])),
        'TOTAL_SPEND':                                entity.get('total_spend', 0.0),
        'TOTAL_LEAKAGE':                              entity.get('total_leakage', 0.0),
        'CATEGORY':                                   entity.get('category'),
        'LEAKAGE_PERCENTAGE':                         entity.get('leakage_percentage', 0.0),
    }
    # merge in your hard‐coded benchmark columns
    record.update(get_benchmarks())
    return record

def upsert_contract_summary(sf_conn, upload_id, record, database, schema, table, sql_template_path):
    """
    MERGE the given record into the specified Snowflake table based on UPLOAD_ID,
    building a single SQL string with literals and executing it directly.
    """
    try:
        # inject UPLOAD_ID into the payload
        record['UPLOAD_ID'] = upload_id

        # columns whose values should be parsed as JSON OBJECT/ARRAY
        json_cols = {
            'CONTRACT_DIGEST','PAYMENT_TERMS','PRICES','SKUS',
            'PAYMENT_INVOICING_TERMS','INSURANCE',
            'VENDOR_NAME_ADDRESS_REGION','RENEWAL_CLAUSE_NOTICE_PERIOD',
            'PERFORMANCE_PENALTIES','PRICING_VALUE_DRIVERS_COMM_SUSTAINABILITY',
            'PARTNERSHIP_CONTRACT_GOVERNANCE'
        }
        # DATE columns (format DD/MM/YYYY)
        date_cols = {'CONTRACT_START_DATE','CONTRACT_EXPIRY_DATE'}

        # build the source SELECT clause with proper SQL literals
        source_lines = []
        for col, val in record.items():
            if val is None:
                literal = "NULL"
            elif col in json_cols:
                esc = str(val).replace("'", "''")
                literal = f"PARSE_JSON('{esc}')"

            elif col in date_cols:
                # convert DD/MM/YYYY → DATE
                literal = f"TO_DATE('{val}','DD/MM/YYYY')"
            elif isinstance(val, (int, float)):
                literal = str(val)
            else:
                # plain string → quoted
                esc = str(val).replace("'", "''")
                literal = f"'{esc}'"
            source_lines.append(f"{literal} AS {col}")
        source_clause = ",\n        ".join(source_lines)

        # build UPDATE SET and INSERT clauses
        update_set = ",\n        ".join(f"{col} = source.{col}"
                                         for col in record.keys() if col != 'UPLOAD_ID')
        insert_cols = ", ".join(record.keys())
        insert_vals = ", ".join(f"source.{col}" for col in record.keys())

        full_table = f'"{database}"."{schema}"."{table}"'
        with open(f"{sql_template_path}/upsert_contract_summary.sql", 'r') as file:
            template = Template(file.read())

        query = template.render(
            full_table=full_table,
            source_clause=source_clause,
            update_set=update_set,
            insert_cols=insert_cols,
            insert_vals=insert_vals
        )

        logger.debug(f"MERGE query for CONTRACT_SUMMARY:{query}")
        sf_conn.cur.execute(query)
        sf_conn.conn.commit()
        logger.info(f"Upserted CONTRACT_SUMMARY for UPLOAD_ID={upload_id}")

    except Exception as e:
        logger.error(f"Failed to upsert CONTRACT_SUMMARY for UPLOAD_ID={upload_id}: {e}", exc_info=True)
        raise
    
def update_contract_summary(conn_params, database, schema, upload_id, entity_json, tenant_id, sql_template_path):
    """
    Main entrypoint: prepares record, upserts into Snowflake, updates PG status.
    """
    try:
        sf_conn = SnowflakeConnection(conn_params)
        record = prepare_summary_record(entity_json)
        upsert_contract_summary(sf_conn, upload_id, record, database, schema, "CONTRACT_SUMMARY", sql_template_path)
        
        update_pg_status.delay(table='doc_ai_document', upload_id=upload_id, status="SUCCESS", schema=tenant_id)
        logger.info(f"Contract summary updated for {record['SUPPLIER']} / {record['REGION']}")
    except Exception as e:
        logger.error(f"Failed to update contract summary: {e}", exc_info=True)
        update_pg_status.delay(table='doc_ai_document', upload_id=upload_id, status="ERROR", schema=tenant_id)
        raise

def upsert_invoice_summary(sf_conn, upload_id, record, database, schema, table, sql_template_path):
    """
    MERGE the given record into the specified Snowflake table based on UPLOAD_ID,
    building a single SQL string with literals and executing it directly.
    """
    try:
        # inject UPLOAD_ID into the payload
        record['UPLOAD_ID'] = upload_id

        # build the source SELECT clause with proper SQL literals
        source_lines = []
        for col, val in record.items():
            if isinstance(val, (int, float)):
                literal = str(val)
            elif val is None:
                literal = "NULL"
            else:
                # plain string → quoted
                esc = str(val).replace("'", "''")
                literal = f"'{esc}'"
            source_lines.append(f"{literal} AS {col}")
        # join the source lines into a single clause
        # with proper indentation for readability
        source_clause = ",\n        ".join(source_lines)

        # build UPDATE SET and INSERT clauses
        update_set = ",\n        ".join(f"{col} = source.{col}"
                                         for col in record.keys() if col != 'UPLOAD_ID')
        # columns to insert
        # (all columns except UPLOAD_ID)
        # and the values to insert
        # (which are the same as the source columns)
        insert_cols = ", ".join(record.keys())
        insert_vals = ", ".join(f"source.{col}" for col in record.keys())

        full_table = f'"{database}"."{schema}"."{table}"'

        with open(f"{sql_template_path}/upsert_invoice_summary.sql", 'r') as file:
            template = Template(file.read())

        # render the final query with the template
        # and the prepared clauses
        query = template.render(
            full_table=full_table,
            source_clause=source_clause,
            update_set=update_set,
            insert_cols=insert_cols,
            insert_vals=insert_vals
        )

        logger.debug(f"MERGE query for Extracted_Invoice_Data:{query}")
        sf_conn.cur.execute(query)
        sf_conn.conn.commit()
        logger.info(f"Upserted Extracted_Invoice_Data for UPLOAD_ID={upload_id}")

    except Exception as e:
        logger.error(f"Failed to upsert Extracted_Invoice_Data for UPLOAD_ID={upload_id}: {e}", exc_info=True)
        raise

def update_extracted_invoice(conn_params, database, schema, upload_id, entity_json, tenant_id, sql_template_path):
    """
    Main entrypoint: prepares record, upserts into Snowflake, updates PG status.
    """
    try:
        sf_conn = SnowflakeConnection(conn_params)
        # record = prepare_invoice_record(entity_json)
        upsert_invoice_summary(sf_conn, upload_id, entity_json, database, schema, "EXTRACTED_INVOICE_DATA", sql_template_path)

        update_pg_status.delay(table='doc_ai_document', upload_id=upload_id, status="SUCCESS", schema=tenant_id)
        logger.info(f"Invoice summary updated for {entity_json['DIM_SUPPLIER']} / {entity_json['DIM_COUNTRY']}")
    except Exception as e:
        logger.error(f"Failed to update invoice summary: {e}", exc_info=True)
        update_pg_status.delay(table='doc_ai_document', upload_id=upload_id, status="ERROR", schema=tenant_id)
        raise