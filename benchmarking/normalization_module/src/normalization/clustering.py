# clustring of the normalised data 

import pandas as pd
import numpy as np
import re
from collections import Counter
import logging

class Clustering:
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans and clusters the DataFrame by the 'B2B Query' column.
        Returns a new DataFrame with cluster information.
        """
        df = df.copy()
        cluster_col = "B2B Query"
        if cluster_col not in df.columns:
            self.logger.warning(f"Column '{cluster_col}' not found. Returning original DataFrame.")
            df["Cluster_ID"] = 0
            return df

        # Clean 'B2B Query'
        df[cluster_col] = df[cluster_col].astype(str).str.replace(r'\bnan\b', '', regex=True).str.strip()
        df[cluster_col] = df[cluster_col].astype(str).str.replace(r'\bnone\b', '', regex=True).str.strip()

        # Remove rows where 'B2B Query' starts with "ZZ" or contains "Product"
        df = df[~df[cluster_col].str.strip().str.startswith("ZZ")].reset_index(drop=True)
        df = df[~df[cluster_col].str.contains(r'\bProduct\b', case=False, na=False)].reset_index(drop=True)

        # Assign Cluster_ID by exact match
        df["Cluster_ID"] = df.groupby(cluster_col, sort=False).ngroup()
        # df["General_Cluster_Query"] = df[cluster_col].str.strip().str.lower()

        return df
