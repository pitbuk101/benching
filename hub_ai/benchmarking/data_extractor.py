import os
import asyncio
import pandas as pd
from datetime import datetime
from multiprocessing import Process, Manager, current_process
from concurrent.futures import ThreadPoolExecutor
import time
import re
from loguru import logger
from typing import Optional, Dict, Any, List, Tuple
import snowflake.connector
import json
import boto3
from botocore.exceptions import ClientError

# Import config module to access schema and table names
import benchmarking.config as config

AWS_REGION = os.getenv('AWS_REGION','us-east-1')  # Default to us-east-1 if not set

# Initialize secrets_manager_client once for efficiency.
try:
    secrets_manager_client = boto3.client('secretsmanager', region_name=AWS_REGION)
    logger.info(f"Successfully built secrets_manager_client object for region: {AWS_REGION}")
except Exception as e:
    logger.error(f"Error building secrets_manager_client object: {e}")
    logger.error("Please ensure your AWS credentials and region are configured correctly.")
    raise

def get_secret(secret_name: str, secrets_manager_client: boto3.client) -> dict:
    """
    Fetches secret credentials from AWS Secrets Manager.

    Args:
        secret_name (str): The name or ARN of the secret to retrieve.
        secrets_manager_client (boto3.client): An initialized boto3 Secrets Manager client.

    Returns:
        dict: The parsed secret string as a dictionary.

    Raises:
        ClientError: If there's an issue fetching the secret from AWS Secrets Manager.
    """
    try:
        response = secrets_manager_client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        if error_code == 'ResourceNotFoundException':
            logger.error(f"Secret '{secret_name}' not found in Secrets Manager in region {AWS_REGION}. Error: {e}")
        elif error_code == 'AccessDeniedException':
            logger.error(f"Permission denied to fetch secret '{secret_name}'. Check IAM role permissions for ARN: {os.environ.get('AWS_ROLE_ARN', 'N/A')}. Error: {e}")
        else:
            logger.error(f"Generic ClientError fetching secret '{secret_name}': {e}")
        raise # Re-raise the exception after logging

def fetch_snowflake_data(
    secret_name: str,
    secrets_manager_client: boto3.client,
    material_description: Optional[str] = None
) -> Optional[pd.DataFrame]:
    conn = None
    try:
        # Fetch the creds dictionary from AWS Secrets Manager
        snowflake_creds = get_secret(secret_name, secrets_manager_client)
        logger.info(f"Successfully fetched Snowflake credentials for secret: {secret_name}.")
        conn = snowflake.connector.connect(
            user=snowflake_creds["EU_SF_USERNAME"],
            password=snowflake_creds["EU_SF_PASSWORD"],
            account=snowflake_creds["EU_SF_ACCOUNT"],
            warehouse=snowflake_creds["EU_SF_WAREHOUSE"],
            database=snowflake_creds["EU_SF_DATABASE_IDP"],
            role=snowflake_creds["EU_SF_ROLE"]
        )
        logger.info("Successfully connected to Snowflake!")

        # Use config values for schema and table
        schema_name = getattr(config, 'SNOWFLAKE_SCHEMA_NAME')
        table_name = getattr(config, 'SNOWFLAKE_TABLE_NAME', 'NORMALISED_DATA')

        snowflake_query_details = {
            "query": "B2B_QUERY",
            "cluster_id": "CLUSTER_ID",
            "description": "ITEM_DESCRIPTION"
        }

        # If material description is provided, filter by it
        if material_description:
            logger.info(f"Fetching B2B query for normalized material_description: {material_description}")
            query = f"""
                WITH DistinctQueries AS (
                    SELECT DISTINCT
                        "{snowflake_query_details['query']}",
                        "{snowflake_query_details['cluster_id']}"
                    FROM "{conn.database}"."{schema_name}"."{table_name}"
                    WHERE "{snowflake_query_details['description']}" = %s
                )
                SELECT *
                FROM DistinctQueries
            """
            logger.info(f"Executing Snowflake query:\n{query}")
            cur = conn.cursor()
            cur.execute(query, (material_description,))
        else:
            logger.info("Fetching distinct cluster-level B2B query (default mode)")
            query = f"""
                WITH DistinctCluster AS (
                    SELECT
                        "{snowflake_query_details['cluster_id']}",
                        "{snowflake_query_details['query']}",
                        ROW_NUMBER() OVER (
                            PARTITION BY "{snowflake_query_details['cluster_id']}"
                            ORDER BY "{snowflake_query_details['query']}"
                        ) AS rn
                    FROM "{conn.database}"."{schema_name}"."{table_name}"
                )
                SELECT
                    "{snowflake_query_details['query']}",
                    "{snowflake_query_details['cluster_id']}",
                FROM DistinctCluster
                WHERE rn = 1
            """
            logger.info(f"Executing Snowflake query:\n{query}")
            cur = conn.cursor()
            cur.execute(query)

        df = cur.fetch_pandas_all()
        logger.info("Successfully fetched data from Snowflake.")
        return df

    except ClientError as e:
        logger.error(f"Failed to retrieve secret '{secret_name}'. ClientError: {e}")
        return None
    except snowflake.connector.errors.ProgrammingError as e:
        logger.error(f"Snowflake connection or query error: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None
    finally:
        if conn:
            conn.close()
            logger.info("Disconnected from Snowflake.")

if __name__ == "__main__":
    SNOWFLAKE_SECRET_NAME = os.getenv('SNOWFLAKE_SECRET_NAME')
    logger.info(f"Running {__file__} directly.")
    # Pass the globally initialized secrets_manager_client
    data = fetch_snowflake_data(SNOWFLAKE_SECRET_NAME, secrets_manager_client)
    if data is not None:
        logger.info(f"Fetched data head:\n{data.head()}")
    else:
        logger.error("No data fetched from Snowflake.")