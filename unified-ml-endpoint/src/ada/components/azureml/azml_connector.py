"""Module for connecting to AzureML endpoints."""

import json
import os
import urllib.request
from typing import Any, Dict, Optional


# pylint: disable=too-few-public-methods
class AzureMLConnector:
    """Class for connecting to AzureML endpoints."""

    def __init__(self, azml_url: str, azml_deployment: str, azml_api_key: Optional[str] = None):
        self.azml_url = azml_url
        self.azml_deployment = azml_deployment
        self.__api_key = azml_api_key or os.getenv("AZML_API_KEY")

    def azml_post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Post a payload to AzureML endpoint."""
        body = json.dumps(payload).encode()
        headers = {
            "Content-Type": "application/json",
            "Authorization": ("Bearer " + self.__api_key),
            "azureml-model-deployment": self.azml_deployment,
        }
        req = urllib.request.Request(self.azml_url, body, headers)
        # 180000 is 3 minutes in milliseconds for request timeout.
        with urllib.request.urlopen(req, timeout=180000) as response:
            response_bytes = response.read()
            return json.loads(response_bytes.decode("utf-8"))
