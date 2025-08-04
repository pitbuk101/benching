import os
import json
import logging
import pandas as pd
import time
import numpy as np
import hashlib
import pickle
from typing import Dict, List, Any, Optional, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from benchmarking.common.s3_utils import check_and_download_file_from_uri
from benchmarking.common.snowflake_utils import read_df_from_snowflake, upload_df_to_snowflake
from benchmarking.common.data_io import load_dataframe
from benchmarking.common.utils import clean_text_for_matching

from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from tenacity import retry, retry_if_exception_type, wait_exponential, stop_after_attempt

from benchmarking.pg_db_utils import PostgresConnector
import benchmarking.normalise.env as env


# class EmbeddingCache:
#     """In-memory cache for embeddings"""
    
#     def __init__(self, cache_dir: str = None):
#         self.cache = {}
#         self.cache_dir = cache_dir
#         if cache_dir:
#             os.makedirs(cache_dir, exist_ok=True)
#             self.cache_file = os.path.join(cache_dir, "embeddings_cache.pkl")
#             self._load_cache()
    
#     def _get_cache_key(self, text: str) -> str:
#         """Generate a hash key for the text"""
#         return hashlib.md5(text.encode('utf-8')).hexdigest()
    
#     def _load_cache(self):
#         """Load cache from disk if it exists"""
#         if os.path.exists(self.cache_file):
#             try:
#                 with open(self.cache_file, 'rb') as f:
#                     self.cache = pickle.load(f)
#             except Exception as e:
#                 print(f"Warning: Could not load cache from disk: {e}")
#                 self.cache = {}
    
#     def _save_cache(self):
#         """Save cache to disk"""
#         if self.cache_dir:
#             try:
#                 with open(self.cache_file, 'wb') as f:
#                     pickle.dump(self.cache, f)
#             except Exception as e:
#                 print(f"Warning: Could not save cache to disk: {e}")
    
#     def get(self, text: str) -> Optional[np.ndarray]:
#         """Get embedding from cache"""
#         key = self._get_cache_key(text)
#         return self.cache.get(key)
    
#     def set(self, text: str, embedding: np.ndarray):
#         """Store embedding in cache"""
#         key = self._get_cache_key(text)
#         self.cache[key] = embedding
#         # Save to disk periodically (every 1000 items)
#         if len(self.cache) % 1000 == 0:
#             self._save_cache()
    
#     def save(self):
#         """Explicitly save cache to disk"""
#         self._save_cache()
    
#     def size(self) -> int:
#         """Get cache size"""
#         return len(self.cache)

class Benchmarker:
    def __init__(self, logger: logging.Logger, secret_name: str, region_name: str = "us-east-1"):
        self.logger = logger
        self.secret_name = secret_name
        self.region_name = region_name

        openai_api_key = env.LLM_OPENAI_API_KEY
        if not openai_api_key:
            raise ValueError("LLM_OPENAI_API_KEY environment variable not set")

        openai_base_url = env.OPENAI_API_BASE
        self.client = OpenAI(api_key=openai_api_key, base_url=openai_base_url, timeout=180.0)
        
        # # Initialize embedding cache
        # cache_dir = getattr(env, 'EMBEDDING_CACHE_DIR', os.path.join(env.BASE_TEMP_DIR, 'embedding_cache'))
        # self.embedding_cache = EmbeddingCache(cache_dir)
        
        # Embedding model configuration
        self.embedding_model = getattr(env, 'EMBEDDING_MODEL', 'text-embedding-3-large')
        self.embedding_batch_size = getattr(env, 'EMBEDDING_BATCH_SIZE', 1000)
        
        self.logger.info(f"Initialized Benchmarker with embedding model: {self.embedding_model}")
        # self.logger.info(f"Embedding cache size: {self.embedding_cache.size()}")

    @retry(
        retry=retry_if_exception_type((Exception,)),
        wait=wait_exponential(min=1, max=60),
        stop=stop_after_attempt(3)
    )
    def _get_embeddings_batch(self, texts: List[str]) -> List[np.ndarray]:
        """Get embeddings for a batch of texts with retry logic"""
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=texts,
                encoding_format="float"
            )
            return [np.array(data.embedding) for data in response.data]
        except Exception as e:
            self.logger.error(f"Error getting embeddings batch: {e}")
            raise

    # def _get_embeddings(self, texts: List[str]) -> List[np.ndarray]:
    #     """Get embeddings for texts, using cache when available"""
    #     embeddings = []
    #     texts_to_embed = []
    #     cache_indices = []
        
    #     # Check cache first
    #     for i, text in enumerate(texts):
    #         if not text or not isinstance(text, str):
    #             embedding_size = 3072 if self.embedding_model == "text-embedding-3-large" else 1536
    #             embeddings.append(np.zeros(embedding_size)) 
    #             continue
                
    #         cached_embedding = self.embedding_cache.get(text)
    #         if cached_embedding is not None:
    #             embeddings.append(cached_embedding)
    #             self.logger.debug(f"Cache hit for text: {text[:50]}...")
    #         else:
    #             embeddings.append(None)  # Placeholder
    #             texts_to_embed.append(text)
    #             cache_indices.append(i)
        
    #     # Get embeddings for uncached texts in batches
    #     if texts_to_embed:
    #         self.logger.info(f"Getting embeddings for {len(texts_to_embed)} new texts")
            
    #         for i in range(0, len(texts_to_embed), self.embedding_batch_size):
    #             batch_texts = texts_to_embed[i:i + self.embedding_batch_size]
    #             batch_indices = cache_indices[i:i + self.embedding_batch_size]
                
    #             try:
    #                 batch_embeddings = self._get_embeddings_batch(batch_texts)
                    
    #                 # Store in cache and update results
    #                 for j, (text, embedding) in enumerate(zip(batch_texts, batch_embeddings)):
    #                     self.embedding_cache.set(text, embedding)
    #                     embeddings[batch_indices[j]] = embedding
                        
    #             except Exception as e:
    #                 self.logger.error(f"Failed to get embeddings for batch: {e}")
    #                 # Fill with zero embeddings as fallback
    #                 for idx in batch_indices:
    #                     embeddings[idx] = np.zeros(1536)
                
    #             # Small delay between batches to avoid rate limiting
    #             time.sleep(0.1)
        
    #     # Save cache periodically
    #     self.embedding_cache.save()
        
    #     return embeddings

    def _calculate_embedding_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts using OpenAI embeddings"""
        try:
            if not text1 or not text2:
                return 0.0
            
            # Clean and normalize texts
            text1_clean = str(text1).lower().strip()
            text2_clean = str(text2).lower().strip()
            
            if not text1_clean or not text2_clean:
                return 0.0
            
            self.logger.debug(f"Calculating embedding similarity:")
            self.logger.debug(f"  Text1: '{text1_clean[:50]}...'")
            self.logger.debug(f"  Text2: '{text2_clean[:50]}...'")
            
            # Get embeddings
            embeddings = self._get_embeddings_batch([text1_clean, text2_clean])
            
            if len(embeddings) != 2:
                self.logger.warning("Failed to get embeddings for similarity calculation")
                return 0.0
            
            embedding1, embedding2 = embeddings
            
            # Calculate cosine similarity
            similarity = cosine_similarity(
                embedding1.reshape(1, -1), 
                embedding2.reshape(1, -1)
            )[0][0]
            
            similarity_score = float(similarity)
            self.logger.debug(f"Embedding similarity score: {similarity_score:.3f}")
            
            return similarity_score
            
        except Exception as e:
            self.logger.warning(f"Error calculating embedding similarity: {e}")
            return 0.0

    def _find_best_matches_embeddings(self, client_queries: Dict[int, str], 
                                    scraped_products: List[Dict[str, Any]], 
                                    cluster_id: int, 
                                    top_k: int = 1) -> Dict[int, Dict[str, Any]]:
        """Find best matches using embedding similarity"""
        
        self.logger.info(f"Cluster {cluster_id}: Finding matches using embeddings for {len(client_queries)} queries vs {len(scraped_products)} products")
        
        # Get embeddings for all client queries
        client_texts = list(client_queries.values())
        client_embeddings = self._get_embeddings_batch(client_texts)
        
        # Get embeddings for all scraped products
        product_texts = [product['description'] for product in scraped_products]
        product_embeddings = self._get_embeddings_batch(product_texts)
        
        # Convert to numpy arrays for efficient computation
        client_embeddings_matrix = np.array(client_embeddings)
        product_embeddings_matrix = np.array(product_embeddings)
        
        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(client_embeddings_matrix, product_embeddings_matrix)
        
        # Find best matches
        best_matches = {}
        
        for i, (client_idx, client_query) in enumerate(client_queries.items()):
            similarities = similarity_matrix[i]
            
            # Get top-k matches
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            for rank, product_idx in enumerate(top_indices):
                similarity_score = similarities[product_idx]
                
                # Only consider matches above a threshold
                if similarity_score > 0.3:  # Adjust threshold as needed
                    original_index = scraped_products[product_idx]['original_index']
                    
                    # Store the best match (rank 0)
                    if rank == 0:
                        best_matches[client_idx] = {
                            'score': similarity_score,
                            'matched_product_index': original_index,
                            'similarity_type': 'embedding'
                        }
                    
                    self.logger.debug(f"Cluster {cluster_id}, Query {client_idx}: "
                                    f"Match rank {rank + 1}, Score: {similarity_score:.3f}")
        
        return best_matches

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
        
        client_df = read_df_from_snowflake("NORMALISED_DATA", workspace_id, self.logger, self.secret_name, self.region_name)

        # Expand the RESPONSE column (JSON) 
        response_dicts = client_df['RESPONSE'].map(json.loads).tolist()
        response_expanded = pd.json_normalize(response_dicts)
        client_df = pd.concat([client_df, response_expanded], axis=1)

        
        self.logger.info(f"Client data columns: {client_df.columns}")

        self.logger.info(f"Loaded client data from Snowflake: {client_df.shape}")

        # 3. Preprocess data
        client_df.columns = [col.upper() for col in client_df.columns]
        client_df['PROCESSED_QUERY'] = client_df['NORMALIZED DESCRIPTION'].astype(str).apply(clean_text_for_matching)
        scraped_df['processed_description'] = scraped_df['title'].astype(str).apply(clean_text_for_matching)
        
        # Fix data type mismatch for cluster IDs
        client_df['CLUSTER_ID'] = client_df['CLUSTER_ID'].astype(int)
        
        scraped_df = scraped_df[scraped_df['cluster_id'].notna()]
        scraped_df = scraped_df[np.isfinite(scraped_df['cluster_id'])]
        scraped_df['cluster_id'] = scraped_df['cluster_id'].astype(int)

        #for testing purpose chose only all the cluster id present in scraped_df only
        # client_df = client_df[client_df['CLUSTER_ID'] < 50]
        # scraped_df = scraped_df[scraped_df['cluster_id'] < 50]
        client_df = client_df[client_df['CLUSTER_ID'].isin(scraped_df['cluster_id'])]

        self.logger.info(f"Client clusters: {sorted(client_df['CLUSTER_ID'].unique())}")
        self.logger.info(f"Scraped clusters: {sorted(scraped_df['cluster_id'].unique())}")

        # 4. Process clusters
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

                client_queries = {
                    idx: row['PROCESSED_QUERY'] 
                    for idx, row in cluster_client.iterrows() 
                    if pd.notna(row['PROCESSED_QUERY']) and isinstance(row['PROCESSED_QUERY'], str) and row['PROCESSED_QUERY'].strip()
                }
                
                scraped_products_list = [
                    {'original_index': idx, 'description': row['processed_description']}
                    for idx, row in cluster_scraped.head(100).iterrows()
                    if pd.notna(row['processed_description']) and isinstance(row['processed_description'], str) and row['processed_description'].strip()
                ]
                
                if not scraped_products_list:
                    self.logger.warning(f"Cluster {cluster_id}: No valid scraped products")
                    return []
                
                # Use embedding-based matching
                best_matches = self._find_best_matches_embeddings(client_queries, scraped_products_list, cluster_id)

                cluster_results = self._create_cluster_results(cluster_id, cluster_client, cluster_scraped, best_matches, url)
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
        final_df = final_df.drop_duplicates()  

        # final_df_path = os.path.join(temp_dir, f"benchmark_results_new_{workspace_id}.csv")
        # final_df.to_csv(final_df_path, index=False)

        if not final_df.empty:
            self.logger.info(f"Total results: {len(final_df)}")
            # self.logger.info(f"Embedding cache final size: {self.embedding_cache.size()}")
            try:
                upload_df_to_snowflake(final_df, "BENCHMARK_RESULTS", workspace_id, self.logger, self.secret_name, self.region_name)
                self.logger.info(f"Benchmark results uploaded to Snowflake for Schema {workspace_id}")
            except Exception as e:
                self.logger.error(f"Failed to upload benchmark results to Snowflake: {e}, workspace_id: {workspace_id}")
        else:
            self.logger.warning("No results found. Aborting upload to Snowflake.")
        # Save cache before finishing
        # self.embedding_cache.save()
        return final_df

    def _create_cluster_results_amazon(self, cluster_id, cluster_client, cluster_scraped, best_matches):
        """Create result records for Amazon scraped data"""
        results = []
        for client_idx, match_info in best_matches.items():
            if match_info['score'] > 0.3:  # Confidence threshold
                try:
                    client_row = cluster_client.iloc[client_idx]
                    scraped_idx = match_info['matched_product_index']
                    if scraped_idx is None or not isinstance(scraped_idx, int) or scraped_idx >= len(cluster_scraped):
                        self.logger.warning(f"Cluster {cluster_id}: Invalid scraped index {scraped_idx}, skipping")
                        continue
                    match_row = cluster_scraped.iloc[scraped_idx]

                    def safe_get(row, key, default=''):
                        val = row.get(key, default)
                        if isinstance(val, str):
                            return val.strip()
                        return str(val).strip() if val is not None else default

                    # Amazon-specific fields
                    currency_info = match_row.get('currency_info', {})
                    currency_code = currency_info.get('code', '') if isinstance(currency_info, dict) else ''
                    net_quantity = safe_get(match_row, 'net_quantity', '')
                    variant_total_price = safe_get(match_row, 'variant_total_price', '')
                    per_unit_price_display = safe_get(match_row, 'per_unit_price_display', '')

                    # If unit_variants exists and is non-empty, pick max quantity variant
                    source_quantity = net_quantity
                    source_spend = variant_total_price
                    source_unit_price = per_unit_price_display
                    unit_variants = match_row.get('unit_variants', None)
                    if isinstance(unit_variants, list) and len(unit_variants) > 0:
                        max_variant = max(unit_variants, key=lambda v: v.get('quantity', 0) if isinstance(v.get('quantity', 0), (int, float)) else 0)
                        source_quantity = max_variant.get('quantity', source_quantity)
                        source_spend = max_variant.get('total_price', source_spend)
                        source_unit_price = max_variant.get('per_unit_price', source_unit_price)

                    # If any of these are blank
                    if not source_unit_price:
                        source_unit_price = safe_get(match_row, 'unit_price', '')
                    if not currency_code:
                        currency_symbol = safe_get(match_row, 'currency_symbol', '')
                        # Map currency symbols to codes
                        currency_map = {'ريال': 'SAR'}
                        currency_code = currency_map.get(currency_symbol, currency_symbol if currency_symbol else 'USD')

                    # Convert empty strings to None 
                    def clean_numeric_value(value):
                        if value == '' or value is None:
                            return None
                        if isinstance(value, str) and value.strip() == '':
                            return None
                        return value

                    # Convert string values to numbers for numeric Snowflake columns
                    def safe_convert_to_number(value):
                        if value is None or value == '':
                            return None
                        if isinstance(value, (int, float)):
                            return value
                        if isinstance(value, str):
                            value = value.strip()
                            if value == '':
                                return None
                            try:
                                # Try to convert to float first, then int if it's a whole number
                                float_val = float(value)
                                if float_val.is_integer():
                                    return int(float_val)
                                return float_val
                            except (ValueError, TypeError):
                                return None
                        return None

                    source_quantity = clean_numeric_value(source_quantity)
                    source_spend = clean_numeric_value(source_spend)
                    source_unit_price = clean_numeric_value(source_unit_price)

                    # CATEGORY and UOM as str and Unit Price Numeric
                    quantity_value = safe_convert_to_number(client_row.get('QUANTITY'))
                    spend_value = safe_convert_to_number(client_row.get('SPEND'))
                    unit_price_value = safe_convert_to_number(client_row.get('UNIT PRICE'))

                    self.logger.info(f"Cluster {cluster_id}: Client {client_idx} Order Quantity: {client_row.get('QUANTITY')}")
  
                    result = {
                        'CLUSTER_ID': cluster_id,
                        'CATEGORY': safe_get(client_row, 'CATEGORY'),
                        'SKU_DESCRIPTION': safe_get(client_row, 'ITEM DESCRIPTION'),
                        'UOM': safe_get(client_row, 'UOM'),
                        'QUANTITY': quantity_value,
                        'CURRENCY': client_row.get('CURRENCY', 'USD'),
                        'SPEND': spend_value,              
                        'UNIT_PRICE': unit_price_value,   
                        'NORMALISED_DESCRIPTION': safe_get(client_row, 'NORMALIZED DESCRIPTION'),
                        'SOURCE_DESCRIPTION': safe_get(match_row, 'title'),
                        'SOURCE_CURRENCY': currency_code,
                        'SOURCE_UNIT_PRICE': source_unit_price,
                        'SOURCE_URL': safe_get(match_row, 'url'),
                        'SIMILARITY_SCORE': round(match_info['score'], 4),
                        'EXTRACTED_QUANTITY': client_row.get('Extracted_Quantity', 1),
                        'SOURCE_QUANTITY': source_quantity,
                        'SOURCE_TOTAL_PRICE': source_spend,
                    }
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Cluster {cluster_id}: Error creating Amazon result for client_idx {client_idx}: {e}")
                    continue
        return results
    

    def _create_cluster_results(self, cluster_id, cluster_client, cluster_scraped, best_matches, url):
        """Create result records for a cluster"""
        
        if isinstance(url, str) and 'amazon' in url.lower():
            return self._create_cluster_results_amazon(cluster_id, cluster_client, cluster_scraped, best_matches)

        results = []
        
        for client_idx, match_info in best_matches.items():
            if match_info['score'] > 0.3:  # Confidence threshold
                try:
                    client_row = cluster_client.iloc[client_idx]
                    scraped_idx = match_info['matched_product_index']
                    
                    if scraped_idx is None or not isinstance(scraped_idx, int) or scraped_idx >= len(cluster_scraped):
                        self.logger.warning(f"Cluster {cluster_id}: Invalid scraped index {scraped_idx}, skipping")
                        continue
                    
                    match_row = cluster_scraped.iloc[scraped_idx]

                    def safe_get_and_strip(row, key, default=''):
                        val = row.get(key, default)
                        if isinstance(val, str):
                            return val.strip()
                        return str(val).strip() if val is not None else default

                    # Convert empty strings to None
                    def clean_numeric_value(value):
                        if value == '' or value is None:
                            return None
                        if isinstance(value, str) and value.strip() == '':
                            return None
                        return value

                    # Convert string values to numbers for numeric
                    def safe_convert_to_number(value):
                        if value is None or value == '':
                            return None
                        if isinstance(value, (int, float)):
                            return value
                        if isinstance(value, str):
                            value = value.strip()
                            if value == '':
                                return None
                            try:
                                float_val = float(value)
                                if float_val.is_integer():
                                    return int(float_val)
                                return float_val 
                            except (ValueError, TypeError):
                                return None
                        return None
                    
                    source_quantity = clean_numeric_value(safe_get_and_strip(match_row, 'quantity'))
                    source_total_price = clean_numeric_value(safe_get_and_strip(match_row, 'total_price', ''))
                    source_unit_price = clean_numeric_value(safe_get_and_strip(match_row, 'price'))
                    
                    quantity_value = safe_convert_to_number(client_row.get('QUANTITY'))
                    spend_value = safe_convert_to_number(client_row.get('SPEND'))
                    unit_price_value = safe_convert_to_number(client_row.get('UNIT PRICE'))
                    
                    result = {
                        'CLUSTER_ID': cluster_id,
                        'CATEGORY': safe_get_and_strip(client_row, 'CATEGORY'),
                        'SKU_DESCRIPTION': safe_get_and_strip(client_row, 'ITEM DESCRIPTION'),
                        'UOM': safe_get_and_strip(client_row, 'UOM'),
                        'QUANTITY': quantity_value,
                        'CURRENCY': client_row.get('CURRENCY', 'USD'),
                        'SPEND': spend_value,
                        'UNIT_PRICE': unit_price_value,
                        'NORMALISED_DESCRIPTION': safe_get_and_strip(client_row, 'NORMALIZED DESCRIPTION'),
                        'SOURCE_DESCRIPTION': safe_get_and_strip(match_row, 'title'),
                        'SOURCE_CURRENCY': safe_get_and_strip(client_row, 'currency', 'USD'),
                        'SOURCE_UNIT_PRICE': source_unit_price,
                        'SOURCE_URL': safe_get_and_strip(match_row, 'url'),
                        'SIMILARITY_SCORE': round(match_info['score'], 4),
                        'EXTRACTED_QUANTITY': client_row.get('Extracted_Quantity', 1),
                        'SOURCE_QUANTITY': source_quantity,
                        'SOURCE_TOTAL_PRICE': source_total_price,

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

def run_benchmarking_job(workspace_id: str, s3_path: str, url: str, secret_name: str, region_name: str = "us-east-1", benchmarking_row_id: str = None):

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
    pg = PostgresConnector(logger, workspace_id)
    pg.connect()
    try:
        try:
            table_name = '"benchmarking_findings"'
            where_clause = f"workspace_id = '{workspace_id}' AND id = '{benchmarking_row_id}'"
            pg.mark_status(table_name, where_clause, status="Benchmarking-In Progress")
        except Exception:
            pass

        # Instantiate
        benchmarker = Benchmarker(logger, secret_name, region_name)

        # Run the benchmarking process
        benchmark_df = benchmarker.run(workspace_id, s3_path, url)
        if benchmark_df.empty:
            logger.warning("Benchmarking resulted in an empty DataFrame.")
            return
        logger.info(f"Benchmarking complete. {len(benchmark_df)} records processed.")

    except Exception as e:
        logger.error(f"Benchmarking job failed for workspace '{workspace_id}'. Error: {e}", exc_info=True)
    finally:
        logger.info(f"Benchmarking job finished for workspace '{workspace_id}'.")
