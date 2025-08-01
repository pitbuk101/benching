"""Utility functions for the LLM models."""

from typing import Any

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import BasePromptTemplate, ChatPromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import Runnable
from langchain_openai import AzureOpenAIEmbeddings
from langgraph.graph import END, START, StateGraph
from langgraph.managed.is_last_step import RemainingSteps
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from ada.utils.logs.logger import get_logger

log = get_logger("llm_utils")


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        documents: list of documents
        remaining_steps: remaining steps
    """

    question: str
    generation: str
    documents: list[str]
    remaining_steps: RemainingSteps


class GradeAnswer(BaseModel):
    """
    Binary score for generation answer.
    Attributes:
        binary_score: 'yes' or 'no' score to indicate whether the answer is grounded in the facts
    """

    binary_score: str = Field(
        description="Answer is relevant to the question, 'yes' or 'no'. No only if its irrelavant.",
    )
    explanation: str = Field(
        description="Explanation for the binary score",
    )


def get_answer_prompt(**kwargs: Any) -> BasePromptTemplate:
    """
    Prompt for grading the hallucination in a generated answer.

    Args:
        kwargs: Additional keyword arguments
    Returns:
        (BasePromptTemplate): Prompt for grading the hallucination in a generated answer.
    """
    system = (
        """You are a grader assessing whether an LLM generation answers the question. """
        """\n Give a binary score 'Yes' or 'no'. 'Yes' means the answer is relevant to question. """
        """This is not a strict answer checking task. """
        """NEVER give 'No' unless answer is totally irrelevant or there is no answer. """
    )
    human_prompt = "Answer: {generation} \n\n User question: {question}" + kwargs.get(
        "custom_grader_prompt",
        "",
    )
    answer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "human",
                (human_prompt),
            ),
        ],
    )
    return answer_prompt


# pylint: disable=R0915
def generate_conversational_rag_graph(
    retriever: BaseRetriever,
    rag_chain: Runnable,
    hallucination_grader: Runnable,
    chat_history: list[tuple[str, str]],
    llm: Any,
    **kwargs: Any,
) -> Runnable:
    """
    Generates a conversational RAG chain.
    Args:
        retriever (BaseRetriever): retriever model to use for the RAG chain
        rag_chain (Runnable): RAG chain model to use for the RAG chain
        retrieval_grader (Runnable): grades the relevance of retrieved documents to a user question
        hallucination_grader (Runnable): model to grade the hallucination in a generated answer
        chat_history [list[tuple[str, str]]]: chat history
        kwargs: Additional keyword arguments
    Returns:
        (Runnable): Compiled RAG chain
    """

    def retrieve(state: dict[str, Any]) -> dict[str, Any]:
        """
        Retrieve documents

        Args:
            state (dict[str, Any]): The current graph state

        Returns:
            state (dict[str, Any]): state, documents, that contains retrieved documents
        """
        question = state["question"]
        if retriever:
            documents = retriever.invoke(question)
            documents = documents[: kwargs.get("max_documents", 5)]
            return {"documents": documents, "question": question}
        return {"documents": "", "question": question}

    def generate(state: dict[str, Any]) -> dict[str, Any]:
        """
        Generate answer

        Args:
            state (dict[str, Any]): The current graph state

        Returns:
            state (dict[str, Any]): New key added to state, generation, that contains LLM generation
        """
        question = state["question"]
        documents = state["documents"]

        params = {"context": documents, "question": question, "chat_history": chat_history}
        if "additional_params" in kwargs:
            params.update(**kwargs["additional_params"])

        generation = rag_chain.invoke(params)

        return {"documents": documents, "question": question, "generation": generation}

    def grade_generation_v_documents_and_question(state: dict[str, Any]) -> str:
        """
        Determines whether the generation is grounded in the document and answers question.

        Args:
            state (dict[str, Any]): The current graph state

        Returns:
            str: Decision for next node to call
        """
        if kwargs.get("additional_params", {}).get("enable_grader", True) is False:
            return "useful"

        question = state["question"]
        generation = state["generation"]

        params = {
            "generation": generation,
            "question": question,
            **kwargs.get("additional_params", {}),
        }

        score = hallucination_grader.invoke(params)
        grade = score.binary_score

        additional_assessment = True

        if kwargs.get("grader_assessment_criteria"):
            additional_assessment = kwargs["grader_assessment_criteria"](score)

        log.info("EXPLANATION : %s", score.explanation)
        log.info("GENERATION: %s", generation)

        if (grade.lower() == "yes" or state["remaining_steps"] < 5) and additional_assessment:
            return "useful"
        if (grade.lower() == "yes" or state["remaining_steps"] < 5) and kwargs.get(
            "custom_mitigation",
        ):
            state["generation"] = kwargs["custom_mitigation"](llm=llm, **params)
            return "useful"
        return "not useful"

    def default(state: dict[str, Any]) -> dict[str, Any]:
        """
        Default function to call when generation is not useful.

        Args:
            state (dict[str, Any]): The current graph state

        Returns:
            str: Next node to call
        """
        question = state["question"]
        documents = state["documents"]
        params = kwargs.get("params", {})
        params["chat_history"] = chat_history
        generation = kwargs["default_function"](**params)
        return {"documents": documents, "question": question, "generation": generation}

    def compressor(state: dict[str, Any]) -> dict[str, Any]:
        """
        Compressor function for RAGS
        Args & Returns:
            state (dict[str, Any]): The current graph state
        """
        question = state["question"]
        documents = state["documents"]
        compressor = LLMChainExtractor.from_llm(kwargs.get("compressor"))
        compressed_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=retriever,
        )
        documents = compressed_retriever.invoke(question)
        return {"documents": documents, "question": question}

    def reranker(state: dict[str, Any]) -> dict[str, Any]:
        """
        Reranker function for RAGS

        Args & Returns:
            state (dict[str, Any]): The current graph state
        """
        question = state["question"]
        documents = state["documents"]
        reranker = FAISS.from_documents(documents, AzureOpenAIEmbeddings()).as_retriever(
            search_kwargs={"k": kwargs.get("max_documents", 5)},
        )
        documents = reranker.invoke(question)
        return {"documents": documents, "question": question}

    workflow = StateGraph(GraphState)

    workflow.add_node("retrieve", retrieve)  # retrieve
    workflow.add_node("generate", generate)  # generate
    if kwargs.get("default_function"):
        workflow.add_node("default", default)
    if kwargs.get("reranker"):
        workflow.add_node("rerank", reranker)
    if kwargs.get("compressor"):
        workflow.add_node("compress", compressor)

    workflow.add_edge(START, "retrieve")
    if kwargs.get("reranker") and kwargs.get("compressor"):
        workflow.add_edge("retrieve", "rerank")
        workflow.add_edge("rerank", "compress")
        workflow.add_edge("compress", "generate")
    elif kwargs.get("reranker") and not kwargs.get("compressor"):
        workflow.add_edge("retrieve", "rerank")
        workflow.add_edge("rerank", "generate")
    elif kwargs.get("compressor"):
        workflow.add_edge("retrieve", "compress")
        workflow.add_edge("compress", "generate")
    else:
        workflow.add_edge("retrieve", "generate")
    workflow.add_conditional_edges(
        "generate",
        grade_generation_v_documents_and_question,
        {
            "useful": END,
            "not useful": ("default" if kwargs.get("default_function") else "retrieve"),
        },
    )

    if kwargs.get("default_function"):
        workflow.add_edge("default", END)

    app = workflow.compile()
    return app


# pylint: enable=R0915
