"""Base class for models."""

import logging
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from ada.utils.config.config_loader import read_config
from ada.utils.io.misc import move_dict_key_to_top, sort_dict_by_key
from ada.utils.metrics.context_manager import get_ai_cost_tags

config = read_config("models.yml")
log = logging.getLogger(__name__)


class Model:  # pylint: disable=too-many-instance-attributes, too-few-public-methods
    """
    The 'key' parameter can be used to steer the model selection (not yet implemented)
    """

    def __init__(self, name: str = "", temp: float = 0.0):
        # Add general models
        self.model_dict = {}
        for model_config in config["models"]:
            model_name = model_config["name"]
            self.model_dict[model_name] = {
                "name": model_config["model_name"],
                "host": model_config["host"],
                "max_tokens": model_config["max_tokens"],
            }

        self.model_dict = sort_dict_by_key(self.model_dict)
        # Adding OpenAI chat model on top
        self.model_dict = move_dict_key_to_top("OpenAI ChatGPT (16k)", self.model_dict)

        # Get input from user if no model name is provided
        self.selected_model = self._find_model_key_by_name(name)

        self.model_name = self.model_dict.get(self.selected_model, {}).get("name", name)
        self.model_host = self.model_dict.get(self.selected_model, {}).get("host", "")

        if name == "":
            self.selected_temp = 0.0
        else:
            self.selected_temp = temp

        self.obj = self._get_model_obj()

    def _find_model_key_by_name(self, name):
        for key, value in self.model_dict.items():
            if value["name"] == name:
                return key
        return None

    def _get_model_obj(self):  # pylint: disable=too-many-return-statements
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable not set")
        # openai_config = read_config("models.yml")
        # openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        # openai.azure_endpoint = openai_config["open_api_base_url"]
        # openai.api_version = openai_config["openai_api_version"]
        # openai.api_type = openai_config["openai_api_type"]

        if "openai-chat" in self.model_host.lower():
            log.info(f"AI gateway call is made with cost tags: {get_ai_cost_tags()}")
            return ChatOpenAI(
                model=self.model_name,  # or any other model
                temperature=self.selected_temp,
                default_headers={"X-Aigateway-User-Defined-Tag": f"{get_ai_cost_tags()}"},
            )
        raise ValueError("Model host not supported.")
