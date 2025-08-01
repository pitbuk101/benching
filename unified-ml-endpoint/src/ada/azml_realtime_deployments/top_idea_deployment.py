"""Azure ML Endpoint for Top Ideas deployment."""

import pathlib
import sys

# pylint: disable=C0413
sys.path.append(str(pathlib.Path(__file__).parents[2]))
# pylint: enable=C0413

from ada.use_cases.idea_generation.top_ideas import run_top_ideas  # noqa: E402


def init():
    """Azure Realtime deployment for Top Ideas."""


def run(json_file: str):
    """Entrypoint function."""
    return run_top_ideas(json_file=json_file)
