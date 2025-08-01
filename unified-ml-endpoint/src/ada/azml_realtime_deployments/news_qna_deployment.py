"""Azure ML Endpoint for News QnA."""

import pathlib
import sys
from typing import Any

# pylint: disable=C0413
sys.path.append(str(pathlib.Path(__file__).parents[2]))
# pylint: enable=C0413

from ada.use_cases.news_qna.exception import NewsQnAException  # noqa: E402
from ada.use_cases.news_qna.news_qna_v2 import run_news_qna  # noqa: E402


def init():
    """Azure Realtime deployment for News QnA"""


def run(json_file: str) -> dict[str, Any]:
    """
    Entrypoint function for News Qna
    Args:
        json_file: payload

    Returns: response for user query

    """
    try:
        return run_news_qna(json_file_str=json_file)
    except NewsQnAException as news_qna_error:
        message = news_qna_error.args[0] if news_qna_error.args else ""
        return {"message": message, "response_type": "summary"}
