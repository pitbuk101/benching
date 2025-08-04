import os
import logging
import pandas as pd
import boto3
import json
from snowflake.snowpark import Session
from snowflake.snowpark.exceptions import SnowparkSQLException

def get_snowflake_credentials_from_aws(region_name: str, logger: logging.Logger):
    """
    Fetch Snowflake credentials from AWS Secrets Manager.
    Args:
        region_name: AWS region where the secret is stored.
        logger: Logger instance.
    Returns:
        A dictionary containing Snowflake credentials.
    """
    try:
        # Fetch the secret name from the environment variable
        secret_name = os.getenv("SNOWFLAKE_SECRET_NAME")
        if not secret_name:
            raise ValueError("Environment variable 'SNOWFLAKE_SECRET_NAME' is not set.")

        logger.info(f"Fetching Snowflake credentials from AWS Secrets Manager: {secret_name}")
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=region_name)
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response['SecretString'])
        logger.info("Successfully fetched Snowflake credentials from AWS Secrets Manager.")
        return secret
    except Exception as e:
        logger.error(f"Failed to fetch Snowflake credentials from AWS Secrets Manager: {e}", exc_info=True)
        raise

def get_snowflake_session(logger: logging.Logger, region_name: str):
    """
    Establishes and returns a Snowflake session using credentials from AWS Secrets Manager.
    Args:
        logger: Logger instance.
        region_name: AWS region where the secret is stored.
    Returns:
        Snowflake session object.
    """
    try:
        # Fetch credentials from AWS Secrets Manager
        creds = get_snowflake_credentials_from_aws(region_name, logger)
        connection_parameters = {
            "account": creds['EU_SF_ACCOUNT'],
            "user": creds['EU_SF_USERNAME'],
            "password": creds['EU_SF_PASSWORD'],
            "role": creds['EU_SF_ROLE'],
            "warehouse": creds['EU_SF_WAREHOUSE'],
            "database": creds['EU_SF_DATABASE_IDP'],
            "schema": creds.get('EU_SF_SCHEMA', 'PUBLIC')
        }
        session = Session.builder.configs(connection_parameters).create()
        logger.info("Snowflake Snowpark session created successfully.")
        return session
    except Exception as e:
        logger.error(f"Failed to create Snowflake session: {e}", exc_info=True)
        raise

def ensure_schema(session, schema, logger):
    """
    Ensure that the specified schema exists in Snowflake, creating it if necessary.
    """
    try:
        session.sql(f'CREATE SCHEMA IF NOT EXISTS "{schema}"').collect()
        logger.info(f"Schema '{schema}' is ready.")
    except Exception as e:
        logger.error(f"Failed to ensure schema '{schema}': {e}", exc_info=True)
        raise

def upload_df_to_snowflake(df: pd.DataFrame, table_name: str, workspace_id: str, logger: logging.Logger, region_name: str):

    table_name_upper = table_name.upper()
    schema = workspace_id
    # Sanitize column names
    df.columns = [col.replace(' ', '_').replace('.', '').replace('(', '').replace(')', '').upper() for col in df.columns]
    try:
        session = get_snowflake_session(logger, region_name)
        ensure_schema(session, schema, logger)
        session.use_schema(f'"{schema}"')
        # Check if table exists
        tables = session.sql(f'SHOW TABLES LIKE \'{table_name_upper}\' IN SCHEMA "{schema}"').collect()
        if tables:
            try:
                logger.info(f"Trying to append to existing table {schema}.{table_name_upper}")
                session.write_pandas(df, table_name_upper, schema=schema, overwrite=False)
            except Exception as e:
                logger.warning(f"Append failed, overwriting table {schema}.{table_name_upper}: {e}")
                session.write_pandas(df, table_name_upper, schema=schema, overwrite=True)
        else:
            logger.info(f"Creating and writing to new table {schema}.{table_name_upper}")
            session.write_pandas(df, table_name_upper, schema=schema, overwrite=True)
        logger.info(f"Upload to Snowflake table {schema}.{table_name_upper} complete.")
    except Exception as e:
        logger.error(f"Error uploading DataFrame to Snowflake: {e}", exc_info=True)
        raise

def read_df_from_snowflake(table_name: str, workspace_id: str, logger: logging.Logger, region_name: str) -> pd.DataFrame:
    """
    Reads a table from Snowflake into a Pandas DataFrame using Snowpark.
    """
    schema = workspace_id
    table_name_upper = table_name.upper()
    try:
        session = get_snowflake_session(logger, region_name)
        session.use_schema(f'"{schema}"')
        df = session.table(table_name_upper).to_pandas()
        logger.info(f"Fetched {len(df)} rows from {schema}.{table_name_upper}")
        return df
    except Exception as e:
        logger.error(f"Error reading table {schema}.{table_name_upper} from Snowflake: {e}", exc_info=True)
        raise

def test_snowflake_connection_and_permissions(workspace_id: str, logger: logging.Logger, region_name: str):
    """
    Test function to verify Snowflake connection, schema, and table permissions using Snowpark.
    """
    schema = workspace_id
    try:
        session = get_snowflake_session(logger, region_name)
        session.use_schema(f'"{schema}"')
        user_info = session.sql("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_DATABASE()").collect()[0]
        logger.info(f"Current user: {user_info[0]}, Role: {user_info[1]}, Database: {user_info[2]}")
        schemas = session.sql(f"SHOW SCHEMAS LIKE '{schema}'").collect()
        if schemas:
            logger.info(f"Schema '{schema}' exists")
        else:
            logger.warning(f"Schema '{schema}' does not exist")
        tables = session.sql(f"SHOW TABLES IN SCHEMA {schema}").collect()
        logger.info(f"Tables in schema '{schema}': {[table['name'] for table in tables]}")
        benchmark_tables = session.sql(f"SHOW TABLES LIKE 'BENCHMARK_RESULTS' IN SCHEMA {schema}").collect()
        if benchmark_tables:
            logger.info(f"BENCHMARK_RESULTS table exists")
            count = session.table("BENCHMARK_RESULTS").count()
            logger.info(f"BENCHMARK_RESULTS table has {count} rows")
        else:
            logger.warning(f"BENCHMARK_RESULTS table does not exist")
        return True
    except Exception as e:
        logger.error(f"Snowflake connection/permission test failed: {e}")
        return False