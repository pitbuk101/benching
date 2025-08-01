import pandas as pd
import logging
from tqdm import tqdm
from omegaconf import DictConfig, ListConfig
from typing import List, Dict, Optional, Tuple 
import concurrent.futures 
import os 

from src.common.llm_service import LLMClient
from src.common.data_io import load_dataframe 
from src.normalization.preprocessors import apply_operations 
from src.common.utils import clean_text_for_llm 
from src.normalization.clustering import Clustering

class Normalizer:
    def __init__(self, config: DictConfig, logger: logging.Logger):
        self.config = config 
        self.norm_config = config.normalization 
        self.client_name = config.client_name
        self.logger = logger
        self.llm_client = LLMClient(config, logger) 
        self.logger.info(f"Normalizer initialized for client: {self.client_name}")

    def _prepare_batch_items_string(self, batch_series: pd.Series) -> str:
        cleaned_items = [clean_text_for_llm(str(item)) for item in batch_series if pd.notna(item)]
        return "\n".join(cleaned_items)

    def _log_df_sample(self, df: pd.DataFrame, df_name: str, num_rows: int = 2):
        if df.empty:
            self.logger.info(f"DataFrame '{df_name}' is empty.")
            return
        self.logger.info(f"First {min(num_rows, len(df))} rows of '{df_name}':")
        try:
            self.logger.info("\n" + df.head(num_rows).to_string())
        except Exception as e:
            self.logger.warning(f"Could not log DataFrame sample for '{df_name}': {e}")

    def _process_single_batch_llm(self, batch_info: Tuple[int, pd.DataFrame]) -> pd.DataFrame:
        batch_idx, current_batch_df = batch_info
        input_text_col = self.norm_config.input_text_column_for_llm
        llm_output_cols = self.norm_config.llm_output_columns
        
        self.logger.info(f"Thread processing LLM Batch {batch_idx + 1}")
        self._log_df_sample(current_batch_df, f"current_batch_df (Batch {batch_idx + 1}) for LLM")

        batch_items_series = current_batch_df[input_text_col]
        batch_items_str = self._prepare_batch_items_string(batch_items_series)
        
        expected_num_rows_for_llm = len(current_batch_df)
        parsed_llm_df_for_batch = pd.DataFrame(index=current_batch_df['_original_index'].values, columns=llm_output_cols)
        parsed_llm_df_for_batch = parsed_llm_df_for_batch.reset_index().rename(columns={'index': '_original_index'})

        if not batch_items_str.strip():
            self.logger.warning(f"Batch {batch_idx + 1} is empty after cleaning. Skipping LLM call.")
            return parsed_llm_df_for_batch

        prompt_args = {
            "batch_items_string": batch_items_str,
            "item_count": expected_num_rows_for_llm
        }
        self.logger.debug(f"Prompt arguments for batch {batch_idx + 1}: {prompt_args}")
        
        try:
            llm_response_text = self.llm_client.generate_text_completion(
                prompt_key=self.norm_config.llm_prompt_key,
                prompt_args=prompt_args
            )
            temp_parsed_df = self.llm_client.parse_csv_from_llm_output(
                csv_text=llm_response_text,
                expected_columns=llm_output_cols,
                expected_rows=expected_num_rows_for_llm
            )
            self.logger.debug(f"Batch {batch_idx + 1} processed by LLM. Parsed results: {len(temp_parsed_df)} rows.")

            if len(temp_parsed_df) == expected_num_rows_for_llm:
                for col in llm_output_cols:
                    if col in temp_parsed_df.columns:
                         parsed_llm_df_for_batch[col] = temp_parsed_df[col].values
            else: 
                self.logger.warning(
                    f"LLM output or parsing for batch {batch_idx + 1} resulted in {len(temp_parsed_df)} rows, "
                    f"expected {expected_num_rows_for_llm}. Will result in NaNs for some items in this batch."
                )
                common_rows = min(len(temp_parsed_df), expected_num_rows_for_llm)
                if common_rows > 0:
                    for col_idx, col_name in enumerate(llm_output_cols):
                        if col_name in temp_parsed_df.columns and col_idx < len(temp_parsed_df.columns): 
                             parsed_llm_df_for_batch.loc[parsed_llm_df_for_batch.index[:common_rows], col_name] = temp_parsed_df.iloc[:common_rows, col_idx].values
        except Exception as e:
            self.logger.error(f"Error processing batch {batch_idx + 1} with LLM: {e}", exc_info=True)
        
        return parsed_llm_df_for_batch

    def run(self, input_df_path: str, ref_df_path: Optional[str] = None) -> pd.DataFrame:
        self.logger.info(f"Starting normalization for input: {input_df_path}")
        df_original = load_dataframe(input_df_path, file_type=input_df_path.split('.')[-1])
        self.logger.info(f"Loaded DataFrame with columns: {df_original.columns.tolist()} and shape: {df_original.shape}")

        # Support source_text_column as a list of possible column names
        source_text_col_config = self.config.input_data.source_text_column
        self.logger.info(f"source_text_col_config type: {type(source_text_col_config)}, value: {source_text_col_config}")

        # Normalize DataFrame columns for matching
        df_columns_normalized = {col.strip().lower(): col for col in df_original.columns}
        self.logger.debug(f"Normalized DataFrame columns for matching: {df_columns_normalized}")

        if isinstance(source_text_col_config, (list, ListConfig)):
            found_col = None
            for col_option in source_text_col_config:
                col_option_normalized = col_option.strip().lower()
                self.logger.debug(f"Trying to match config column '{col_option}' (normalized: '{col_option_normalized}')")
                if col_option_normalized in df_columns_normalized:
                    found_col = df_columns_normalized[col_option_normalized]
                    self.logger.info(f"Matched source text column: '{found_col}'")
                    break
            if not found_col:
                self.logger.error(
                    f"None of the source text columns {source_text_col_config} found in uploaded file. "
                    f"Available columns: {df_original.columns.tolist()}"
                )
                raise ValueError(
                    f"None of the source columns {source_text_col_config} found in uploaded file."
                )
            source_text_col = found_col
        else:
            col_option_normalized = source_text_col_config.strip().lower()
            self.logger.debug(f"Trying to match config column '{source_text_col_config}' (normalized: '{col_option_normalized}')")
            if col_option_normalized not in df_columns_normalized:
                self.logger.error(
                    f"Source text column '{source_text_col_config}' not found in uploaded file. "
                    f"Available columns: {df_original.columns.tolist()}"
                )
                raise ValueError(
                    f"Source column '{source_text_col_config}' not in uploaded file."
                )
            source_text_col = df_columns_normalized[col_option_normalized]
            self.logger.info(f"Matched source text column: '{source_text_col}'")
        
        client_df = df_original.copy()
        # Rename the source column to the internal standard name for processing
        if source_text_col != self.norm_config.input_text_column_for_llm:
            self.logger.info(f"Renaming column '{source_text_col}' to '{self.norm_config.input_text_column_for_llm}' for LLM processing.")
            client_df.rename(columns={source_text_col: self.norm_config.input_text_column_for_llm}, inplace=True)
        else:
            self.logger.info(f"No renaming needed for source column '{source_text_col}'.")

        self.logger.info(f"Loaded client data: {len(client_df)} rows")
        self._log_df_sample(client_df, "Initial client_df")

        client_df = client_df.reset_index().rename(columns={'index': '_original_index'})
        self.logger.debug(f"Client DataFrame after reset_index: columns={client_df.columns.tolist()}")

        if self.norm_config.get("pre_llm_operations"):
            self.logger.info("Applying pre-LLM processing operations...")
            client_df = apply_operations(client_df, self.norm_config.pre_llm_operations, config=self.config) 
            self.logger.info("Pre-LLM processing complete.")
            self._log_df_sample(client_df, "client_df after pre-LLM processing")

        valid_df_for_llm = client_df[client_df[self.norm_config.input_text_column_for_llm].notna() & (client_df[self.norm_config.input_text_column_for_llm].astype(str).str.strip() != "")].copy()
        self.logger.info(f"Number of valid rows for LLM processing: {len(valid_df_for_llm)} (out of {len(client_df)})")
        self._log_df_sample(valid_df_for_llm, "valid_df_for_llm")

        batch_size = self.config.llm.get("batch_size", 10)
        self.logger.info(f"Batch size for LLM: {batch_size}")
        batches_to_process = [valid_df_for_llm.iloc[i:i + batch_size] for i in range(0, len(valid_df_for_llm), batch_size) if not valid_df_for_llm.iloc[i:i + batch_size].empty]
        self.logger.info(f"Total batches to process: {len(batches_to_process)}")

        llm_results_list = []
        max_workers = self.config.llm.get("max_workers_normalization", os.cpu_count() or 1)
        self.logger.info(f"Using {max_workers} parallel workers for LLM normalization.")

        if batches_to_process:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                batch_info_list = list(enumerate(batches_to_process))
                self.logger.info(f"Submitting {len(batch_info_list)} batches to ThreadPoolExecutor.")
                future_results = list(tqdm(executor.map(self._process_single_batch_llm, batch_info_list), 
                                           total=len(batches_to_process), 
                                           desc=f"Parallel LLM Normalization"))
                llm_results_list.extend(future_results)
                self.logger.info(f"LLM processing complete for all batches.")
        
        if llm_results_list:
            all_llm_results_df = pd.concat(llm_results_list)
            self.logger.info(f"Concatenated all LLM batch results: {len(all_llm_results_df)} rows. Columns: {all_llm_results_df.columns.tolist()}")
            # Merge original data with LLM results
            final_df = pd.merge(df_original, all_llm_results_df, left_index=True, right_on='_original_index', how='left')
            self.logger.info(f"Merged original DataFrame with LLM results. Shape: {final_df.shape}")
            if '_original_index' in final_df.columns:
                final_df.drop(columns=['_original_index'], inplace=True)
                self.logger.info("Dropped '_original_index' column after merge.")
            # Save to local directory
            # final_df.to_csv("./data/temp/final_normalized_output.csv", index=False)
            self.logger.info("Saved final normalized output to './data/temp/final_normalized_output.csv'")
        else:
            self.logger.warning("No results were generated by the LLM process.")
            final_df = df_original.copy()
            for col in self.norm_config.llm_output_columns:
                final_df[col] = pd.NA
            self.logger.info(f"Added empty LLM output columns: {self.norm_config.llm_output_columns}")
        
        self.logger.info(f"Normalization complete. Final DataFrame shape: {final_df.shape}")

        # Apply Post Normalization Operations i.e clustering (below is the refrence code to do some clustering, maybe we can have a clustring.py and will import here): 
        clustering = Clustering(self.logger)
        new_final_df = clustering.run(final_df)
        new_final_df.to_csv("./data/temp/final_normalized_clustered_output.csv", index=False)

        return new_final_df