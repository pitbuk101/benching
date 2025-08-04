import pandas as pd
import logging
from typing import List, Dict, Any
import normalise.env as env

from normalise.src.common.utils import expand_abbreviations, normalize_inch_quotes, clean_text_for_llm

logger = logging.getLogger(__name__)

# --- Preprocessor Registry ---
PREPROCESSOR_REGISTRY = {}

def register_preprocessor(name):
    def decorator(func):
        PREPROCESSOR_REGISTRY[name] = func
        return func
    return decorator

# --- Preprocessing Functions ---
# (Signatures updated to accept df as first arg, then specific args from config)

@register_preprocessor("extract_regex")
def extract_with_regex(df: pd.DataFrame, source_column: str, target_column: str, pattern: str, 
                       fail_on_error: bool = False, **kwargs) -> pd.DataFrame:
    logger.info(f"Applying regex extraction: '{source_column}' -> '{target_column}' with pattern '{pattern}'")
    if source_column not in df.columns:
        msg = f"Source column '{source_column}' not found in DataFrame for regex extraction."
        logger.error(msg)
        if fail_on_error: raise KeyError(msg)
        return df
    try:
        df[target_column] = df[source_column].astype(str).str.extract(pattern, expand=False)
    except Exception as e:
        msg = f"Error during regex extraction on column '{source_column}': {e}"
        logger.error(msg)
        if fail_on_error: raise
    return df

@register_preprocessor("pad_string")
def pad_string_column(df: pd.DataFrame, column: str, length: int, char: str, 
                      side: str = 'right', fail_on_error: bool = False, **kwargs) -> pd.DataFrame:
    logger.info(f"Padding string column: '{column}' to length {length} with '{char}' on {side}")
    if column not in df.columns:
        msg = f"Column '{column}' not found in DataFrame for padding."
        logger.error(msg)
        if fail_on_error: raise KeyError(msg)
        return df
    try:
        if side == 'right':
            df[column] = df[column].apply(lambda x: str(x).ljust(length, char) if pd.notnull(x) else x)
        elif side == 'left':
            df[column] = df[column].apply(lambda x: str(x).rjust(length, char) if pd.notnull(x) else x)
        else:
            raise ValueError(f"Invalid padding side: {side}. Choose 'left' or 'right'.")
    except Exception as e:
        msg = f"Error padding column '{column}': {e}"
        logger.error(msg)
        if fail_on_error: raise
    return df

@register_preprocessor("rename_column")
def rename_df_column(df: pd.DataFrame, old_name: str, new_name: str, 
                     fail_on_error: bool = False, **kwargs) -> pd.DataFrame:
    logger.info(f"Renaming column: '{old_name}' -> '{new_name}'")
    if old_name not in df.columns:
        msg = f"Column '{old_name}' not found for renaming."
        logger.error(msg)
        if fail_on_error: raise KeyError(msg)
        return df
    try:
        df.rename(columns={old_name: new_name}, inplace=True)
    except Exception as e:
        msg = f"Error renaming column '{old_name}': {e}"
        logger.error(msg)
        if fail_on_error: raise
    return df

@register_preprocessor("merge_with_reference")
def merge_df_with_reference(df: pd.DataFrame, ref_df: pd.DataFrame, 
                            left_on: str, right_on: str, how: str = 'left', 
                            suffixes: List[str] = None, fail_on_error: bool = False, **kwargs) -> pd.DataFrame:
    logger.info(f"Merging DataFrame on '{left_on}' (left) and '{right_on}' (right), how='{how}'")
    if ref_df is None: # ref_df is passed directly, not from kwargs
        msg = "Reference DataFrame (ref_df) is None for merge operation."
        logger.error(msg)
        if fail_on_error: raise ValueError(msg)
        return df
    if left_on not in df.columns:
        msg = f"Merge key '{left_on}' not found in left DataFrame."
        logger.error(msg)
        if fail_on_error: raise KeyError(msg)
        return df
    if right_on not in ref_df.columns:
        msg = f"Merge key '{right_on}' not found in reference DataFrame."
        logger.error(msg)
        if fail_on_error: raise KeyError(msg)
        return df
        
    df[left_on] = df[left_on].astype(str)
    ref_df[right_on] = ref_df[right_on].astype(str)

    try:
        merged_df = pd.merge(df, ref_df, left_on=left_on, right_on=right_on, how=how, suffixes=suffixes or ('_x', '_y'))
        return merged_df
    except Exception as e:
        msg = f"Error during merge operation: {e}"
        logger.error(msg)
        if fail_on_error: raise
    return df 

@register_preprocessor("dropna")
def drop_na_rows(df: pd.DataFrame, subset_columns: List[str], fail_on_error: bool = False, **kwargs) -> pd.DataFrame:
    logger.info(f"Dropping NA rows based on subset: {subset_columns}")
    valid_subset = [col for col in subset_columns if col in df.columns]
    if len(valid_subset) != len(subset_columns):
        missing = set(subset_columns) - set(valid_subset)
        msg = f"One or more subset columns for dropna not found: {missing}"
        logger.warning(msg) 
        if not valid_subset and fail_on_error: 
             raise KeyError(msg)
        if not valid_subset:
            return df 
    try:
        df.dropna(subset=valid_subset, inplace=True)
    except Exception as e:
        msg = f"Error dropping NA rows: {e}"
        logger.error(msg)
        if fail_on_error: raise
    return df

@register_preprocessor("strip_column")
def strip_column_whitespace(df: pd.DataFrame, column: str, fail_on_error: bool = False, **kwargs) -> pd.DataFrame:
    logger.info(f"Stripping whitespace from column: '{column}'")
    if column not in df.columns:
        msg = f"Column '{column}' not found for stripping whitespace."
        logger.error(msg)
        if fail_on_error: raise KeyError(msg)
        return df
    try:
        df[column] = df[column].astype(str).str.strip()
    except Exception as e:
        msg = f"Error stripping column '{column}': {e}"
        logger.error(msg)
        if fail_on_error: raise
    return df

@register_preprocessor("clean_text_basic")
def apply_clean_text_for_llm(df: pd.DataFrame, column: str, fail_on_error: bool = False, **kwargs) -> pd.DataFrame:
    logger.info(f"Applying basic text cleaning (for LLM) to column: '{column}'")
    if column not in df.columns:
        msg = f"Column '{column}' not found for basic text cleaning."
        logger.error(msg)
        if fail_on_error: raise KeyError(msg)
        return df
    try:
        df[column] = df[column].apply(clean_text_for_llm)
    except Exception as e:
        msg = f"Error applying basic text cleaning to column '{column}': {e}"
        logger.error(msg)
        if fail_on_error: raise
    return df

@register_preprocessor("normalize_inches")
def apply_normalize_inch_quotes(df: pd.DataFrame, column: str, fail_on_error: bool = False, **kwargs) -> pd.DataFrame:
    logger.info(f"Normalizing inch quotes in column: '{column}'")
    if column not in df.columns:
        msg = f"Column '{column}' not found for normalizing inch quotes."
        logger.error(msg)
        if fail_on_error: raise KeyError(msg)
        return df
    try:
        df[column] = df[column].apply(normalize_inch_quotes)
    except Exception as e:
        msg = f"Error normalizing inch quotes in column '{column}': {e}"
        logger.error(msg)
        if fail_on_error: raise
    return df

@register_preprocessor("apply_abbreviations")
def apply_expand_abbreviations(df: pd.DataFrame, column: str, abbr_map: Dict = None, # Made abbr_map optional here
                               abbreviations_map_key: str = None, # Added to get from config if abbr_map not passed
                               fail_on_error: bool = False, **kwargs) -> pd.DataFrame:
    logger.info(f"Expanding abbreviations in column: '{column}'")
    if column not in df.columns:
        msg = f"Column '{column}' not found for expanding abbreviations."
        logger.error(msg)
        if fail_on_error: raise KeyError(msg)
        return df

    # If abbr_map is not directly provided, try to get it using abbreviations_map_key from kwargs (passed from apply_operations)
    if abbr_map is None and abbreviations_map_key and "config_maps" in kwargs: # config_maps would be main_config.abbreviations_maps
        abbr_map = kwargs["config_maps"].get(abbreviations_map_key)

    if not isinstance(abbr_map, dict):
        msg = f"Abbreviations map is not a dictionary or not found for column '{column}'. Key: {abbreviations_map_key}"
        logger.warning(msg) # Warn instead of error if map is missing, effectively skipping this step
        return df # Return df unchanged if no valid map
    try:
        df[column] = df[column].apply(lambda x: expand_abbreviations(x, abbr_map))
    except Exception as e:
        msg = f"Error expanding abbreviations in column '{column}': {e}"
        logger.error(msg)
        if fail_on_error: raise
    return df


def apply_operations(df: pd.DataFrame, operations: List[Dict[str, Any]], ref_df: pd.DataFrame = None) -> pd.DataFrame:
    """
    Applies a list of preprocessing operations to the DataFrame.
    Each operation is an OmegaConf node from the list in the config.
    """
    if not operations:
        return df
    
    current_df = df.copy()
    for op_config_node in operations: # op_config_node is an OmegaConf node
        op_type = op_config_node.get("type")
        if not op_type:
            logger.warning(f"Operation config missing 'type': {op_config_node}. Skipping.")
            continue
        
        preprocessor_func = PREPROCESSOR_REGISTRY.get(op_type)
        if not preprocessor_func:
            logger.warning(f"Unknown preprocessor type: '{op_type}'. Skipping operation: {op_config_node}")
            continue
            
        # Convert the OmegaConf node for this specific operation's parameters to a Python dict
        # This avoids issues when trying to modify it or pass to functions expecting dicts.
        # 'type' is already extracted, so we pass the rest.
        params_from_yaml = {k: v for k, v in op_config_node.items() if k != "type"}

        logger.info(f"Executing preprocessor: {op_type} with params from YAML: {params_from_yaml}")
        
        try:
            # Prepare arguments for the preprocessor function
            call_args = params_from_yaml.copy() # Start with YAML params

            # Special handling for operations needing additional runtime data (like ref_df or main config for maps)
            if op_type == "merge_with_reference":
                # ref_df is passed as a direct keyword argument to merge_df_with_reference
                current_df = preprocessor_func(current_df, ref_df=ref_df, **call_args)
            elif op_type == "apply_abbreviations":
                # Pass the main config's abbreviation maps if needed by the preprocessor
                if "abbr_map" not in call_args and call_args.get("abbreviations_map_key") and env.config and hasattr(env.config, "abbreviations_maps"):
                    call_args["config_maps"] = env.config.abbreviations_maps
                current_df = preprocessor_func(current_df, **call_args)
            else:
                # For other functions, pass params from YAML directly
                current_df = preprocessor_func(current_df, **call_args)
        except Exception as e:
            logger.error(f"Failed to apply operation {op_type} with params {params_from_yaml}: {e}", exc_info=True)
            if op_config_node.get("fail_on_error", False): 
                raise
            logger.warning(f"Continuing after error in operation {op_type} as fail_on_error is false or not set.")
    return current_df