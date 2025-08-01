import httpx
import re
from bs4 import BeautifulSoup

from src.utils.logs import get_custom_logger
logger = get_custom_logger(__name__)

def extract_url(text: str) -> str:
    match = re.search(r'https?://\S+', text)
    return match.group(0) if match else ''

def extract_text_from_url(url: str) -> str:
    
    try:
        url = extract_url(url)
        with httpx.Client(timeout=100) as client:
            response = client.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove scripts and styles
            for script_or_style in soup(['script', 'style']):
                script_or_style.decompose()

            # Get text and clean it
            text = soup.get_text(separator=' ', strip=True)
            return text

    except httpx.HTTPError as e:
        logger.info(f"Request failed: {e}")
        return f"Request failed: {e}"
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return f"An error occurred: {e}"
