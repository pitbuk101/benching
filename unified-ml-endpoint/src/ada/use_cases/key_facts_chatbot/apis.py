import httpx

from ada.use_cases.key_facts_chatbot.configs import Configuration
from ada.use_cases.key_facts_chatbot.encode_secret import generate_jwt
from ada.utils.logs.logger import get_logger

logger = get_logger("kf_chatbot:api")


async def hit_api(client: httpx.AsyncClient, config: Configuration, json_data: dict):
    jwt_token = generate_jwt()
    config.headers["authorization"] = f"Bearer {jwt_token}"

    external_response = await client.post(
        config.external_api_url,
        json=json_data,
        headers=config.headers,
        timeout=None,
    )
    if external_response.status_code != 200:
        raise Exception(f"Error querying external API: {external_response.text}")
    return external_response
