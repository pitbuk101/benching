"""All file related io functions, such as read and write."""
import os

import pandas as pd

from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger

azml_conf = read_config("azml_deployment.yaml")
azml_global_conf = azml_conf["global"]
log = get_logger("read_parquet_file")


def read_parquet(
    file_path: str, convert_to_str=False, dropna=False, convert_dtypes=None
) -> pd.DataFrame:
    """
    Returning data from parquet file as DataFrame

    Args:
        file_path (str): absolute path of the input file
        convert_to_str (bool): Flag to check if all the columns to be converted to string
        dropna (bool): Flag to check if NaN / empty rows to be dropped
        convert_dtypes (None | Dict(str, obj))

    Returns:
        parquet_df: Input file data as DataFrame with pre-processing if applicable
    """
    if not os.path.exists(file_path):
        log.info("Error reading parquet file from %s. Exiting", file_path)
        raise FileNotFoundError

    parquet_df = pd.read_parquet(file_path)

    # Convert specific columns to string
    if convert_dtypes:
        for column, dtype in convert_dtypes.items():
            parquet_df[column] = parquet_df[column].astype(dtype)

    if convert_to_str:
        parquet_df = parquet_df.map(str)

    if dropna:
        parquet_df = parquet_df.dropna()

    return parquet_df
