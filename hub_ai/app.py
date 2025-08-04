from fastapi import FastAPI, Request, HTTPException
from benchmarking.web_scrapper import main as web_scrapper_main
from benchmarking.quick_scrape import main_quick_scrape
from benchmarking.benchmarking_job import run_benchmarking_job
from normalization.app import run_normalization_job
from loguru import logger
import boto3
import json
import os
import sys
import asyncio



AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Secrets Manager client
secrets_manager_client = boto3.client('secretsmanager', region_name=AWS_REGION)



def parse_s3_path(s3_path: str):
    if s3_path and s3_path.startswith("s3://"):
        path_parts = s3_path[5:].split('/', 1)
        bucket = path_parts[0]
        key = path_parts[1] if len(path_parts) > 1 else ""
        return bucket, key
    else:
        logger.error("Invalid or missing S3path in event.")
        return None, None

def handle_normalization(event: dict):
    logger.info("Received normalization request, triggering normalization process")
    s3_bucket, s3_key = parse_s3_path(event["S3path"])
    run_normalization_job(
        workspace_id=event.get("workspace_id"),
        folder_id=s3_key,
        S3_INPUT_BUCKET=s3_bucket,
        custom_name=event.get("custom_name"),
        secret_name=secret_name,
        region_name=AWS_REGION
    )

def main(event):
    s3_path = event.get("S3path")
    smart_grab = event.get("smart_grab", False)
    is_normalisation = event.get("is_normalisation", False)

    SF_CREDENTIAL_SECRET_ID = os.getenv('SNOWFLAKE_SECRET_NAME')

    # Trigger normalization if conditions match
    if is_normalisation and s3_path is not None and smart_grab is False:
        logger.info("Received normalization request, triggering normalization process")
        handle_normalization(event)
        return

    # Trigger data enrichment if smart_grab is False and not normalization
    if smart_grab is False and is_normalisation is False:
        logger.info("Received data enrichment request, triggering data enrichment and benchmarking process")
        web_scrapper_main(event, secret_name=secret_name, region_name=AWS_REGION)
        return

    # Trigger quick scrape if smart_grab is True and not normalization
    if smart_grab is True and is_normalisation is False:
        logger.info("Received quick scrape request, triggering quick scrape process")
        asyncio.run(main_quick_scrape(event, secret_name=secret_name, region_name=AWS_REGION))
        return




if __name__ == "__main__":
    secret_name = os.getenv("SNOWFLAKE_SECRET_NAME")
    region_name = os.getenv("AWS_REGION", "us-east-1") 
    raw_event = os.getenv("EVENT_PAYLOAD")
    if not raw_event:
        logger.error(" Application will run once new event is received. Exiting. {raw_event}")
    else:
        try:
            event = json.loads(raw_event)
            logger.info(f"DEBUG: type(event) = {type(event)}")
            logger.info(f"DEBUG: event = {event}")
            # event = #event_wrapper.get("detail", {})
            main(event)
            logger.info("Event processing completed successfully")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid EVENT_PAYLOAD JSON. Error: {e}")
            logger.error(f"Raw payload: {raw_event}")
        except Exception as e:
            logger.error(f"Error processing event: {e}")
            exit(1)
    
    logger.info("Container execution completed")  
        
