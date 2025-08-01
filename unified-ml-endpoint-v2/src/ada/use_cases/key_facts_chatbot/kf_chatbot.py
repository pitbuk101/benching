import httpx

from ada.use_cases.key_facts_chatbot.apis import hit_api
from ada.use_cases.key_facts_chatbot.configs import kf_chatbot_config
from ada.use_cases.key_facts_chatbot.datamodels import ErrorResponse, QueryRequest
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time

logger = get_logger("kf_chatbot")


@log_time
async def kf_chatbot(request: QueryRequest, tenant_id: str):
    """
    This Endpoint acceps a query and fetches the result from KF chatbot
    """
    try:
        async with httpx.AsyncClient() as client:
            # extract the query from the request
            question = request.query
            # create the payload for the create asking task model
            json_data = {"query": question, "tenant_id": tenant_id}
            # Hit the api
            response = await hit_api(client, kf_chatbot_config, json_data)
            return response.json()
    except Exception as e:
        logger.info(f"Error: {e} ")
        return ErrorResponse(error="No data found", status_code=200)
