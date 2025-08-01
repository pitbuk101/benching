"""Azure ML Endpoint for Key facts deployment."""

# flake8: noqa: E402
import json
import pathlib
import sys
from typing import Any

# pylint: disable=C0413
sys.path.append(str(pathlib.Path(__file__).parents[2]))
# pylint: enable=C0413

from ada.use_cases.negotiation_factory.negotiation_ppt_gen import run_nf_ppt_generation
from ada.use_cases.ppt_generation.ppt_generation import run_ppt_generation


def init():
    """Azure Realtime deployment for PPT generation."""


def run(json_data: str) -> dict[str, Any]:
    """
    Run the complete process of generating a PowerPoint presentation based on
     the provided JSON data.

    Args:
    json_data (str): Input JSON data containing user questions, data, and few-shot examples.

    Returns:
    dict[str, Any]: The generated PowerPoint file along with other metadata about the deployment.
    """
    json_data_dict = json.loads(json_data)
    if json_data_dict.get("page_id") == "negotiation":
        json_data_dict["negotiation"]["tenant_id"] = json_data_dict["tenant_id"]
        return run_nf_ppt_generation(json_data_dict["negotiation"])

    return run_ppt_generation(json_data)
