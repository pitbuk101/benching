import os

import pytest

from ada.utils.config.config_loader import read_config


@pytest.mark.temp
def test_config_loader():
    """
    Test config_loader
    """
    config = read_config("models.yml")
    assert config["openai_api_version"] == "2024-04-01-preview"

    if os.getenv("ENV_TYPE") in ["prod-us"]:
        assert (
            config["open_api_base_url"]
            == "https://azure.us.prod.ai-gateway.quantumblack.com/5567f85f-ea56-48e8-9603-59c23ece68f3/"
        )
    elif os.getenv("ENV_TYPE") in ["dev", "staging"]:
        assert (
            config["open_api_base_url"]
            == "https://azure.eu.prod.ai-gateway.quantumblack.com/53ebe57f-e2e2-4659-989c-7e0e1ab7c4f6/"
        )
    elif os.getenv("ENV_TYPE") in ["prod-eu"]:
        assert (
            config["open_api_base_url"]
            == "https://azure.eu.prod.ai-gateway.quantumblack.com/5db4dbf6-76e0-4220-b9f6-cc4b9839027e/"
        )

    assert config["openai_api_type"] == "azure"
    assert config["embedding_engine"] == "text-embedding-ada-002"
    assert config["threshold_idea_area"] == 0.30
    assert config["top_1_search_result"] == 1
    assert isinstance(config["models"], list)
    assert isinstance(config["models"][0], dict)
