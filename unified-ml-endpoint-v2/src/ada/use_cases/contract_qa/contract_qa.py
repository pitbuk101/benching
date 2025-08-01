"""Contract QA use case."""

import json

from sklearn.pipeline import Pipeline

from ada.components.db.pg_operations import (
    fuzzy_search_contract_content,
    get_content_from_db,
)
from ada.components.llm_models.model_base import Model
from ada.components.vectorstore.vectorstore import VectorStoreFactory
from ada.use_cases.contract_qa.contract_qa_util import (
    answer_regular_questions,
    get_question_type,
    is_integer,
)
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time

log = get_logger("contract_qna")
contract_qa_config = read_config("use-cases.yml")["contract_qna"]


@log_time
def run_contract_qa(
    json_file_str: str,
    question_classifier_model: Pipeline,
) -> list[dict[str, str]]:
    """
    Run Contract QA.

    Args:
        json_file_str (str): json payload from realtime endpoint
        question_classifier_model (Pipeline): trained classifier model to predict question type
    Returns:
        (list[dict[str, str]]): A list of answers to corresponding input questions
    """
    json_file = json.loads(json_file_str)

    questions = json_file.get("question", "")
    tenant_id = json_file.get("tenant_id", "")

    output = []

    if "document_id" in json_file and is_integer(json_file.get("document_id")):
        doc_id = int(json_file["document_id"])
        output = get_contract_ai_response(doc_id, questions, question_classifier_model, tenant_id)
    elif doc_id := search_contract_details(questions, tenant_id):
        output = get_contract_ai_response(doc_id, questions, question_classifier_model, tenant_id)

    answer = """We were unable to find the answer you are looking for, as the document details
        aren't present in the system. Please go to Documents AI and click on the contract
        for which you want more details."""
    for question in questions:
        output.append(
            {
                "question": question,
                "answer": answer,
                "sources": "",
            },
        )
    return output


def search_contract_details(questions, tenant_id):
    """
    Search_contract_details

    Args:
        questions (list(str)): user questions on contracts
    Returns:
        (int): document id of the contract whihc is matching with some user query
    """
    doc_id = fuzzy_search_contract_content(questions, tenant_id)
    return doc_id if (is_integer(doc_id)) else None


def get_contract_ai_response(
    doc_id: int,
    questions,
    question_classifier_model,
    tenant_id,
):
    """
      Retrieves contract details from a document based on user queries.

    This function processes a given document (specified by `doc_id`) to extract
    relevant contract details based on the questions provided.
    It uses a question classifier model to categorize the questions,
    and retrieves answers by interacting with a document content database and
    a question-answering model.

    Args:
        doc_id (int): The unique identifier of the document in the database.
        questions (list of str): A list of user questions related to the contract.
        question_classifier_model: The model used to classify the type of each question.
        tenant_id: The tenant identifier used to retrieve the correct document content.

    Returns:
        list: A list of responses to the user queries. Each response corresponds
        to the answer to one of the input questions, which may involve searching within
        the document's content.

    Example:
        result = get_contract_details_from_document(12345,
          ["What is the contract duration?", "Who signed the contract?"],
          classifier_model, tenant_id)
        print(result)  # Output: ['2 years', 'John Doe']
    """
    df_doc_chunks = get_content_from_db(tenant_id=tenant_id, document_id=doc_id)
    final_output = []
    log.info(
        f"""
             Doc ID on which the processing to be done {doc_id}
             and dock chunk size ={len(df_doc_chunks)}
             """,
    )
    if len(df_doc_chunks) > 0:
        model = Model(name=contract_qa_config["model"]["openai_model_name"])
        vector_store_factory = VectorStoreFactory()
        vectorstore = vector_store_factory.faiss_from_embeddings(doc_chunk=df_doc_chunks)
        # find category from QnA classifier
        for question in questions:
            params = {
                "question_classifier_model": question_classifier_model,
                "question": question,
                "doc_id": doc_id,
                "tenant_id": tenant_id,
                "df_doc_chunks": df_doc_chunks,
                "model": model,
                "vectorstore": vectorstore,
                "search_k": contract_qa_config["retriever_search_k"],
                "model_host": model.model_host,
            }

            predicted_class = get_question_type(**params)
            contract_qa_fn = globals().get(
                contract_qa_config["function_map"].get(predicted_class, ""),
            )

            response_fn = contract_qa_fn or answer_regular_questions
            response = response_fn(**params)
            final_output.append(response)

    log.info(json.dumps(final_output))
    return final_output
