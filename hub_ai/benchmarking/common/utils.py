import pandas as pd
import re
import logging

logger = logging.getLogger(__name__)

def clean_text_for_llm(text: str) -> str:
    """
    Basic cleaning for text before sending to LLM.
    Removes newlines, extra spaces, and normalizes quotes.
    From Adbc_Flow.ipynb: clean_text
    """
    if pd.isna(text):
        return "N/A" # Or "" depending on how LLM should treat it
    text = str(text).replace('"', "'").replace('\n', ' ').replace('\r', '').replace(',', ';')
    text = re.sub(r'\s+', ' ', text).strip() # Replace multiple spaces with single
    return text

def clean_text_for_matching(text: str) -> str:
    """
    More aggressive cleaning for text comparison/matching.
    Converts to lowercase, removes punctuation (except spaces, dots, slashes for versions/sizes).
    From valve_flow.ipynb: client_df['processed_query'] and scraped_df['processed_description']
    """
    if pd.isna(text):
        return ""
    text = str(text).lower()
    # Keep letters, numbers, spaces, dots, slashes. Replace others with space.
    text = re.sub(r'[^a-z0-9\s\./]', ' ', text) 
    text = re.sub(r'\s+', ' ', text).strip() # Consolidate multiple spaces
    return text


def normalize_inch_quotes(text: str) -> str:
    """
    Replaces double quotes with ' inch'.
    From valve_flow.ipynb.
    """
    if pd.isna(text):
        return text
    return str(text).replace('"', ' inch')

def expand_abbreviations(text: str, abbr_map: dict) -> str:
    """
    Expands abbreviations in a text string using a provided map.
    Case-insensitive replacement.
    From Adbc_Flow.ipynb and ALG_FLOW.ipynb (replace_abbreviations).
    """
    if pd.isna(text) or not isinstance(abbr_map, dict):
        return text
    
    text_str = str(text)
    for abbr, full_form in abbr_map.items():
        # Use regex for whole word replacement, case insensitive
        pattern = r'\b' + re.escape(abbr) + r'\b'
        try:
            text_str = re.sub(pattern, full_form, text_str, flags=re.IGNORECASE)
        except re.error as e:
            logger.warning(f"Regex error while expanding abbreviation '{abbr}': {e}")
    return text_str.strip()


def parse_price_range(price_str: str, strategy: str = "max_from_range_usd") -> float:
    """
    Parses a price string (e.g., "US$ 10.50 - 12.00", "US$ 5.00") and extracts a single price.
    Strategies: "max_from_range_usd", "min_from_range_usd", "avg_from_range_usd".
    From Adbc_Flow.ipynb.
    """
    if pd.isna(price_str):
        return 0.0
    
    price_str = str(price_str).upper().replace("US$", "").replace("USD", "").strip()
    
    numbers = []
    # Find all sequences of digits, optionally with a decimal point
    # This regex is a bit more robust for various formats
    found_numbers = re.findall(r'\d+\.\d+|\d+', price_str)
    for num_str in found_numbers:
        try:
            numbers.append(float(num_str))
        except ValueError:
            logger.warning(f"Could not convert '{num_str}' to float from price string '{price_str}'")
            continue
            
    if not numbers:
        return 0.0

    if "max_from_range" in strategy.lower():
        return max(numbers)
    elif "min_from_range" in strategy.lower():
        return min(numbers)
    elif "avg_from_range" in strategy.lower():
        return sum(numbers) / len(numbers) if numbers else 0.0
    else: # Default to max or first found if strategy is unknown
        logger.warning(f"Unknown price parsing strategy: {strategy}. Defaulting to max.")
        return max(numbers)