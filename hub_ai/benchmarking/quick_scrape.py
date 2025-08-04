import asyncio
import aiohttp
import pandas as pd
import ast
from datetime import datetime
import io
import boto3
from loguru import logger
import os
from openai import AsyncOpenAI
from benchmarking.data_extractor import fetch_snowflake_data, secrets_manager_client
import benchmarking.config as config
from benchmarking.benchmarking_job import run_benchmarking_job
from normalization.app import run_normalization_job
from benchmarking.pg_db_utils import PostgresConnector
import time

EXPORT_S3_BUCKET = os.getenv('EXPORT_S3_BUCKET')
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
website_config = ["www.rakuten.com", "www.alibaba.com", "www.amazon.jp", "www.amazon.ae"]

s3_client = boto3.client("s3")

async def generate_prompt(input_keyword, website_config):
    generic_prompt = f"""find all supplier selling {input_keyword} , it is a user input material description , fetch relavant products by cleaning it
CRITICAL: Return ONLY a valid Python list of dictionaries in this exact format, with no additional text, explanations, or markdown formatting, example output:
[{{"title": "HP Laptop 15t-fd000, 15.6", "price": "819.99","supplier":"supplier1","currency":"$"}}, {{"title": "HP Laptop 15t-fd000, 15.6", "price": "$699.99","supplier":"Supplier2","currency":"$"}}]

WEBSITE EXAMPLE TO SCRAPE FROM : {website_config}, these or any other which you feel.
Scrape maximum data from these websites. Move to every page up to 10 pages for every keyword.
Requirements:
- Include Title and Price & source supplier for each laptop
- Ensure Price includes the exact currency mentioned on the website
- No text before or after the list
- No ```python``` or ```json``` code blocks
- Just the raw list data
- [CRITICAL] if any value is not available, put NA for that value
- [CRITICAL] Structure is most important for me, as I want to convert this to Python dataframe
- [CRITICAL] Scrape all products available related to {input_keyword}, scrape till 10 pages on any website
- [CRITICAL] Give me latest data only
- [CRITICAL] "price" should contain numeric value only/or a price range e.g., "100.00" or "85.50" or "85-100". Currency column will have the currecny stored.
"""
    return generic_prompt

async def fetch_llm_response(session, query, website_config):
    try:
        prompt = await generate_prompt(query, website_config)
        # Assuming you have client already configured as AsyncOpenAI instance elsewhere
        response = await client.responses.create(
            model="gpt-4.1",
            tools=[{"type": "web_search_preview"}],
            input=prompt
        )
        return response.output_text
    except Exception as e:
        raise Exception(f"Error fetching response from OpenAI: {e}")

def fix_array(text):
    last_complete = text.rfind('"}')
    if last_complete != -1:
        return text[:last_complete + 2] + ']'
    return text

def clean_df(result_df):
    if result_df is None or result_df.empty:
        logger.warning("Result DataFrame is empty or None.")
        return None

    if "title" in result_df.columns and "price" in result_df.columns:
        result_df = result_df.dropna(subset=["title", "price"])
        result_df = result_df[result_df["title"].str.strip() != "NA"]
        result_df = result_df.drop_duplicates(subset=["title", "price"])
        return result_df
    else:
        logger.warning("Expected columns 'title', 'price' not found in the DataFrame.")
        return None

async def process_query(session, query, cluster_id, website_config, results):
    try:
        resp_text = await fetch_llm_response(session, query, website_config)
        fixed = fix_array(resp_text)
        data = ast.literal_eval(fixed)
        for row in data:
            row['query'] = query
            row['scraped_at'] = datetime.utcnow().isoformat()
            row['cluster_id'] = cluster_id
            results.append(row)
        logger.info(f"Successfully processed query: {query}")
    except Exception as e:
        logger.error(f"Error processing query {query}: {e}")

async def main_quick_scrape(event, secret_name, region_name):
    SF_CREDENTIAL_SECRET_ID = os.getenv('SNOWFLAKE_SECRET_NAME')
   
    results = []

    is_material = event.get("is_material", False)
    workspace_id = event.get("workspace_id")
    material_desc = event.get("material_description") if is_material else None
    benchmarking_row_id = event.get("row_id", None)

    pg = PostgresConnector(logger,workspace_id)
    pg.connect()

    try:
        table_name = '"benchmarking_findings"'
        where_clause = f"workspace_id = '{workspace_id}' and id = '{benchmarking_row_id}'"
        pg.mark_status(table_name,where_clause,status="Scrapping-In Progress")
    except Exception:
        pass

    if is_material and not material_desc:
        logger.error("'material_description' must be provided when 'is_material' is True. Exiting.")
        return

    if not is_material and not workspace_id:
        logger.error("'workspace_id' must be provided when 'is_material' is False. Exiting.")
        return

    config.SNOWFLAKE_SCHEMA_NAME = workspace_id
    logger.info(f"[ Using Snowflake schema: {config.SNOWFLAKE_SCHEMA_NAME} for quick scrapping")

    # if is_material and material_desc: 
        # try:
        #     logger.info(f"Starting normalization for material: '{material_desc}'")
        #     import time 
        #     # st_time = time.time()
        #     # run_normalization_job(
        #     #     workspace_id=workspace_id,
        #     #     folder_id=None,
        #     #     S3_INPUT_BUCKET=None,
        #     #     custom_name=f"material_normalisation_{material_desc}",
        #     #     secret_name=secret_name,
        #     #     region_name=region_name,
        #     #     material_description=material_desc,
        #     #     benchmarking_row_id=benchmarking_row_id
        #     # )
        #     # en_time = time.time() 
            
        #     # logger.info(f"Normalization job took {en_time - st_time} seconds for material")
        #     logger.info(f"Normalization job completed successfully for: '{material_desc}'")
        # except Exception as e:
        #     logger.error(f"Normalization job failed for '{material_desc}': {e}")
        #     raise
        # query_lst = [[material_desc, 'MATERIAL_CLUSTER']]
    # else:
    # df = fetch_snowflake_data(SF_CREDENTIAL_SECRET_ID, secrets_manager_client,
                            #    material_description=material_desc if is_material else None)
    # if df is None or df.empty:
    #     logger.error(f"[{workspace_id}] No queries fetched from Snowflake. Skipping.")
    #     return
    # if "B2B_QUERY" not in df.columns or "CLUSTER_ID" not in df.columns:
    #     logger.error(f"[{workspace_id}] Snowflake data missing required columns.")
    #     return
    # query_lst = list(df[['B2B_QUERY', 'CLUSTER_ID']].itertuples(index=False, name=None))
    st_time = time.time()
    query_lst = [[material_desc,0]]
    async with aiohttp.ClientSession() as session:
        tasks = [
            process_query(session, query, cluster_id, website_config, results)
            for query, cluster_id in query_lst
        ]
        await asyncio.gather(*tasks)

    df = pd.DataFrame(results)
    en_time = time.time()
    logger.info(f"Total time taken for scraping: {en_time - st_time} seconds")
    df = clean_df(df)

    if df is None or df.empty:
        logger.error("No valid data to save. Exiting.")
        return

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    website = 'quick_scrape_openai'
    file_name = f"{website}_{timestamp}.csv"
    s3_key = f"{workspace_id}/{timestamp}/{file_name}"
    full_s3_uri = f"s3://{EXPORT_S3_BUCKET}/{s3_key}"

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    s3_client.put_object(Bucket=EXPORT_S3_BUCKET, Key=s3_key, Body=csv_buffer.read())
    logger.success(f"[{website}] for workspace_id:{workspace_id} Uploaded to {full_s3_uri}")
    try:
        table_name = '"benchmarking_findings"'
        pg.mark_status(table_name,where_clause,status="Scrapping-Completed")
    except Exception:
        pass
    # Benchmarking job call
    st_time_bench = time.time()
    run_benchmarking_job(
        workspace_id=workspace_id,
        s3_path=full_s3_uri,
        url=workspace_id,
        secret_name=secret_name,
        region_name=region_name,
        benchmarking_row_id=benchmarking_row_id
    )
    en_time_bench = time.time()
    logger.info(f"Total time taken for benchmarking: {en_time - st_time} seconds")