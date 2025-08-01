import pandas as pd
from ada.utils.logs.time_logger import log_time
from ada.use_cases.key_facts_chatbot.datamodels import QueryRequest
from ada.use_cases.key_facts_chatbot.kf_chatbot import kf_chatbot


def extract_data_from_response(response_dict, use_driver):
    if "error" in response_dict:
        return pd.DataFrame({"error": [response_dict["error"]]})
    if use_driver:
        columns = response_dict["result"]["columns"]
        values = response_dict["result"]["data"]
        df = pd.DataFrame(values, columns=columns)
    else:
        columns = [col["name"] for col in response_dict["result"]["data"]["previewData"]["columns"]]
        values = response_dict["result"]["data"]["previewData"]["data"]
        df = pd.DataFrame(values, columns=columns)
    return df, response_dict["sql"], response_dict["fixed_query"]

@log_time
async def fetch(data, tenant_id, generation_type=""):
    try:
        query = QueryRequest(query=data)
        response = await kf_chatbot(query, tenant_id)

        res = extract_data_from_response(dict(response), query.use_driver)

        return res
    except Exception as e:
        raise e
