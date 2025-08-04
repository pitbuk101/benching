import pandas as pd
import logging
from tqdm import tqdm
from typing import Optional, Tuple, Generator
import concurrent.futures
import os

from normalise.src.common.llm_service import LLMClient
from normalise.src.common.data_io import load_dataframe
from normalise.src.normalization.preprocessors import apply_operations
from normalise.src.common.utils import clean_text_for_llm
from normalise.src.normalization.clustering import Clustering
import normalise.env as env


class Normalizer:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.client_name = env.CLIENT_NAME
        self.llm_client = LLMClient(logger)
        self.norm_config = env
        self.logger.info(f"Normalizer initialized for client: {self.client_name}")

    def _prepare_batch_items_string(self, batch_series: pd.Series) -> str:
        cleaned_items = batch_series.dropna().astype(str).apply(clean_text_for_llm).tolist()
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
        input_text_col = env.NORM_INPUT_TEXT_COLUMN_FOR_LLM
        llm_output_cols = env.NORM_LLM_OUTPUT_COLUMNS

        self.logger.info(f"Thread processing LLM Batch {batch_idx + 1}")
        self._log_df_sample(current_batch_df, f"Batch {batch_idx + 1} for LLM")

        batch_items_series = current_batch_df[input_text_col]
        batch_items_str = self._prepare_batch_items_string(batch_items_series)

        expected_rows = len(current_batch_df)
        parsed_df = pd.DataFrame(index=current_batch_df['_original_index'], columns=llm_output_cols)
        parsed_df.reset_index(inplace=True)
        parsed_df.rename(columns={'index': '_original_index'}, inplace=True)

        if not batch_items_str.strip():
            self.logger.warning(f"Batch {batch_idx + 1} is empty after cleaning. Skipping LLM call.")
            return parsed_df

        prompt_args = {
            "batch_items_string": batch_items_str,
            "item_count": expected_rows
        }

        try:
            llm_response = self.llm_client.generate_text_completion(
                prompt_key=env.NORM_LLM_PROMPT_KEY,
                prompt_args=prompt_args
            )
            temp_parsed_df = self.llm_client.parse_csv_from_llm_output(
                csv_text=llm_response,
                expected_columns=llm_output_cols,
                expected_rows=expected_rows
            )
            if len(temp_parsed_df) == expected_rows:
                for col in llm_output_cols:
                    parsed_df[col] = temp_parsed_df.get(col)
            else:
                common_rows = min(len(temp_parsed_df), expected_rows)
                for col in llm_output_cols:
                    if col in temp_parsed_df.columns:
                        parsed_df.loc[:common_rows - 1, col] = temp_parsed_df[col][:common_rows].values
        except Exception as e:
            self.logger.error(f"Error processing batch {batch_idx + 1}: {e}", exc_info=True)
        return parsed_df

    def _generate_batches(self, df: pd.DataFrame, batch_size: int) -> Generator[Tuple[int, pd.DataFrame], None, None]:
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i + batch_size]
            if not batch.empty:
                yield i // batch_size, batch

    def run(
        self,
        input_df_path: Optional[str] = None,
        ref_df_path: Optional[str] = None,
        material_description: Optional[str] = None
    ) -> pd.DataFrame:
        if material_description:
            self.logger.info(f"Running normalization for material description.")
            col = env.INPUT_SOURCE_TEXT_COLUMN
            source_col = col if isinstance(col, str) else col[0]
            input_df = pd.DataFrame([{source_col: material_description}])
        elif input_df_path:
            self.logger.info(f"Loading data from: {input_df_path}")
            input_df = load_dataframe(input_df_path, file_type=input_df_path.split('.')[-1])
        else:
            raise ValueError("Provide either input_df_path or material_description.")

        df_original = input_df  
        source_col_config = env.INPUT_SOURCE_TEXT_COLUMN
        df_col_lookup = {c.lower().strip(): c for c in df_original.columns}

        if isinstance(source_col_config, list):
            matched_col = next((df_col_lookup[c.lower().strip()] for c in source_col_config if c.lower().strip() in df_col_lookup), None)
            if not matched_col:
                raise ValueError(f"No matching source text column in {df_original.columns.tolist()}")
        else:
            key = str(source_col_config).lower().strip()
            matched_col = df_col_lookup.get(key)
            if not matched_col:
                raise ValueError(f"Source text column '{source_col_config}' not found.")

        client_df = df_original
        if matched_col != env.NORM_INPUT_TEXT_COLUMN_FOR_LLM:
            client_df.rename(columns={matched_col: env.NORM_INPUT_TEXT_COLUMN_FOR_LLM}, inplace=True)

        client_df.reset_index(inplace=True)
        client_df.rename(columns={'index': '_original_index'}, inplace=True)

        if getattr(env, 'NORM_PRE_LLM_OPERATIONS', None):
            client_df = apply_operations(client_df, env.NORM_PRE_LLM_OPERATIONS)

        valid_df = client_df[
            client_df[env.NORM_INPUT_TEXT_COLUMN_FOR_LLM].notna() &
            client_df[env.NORM_INPUT_TEXT_COLUMN_FOR_LLM].astype(str).str.strip().ne("")
        ]

        batch_size = env.LLM_BATCH_SIZE
        max_workers = env.LLM_MAX_WORKERS_NORMALIZATION
        batch_gen = self._generate_batches(valid_df, batch_size)
        llm_results_list = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_results = list(
                tqdm(
                    executor.map(self._process_single_batch_llm, batch_gen),
                    total=(len(valid_df) + batch_size - 1) // batch_size,
                    desc="LLM Normalization"
                )
            )
            llm_results_list.extend(future_results)

        if llm_results_list:
            llm_df = pd.concat(llm_results_list)
            final_df = pd.merge(df_original, llm_df, left_index=True, right_on='_original_index', how='left')
            final_df.drop(columns=['_original_index'], inplace=True, errors='ignore')
        else:
            final_df = df_original
            for col in env.NORM_LLM_OUTPUT_COLUMNS:
                final_df[col] = pd.NA

        self.logger.info(f"Running clustering on normalized data.")
        clustering = Clustering(self.logger)
        clustered_df = clustering.run(final_df)
        return clustered_df
