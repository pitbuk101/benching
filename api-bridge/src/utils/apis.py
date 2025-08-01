from fastapi import HTTPException
import httpx
from src.configs.configs_model import Settings as Configuration
from loguru import logger

async def execute_api(client: httpx.AsyncClient, type, config: Configuration, api_path: str, payload: dict=None):
    try:
        if type == "post":
            external_response = await client.post(f"{config.EXTERNAL_API_URL}/{api_path}", json=payload, headers=config.headers, timeout=100)
        elif type == "get":
            external_response = await client.get(f"{config.EXTERNAL_API_URL}/{api_path}", headers=config.headers, timeout=100)
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