import asyncio
from typing import Union
from loguru import logger
import json
import httpx
from time import sleep
from fastapi import APIRouter, Request
from src.models.datamodels import ErrorResponse, QueryRequest, QueryResponse
from src.utils.apis import execute_api
from src.utils.snowflake_driver import SnowflakeDatabaseFactory
from src.configs.configs_model import config


bridge_router = APIRouter()


@bridge_router.post("/query", response_model=Union[QueryResponse, ErrorResponse])
async def query(request: QueryRequest, original_request: Request):
    """
    This Endpoint accepts a query and fetches the result from wren ai service
    """
    try:
        async with httpx.AsyncClient() as client:
            logger.debug(f"Original Request: {original_request.json()}")
            # extract the query from the request
            question = request.query
            tenant_id = request.tenant_id
            region = request.region
            # !: Since there is only 1 client in US region
            # !: We are making sure that region is always set to eu
            # TODO: This code needs to go away once we have multiple clients in US region
            conn_params = config.conn_params[tenant_id]
            # logger.info(f"Connection Params: {conn_params}")
            temp_tenant_id = conn_params["temp_tenant_id"]

            region = conn_params["region"]
            logger.info(f"Tenant ID: {tenant_id}")
            logger.info(f"Region: {region}")
            logger.info(f"Temp Tenant ID: {temp_tenant_id}")
            # Setting Up the payload for the external api
            json_data = {"query": question, "tenant_id": tenant_id}
            # Hit the api
            config.headers["authorization"] = original_request.headers.get("authorization")
            config.headers["service"] = "api-bridge-service"
            logger.debug(f"payload: {json_data}")
            response = await execute_api(client=client,type="post",config=config,api_path="asks", payload=json_data)
            # Extract the query_id from the response
            response_json = response.json()
            logger.info(f"Asks API Response: {json.dumps(response_json, indent=4)}")
            query_id = response_json["query_id"]
            # Check the status of the query
            check=True
            while check:
                response = await execute_api(client=client,type="get", config=config, api_path=f"asks/{query_id}/result")
                response_json = response.json()
                logger.info(f"Asks/{query_id}/result API Response: {json.dumps(response_json, indent=4)}")
                if response_json['status'].lower() == 'finished':
                    check=False
                elif response_json['status'].lower() == 'failed':
                    return ErrorResponse(error="No data found",status_code=200)
                else:
                    # sleep(2)
                    await asyncio.sleep(2)
            # Extract SQL from successful 
            sql = response_json['response'][0]['sql']
            fixed_query = response_json['response'][0]['fixed_query']
            # TODO: Call DB asnyc directly instead of preview data model
            logger.info("Using Snowflake Driver")
            logger.info(f"Fetching creds for region: {region}")
            # Cleaning Up the SQL
            sql = (
                sql
                .replace('DATA_', 'DATA.')
                # ! Exception for query with TXT_DATA_POINT
                .replace('TXT_DATA.POINT', 'TXT_DATA_POINT')
                .replace('"', '')

            )
            sql = f"USE DATABASE \"{temp_tenant_id}\";{sql}"
            logger.info(f"Query: {sql}")
            db = SnowflakeDatabaseFactory(conn_params)
            logger.info("SF Creation Success")
            result = await db.query(sql)
            logger.info(f"Query Result: {result}")
            return QueryResponse(original_query=request.query,result=result,status_code=200, sql=sql,fixed_query=fixed_query)
    except Exception as e:
        logger.exception(f"Error: {e} ")
        return ErrorResponse(error="No data found",status_code=200)
