"""Azure ML Endpoint for Idea generation deployment."""

import pathlib
import sys

# pylint: disable=C0413
sys.path.append(str(pathlib.Path(__file__).parents[2]))
# pylint: enable=C0413

from ada.use_cases.idea_generation.idea_generation_v3 import (  # noqa: E402
    run_idea_generation_v3,
)


def init():
    """Azure Realtime deployment for Idea generation."""


def run(json_file: str, chat_history: list):
    """Entrypoint function."""
    return run_idea_generation_v3(json_file_str=json_file, chat_history=chat_history)
