"""
SourceAI Knowledge Workflow
"""

import json

from langchain_community.chat_message_histories import ChatMessageHistory

from ada.components.db.pg_connector import PGConnector
from ada.components.llm_models.document_qna import extract_links
from ada.components.llm_models.generic_calls import (
    generate_conversational_rag_agent_response,
)
from ada.components.prompts.prompts import (
    doc_q_and_a_prompt,
    doc_qna_step_by_step_sys_prompt,
)
from ada.components.vectorstore.vectorstore import PGRetriever
from ada.use_cases.source_ai_knowledge.exception import SourceAIKnowledgeException
from ada.use_cases.source_ai_knowledge.tools.doc_summary_qa_tool import (
    ProcurementKnowledgeTool,
)
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger

model_config = read_config("models.yml")
source_ai_conf = read_config("use-cases.yml")["source_ai_knowledge"]
log = get_logger("source_ai_knowledge")


def run_source_ai_knowledge(
    json_file: str,
    chat_history: ChatMessageHistory,
    pg_db_conn: PGConnector,
) -> dict[str, str]:
    """
    Function to answer source-ai intent questions
    Args:
        json_file(str): json payload from realtime endpoint
        chat_history(ChatMessageHistory): Object of ChatMessageHistory containing history
         conversation with sourceAI

    Returns:
        Dict[str, str]: Response for the user question
    """

    json_data = json.loads(json_file)
    question = json_data["user_input"]
    intent = json_data["intent"]
    category = json_data["category"]

    # Step 1: Validate intent
    if intent != "source ai knowledge":
        err_msg = "intent retrieved from realtime params is not valid!"
        log.error(err_msg)
        log.info("Intent retrieved from the realtime params : %s", intent)
        raise SourceAIKnowledgeException(err_msg)

    sys_prompt_template = doc_qna_step_by_step_sys_prompt()
    prompt = doc_q_and_a_prompt(
        sys_prompt_template,
        model_host="openai-chat",
        include_sources=True,
    )
    retriever = PGRetriever(
        pg_db_conn=pg_db_conn,
        k=source_ai_conf["multidocs_count"],
        table_name=source_ai_conf["tables"]["chunk_table"],
        embeddings_model=source_ai_conf["model"]["embedding_model_name"],
        embeddings_column_name="embedding",
        column_names=["chunk_content", "page"],
        conditions=f"category_name in ('{category}', 'ALL', 'all') or category_name is NULL",
    )
    default_params = {
        "query": question,
    }
    default_function = ProcurementKnowledgeTool(category).execute
    response = generate_conversational_rag_agent_response(
        user_query=question,
        prompt=prompt,
        chat_history=chat_history,
        retriever=retriever,
        model=source_ai_conf["model"]["rag_model_name"],
        fast_model=source_ai_conf["model"]["fast_model"],
        default_function=default_function,
        params=default_params,
    )
    response_val = response.get("generation", {})
    log.info("sourceai response: %s", response_val)
    if isinstance(response_val, str):
        answer, links = extract_links(response_val)
        response["answer"] = answer
        response["links"] = links
        return {
            "result": answer,
            "links": links,
            "response_type": "source-ai-knowledge",
        }
    return response_val
