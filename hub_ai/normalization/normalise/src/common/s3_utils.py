import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError
import logging
import re
import pandas as pd

def get_s3_client(logger: logging.Logger):
    """Initializes and returns an S3 client using credentials from environment variables."""
    try:
        client = boto3.client('s3')
        return client
    except Exception as e:
        logger.error(f"Failed to create S3 client: {e}")
        raise

def parse_s3_uri(s3_uri: str):
    match = re.match(r's3://([^/]+)/(.+)', s3_uri)
    if not match:
        raise ValueError(f"Invalid S3 URI: {s3_uri}")
    bucket, key = match.group(1), match.group(2)
    return bucket, key

def check_and_download_file(bucket_name: str, key: str, local_dir: str, logger: logging.Logger) -> tuple:
    """
    Legacy function for /normalize and other code: download a file from S3 using bucket and key.
    """
    logger.info(f"[DEBUG] check_and_download_file called with bucket={bucket_name}, key={key}")
    s3_client = get_s3_client(logger)
    logger.info(f"[S3_UTILS] Using S3 bucket: {bucket_name} for key: {key}")
    key = key.strip()
    # Check if file exists
    try:
        s3_client.head_object(Bucket=bucket_name, Key=key)
    except ClientError as e:
        code = e.response['Error']['Code']
        if code in ('404', '400', 'NoSuchKey', '403'):
            logger.error(f"File not found in S3 at '{bucket_name}/{key}' (head_object {code})")
            raise FileNotFoundError(f"File not found in S3 at '{bucket_name}/{key}' (head_object {code})")
        else:
            logger.error(f"An S3 client error occurred: {e}")
            raise
    local_file_path = os.path.join(local_dir, os.path.basename(key))
    logger.info(f"Downloading S3 file '{key}' to '{local_file_path}' from bucket '{bucket_name}'...")
    s3_client.download_file(bucket_name, key, local_file_path)
    
    file_ext = os.path.splitext(local_file_path)[-1].lower()
    if file_ext == ".csv":
        df = pd.read_csv(local_file_path, encoding='utf-8')
        row_count = len(df)
    elif file_ext in [".xlsx", ".xls"]:
        df = pd.read_excel(local_file_path)
        row_count = len(df)
    else:
        row_count = None  # Or handle other formats as needed

    return local_file_path, row_count

def check_and_download_file_from_uri(s3_uri: str, local_dir: str, logger: logging.Logger) -> str:
    """
    Download a file from S3 using a full S3 URI (s3://bucket/key). No legacy function call.
    """
    match = re.match(r's3://([^/]+)/(.+)', s3_uri)
    if not match:
        raise ValueError(f"Invalid S3 URI: {s3_uri}")
    bucket_name, key = match.group(1), match.group(2)
    logger.info(f"[DEBUG] Parsed S3 URI: bucket={bucket_name}, key={key}")
    s3_client = get_s3_client(logger)
    logger.info(f"[S3_UTILS] Using S3 bucket: {bucket_name} for key: {key}")
    key = key.strip()
    # Check if file exists
    try:
        s3_client.head_object(Bucket=bucket_name, Key=key)
    except ClientError as e:
        code = e.response['Error']['Code']
        if code in ('404', '400', 'NoSuchKey', '403'):
            logger.error(f"File not found in S3 at '{bucket_name}/{key}' (head_object {code})")
            raise FileNotFoundError(f"File not found in S3 at '{bucket_name}/{key}' (head_object {code})")
        else:
            logger.error(f"An S3 client error occurred: {e}")
            raise
    local_file_path = os.path.join(local_dir, os.path.basename(key))
    logger.info(f"Downloading S3 file '{key}' to '{local_file_path}' from bucket '{bucket_name}'...")
    s3_client.download_file(bucket_name, key, local_file_path)
    return local_file_path