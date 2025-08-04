import os
import json
import logging
import pandas as pd
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from benchmarking.common.s3_utils import check_and_download_file_from_uri
from benchmarking.common.snowflake_utils import read_df_from_snowflake, upload_df_to_snowflake
from benchmarking.common.data_io import load_dataframe
from benchmarking.common.utils import clean_text_for_matching
from benchmarking.prompts.normalization_prompts import benchmarking_match_prompt
from openai import OpenAI, AsyncOpenAI, RateLimitError, APIError
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio
from tenacity import retry, retry_if_exception_type, wait_exponential, stop_after_attempt

# import normalise.env as env
#
from benchmarking.pg_db_utils import PostgresConnector
# from normalise.src.common.logging_config import setup_logging

import logging
import benchmarking.normalise.env as env

class Benchmarker:
    def __init__(self, logger: logging.Logger,secret_name: str, region_name: str = "us-east-1"):
        self.logger = logger
        self.secret_name = secret_name
        self.region_name = region_name

        self.model_name = env.LLM_MODEL
        openai_api_key = env.LLM_OPENAI_API_KEY
        if not openai_api_key:
            raise ValueError("LLM_OPENAI_API_KEY environment variable not set")

        openai_base_url = env.OPENAI_API_BASE
        self.client = OpenAI(api_key=openai_api_key, base_url=openai_base_url, timeout=180.0)
        
        # Initialize TF-IDF vectorizer for cosine similarity
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 2),
            max_features=1000,
            min_df=1,
            max_df=0.95
        )

    def _calculate_cosine_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two text strings"""
        try:
            if not text1 or not text2:
                return 0.0
            
            # Clean and normalize texts
            text1_clean = str(text1).lower().strip()
            text2_clean = str(text2).lower().strip()
            
            if not text1_clean or not text2_clean:
                return 0.0
            
            # Log the texts being compared for debugging
            self.logger.debug(f"Comparing texts for cosine similarity:")
            self.logger.debug(f"  Text1: '{text1_clean}'")
            self.logger.debug(f"  Text2: '{text2_clean}'")
            
            # Create a temporary vectorizer for this comparison
            # Use simpler parameters that work better with multilingual text
            temp_vectorizer = TfidfVectorizer(
                lowercase=True,
                stop_words=None,  # Don't use English stop words for multilingual text
                ngram_range=(1, 1),  # Use only unigrams
                max_features=500,
                min_df=1,
                max_df=1.0,  # Allow all terms
                token_pattern=r'(?u)\b\w+\b'  # Unicode-aware word boundaries
            )
            
            # Vectorize the texts
            texts = [text1_clean, text2_clean]
            tfidf_matrix = temp_vectorizer.fit_transform(texts)
            
            # Check if we have any features
            if tfidf_matrix.shape[1] == 0:
                self.logger.debug("No features found in TF-IDF matrix")
                return 0.0
            
            # Get feature names for debugging
            feature_names = temp_vectorizer.get_feature_names_out()
            self.logger.debug(f"TF-IDF features: {feature_names}")
            
            # Calculate cosine similarity
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            similarity_score = float(similarity_matrix[0][0])
            
            # Log for debugging
            self.logger.debug(f"Cosine similarity score: {similarity_score:.3f}")
            
            return similarity_score
            
        except Exception as e:
            self.logger.warning(f"Error calculating cosine similarity between '{text1[:50]}...' and '{text2[:50]}...': {e}")
            return 0.0

    def _calculate_hybrid_score(self, llm_score: float, cosine_score: float, 
                              llm_weight: float = 0.7, cosine_weight: float = 0.3) -> float:
        """Calculate hybrid score combining LLM and cosine similarity scores"""
        if llm_weight + cosine_weight != 1.0:
            # Normalize weights
            total_weight = llm_weight + cosine_weight
            llm_weight /= total_weight
            cosine_weight /= total_weight
        
        hybrid_score = (llm_score * llm_weight) + (cosine_score * cosine_weight)
        return round(hybrid_score, 4)

    def run(self, workspace_id: str, s3_path: str, url: str) -> pd.DataFrame:
        """Main benchmarking function"""
        
        # 1. Download scraped data from S3
        temp_dir = os.path.join(env.BASE_TEMP_DIR, f"benchmark_{workspace_id}")
        os.makedirs(temp_dir, exist_ok=True)
        bucket_name = env.S3_BENCHMARK_INPUT_BUCKET
        self.logger.info(f"[BENCHMARK] Using S3 bucket: {bucket_name}, path: {s3_path}")
        
        try:
            scraped_file_path = check_and_download_file_from_uri(s3_path, temp_dir, self.logger)
            self.logger.info(f"[BENCHMARK] Downloaded file from S3: {scraped_file_path}")
        except Exception as e:
            self.logger.error(f"[BENCHMARK] Failed to download file from S3: {e}")
            raise

        # 2. Load data
        scraped_df = load_dataframe(scraped_file_path)
        self.logger.info(f"Loaded scraped data: {scraped_df.shape}")
        
        client_df = read_df_from_snowflake("NORMALISED_DATA", workspace_id, self.logger,self.secret_name,self.region_name)
        self.logger.info(f"Loaded client data from Snowflake: {client_df.shape}")

        # 3. Preprocess data
        client_df.columns = [col.upper() for col in client_df.columns]
        client_df['PROCESSED_QUERY'] = client_df['NORMALIZED_DESCRIPTION'].astype(str).apply(clean_text_for_matching)
        scraped_df['processed_description'] = scraped_df['title'].astype(str).apply(clean_text_for_matching)
        
        # Fix data type mismatch for cluster IDs
        client_df['CLUSTER_ID'] = client_df['CLUSTER_ID'].astype(int)
        scraped_df['cluster_id'] = scraped_df['cluster_id'].astype(int)
        
        self.logger.info(f"Client clusters: {sorted(client_df['CLUSTER_ID'].unique())}")
        self.logger.info(f"Scraped clusters: {sorted(scraped_df['cluster_id'].unique())}")

        # 4. Process clusters (simple approach like matching.py)
        unique_cluster_ids = sorted(client_df['CLUSTER_ID'].dropna().unique())
        self.logger.info(f"Processing {len(unique_cluster_ids)} clusters: {unique_cluster_ids}")
        all_results = []

        def process_cluster(cluster_id):
            try:
                cluster_start_time = time.perf_counter()
                cluster_client = client_df[client_df['CLUSTER_ID'] == cluster_id].reset_index(drop=True)
                cluster_scraped = scraped_df[scraped_df['cluster_id'] == cluster_id].reset_index(drop=True)
                if cluster_scraped.empty or cluster_client.empty:
                    self.logger.warning(f"Cluster {cluster_id}: No data found. Client: {len(cluster_client)}, Scraped: {len(cluster_scraped)}")
                    return []
                self.logger.info(f"Cluster {cluster_id}: Processing {len(cluster_client)} client queries vs {len(cluster_scraped)} scraped products")

                client_queries = {idx: row['PROCESSED_QUERY'] for idx, row in cluster_client.iterrows() if pd.notna(row['PROCESSED_QUERY']) and isinstance(row['PROCESSED_QUERY'], str) and row['PROCESSED_QUERY'].strip()}
                scraped_products_list = [
                    {'original_index': idx, 'description': row['processed_description']}
                    for idx, row in cluster_scraped.head(100).iterrows()
                    if pd.notna(row['processed_description']) and isinstance(row['processed_description'], str) and row['processed_description'].strip()
                ]
                if not scraped_products_list:
                    self.logger.warning(f"Cluster {cluster_id}: No valid scraped products")
                    return []
                overall_best_matches = self._get_cluster_matches(client_queries, scraped_products_list, cluster_id)
                cluster_results = self._create_cluster_results(cluster_id, cluster_client, cluster_scraped, overall_best_matches)
                cluster_end_time = time.perf_counter()
                self.logger.info(f"Cluster {cluster_id}: Found {len(cluster_results)} matches. Time: {cluster_end_time - cluster_start_time:.2f}s")
                return cluster_results
            except Exception as e:
                self.logger.error(f"Cluster {cluster_id}: Error in processing: {e}", exc_info=True)
                return []

        # Parallel cluster processing
        max_workers = getattr(env, 'LLM_MAX_WORKERS_BENCHMARKING', env.LLM_MAX_WORKERS_NORMALIZATION)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_cluster, cluster_id): cluster_id for cluster_id in unique_cluster_ids}
            for future in as_completed(futures):
                cluster_id = futures[future]
                try:
                    results = future.result()
                    all_results.extend(results)
                except Exception as e:
                    self.logger.error(f"Cluster {cluster_id}: Exception in future: {e}", exc_info=True)

        # 5. Save results
        final_df = pd.DataFrame(all_results)
        if not final_df.empty:
            self.logger.info(f"Total results: {len(final_df)}")
            try:
                upload_df_to_snowflake(final_df, "BENCHMARK_RESULTS", workspace_id, self.logger,self.secret_name,self.region_name)
                self.logger.info(f"Benchmark results uploaded to Snowflake for Schema {workspace_id}")
            except Exception as e:
                self.logger.error(f"Failed to upload benchmark results to Snowflake: {e} , workspace_id: {workspace_id}")
        else:
            self.logger.warning("No results found. Aborting upload to Snowflake.")
        return final_df

    async def _get_bulk_matches_from_llm_async(self, client_queries_dict, scraped_chunk_dict, cluster_id):
        """
        Async, batched, structured LLM matching.
        """
        client = AsyncOpenAI(api_key=env.LLM_OPENAI_API_KEY, base_url=env.OPENAI_API_BASE)
        model = self.model_name
        client_items = list(client_queries_dict.items())
        batch_size = 20  
        results = []

        @retry(
            retry=retry_if_exception_type((RateLimitError, APIError)),
            wait=wait_exponential(min=2, max=30),
            stop=stop_after_attempt(5)
        )
        async def call_llm(batch):
            client_list_str = "\n".join([f'{cq_id}: "{desc}"' for cq_id, desc in batch])
            scraped_list_str = "\n".join([f'{p_idx}: "{desc}"' for p_idx, desc in scraped_chunk_dict.items()])
            prompt_data = benchmarking_match_prompt(
                client_list_str=client_list_str,
                scraped_list_str=scraped_list_str
            )
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt_data["system_message"]},
                    {"role": "user", "content": prompt_data["user_template"]}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )
            response_text = response.choices[0].message.content.strip()
            data = json.loads(response_text)
            for key, value in data.items():
                if isinstance(value, list):
                    self.logger.info(f"Cluster {cluster_id}: LLM returned {len(value)} matches")
                    return value
            self.logger.warning(f"Cluster {cluster_id}: No matches returned.")
            return []

        tasks = []
        for i in range(0, len(client_items), batch_size):
            batch = client_items[i:i+batch_size]
            tasks.append(call_llm(batch))
        batch_results = await asyncio.gather(*tasks, return_exceptions=False)
        for r in batch_results:
            if r:
                results.extend(r)
        return results

    def _get_cluster_matches(self, client_queries, scraped_products_list, cluster_id):
        """Get matches for a cluster using LLM """
        
        # Create chunk dictionary with sequential indices
        chunk_dict = {idx: item['description'] for idx, item in enumerate(scraped_products_list)}
        
        # Get matches from LLM
        matches = asyncio.run(self._get_bulk_matches_from_llm_async(client_queries, chunk_dict, cluster_id))
        
        # Process results and calculate hybrid scores
        overall_best_matches = {}
        for match in matches:
            if not all(k in match for k in ['client_query_id', 'score', 'matched_product_index']):
                continue
                
            cq_id = match.get('client_query_id')
            llm_score = match.get('score', 0)
            llm_index = match.get('matched_product_index')
            translated_title = match.get('translated_title', 'N/A')
            
            if cq_id is None or llm_index is None:
                continue
                
            # Convert LLM index back to original index
            if llm_index < len(scraped_products_list):
                original_index = scraped_products_list[llm_index]['original_index']
            else:
                self.logger.warning(f"Cluster {cluster_id}: Invalid LLM index {llm_index}")
                continue
            
            # Calculate cosine similarity between client query and TRANSLATED product title
            client_query_text = client_queries.get(cq_id, "")
            
            # Use translated title for cosine similarity if available, otherwise fall back to original
            if translated_title and translated_title != 'N/A':
                product_text_for_cosine = translated_title
                self.logger.debug(f"Cluster {cluster_id}: Using translated title for cosine: '{translated_title}'")
            else:
                product_text_for_cosine = scraped_products_list[llm_index]['description']
                self.logger.debug(f"Cluster {cluster_id}: Using original description for cosine: '{product_text_for_cosine}'")
            
            cosine_score = self._calculate_cosine_similarity(client_query_text, product_text_for_cosine)
            
            # Calculate hybrid score
            hybrid_score = self._calculate_hybrid_score(llm_score, cosine_score, llm_weight=0.7, cosine_weight=0.3)
            
            self.logger.debug(f"Cluster {cluster_id}, Query {cq_id}: LLM={llm_score:.3f}, Cosine={cosine_score:.3f}, Hybrid={hybrid_score:.3f}")
            self.logger.debug(f"Client: '{client_query_text}'")
            self.logger.debug(f"Product: '{product_text_for_cosine}'")
            
            if hybrid_score > overall_best_matches.get(cq_id, {}).get('score', -1):
                overall_best_matches[cq_id] = {
                    "score": hybrid_score,
                    "llm_score": llm_score,
                    "cosine_score": cosine_score,
                    "matched_product_index": original_index,
                    "translated_title": translated_title
                }
        
        return overall_best_matches

    def _create_cluster_results(self, cluster_id, cluster_client, cluster_scraped, overall_best_matches):
        """Create result records for a cluster"""
        results = []
        
        for client_idx, best_match_info in overall_best_matches.items():
            if best_match_info['score'] > 0.5:  # Confidence threshold
                try:
                    client_row = cluster_client.iloc[client_idx]
                    scraped_idx = best_match_info['matched_product_index']
                    
                    if scraped_idx is None or not isinstance(scraped_idx, int) or scraped_idx >= len(cluster_scraped):
                        self.logger.warning(f"Cluster {cluster_id}: Invalid scraped index {scraped_idx}, skipping")
                        continue
                    
                    match_row = cluster_scraped.iloc[scraped_idx]
                    
                    def safe_get_and_strip(row, key, default=''):
                        val = row.get(key, default)
                        if isinstance(val, str):
                            return val.strip()
                        return str(val).strip() if val is not None else default
                    
                    result = {
                        'CLUSTER_ID': cluster_id,
                        'CATEGORY': safe_get_and_strip(client_row, 'CATEGORY'),
                        'SKU_DESCRIPTION': safe_get_and_strip(client_row, 'DESCRIPTION'),
                        'UOM': safe_get_and_strip(client_row, 'UOM'),
                        'QUANTITY': client_row.get('QUANTITY'),
                        'SPEND': client_row.get('SPEND', 0),
                        'NORMALISED_DESCRIPTION': safe_get_and_strip(client_row, 'NORMALIZED_DESCRIPTION'),
                        'SOURCE_DESCRIPTION': best_match_info['translated_title'], #match_row['title'],
                        'SOURCE_CURRENCY': safe_get_and_strip(client_row, 'PURCHASE_CURRENCY','USD'),
                        'SOURCE_UNIT_PRICE': safe_get_and_strip(match_row, 'price'),
                        'SOURCE_URL': safe_get_and_strip(match_row, 'url'),
                        'SIMILARITY_SCORE': round(best_match_info['score'], 4),
                        'EXTRACTED_QUANTITY': client_row.get('EXTRACTED_QUANTITY', 1),
                        # 'SOURCE_SPEND': client_row.get('QUANTITY', 1) * safe_get_and_strip(match_row, 'price') * client_row.get('EXTRACTED_QUANTITY', 1),
                    }
                    results.append(result)
                    
                except Exception as e:
                    self.logger.error(f"Cluster {cluster_id}: Error creating result for client_idx {client_idx}: {e}")
                    continue
        
        return results 
    



def setup_logging() -> logging.Logger:
    """
    Sets up logging for the application based on the provided configuration.
    """
    log_level_str = env.LOG_LEVEL.upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    log_format = env.LOG_FORMAT
    date_format = env.LOG_DATE_FORMAT
    logger_name = env.CLIENT_NAME
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    if logger.hasHandlers():
        logger.handlers.clear()
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    formatter = logging.Formatter(log_format, datefmt=date_format)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.propagate = False
    logger.info(f"Logging setup complete for {logger_name}. Level: {log_level_str}")
    return logger


def run_benchmarking_job(workspace_id: str, s3_path: str, url: str, secret_name: str, region_name: str = "us-east-1",benchmarking_row_id: str = None):
    """
    Runs the benchmarking job for a given workspace.
    Args:
        workspace_id: The ID of the workspace.
        s3_path: The S3 path to the input data.
        url: The URL for benchmarking.
        secret_name: The name of the Snowflake secret in AWS Secrets Manager.
        region_name: The AWS region where the secret is stored (default: "us-east-1").
    """
    logger = setup_logging()
    temp_run_dir = os.path.join(env.BASE_TEMP_DIR, f"benchmark_{workspace_id}")
    os.makedirs(temp_run_dir, exist_ok=True)
    pg = PostgresConnector(logger,workspace_id)
    pg.connect()
    try:
        try:
            table_name = '"benchmarking_findings"'
            where_clause = f"workspace_id = '{workspace_id}' AND id = '{benchmarking_row_id}'"
            pg.mark_status(table_name, where_clause, status="Benchmarking-In Progress")
        except Exception:
            pass

        # Instantiate the Benchmarker class with the required arguments
        benchmarker = Benchmarker(logger, secret_name, region_name)

        # Run the benchmarking process
        benchmark_df = benchmarker.run(workspace_id, s3_path, url)
        if benchmark_df.empty:
            logger.warning("Benchmarking resulted in an empty DataFrame.")
            return
        logger.info(f"Benchmarking complete. {len(benchmark_df)} records processed.")
        try:
            table_name = '"benchmarking_findings"'
            pg.mark_status(table_name, where_clause, status="Completed")
        except Exception:
            pass
    except Exception as e:
        logger.error(f"Benchmarking job failed for workspace '{workspace_id}'. Error: {e}", exc_info=True)
    finally:
        logger.info(f"Benchmarking job finished for workspace '{workspace_id}'.")