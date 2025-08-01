import os
import logging
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
from snowflake.connector import connect
from omegaconf import DictConfig

def get_snowflake_connection(sf_config: DictConfig, logger: logging.Logger):
    """Establishes and returns a connection to Snowflake."""
    try:
        logger.info(f"connecting to Snowflake database: {sf_config.database_env_var}")
        logger.info(f"connecting to Snowflake account: {sf_config.account_env_var}")

        conn = connect(
            user=sf_config.user_env_var,
            password=sf_config.password_env_var,
            account=sf_config.account_env_var,
            warehouse=sf_config.warehouse_env_var,
            database=sf_config.database_env_var,
            role=sf_config.role_env_var,
        )
        logger.info("Snowflake connection successful.")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to Snowflake: {e}", exc_info=True)
        raise

def upload_df_to_snowflake(df: pd.DataFrame, table_name: str, snowflake_config: DictConfig, workspace_id: str, logger: logging.Logger):
    """
    Uploads a Pandas DataFrame to a specified Snowflake table.
    If the table exists and columns match, append. If columns differ, overwrite the table.
    """
    schema = workspace_id
    table_name_upper = table_name.upper()  # Ensure table name is uppercase

    # Sanitize column names for Snowflake (remove special characters, spaces, etc.)
    sanitized_columns = {col: col.replace(' ', '_').replace('.', '').replace('(', '').replace(')', '').upper() for col in df.columns}
    df.rename(columns=sanitized_columns, inplace=True)

    try:
        with get_snowflake_connection(snowflake_config, logger) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"USE DATABASE {snowflake_config.database_env_var}")
                # Check if schema exists, create if it doesn't
                cursor.execute(f"SHOW SCHEMAS LIKE '{schema}'")
                existing_schemas = cursor.fetchall()
                if not existing_schemas:
                    logger.info(f"Schema '{schema}' does not exist. Creating it...")
                    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS \"{schema}\"")
                    logger.info(f"Schema '{schema}' created successfully.")
                else:
                    logger.info(f"Schema '{schema}' already exists.")
                cursor.execute(f'USE SCHEMA "{schema}"')

                logger.info(f"Preparing to write to Snowflake table: {schema}.{table_name_upper}")
                logger.info(f"DataFrame shape: {df.shape}, columns: {list(df.columns)}")

                # Check if table exists before writing
                cursor.execute(f"SHOW TABLES LIKE '{table_name_upper}' IN SCHEMA \"{schema}\"")
                existing_tables = cursor.fetchall()
                append_mode = False
                if existing_tables:
                    logger.info(f"Table {schema}.{table_name_upper} already exists - checking columns for append/overwrite logic")
                    # Get existing table columns
                    cursor.execute(f'DESC TABLE "{schema}"."{table_name_upper}"')
                    table_columns = [row[0].upper() for row in cursor.fetchall()]
                    df_columns = [col.upper() for col in df.columns]
                    if table_columns == df_columns:
                        logger.info(f"Table columns match DataFrame columns. Will append data.")
                        append_mode = True
                    else:
                        logger.warning(f"Table columns {table_columns} do not match DataFrame columns {df_columns}. Will overwrite table.")
                else:
                    logger.info(f"Table {schema}.{table_name_upper} will be created")

                # Write to Snowflake: append if columns match, else overwrite
                success, nchunks, nrows, _ = write_pandas(
                    conn=conn,
                    df=df,
                    table_name=table_name_upper,
                    schema=schema,
                    auto_create_table=True,
                    overwrite=not append_mode
                )

                if success:
                    logger.info(f"Successfully {'appended' if append_mode else 'overwritten'} {nrows} rows in {nchunks} chunks to table '{table_name_upper}'.")
                    cursor.execute(f"SELECT COUNT(*) FROM \"{schema}\".\"{table_name_upper}\"")
                    row_count = cursor.fetchone()[0]
                    logger.info(f"Verified table {schema}.{table_name_upper} now has {row_count} total rows")
                    cursor.execute(f"SHOW TABLES IN SCHEMA \"{schema}\"")
                    all_tables = cursor.fetchall()
                    logger.info(f"All tables in schema {schema}: {[table[1] for table in all_tables]}")
                    logger.info(f"To verify the table, run this query in Snowflake:")
                    logger.info(f"SELECT * FROM \"{schema}\".\"{table_name_upper}\";")
                else:
                    logger.error(f"Failed to write data to Snowflake table '{table_name_upper}'.")
                    raise RuntimeError("Snowflake write_pandas operation failed.")
    except Exception as e:
        logger.error(f"An error occurred during Snowflake upload: {e}", exc_info=True)
        raise

def read_df_from_snowflake(table_name: str, snowflake_config: DictConfig, workspace_id: str, logger: logging.Logger) -> pd.DataFrame:
    """
    Reads a table from Snowflake into a Pandas DataFrame.
    Args:
        table_name: Name of the table to read.
        snowflake_config: Snowflake config (DictConfig)
        workspace_id: Used as schema
        logger: Logger
    Returns:
        pd.DataFrame
    """
    schema = workspace_id
    try:
        with get_snowflake_connection(snowflake_config, logger) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"USE DATABASE {snowflake_config.database_env_var}")
                cursor.execute(f'USE SCHEMA "{schema}"')
                sql = f'SELECT * FROM "{schema}"."{table_name}"'
                logger.info(f"Executing query: {sql}")
                cursor.execute(sql)
                df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])
                logger.info(f"Fetched {len(df)} rows from {schema}.{table_name}")
                return df
    except Exception as e:
        logger.error(f"Error reading table {schema}.{table_name} from Snowflake: {e}", exc_info=True)
        raise

def test_snowflake_connection_and_permissions(snowflake_config: DictConfig, workspace_id: str, logger: logging.Logger):
    """
    Test function to verify Snowflake connection, schema, and table permissions.
    """
    schema = workspace_id
    try:
        with get_snowflake_connection(snowflake_config, logger) as conn:
            with conn.cursor() as cursor:
                # Test 1: Check current user and role
                cursor.execute("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_DATABASE()")
                user_info = cursor.fetchone()
                logger.info(f"Current user: {user_info[0]}, Role: {user_info[1]}, Database: {user_info[2]}")
                
                # Test 2: Check if schema exists
                cursor.execute(f"SHOW SCHEMAS LIKE '{schema}'")
                schemas = cursor.fetchall()
                if schemas:
                    logger.info(f"Schema '{schema}' exists")
                else:
                    logger.warning(f"Schema '{schema}' does not exist")
                
                # Test 3: Try to use the schema
                try:
                    cursor.execute(f'USE SCHEMA "{schema}"')
                    logger.info(f"Successfully switched to schema '{schema}'")
                except Exception as e:
                    logger.error(f"Cannot use schema '{schema}': {e}")
                    return False
                
                # Test 4: List tables in schema
                cursor.execute(f"SHOW TABLES IN SCHEMA \"{schema}\"")
                tables = cursor.fetchall()
                logger.info(f"Tables in schema '{schema}': {[table[1] for table in tables]}")
                
                # Test 5: Check specific table
                cursor.execute(f"SHOW TABLES LIKE 'BENCHMARK_RESULTS' IN SCHEMA \"{schema}\"")
                benchmark_tables = cursor.fetchall()
                if benchmark_tables:
                    logger.info(f"BENCHMARK_RESULTS table exists")
                    # Test 6: Try to query the table
                    cursor.execute(f'SELECT COUNT(*) FROM "{schema}"."BENCHMARK_RESULTS"')
                    count = cursor.fetchone()[0]
                    logger.info(f"BENCHMARK_RESULTS table has {count} rows")
                else:
                    logger.warning(f"BENCHMARK_RESULTS table does not exist")
                
                return True
                
    except Exception as e:
        logger.error(f"Snowflake connection/permission test failed: {e}")
        return False