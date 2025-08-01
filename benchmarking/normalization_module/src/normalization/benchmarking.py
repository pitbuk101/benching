import os
import json
import logging
import pandas as pd
import time
import numpy as np
from omegaconf import DictConfig
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.common.s3_utils import check_and_download_file_from_uri
from src.common.snowflake_utils import read_df_from_snowflake, upload_df_to_snowflake
from src.common.data_io import load_dataframe
from src.common.utils import clean_text_for_matching
from src.normalization.clustering import Clustering
from src.prompts.normalization_prompts import benchmarking_match_prompt
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed

class Benchmarker:
    def __init__(self, config: DictConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger
        # Initialize OpenAI client for benchmarking
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI environment variable not set")
        
        openai_base_url = os.getenv("OPENAI_BASE_URL")
        self.client = OpenAI(api_key=openai_api_key, base_url=openai_base_url, timeout=180.0)
        self.model_name = "gpt-4o"
        
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
        """Main benchmarking function - simple and effective like matching.py"""
        
        # 1. Download scraped data from S3
        temp_dir = os.path.join(self.config.paths.base_temp_dir, f"benchmark_{workspace_id}")
        os.makedirs(temp_dir, exist_ok=True)
        bucket_name = self.config.s3.benchmark_input_bucket
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
        
        client_df = read_df_from_snowflake("NORMALISED_DATA", self.config.snowflake, workspace_id, self.logger)
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
        # For testing, only process first 5 clusters
        unique_cluster_ids = unique_cluster_ids[:50]
        self.logger.info(f"Processing {len(unique_cluster_ids)} clusters: {unique_cluster_ids}")
        
        all_results = []
        
        for cluster_id in unique_cluster_ids:
            cluster_start_time = time.perf_counter()
            
            # Get cluster data
            cluster_client = client_df[client_df['CLUSTER_ID'] == cluster_id].reset_index(drop=True)
            cluster_scraped = scraped_df[scraped_df['cluster_id'] == cluster_id].reset_index(drop=True)
            
            if cluster_scraped.empty or cluster_client.empty:
                self.logger.warning(f"Cluster {cluster_id}: No data found. Client: {len(cluster_client)}, Scraped: {len(cluster_scraped)}")
                continue
            
            self.logger.info(f"Cluster {cluster_id}: Processing {len(cluster_client)} client queries vs {len(cluster_scraped)} scraped products")
            
            # Save cluster scraped data locally for inspection
            cluster_scraped_path = os.path.join(temp_dir, f'cluster_{cluster_id}_scraped_data.csv')
            cluster_scraped.to_csv(cluster_scraped_path, index=False)
            self.logger.info(f"Saved cluster {cluster_id} scraped data to {cluster_scraped_path}")
            
            # Prepare client queries and scraped products (take only first 100)
            client_queries = {}
            for idx, row in cluster_client.iterrows():
                query = row['PROCESSED_QUERY']
                if pd.notna(query) and isinstance(query, str) and query.strip():
                    client_queries[idx] = query
            
            scraped_products_list = []
            for idx, row in cluster_scraped.head(100).iterrows():
                desc = row['processed_description']
                if pd.notna(desc) and isinstance(desc, str) and desc.strip():
                    scraped_products_list.append({'original_index': idx, 'description': desc})
            
            if not scraped_products_list:
                self.logger.warning(f"Cluster {cluster_id}: No valid scraped products")
                continue
            
            self.logger.info(f"Cluster {cluster_id}: Using {len(scraped_products_list)} scraped products")
            
            # Matches
            overall_best_matches = self._get_cluster_matches(client_queries, scraped_products_list, cluster_id)
            
            # Results
            cluster_results = self._create_cluster_results(cluster_id, cluster_client, cluster_scraped, overall_best_matches)
            all_results.extend(cluster_results)
            
            cluster_end_time = time.perf_counter()
            self.logger.info(f"Cluster {cluster_id}: Found {len(cluster_results)} matches. Time: {cluster_end_time - cluster_start_time:.2f}s")

        # 5. Save results
        final_df = pd.DataFrame(all_results)
        if not final_df.empty:
            self.logger.info(f"Total results: {len(final_df)}")
            # Apply clustering
            # clustering = Clustering(self.logger)
            # final_df = clustering.run(final_df)
            
            # Upload to Snowflake
            try:
                upload_df_to_snowflake(final_df, "BENCHMARK_RESULTS", self.config.snowflake, workspace_id, self.logger)
                self.logger.info(f"Benchmark results uploaded to Snowflake for workspace {workspace_id}")
            except Exception as e:
                self.logger.error(f"Failed to upload benchmark results to Snowflake: {e}")
        else:
            self.logger.warning("No results found. Aborting upload to Snowflake.")
            
        return final_df

    def _get_cluster_matches(self, client_queries, scraped_products_list, cluster_id):
        """Get matches for a cluster using LLM - simple approach like matching.py"""
        
        # Create chunk dictionary with sequential indices
        chunk_dict = {idx: item['description'] for idx, item in enumerate(scraped_products_list)}
        
        # Get matches from LLM
        matches = self._get_bulk_matches_from_llm(client_queries, chunk_dict, cluster_id)
        
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
            self.logger.debug(f"  Client: '{client_query_text}'")
            self.logger.debug(f"  Product: '{product_text_for_cosine}'")
            
            if hybrid_score > overall_best_matches.get(cq_id, {}).get('score', -1):
                overall_best_matches[cq_id] = {
                    "score": hybrid_score,
                    "llm_score": llm_score,
                    "cosine_score": cosine_score,
                    "matched_product_index": original_index,
                    "translated_title": translated_title
                }
        
        return overall_best_matches

    def _get_bulk_matches_from_llm(self, client_queries_dict, scraped_chunk_dict, cluster_id):
        """LLM matching function - simple JSON approach like matching.py"""
        
        client_list_str = "\n".join([f'{cq_id}: "{desc}"' for cq_id, desc in client_queries_dict.items()])
        scraped_list_str = "\n".join([f'{p_idx}: "{desc}"' for p_idx, desc in scraped_chunk_dict.items()])

        prompt_data = benchmarking_match_prompt(
            client_list_str=client_list_str,
            scraped_list_str=scraped_list_str
        )
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": prompt_data["system_message"]},
                        {"role": "user", "content": prompt_data["user_template"]}
                    ],
                    temperature=0,
                    response_format={"type": "json_object"}
                )
                
                response_text = response.choices[0].message.content.strip()
                data = json.loads(response_text)
                
                # Extract matches from JSON response
                for key, value in data.items():
                    if isinstance(value, list):
                        self.logger.info(f"Cluster {cluster_id}: LLM returned {len(value)} matches")
                        return value
                
                self.logger.warning(f"Cluster {cluster_id}: JSON object returned, but no list of matches found. Response: {response_text}")
                return []
                
            except json.JSONDecodeError as e:
                self.logger.error(f"Cluster {cluster_id}: JSON parsing error. Raw text: {response_text[:200]}... Error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return []
            except Exception as e:
                self.logger.error(f"Cluster {cluster_id}: LLM API call error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return []
        
        return []

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
                        'ORIGINAL_NORMALISED_DESCRIPTION': safe_get_and_strip(client_row, 'NORMALIZED_DESCRIPTION'),
                        'MATCHED_TITLE_ORIGINAL_LANGUAGE': match_row['title'],
                        'PRICE_CURRENCY': safe_get_and_strip(client_row, 'PURCHASE_CURRENCY','USD'),
                        'UID': safe_get_and_strip(client_row, 'UID'),
                        'UOM': safe_get_and_strip(client_row, 'UOM'),
                        'TRANSLATED_MATCHED_TITLE': best_match_info['translated_title'],
                        'MATCHED_PRICE_RANGE': safe_get_and_strip(match_row, 'price'),
                        'PRODUCT_LINK': safe_get_and_strip(match_row, 'url'),
                        'SIMILARITY_SCORE': round(best_match_info['score'], 4),
                        'EXTRACTED_QUANTITY': client_row.get('QUANTITY', 1),
                        'ORIGINAL_SPEND': client_row.get('Spends (USD)', 0),
                    }
                    results.append(result)
                    
                except Exception as e:
                    self.logger.error(f"Cluster {cluster_id}: Error creating result for client_idx {client_idx}: {e}")
                    continue
        
        return results 