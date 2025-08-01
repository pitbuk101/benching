import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

def load_dataframe(file_path: str, file_type: str = None, **kwargs) -> pd.DataFrame:
    """
    Loads a dataframe from a file.
    Automatically determines file_type from extension if not provided.
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_type:
        file_type = file_path.split('.')[-1].lower()

    logger.info(f"Loading dataframe from: {file_path} (type: {file_type})")
    try:
        if file_type == 'csv':
            return pd.read_csv(file_path, **kwargs)
        elif file_type in ['xls', 'xlsx']:
            return pd.read_excel(file_path, **kwargs)
        # Add more types as needed (e.g., parquet, json)
        else:
            logger.error(f"Unsupported file type: {file_type} for file: {file_path}")
            raise ValueError(f"Unsupported file type: {file_type}")
    except Exception as e:
        logger.error(f"Error loading dataframe from {file_path}: {e}")
        raise

def save_dataframe(df: pd.DataFrame, file_path: str, file_type: str = None, index: bool = False, **kwargs):
    """
    Saves a dataframe to a file.
    Automatically determines file_type from extension if not provided.
    """
    if not file_type:
        file_type = file_path.split('.')[-1].lower()

    # Ensure the directory exists
    dir_name = os.path.dirname(file_path)
    if dir_name: # Check if dirname is not empty (e.g. for files in current dir)
        os.makedirs(dir_name, exist_ok=True)

    logger.info(f"Saving dataframe to: {file_path} (type: {file_type})")
    try:
        if file_type == 'csv':
            df.to_csv(file_path, index=index, **kwargs)
        elif file_type in ['xls', 'xlsx']:
            df.to_excel(file_path, index=index, **kwargs)
        # Add more types as needed
        else:
            logger.error(f"Unsupported file type for saving: {file_type} for file: {file_path}")
            raise ValueError(f"Unsupported file type for saving: {file_type}")
        logger.info(f"Successfully saved dataframe to {file_path}")
    except Exception as e:
        logger.error(f"Error saving dataframe to {file_path}: {e}")
        raise
