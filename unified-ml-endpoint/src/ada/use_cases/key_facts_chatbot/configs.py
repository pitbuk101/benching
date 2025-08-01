import os

from pydantic import BaseModel

from ada.utils.config.config_loader import read_config

kf_config = read_config("kf_chatbot.yaml")


class Configuration(BaseModel):
    external_api_url: str = kf_config["external_api_url"]
    headers: dict = {
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Origin": kf_config["origin"],
        "Referer": kf_config["referer"],
        "accept": "*/*",
        "content-type": "application/json",
        "authorization": " ",
    }
    enabled: bool = kf_config["kf_chatbot_enabled"]
    open_world_response: bool = kf_config["open_world_response"]
    conn_params: dict = kf_config["conn_params"]
    conn_params["password"] = os.getenv("SNOWFLAKE_PASSWORD")


kf_chatbot_config = Configuration()
