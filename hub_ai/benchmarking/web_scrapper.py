import os
import json
import asyncio
from urllib.parse import quote_plus, urljoin,urlparse
from multiprocessing import current_process, Process, Manager
from pathlib import Path
from typing import List, Dict, Tuple, Any, Optional
from concurrent.futures import ThreadPoolExecutor
from benchmarking.data_extractor import fetch_snowflake_data, secrets_manager_client
import pandas as pd
from loguru import logger
from datetime import datetime
from normalization.app import run_normalization_job
import benchmarking.config as config
from crawl4ai import (
    AsyncWebCrawler, CrawlerRunConfig, JsonCssExtractionStrategy, CrawlResult
)
import boto3
import io
from io import StringIO
import aiohttp
from bs4 import BeautifulSoup
import re
import requests
from benchmarking.quick_scrape import main_quick_scrape
from benchmarking.benchmarking_job import run_benchmarking_job
from benchmarking.pg_db_utils import PostgresConnector
from benchmarking.amazon_crawler import ComprehensiveScraper,comprehensive_product_analysis


# Constants for multiprocessing and threading
MAX_CONCURRENT_TASKS = 2        
MAX_THREADS_PER_NODE = 2
QUERIES_PER_NODE = 5           

EXPORT_S3_BUCKET = os.getenv('EXPORT_S3_BUCKET', 'sai-genai-data-export')

def convert_schema_for_crawl4ai(fields_raw: List[dict], base_selector: str) -> dict:
    """
    Convert raw schema fields into the format expected by crawl4ai
    Dynamically uses the base selector from the website config.
    """
    return {
        "baseSelector": base_selector,
        "fields": fields_raw
    }


def detect_currency(price_str: str) -> Optional[str]:
    """
    Detects currency code from a price string using CURRENCY_SYMBOLS_MAP keys.
    """
    if not price_str:
        return None
    price_str = price_str.strip()
    for symbol, code in config.CURRENCY_SYMBOLS_MAP.items():
        # Use regex to detect symbol as standalone or prefix
        pattern = re.escape(symbol)
        if re.search(pattern, price_str):
            return code
    return None


def normalize_url(url: Optional[str], base_url: str) -> Optional[str]:
    """
    Normalize URL, converting relative URLs to absolute URLs based on base_url.
    """
    if not url:
        return None
    if url.startswith("http"):
        return url
    # Use urljoin for robustness
    return urljoin(base_url, url)


async def get_available_pages(session: aiohttp.ClientSession, url: str, pagination_selector: str) -> int:
    """
    Detects how many pages are available from the first page.
    Caps the value at 25.
    """
    try:
        async with session.get(url) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            pagination_elements = soup.select(pagination_selector)
            if pagination_elements:
                page_numbers = []
                for elem in pagination_elements:
                    text = elem.get_text(strip=True)
                    page_numbers += [int(n) for n in re.findall(r"\d+", text)]
                max_page = max(page_numbers) if page_numbers else 1
                return min(max_page, 10)
            return 1
    except Exception as e:
        logger.warning(f"Pagination detection failed at {url}: {e}")
        return 1


async def scrape_query(keyword: str, cluster_id: str, website_name: str,
                       shared_html_debug: Dict[str, str], max_pages: int = 50) -> List[Dict[str, Any]]:
    node_name = current_process().name
    website_config = config.website_configs.get(website_name)
    if not website_config:
        logger.error(f"[{node_name} | {cluster_id} | {keyword} | {website_name}] No config found.")
        return []

    encoded = quote_plus(keyword)
    base_url_template = website_config["base_url_template"]
    base_selector = website_config["extraction_css_selector"]
    schema_fields = website_config["product_schema"]
    selectors_strategy = website_config.get("selectors_strategy", "first")
    pagination_selector = website_config.get("pagination_selector", "")

    # Safety check to ensure page_num is in the template
    if "{page_num}" not in base_url_template:
        logger.error(f"[{node_name}] base_url_template for {website_name} must include '{{page_num}}' placeholder.")
        return []

    schema_for_crawl = convert_schema_for_crawl4ai(schema_fields, base_selector)
    extraction_strategy = JsonCssExtractionStrategy(schema_for_crawl)
    crawl_config = CrawlerRunConfig(extraction_strategy=extraction_strategy)

    all_items: List[Dict[str, Any]] = []
    visited_urls = set()

    try:
        async with AsyncWebCrawler() as crawler:
            async with aiohttp.ClientSession() as session:
                # Detect how many pages are available
                first_page_url = base_url_template.format(encoded_keyword=encoded, page_num=1)
                actual_pages = await get_available_pages(session, first_page_url, pagination_selector) if pagination_selector else min(max_pages, 25)
                actual_pages = min(actual_pages, 10)

                logger.info(f"[{node_name} | {cluster_id}] Scraping {actual_pages} pages for '{keyword}'")

                for page_num in range(1, actual_pages + 1):
                    try:
                        start_url = base_url_template.format(encoded_keyword=encoded, page_num=page_num)

                        if start_url in visited_urls:
                            logger.warning(f"[{node_name}] Duplicate URL detected for {keyword}: {start_url}. Skipping.")
                            continue
                        visited_urls.add(start_url)

                        logger.debug(f"[Page {page_num}] URL: {start_url}")

                        # Fetch raw HTML for debug
                        async with session.get(start_url) as resp:
                            raw_bytes = await resp.read()
                            try:
                                raw_html = raw_bytes.decode("utf-8")
                            except UnicodeDecodeError:
                                try:
                                    raw_html = raw_bytes.decode("shift_jis")
                                except UnicodeDecodeError as e:
                                    logger.error(f"[{node_name}] Failed to decode response from {start_url}: {e}")
                                    continue
                            shared_html_debug[f"{cluster_id}_{keyword}_{page_num}"] = raw_html[:1000]
                            logger.debug(f"[{node_name}] Raw HTML snippet (first 1000 chars):\n{raw_html[:1000]}")

                            # Check for "no products found" signal
                            soup = BeautifulSoup(raw_html, "html.parser")
                            base_elements = soup.select(base_selector)
                            logger.debug(f"[{node_name}] Page {page_num}: Found {len(base_elements)} elements with base selector.")

                            if len(base_elements) == 0:
                                logger.warning(f"[{node_name}] No products found on page {page_num}, skipping remaining pages.")
                                break  # Stop processing this query if no products are found

                            # Field debug info
                            for field in schema_fields:
                                name = field.get("name")
                                selector = field.get("selector")
                                total_matches = sum(len(elem.select(selector)) for elem in base_elements)
                                logger.debug(f"[{node_name}] Field '{name}' selector '{selector}' matched {total_matches} elements")

                        # Run actual crawler
                        result_list: List[CrawlResult] = await crawler.arun(
                            url=start_url,
                            config=crawl_config,
                            extraction_css_selector=base_selector,
                            selectors_strategy=selectors_strategy,
                        )

                        for cr in result_list:
                            if cr.success and getattr(cr, "extracted_content", None):
                                try:
                                    items = json.loads(cr.extracted_content)
                                    logger.debug(f"[{node_name}] Page {page_num}: Extracted {len(items)} items.")
                                except json.JSONDecodeError:
                                    logger.warning(f"[{node_name}] Page {page_num}: JSON decode failed.")
                                    continue

                                for it in items:
                                    raw_price = it.get("price", "")
                                    currency = detect_currency(str(raw_price))

                                    img = it.get("image_url") or it.get("image")
                                    it["image_url"] = normalize_url(img, start_url) if img else None

                                    url = it.get("url")
                                    it["url"] = normalize_url(url, start_url) if url else None

                                    it.update({
                                        "Source_URL": cr.url,
                                        "cluster_id": cluster_id,
                                        "query": keyword,
                                        "website": website_name,
                                        "scraped_at": datetime.utcnow().isoformat(),
                                        "currency": currency,
                                    })

                                    all_items.append(it)
                            else:
                                logger.warning(f"[{node_name}] Page {page_num}: No valid content at {cr.url}")

                    except Exception as page_err:
                        logger.exception(f"[{node_name}] Failed page {page_num}: {page_err}")

        logger.success(f"[{node_name}] Scraped {len(all_items)} total items.")
        return all_items

    except Exception as e:
        logger.exception(f"[{node_name}] Scraping failed: {e}")
        return []




def node_worker(query_chunk: List[Tuple[str, str, str]],
                shared_data_list: List[Dict],
                shared_html_debug: Dict):
    node_name = current_process().name
    logger.info(f"{node_name} started with {len(query_chunk)} queries.")

    def run_scrape(keyword: str, cluster_id: str, website: str) -> List[Dict]:
        return asyncio.run(scrape_query(keyword, cluster_id, website, shared_html_debug))

    with ThreadPoolExecutor(max_workers=MAX_THREADS_PER_NODE) as executor:
        futures = []
        for keyword, cluster_id, website in query_chunk:
            future = executor.submit(run_scrape, keyword, cluster_id, website)
            futures.append((future, keyword, cluster_id, website))

        for future, keyword, cluster_id, website in futures:
            try:
                products = future.result()
                if products:
                    shared_data_list.extend(products)
                    logger.success(f"[{node_name}] {len(products)} items from '{keyword}' ({website})")
                else:
                    logger.warning(f"[{node_name}] ⚠️ No items from '{keyword}' ({website})")
            except Exception as e:
                logger.error(f"[{node_name}] Thread error for {keyword}/{website}: {e}", exc_info=True)

    logger.info(f"{node_name} finished.")


def split_into_chunks(lst: List[Any], n: int):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

async def run_amazon_scraper(
    query_cluster_pairs: List[Tuple[str, str]],
    domain: str,
    workspace_id: str,
    secret_name: str,
    region_name: str,
    benchmarking_row_id: str
):
    all_results = []

    for search_query, cluster_id in query_cluster_pairs:
        logger.info(f"🔍 Running comprehensive scraper for: {search_query} (cluster_id: {cluster_id})")
        try:
            # products = await comprehensive_product_analysis(
            #     search_query=search_query,
            #     domain=domain,
            #     num_pages=1
            # )
            products = await comprehensive_product_analysis(
                search_query=search_query,
                workspace_id=workspace_id,
                secret_name=secret_name,
                region_name=region_name,
                benchmarking_row_id=benchmarking_row_id,
                cluster_id=cluster_id,
                domain=domain,
                num_pages=1
            )

            if not products:
                logger.warning(f"⚠️ No partial products found for: {search_query}")
                continue

            product_urls = [{"url": p.get("url", ""), "query": search_query, "cluster_id": cluster_id} for p in products if p.get("url")]
            if not product_urls:
                logger.warning(f"⚠️ No valid product URLs found for query: {search_query}")
                continue

            scraper = ComprehensiveScraper(domain=domain)
            detailed_products = await scraper.get_comprehensive_product_details(
                product_urls=product_urls,
                workspace_id=workspace_id,
                secret_name=secret_name,
                region_name=region_name,
                benchmarking_row_id=benchmarking_row_id,
                cluster_id=cluster_id
            )

            all_results.extend(detailed_products)

        except Exception as e:
            logger.error(f"❌ Error scraping for '{search_query}' (cluster_id: {cluster_id}): {e}")

    return all_results



def map_website_url_to_config_key(url: str) -> str:
    url = url.lower()
    if "www.rakuten.com" in url or "www.rakuten.co.jp" in url:
        return "rakuten"
    elif "www.alibaba.com" in url:
        return "alibaba"
    elif "www.amazon.jp" in url:
        return "amazon_jpn"
    elif "www.amazon.ae" in url:
        return "amazon_uae"
    elif "www.made-in-china.com" in url:
        return "made_in_china"
    elif "www.amazon.sa" in url:
        return "amazon_sa"

def main(event: dict, secret_name, region_name):
    SF_CREDENTIAL_SECRET_ID = os.getenv("SNOWFLAKE_SECRET_NAME")
    AWS_REGION = os.getenv("AWS_REGION")
    secrets_manager_client = boto3.client("secretsmanager", region_name=AWS_REGION)
    is_material = event.get("is_material", False)
    workspace_id = event.get("workspace_id")
    material_desc = event.get("material_description") if is_material else None
    urls = event.get("url")
    benchmarking_row_id = event.get("row_id", None)
    where_clause = f"workspace_id = '{workspace_id}' and id = '{benchmarking_row_id}'"
    table_name = '"benchmarking_findings"'

    pg = PostgresConnector(logger, workspace_id)
    pg.connect() 

    if not workspace_id:
        logger.error("'workspace_id' must be provided in event. Exiting.")
        pg.mark_status(table_name, where_clause, status="Workspace-ID-Missing")
        return

    if is_material and not material_desc:
        logger.error("'material_description' must be provided when 'is_material' is True. Exiting.")
        pg.mark_status(table_name, where_clause, status="Material-Description-Missing")
        return

    if not urls:
        logger.error("Website(s) must be provided in event['url']. Exiting.")
        pg.mark_status(table_name, where_clause, status="No-Website-Provided")
        return

    if isinstance(urls, str):
        logger.info(f"Received website(s) from event: {urls}") 
        urls = [urls]
    elif not isinstance(urls, list):
        logger.error("event['url'] must be a string or list of strings. Exiting.")
        pg.mark_status(table_name, where_clause, status="Invalid-URL-Format")
        return

    pg.mark_status(table_name, where_clause, status="Process Started")
    logger.info(f"Starting scraping for workspace_id: {workspace_id}, urls: {urls}, is_material: {is_material}")

    if is_material:
        try:
            logger.info(f"Starting normalization for material: '{material_desc}'")
            pg.mark_status(table_name, where_clause, status="Normalization-In-Progress")
            run_normalization_job(
                workspace_id=workspace_id,
                folder_id=None,
                S3_INPUT_BUCKET=None,
                custom_name=f"material_normalisation_{material_desc}",
                secret_name=secret_name,
                region_name=region_name,
                material_description=material_desc
            )
            logger.info(f"Normalization job completed successfully for: '{material_desc}'")
        except Exception as e:
            logger.error(f"Normalization job failed for '{material_desc}': {e}")
            pg.mark_status(table_name, where_clause, status="Normalization-Failed")
            raise

    for website in urls:
        website_config_key = map_website_url_to_config_key(website)
        query_triplets = []

        config.SNOWFLAKE_SCHEMA_NAME = workspace_id
        logger.info(f"[{website}] Using schema: {config.SNOWFLAKE_SCHEMA_NAME}")

        try:
            if is_material:
                logger.info(f"[{website}] is_material=True — using normalization queries.")
                df = fetch_snowflake_data(
                    secret_name=SF_CREDENTIAL_SECRET_ID,
                    secrets_manager_client=secrets_manager_client,
                    material_description=material_desc
                )
            else:
                logger.info(f"[{website}] Fetching B2B query from Snowflake")
                df = fetch_snowflake_data(
                    secret_name=SF_CREDENTIAL_SECRET_ID,
                    secrets_manager_client=secrets_manager_client
                )

            if df is None or df.empty or "B2B_QUERY" not in df.columns:
                msg = "[{website}] No queries fetched from Snowflake." if df is None or df.empty else "[{website}] 'B2B_QUERY' column missing in Snowflake data."
                logger.warning(msg)
                pg.mark_status(table_name, where_clause, status="No-data-available-to-benchmark")
                return

            query_triplets = [
                (row["B2B_QUERY"], row.get("CLUSTER_ID", None), website_config_key)
                for _, row in df.iterrows()
            ]
            if not query_triplets:
                logger.warning(f"[{website}] No queries to scrape.")
                pg.mark_status(table_name, where_clause, status="No-Queries-To-Scrape")
                return
            else:
                logger.debug(f"[{website}] Material query triplets: {query_triplets}")

        except Exception as e:
            logger.error(f"[{website}] Error fetching queries from Snowflake: {e}")
            pg.mark_status(table_name, where_clause, status="Data-Fetch-Error")
            return

        parsed = urlparse(website)
        benchmark_url = website if parsed.scheme and parsed.netloc else f"https://{website}"

        if "amazon" in website_config_key:
            logger.info(f"[{website}] Detected Amazon domain — using comprehensive scraper.")
            domain_map = {
                "amazon_uae": "amazon.ae",
                "amazon_jpn": "amazon.co.jp",
                "amazon_sa": "amazon.sa",
                "amazon_in": "amazon.in"
            }
            actual_domain = domain_map.get(website_config_key, website_config_key)

            query_pairs = [(q[0].strip(), q[1]) for q in query_triplets if q[0] and q[0].strip()]
            if not query_pairs:
                logger.warning(f"[{website}] All queries are empty — skipping.")
                continue

            logger.info(f"[{website}] Launching Amazon scraper with domain: {actual_domain}")
            result_list = asyncio.run(
                run_amazon_scraper(
                    query_cluster_pairs=query_pairs,
                    domain=actual_domain,
                    workspace_id=workspace_id,
                    secret_name=secret_name,
                    region_name=region_name,
                    benchmarking_row_id=benchmarking_row_id
                )
            )

        else:
            logger.info(f"[{website}] Non-Amazon domain — running scrape_query + benchmarking.")

            query_chunks = list(split_into_chunks(query_triplets, QUERIES_PER_NODE))
            manager = Manager()
            shared_data_list = manager.list()
            shared_html_debug = manager.dict()

            processes = []
            for chunk in query_chunks[:MAX_CONCURRENT_TASKS]:
                p = Process(target=node_worker, args=(chunk, shared_data_list, shared_html_debug))
                p.start()
                processes.append(p)

            for p in processes:
                p.join()

            result_list = list(shared_data_list)

        if not result_list:
            logger.error(f"[{website}] No data scraped.")
            pg.mark_status(table_name, where_clause, status=f"Failed for {website}")
            continue
        else:
            logger.info(f"[{website}] Scraped {len(result_list)} items.")
            pg.mark_status(table_name, where_clause, status="Scrapping-Completed")

            result_df = pd.DataFrame(result_list)

            if {"title", "url", "price"}.issubset(result_df.columns):
                result_df = result_df.dropna(subset=["title", "url", "price"])
                result_df = result_df[result_df["title"].str.strip() != ""]
                result_df = result_df.drop_duplicates(subset=["title", "url"])
                logger.info(f"[{website}] Cleaned result has {len(result_df)} items.")

            # Save to S3
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            file_name = f"{website.replace('.', '_')}_{timestamp}.csv"
            s3_key = f"{workspace_id}/{timestamp}/{file_name}"
            full_s3_uri = f"s3://{EXPORT_S3_BUCKET}/{s3_key}"

            csv_buffer = io.BytesIO()
            result_df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
            csv_buffer.seek(0)

            s3_client = boto3.client("s3",region_name=region_name)
            s3_client.put_object(Bucket=EXPORT_S3_BUCKET, Key=s3_key, Body=csv_buffer.read())
            logger.success(f"[{website}] Uploaded to {full_s3_uri}")

            run_benchmarking_job(
                workspace_id=workspace_id,
                s3_path=full_s3_uri,
                url=benchmark_url,
                secret_name=secret_name,
                region_name=region_name,
                benchmarking_row_id=benchmarking_row_id
            )
            
        logger.info(f"[{website}] Benchmarking job completed successfully.")
        pg.mark_status(table_name, where_clause, status="Completed")