from fastapi import HTTPException
import httpx
from src.configs.configs_model import Settings as Configuration
from src.utils.logs import get_custom_logger
logger = get_custom_logger(__name__)

def execute_api(client: httpx.Client, type, config: Configuration, api_path: str, payload: dict=None):
    logger.debug(f"Hitting API: {config.EXTERNAL_API_URL}")
    logger.debug(f"Hitting API Path: {api_path}")
    try:
        if type == "post":
            external_response = client.post(f"{config.EXTERNAL_API_URL}/{api_path}", json=payload, headers=config.headers, timeout=100)
        elif type == "get":
            external_response = client.get(f"{config.EXTERNAL_API_URL}/{api_path}", headers=config.headers, timeout=100)
    except Exception as e:
        logger.exception(f"Error querying external API: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error querying external API: {e}"
        )
    logger.info(f"External API Response: {external_response.text}")
    if external_response.status_code != 200:
        raise HTTPException(
            status_code=external_response.status_code,
            detail=f"Error querying external API: {external_response.text}"
        )
    return external_response