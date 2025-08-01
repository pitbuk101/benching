"""Idea generation v3 module to be integrated with unified chat model MVP"""

import json
from typing import Any

from ada.use_cases.idea_generation.idea_generation_v2 import run_idea_generation_v2
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time

idea_generation_conf = read_config("use-cases.yml")["idea_generation_chat"]
model_config = idea_generation_conf["model"]
pg_config = idea_generation_conf["tables"]
log = get_logger("idea_generation_v3")


@log_time
def run_idea_generation_v3(
    json_file_str: str,
    chat_history: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Idea Generation model to generate RCA, Ideas, Linked Insights and user input responses

    Args:
        json_file_str (str): json payload from realtime endpoint
        chat_history (list[dict[str, Any]]): list of chat_history from the
    Returns:
        dict[str, Any] : Dictionary consists chat_id, response_type and the model response
    """
    json_file: dict[str, Any] = json.loads(json_file_str)

    insights = json_file.get("pinned_elements", {}).pop("insights", [])
    json_file["pinned_elements"]["pinned_insights"] = insights

    root_causes = json_file.get("pinned_elements", {}).pop("root_causes", [])
    json_file["pinned_elements"]["pinned_root_causes"] = root_causes

    ideas = json_file.get("pinned_elements", {}).pop("ideas", [])
    json_file["pinned_elements"]["pinned_ideas"] = ideas

    selected_idea_id = json_file.get("selected_elements", {}).pop("id", "")
    selected_idea = json_file.get("selected_elements", {}).pop("idea", "")
    selected_idea_description = json_file.get("selected_elements", {}).pop("idea_description", "")
   
    json_file["general_info"] = {"id":selected_idea_id,"idea":selected_idea,"idea_description":selected_idea_description}
    return run_idea_generation_v2(
        json_file=json.dumps(json_file),
        chat_history=chat_history,
    )
