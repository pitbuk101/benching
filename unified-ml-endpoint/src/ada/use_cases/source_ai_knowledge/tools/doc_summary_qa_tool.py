"""DocumentSummaryQaTool is responsible for handling q-a tasks based on document summaries.
It retrieves relevant document summaries from a database, performs similarity search, and uses LLM
to provide answers to user queries"""

from typing import Any

from ada.components.llm_models.generic_calls import generate_chat_response_with_chain
from ada.components.prompts.prompts import general_answer_prompt
from ada.use_cases.source_ai_knowledge.exception import SourceAIKnowledgeException
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time

source_ai_conf = read_config("use-cases.yml")["source_ai_knowledge"]
model_config = read_config("models.yml")
log = get_logger("source_ai_knowledge")


class ProcurementKnowledgeTool:
    """If answer is not found in any of the tools, get answer from general procurement knowledge"""

    def __init__(self, category: str):
        self.category = category
        self.llm_model_name = source_ai_conf["model"]["general_model_name"]

    @log_time
    def execute(self, query: str, **kwargs: Any) -> dict:
        log.info("Executing ProcurementKnowledgeTool %d", len(kwargs))
        try:
            prompt_template = general_answer_prompt(query, self.category)
            response = generate_chat_response_with_chain(
                prompt_template,
                model=source_ai_conf["model"]["general_model_name"],
            )
            return {"result": response, "response_type": "procurement-knowledge"}
        except SourceAIKnowledgeException as err:
            log.error(err.args[0])
            return {"result": err.args[0]}
