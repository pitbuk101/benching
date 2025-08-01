""" Generic functions module for langchain calls"""

from typing import Any
import os
from dotenv import load_dotenv

import openai
import retrying
from langchain.memory import (
    ConversationBufferWindowMemory,
    ConversationSummaryBufferMemory,
)
from langchain_community.callbacks import get_openai_callback
from langchain_community.chat_message_histories import ChatMessageHistory

# from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.documents import Document
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import BaseTransformOutputParser, StrOutputParser
from langchain_core.prompts import (
    BasePromptTemplate,
    ChatPromptTemplate,
    PromptTemplate,
)
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import Runnable, RunnableParallel, RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from tenacity import retry, stop_after_attempt, wait_random_exponential

from ada.components.llm_models.generic_utils import (
    GradeAnswer,
    generate_conversational_rag_graph,
    get_answer_prompt,
)
from ada.components.llm_models.model_base import Model
from ada.utils.config.config_loader import read_config
from ada.utils.format.format import format_docs
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time
from ada.utils.metrics.context_manager import get_ai_cost_tags

log = get_logger("generic_calls")
component_conf = read_config("models.yml")
load_dotenv()


os.environ['OPENAI_API_KEY'] = os.getenv('LLM_OPENAI_API_KEY')
os.environ['OPENAI_BASE_URL'] = os.getenv('OPENAI_API_BASE')

def create_qa_chain(
    retriever: BaseRetriever,
    prompt: ChatPromptTemplate,
    model: str | BaseLanguageModel = "gpt-4o-mini",
    temperature: float = 0.0,
    return_sources: bool = False,
) -> Runnable:
    """
    Create a retrieval QA sources chain.

    Args:
        retriever (Any): retriever object for vectorstore.
        prompt (ChatPromptTemplate): prompt message.
        model (str): model name.
        temperature (float): model temperature.
        return_sources (bool): langchain retrieval argument
    Returns:
        QA chain object.
    """
    llm = Model(name=model, temp=temperature).obj if isinstance(model, str) else model
    if return_sources:
        chain = (
            RunnablePassthrough.assign(context=lambda x: format_docs(x["context"]))
            | prompt
            | llm
            | StrOutputParser()
        )
        rag_chain_with_source = RunnableParallel(
            {"context": retriever, "question": RunnablePassthrough()},
        ).assign(answer=chain)

        return rag_chain_with_source
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}  # type: ignore
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


@retry(
    wait=wait_random_exponential(min=1, max=60),
    stop=stop_after_attempt(6),
)
def run_qa_chain(chain: Runnable, input_question: str | dict[str, Any]) -> Any:
    """
    Send a question to the document QA chain.
    Uses RetrievalQAWithSourcesChain as input chain class.

    Args:
        chain (Runnable): The chain to send the question to.
        input_question (str| dict[str, Any]): The question to send to the chain.

    Returns:
        (Any): The response from the qa chain
    """
    log.info("Question sent to chain: %s", input_question)
    output = chain.invoke(input_question)
    return output


def generate_qa_chain_response_with_sources(
    user_query: str,
    retriever: BaseRetriever,
    prompt: ChatPromptTemplate,
    model: str = "gpt-4o-mini",
    temperature: float = 0.0,
) -> tuple[str, list[Document]]:
    """
    This function create and run langchain qa chain
    Args:
        user_query (str): user query or question to be answered
        retriever (BaseRetriever): Any kind of retriever object like vector retriever
        prompt (ChatPromptTemplate): langchain chat prompt template object
        model (str): model to use in qa chain, default `gpt-4o-mini`
        temperature (float): temperature to be used in model , default 0
    Returns:
        (tuple[str, list[Document]]): return answer of the question along with the source documents
    """
    chain = create_qa_chain(retriever, prompt, model, temperature, return_sources=True)
    response = run_qa_chain(chain, user_query)
    return response["answer"], response["context"]


def generate_qa_chain_response_without_sources(
    user_query: str,
    retriever: BaseRetriever,
    prompt: ChatPromptTemplate,
    model: str = "gpt-4o-mini",
    temperature: float = 0.0,
) -> str:
    """
    This function create and run langchain qa chain
    Args:
        user_query (str): user query or question to be answered
        retriever (BaseRetriever): Any kind of retriever object like vector retriever
        prompt (ChatPromptTemplate): langchain chat prompt template object
        model (str): model to use in qa chain, default `gpt-4o-mini`
        temperature (float): temperature to be used in model , default 0
    Returns:
        str: return answer of the question without details the source documents
    """
    chain = create_qa_chain(retriever, prompt, model, temperature, return_sources=False)
    response = run_qa_chain(chain, user_query)
    return response


@log_time
@retry(
    wait=wait_random_exponential(min=1, max=3),
    stop=stop_after_attempt(6),
)
def generate_chat_response(
    messages: list[dict[str, str]],
    model: str | BaseLanguageModel = "gpt-4o",
    temperature: float = 0,
    response_format: str = "",
    parser: BaseTransformOutputParser | None = None,
    **kwargs: Any,
) -> str:
    """
    Create a chat completion openai call using list of messages. Retry 6 times.

    Args:
        messages (list[dict[str, str]]): messages to api call.
        model (str | BaseLanguageModel): model name.
        temperature (float): model temperature.
        response_format (str): output format, either "text" or "json_object"
        parser (BaseTransformOutputParser | None): Is a parser object to
        ensure the format of the output
        kwargs (Any): additional arguments
    Returns:
        response from api call.
    """
    log.info("len kwargs: %s", len(kwargs))
    params = {
        "response_format": {"type": response_format} if response_format else {},
    }
    params = {key: value for key, value in params.items() if value}
    model_val = Model(name=model, temp=temperature).obj if isinstance(model, str) else model
    llm = model_val | parser if parser else model_val
    check_response = llm.invoke(messages, **params)
    response = check_response if parser else check_response.content
    return response


@log_time
@retry(
    wait=wait_random_exponential(min=1, max=60),
    stop=stop_after_attempt(6),
)
def generate_chat_response_with_chain(
    prompt: BasePromptTemplate,
    model: str | BaseLanguageModel = "gpt-4o-mini",
    temperature: float = 0,
    prompt_params: dict[str, Any] | None = None,
    parser: BaseTransformOutputParser | None = None,
    response_schema: Any | None = None,
    response_format: str | None = None,
) -> str:
    """
    Generate a chat response using a chain of prompts and models.

    This function creates a chat completion call using a list of messages and retries up to 6 times
    in case of failures. It supports structured output using a response schema and format.

    Args:
        prompt (BasePromptTemplate): The prompt template to use for the chat.
        model (str | BaseLanguageModel): Model name/object for the chat, default is `gpt-4o-mini`.
        temperature (float): The temperature to use for the model, default is 0.
        prompt_params (dict[str, Any] | None): Parameters to pass to the prompt, default is None.
        parser (PydanticOutputParser | None): The parser to use for the output, default is None.
        response_schema (Any | None): The schema to use for the structured output, default is None.
        response_format (str | None): The format of the response, either "text" or
        "json_object", default is None.

    Returns:
        str: The response from the chat completion call.
    """
    llm = Model(model, temp=temperature).obj if isinstance(model, str) else model

    if response_schema and response_format:
        llm.with_structured_output(response_schema, method=response_format)
    elif response_schema:
        llm.with_structured_output(response_schema)
    elif response_format:
        llm.with_structured_output(None, method=response_format)

    if parser:
        chain = prompt | llm | parser
    else:
        chain = prompt | llm

    with get_openai_callback() as call_back:
        params = prompt_params if prompt_params else {}
        chain_response = chain.invoke(params)
        log.info("Total Cost (USD): $%s", format(call_back.total_cost, ".6f"))

    if parser or response_schema or response_format:
        return chain_response
    return chain_response.content


@log_time
def get_chat_message_history(session_id: str, **kwargs: Any) -> ChatMessageHistory:
    """
    Takes the list of chat history from the common chat history table and
    returns a chat memory object.

    Args:
        session_id (str): Chat ID of the session.
        chat_history_from_db (list[Any]): Chat memory from the database.
        model (str): Model used in LLM.
        memory_type (str): The type of memory to be used, either "window" or "summary".
        window_size (int): The number of messages to be kept in memory.
        temperature (float): Temperature to set the level of creativity of the model.

    Returns:
        ChatMessageHistory: Object of ChatMessageHistory.
    """
    log.info("Session id %s", session_id)
    messages = []
    for chat_history in kwargs.get("chat_history_from_db", []):
        chat_history = dict(chat_history)
        messages.append(HumanMessage(content=str(chat_history["request"])))
        messages.append(
            AIMessage(
                content=f"""Answered By
                                   {chat_history["model_used"]}: {str(chat_history["response"])}""",
            ),
        )
    model_obj = Model(kwargs.get("model", "gpt-4o-mini"), temp=kwargs.get("temperature", 0)).obj
    memory = (
        ConversationBufferWindowMemory(
            chat_memory=ChatMessageHistory(messages=messages),
            k=kwargs.get("window_size", 3),
        ).buffer_as_messages
        if kwargs.get("memory_type", "window") == "window"
        else ConversationSummaryBufferMemory(
            chat_memory=ChatMessageHistory(messages=messages),
            max_token_limit=500,
            llm=model_obj,
        ).buffer
    )
    return ChatMessageHistory(messages=memory)


# @retrying.retry(wait_fixed=3000, stop_max_attempt_number=5)
def generate_embeddings_from_string(
    text: str,
    embeddings_model: str = "text-embedding-ada-002",
) -> list[float]:
    """
    Generate embeddings from string of text.
    This will be used to vectorize data and user input for interactions with Azure OpenAI.

    Args:
        text (str): input text to create embedding
        embeddings_model (str): model to use for embedding generation
    Returns:
        (list[float]): List of the embeddings
    """
    log.info("Generating embeddings for text: %s", text[:50])  # Log first 50 characters
    try:
        embeddings =  (
            openai.embeddings.create(
                input=text,
                model=embeddings_model,
                extra_headers={"X-Aigateway-User-Defined-Tag": f"{get_ai_cost_tags()}"},
            )
            .data[0]
            .embedding
        )
        log.info("Generated embeddings", embeddings)  # Log first 50 characters
        return embeddings
    except Exception as exp:
        log.error("Error in generating embeddings: %s", exp)


@retry(
    wait=wait_random_exponential(min=1, max=60),
    stop=stop_after_attempt(6),
)
def create_conversation_chain(
    prompt: PromptTemplate,
    model: str,
    temperature: float = 0.0,
    input_message_key: str = "input",
    history_message_key: str = "history",
) -> RunnableWithMessageHistory:
    """
    Create conversation chain with user chat memory

    Args:
        prompt (PromptTemplate): prompt message.
        model (str): model name.
        temperature (float): model temperature.
        input_message_key (str): Name of the input to the prompt
        history_message_key: key of the history
    Returns:
        (Runnable) Conversation Chain object.
    """
    model = Model(model, temp=temperature).obj
    chain = prompt | model
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history=get_chat_message_history,
        input_messages_key=input_message_key,
        history_messages_key=history_message_key,
    )
    return chain_with_history


@log_time
@retry(
    wait=wait_random_exponential(min=1, max=60),
    stop=stop_after_attempt(6),
)
def run_conversation_chain(
    conversation_chain: RunnableWithMessageHistory,
    input_str: str,
    chat_history_from_db: list[Any],
    session_id: str,
    model: str,
    memory_type: str = "window",
    window_size: int = 3,
    temperature: float = 0,
) -> str:
    """
    Run the conversation chain with the given input.

    Args:
        conversation_chain (RunnableWithMessageHistory): The conversation chain object with history.
        input_str (str): inputs for getting the response from llm
        chat_history_from_db (list[Any]): Chat memory from db
        session_id: chat ID of the session,
        model (str): model name.
        temperature (float): model temperature.
    Returns:
        The result of running the conversation chain with the input string.
    """
    response = conversation_chain.invoke(
        {"input": input_str},
        config={
            "configurable": {
                "chat_history_from_db": chat_history_from_db,
                "memory_type": memory_type,
                "model": model,
                "session_id": session_id,
                "temperature": temperature,
                "window_size": window_size,
            },
        },
    )
    return response.content


@log_time
def run_conversation_chat(
    chat_history: list[Any],
    prompt: PromptTemplate,
    input_str: str,
    model: str,
    memory_type: str = "window",
    window_size: int = 3,
    temperature: float = 0.3,
    input_message_key: str = "input",
    history_message_key: str = "history",
    session_id: str = "",
) -> str:
    """
    Takes the prompt and generates a response based on the inputs,
    chat history and the prompt
    Args:
        chat_history (list[Any]): extracted chat history from database
        prompt (PromptTemplate): Prompt for the LLM call
        input_str (input_str): inputs for getting the response from llm
        model(str): model used in llm
        memory_type (str): Choice of window or summary to choose the type of memory
        window_size (str): size of the window , default 3
        temperature (float): temperature to set the level of creativity of the model
        input_message_key (str): Name of the input to the prompt
        history_message_key (str): key of the history
        session_id (str): provided session id
    Returns:
        (str): response of the conversation chain
    """
    conversation_chain = create_conversation_chain(
        prompt=prompt,
        model=model,
        temperature=temperature,
        input_message_key=input_message_key,
        history_message_key=history_message_key,
    )

    response = run_conversation_chain(
        conversation_chain=conversation_chain,
        input_str=input_str,
        chat_history_from_db=chat_history,
        model=model,
        memory_type=memory_type,
        window_size=window_size,
        temperature=temperature,
        session_id=session_id,
    )
    return response


def generate_conversational_rag_agent_response(
    user_query: str,
    prompt: ChatPromptTemplate | PromptTemplate,
    chat_history: list[tuple[str, str]],
    retriever: BaseRetriever | None = None,
    model: str = "gpt-4o",
    fast_model: str = "gpt-4o",
    temperature: float = 0.3,
    **kwargs: Any,
) -> dict[str, str]:
    """
    This function create and run langchain qa agent chain
    Args:
        retriever: BaseRetriever for document retrieval tasks
        fast_model: faster and smaller llm for specific tasks
        user_query (str): user query or question to be answered
        prompt (ChatPromptTemplate): langchain chat prompt template object
        chat_history (list[tuple[str, str]]): chat history to be used in the chain
        model (str): model to use in qa chain, default `gpt-35-turbo`
        temperature (float): temperature to be used in model , default 0
        kwargs (Any): additional arguments
    Returns:
        dict[str, str]: return answer of the question without details the source documents
    """
    try:
        llm = Model(name=model, temp=temperature).obj if isinstance(model, str) else model
        fast_llm = (
            Model(name=fast_model, temp=temperature).obj if isinstance(fast_model, str) else fast_model
        )
        grader = kwargs.get("custom_grader", GradeAnswer)
        structured_llm_grader = fast_llm.with_structured_output(grader)
        hallucination_grader = get_answer_prompt() | structured_llm_grader

        parser = kwargs.get("custom_parser", StrOutputParser())
        if kwargs.get("fast_llm_for_rag_chain", False) is True:
            llm = fast_llm

        rag_chain = prompt | llm | parser  # if retriever is None it acts as a conversation chain
        rag_graph = generate_conversational_rag_graph(
            retriever=retriever,
            rag_chain=rag_chain,
            hallucination_grader=hallucination_grader,
            chat_history=chat_history,
            llm=fast_llm,
            **kwargs,
        )

        params = {"question": user_query}
        if "additional_params" in kwargs:
            params.update(**kwargs["additional_params"])
        response = rag_graph.invoke(params)
        return response
    except Exception as exp:
        log.error("Error in generating response: %s", exp)
        return {"error": "Error in generating response"}
