"The file contains the utility functions for the summary generation"
import operator
from typing import Annotated, Any, Literal, TypedDict

from langchain.chains.combine_documents.reduce import collapse_docs, split_list_of_docs
from langchain_core.documents import Document
from langchain_core.runnables import Runnable
from langchain.chat_models import ChatOpenAI
from langgraph.constants import Send
from langgraph.graph import END, START, StateGraph
from langgraph.managed.is_last_step import RemainingSteps

from ada.utils.config.config_loader import read_config

benchmarking_conf = read_config("use-cases.yml")["benchmarking"]


class OverallState(TypedDict):
    """
    Represents the overall state of the main graph.

    This class encapsulates all the relevant information for managing the
    state of the document processing graph. It includes the original
    document contents, individual summaries, collapsed summaries, and
    a final summary.

    Attributes:
        contents (list[str]): A list of strings representing the contents
            of the input documents.
        summaries (Annotated[list, operator.add]): A list of summaries
            generated from individual nodes, combined using the
            `operator.add` function. This attribute is used to aggregate
            all individual node summaries into a comprehensive list.
        collapsed_summaries (list[Document]): A list of Document objects
            that represent the collapsed or processed summaries from
            the individual nodes.
        final_summary (str): A string containing the final, aggregated
            summary of the entire document collection.
    """

    contents: list[str]
    summaries: Annotated[list, operator.add]
    collapsed_summaries: list[Document]
    final_summary: str
    remaining_steps: RemainingSteps


class SummaryState(TypedDict):
    """
    Represents the state of a node responsible for generating summaries.

    This class holds the information for a single node in the graph that
    processes documents to produce summaries. Each node in the graph will
    have its own `SummaryState` containing the content that it processes.

    Attributes:
        content (str): The content of the document or text that the node
            is responsible for summarizing. This is typically the input
            data for generating a summary.
    """

    content: str


def generate_summary_chain(
    llm: ChatOpenAI,
    map_chain: Runnable,
    reduce_chain: Runnable,
) -> Any:
    """
    Coordinates the summarization graph creation by mapping, collapsing,
    and generating a final summary.

    This asynchronous function orchestrates the summarization workflow, which involves:
    1. Mapping each document to a summarization node.
    2. Collapsing the summaries into a final set of aggregated summaries.
    3. Generating a comprehensive final summary from the collapsed summaries.

    The function integrates multiple stages of the process using provided `map_chain` and
    `reduce_chain` instances to handle summarization and aggregation tasks.

    Args:
        llm (Model): An instance of a language model that has a method `get_num_tokens` to
                     calculate the number of tokens for a given text.
        map_chain (Runnable): An instance of a Runnable chain used for mapping documents
            to summarization nodes. It should have an `ainvoke` method that processes
            document contents and returns intermediate summaries.
        reduce_chain (Runnable): An instance of a Runnable chain used for aggregating
            collapsed summaries into the final summary. It should have an `ainvoke` method
            that processes the list of collapsed summaries to produce a comprehensive final summary.

    Returns:
        (Any) A graph for summary creation
    """

    def length_function(documents: list[Document]) -> int:
        """
        Calculate the total number of tokens in a list of documents using a language model.

        This function iterates over a list of `Document` objects and computes the total number
        of tokens by querying the provided language model (`llm`) for each document's page
        content. It sums up the token counts for all documents and returns the total.
        Args:
            documents (list[Document]): A list of `Document` objects, where each document contains
                                        a `page_content` attribute representing the text content.
        Returns:
            int: The total number of tokens across all provided documents."""
        return sum(llm.get_num_tokens(doc.page_content) for doc in documents)

    def generate_summary(state: SummaryState) -> dict[str, list[str]]:
        """
        Asynchronously generates a summary for the given content using a map chain.

        This function processes the content provided in the `SummaryState` using
        the specified `map_chain`, which is a runnable chain of operations.
        The function returns the generated summary encapsulated in a dictionary.

        Args:
            state (SummaryState): The state of the node, containing the content
                to be summarized. This should be a dictionary with a single key
                "content" that holds the text to be processed.

        Returns:
            dict[str, list[str]]: A dictionary with a single key "summaries" that
                maps to a list of strings. Each string in the list represents a
                generated summary."""
        response = map_chain.invoke(state["content"])
        return {"summaries": [response]}

    def map_summaries(state: OverallState) -> list[Send]:
        """
        Maps the documents to the summarization nodes in the graph.

        This function takes the overall state of the document processing graph
        and creates a list of `Send` objects. Each `Send` object represents a
        task to be executed by a node in the graph, where each task involves
        summarizing one of the documents.

        Args:
            state (OverallState): The overall state of the graph, containing the
                input documents. This should be a dictionary with a key "contents"
                that holds a list of document contents to be processed.

        Returns:
            list[Send]: A list of `Send` objects, where each object contains:
                - The name of the node responsible for summarization ("generate_summary").
                - The state to be sent to that node, which includes the content of
                a single document to be summarized.
        """
        return [Send("generate_summary", {"content": content}) for content in state["contents"]]

    def collect_summaries(state: OverallState) -> dict[str, list[Document]]:
        """
        Collects and formats the summaries into `Document` objects.

        This function takes the overall state of the document processing graph
        and converts each summary into a `Document` object. The resulting
        dictionary contains the processed summaries as `Document` objects.

        Args:
            state (OverallState): The overall state of the graph, which includes
                the generated summaries. This should be a dictionary with a key
                "summaries" that holds a list of summary strings.

        Returns:
            dict[str, list[Document]]: A dictionary with a single key
                "collapsed_summaries" that maps to a list of `Document` objects.
                Each `Document` object is created from a summary string.

        """
        return {"collapsed_summaries": [Document(summary) for summary in state["summaries"]]}

    def collapse_summaries(state: OverallState) -> dict[str, list[Document]]:
        """
        Collapses a list of `Document` objects into aggregated summaries using a reduce chain.

        This asynchronous function processes a list of collapsed summaries and
        aggregates them into a final set of summaries using the provided `reduce_chain`.
        The process involves splitting the documents into manageable chunks, invoking
        the reduce chain on each chunk, and then combining the results.

        Args:
            state (OverallState): The overall state of the graph, which includes
                the collapsed summaries. This should be a dictionary with a key
                "collapsed_summaries" that holds a list of `Document` objects
        Returns:
            dict[str, list[Document]]: A dictionary with a single key
                "collapsed_summaries" that maps to a list of `Document` objects.
                Each `Document` in the list represents an aggregated summary.
        """
        token_max = benchmarking_conf.get("token_max", 1000)
        doc_lists = split_list_of_docs(state["collapsed_summaries"], length_function, token_max)
        results = []
        for doc_list in doc_lists:
            results.append(collapse_docs(doc_list, reduce_chain.invoke))

        return {"collapsed_summaries": results}

    def should_collapse(
        state: OverallState,
    ) -> Literal["collapse_summaries", "generate_final_summary"]:
        """
        Determines whether to collapse summaries further or generate the
        final summary based on token count.

        This function evaluates the number of tokens in the `collapsed_summaries` from the
        overall state and decides the next step in the document processing graph. It uses
        a predefined token threshold to determine whether the summaries need further collapsing
        or if the final summary should be generated.

        Args:
            state (OverallState): The overall state of the graph, which includes
                the collapsed summaries. This should be a dictionary with a key
                "collapsed_summaries" that holds a list of `Document` objects.

        Returns:
            Literal["collapse_summaries", "generate_final_summary"]: A string indicating
                the next processing step:
                - "collapse_summaries" if the number of tokens in the collapsed summaries
                exceeds the threshold specified by `token_max`.
                - "generate_final_summary" if the number of tokens is within the acceptable range.

        """
        token_max = benchmarking_conf.get("token_max", 1000)
        num_tokens = length_function(state["collapsed_summaries"])
        if num_tokens > token_max and state["remaining_steps"] > 2:
            return "collapse_summaries"
        return "generate_final_summary"

    def generate_final_summary(state: OverallState) -> dict[str, str]:
        """
        Generates the final summary from the collapsed summaries using a reduce chain.

        This asynchronous function aggregates the `collapsed_summaries` from the
        overall state by processing them through a `reduce_chain`. The result is
        a comprehensive final summary of the entire document collection.

        Args:
            state (OverallState): The overall state of the graph, which includes
                the collapsed summaries. This should be a dictionary with a key
                "collapsed_summaries" that holds a list of `Document` objects.
        Returns:
            dict[str, str]: A dictionary with a single key "final_summary" that maps
                to a string containing the final aggregated summary of the documents.
        """
        response = reduce_chain.invoke(state["collapsed_summaries"])
        return {"final_summary": response}

    graph = StateGraph(OverallState)
    graph.add_node("generate_summary", generate_summary)  # same as before
    graph.add_node("collect_summaries", collect_summaries)
    graph.add_node("collapse_summaries", collapse_summaries)
    graph.add_node("generate_final_summary", generate_final_summary)

    # Edges:
    graph.add_conditional_edges(START, map_summaries, ["generate_summary"])
    graph.add_edge("generate_summary", "collect_summaries")
    graph.add_conditional_edges("collect_summaries", should_collapse)
    graph.add_conditional_edges("collapse_summaries", should_collapse)
    graph.add_edge("generate_final_summary", END)

    app = graph.compile()
    return app
