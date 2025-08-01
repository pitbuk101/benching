import gzip
import json
import logging
from io import BytesIO

import azure.functions as func
from pg_connector import PGConnector

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


def _create_error_message(error: str) -> str:
    return json.dumps({"error": f"Internal Error: {error}"})


@app.route(route="postgres_relay")
def postgres_relay(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")
    data = req.get_json()
    logging.info(f"Data received: {data}")

    query_to_execute = data.get("query", None)
    if not isinstance(query_to_execute, str):
        func.HttpResponse(
            _create_error_message("The input `query` should be a string type."),
            status_code=442,
        )

    cursor_type = data.get("cursor_type", None)
    if not isinstance(cursor_type, str):
        func.HttpResponse(
            _create_error_message("The input `cursor` should be a string type."),
            status_code=442,
        )

    tenant_id = data.get("tenant_id", None)
    if not isinstance(tenant_id, str):
        func.HttpResponse(
            _create_error_message("The input `tenant_id` should be a string type."),
            status_code=442,
        )

    tenant_key = data.get("tenant_key", None)
    if not isinstance(tenant_key, str):
        func.HttpResponse(
            _create_error_message("The input `tenant_key` should be a string type."),
            status_code=442,
        )

    values = data.get("values", None)
    if values and not isinstance(values, list):
        func.HttpResponse(
            _create_error_message("The input `values` should be a list type."),
            status_code=442,
        )

    query_kwargs = data.get("query_kwargs", None)
    if query_kwargs and not isinstance(query_kwargs, dict):
        func.HttpResponse(
            _create_error_message("The input `query_kwargs` should be a dict type."),
            status_code=442,
        )
    try:
        pg_conn = PGConnector(tenant_id=tenant_id, tenant_key=tenant_key, cursor_type=cursor_type)

        execution_args = {
            "query": query_to_execute,
        }
        if values:
            execution_args["values"] = values
        if query_kwargs:
            for key, value in query_kwargs.items():
                logging.warning("Key %s not supported.", key)

        results = pg_conn.execute(*execution_args.values())
        response_json = json.dumps(results, default=str)
        # Compress the JSON string using gzip
        compressed_data = BytesIO()
        with gzip.GzipFile(fileobj=compressed_data, mode="wb") as gz_file:
            gz_file.write(response_json.encode("utf-8"))

            # Get the compressed data as bytes
        compressed_data_bytes = compressed_data.getvalue()
        return func.HttpResponse(
            compressed_data_bytes,
            status_code=200,
            headers={
                "Content-Encoding": "gzip",
                "Content-Type": "application/json",
                "something": "simething",
            },
        )
    except Exception as e:
        return func.HttpResponse(_create_error_message(str(e)), status_code=500)
