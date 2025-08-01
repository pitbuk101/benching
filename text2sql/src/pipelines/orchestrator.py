from src.utils.logs import get_custom_logger
from src.datamodels.state_model import Text2SQLState
from src.pipelines.generation.sql_generation import (
    query_stabilisation,
    sql_retriever,
    get_cache,
    check_cache_hit,
    query_reranker,
    db_schema_retriever,
    sql_generator,
    sql_validation,
    sql_validation_response_parsing,
    sql_correction,
    response
)
from langgraph.graph import StateGraph, END, START
logger = get_custom_logger(__name__)

# Define a function to build and return the flow
def build_ada_chat_flow():
    graph = StateGraph(Text2SQLState)
    # Nodes
    graph.add_node("QueryStabilisation", query_stabilisation)
    graph.add_node("CheckCache", get_cache)
    graph.add_node("SQLRetriever", sql_retriever)
    graph.add_node("QueryReranker", query_reranker)
    graph.add_node("DBSchemaRetriever", db_schema_retriever)
    graph.add_node("SQLGenerator", sql_generator)
    graph.add_node("SQLValidation", sql_validation)
    graph.add_node("SQLCorrection", sql_correction)
    graph.add_node("Response", response)

    graph.add_edge(START, "QueryStabilisation")
    graph.add_edge("QueryStabilisation", "CheckCache")
    graph.add_conditional_edges("CheckCache", check_cache_hit, {
        "Hit": "Response",
        "Miss": "SQLRetriever"
    })
    graph.add_edge("SQLRetriever", "QueryReranker")
    graph.add_edge("QueryReranker", "DBSchemaRetriever")
    graph.add_edge("DBSchemaRetriever", "SQLGenerator")
    graph.add_edge("SQLGenerator", "SQLValidation")
    graph.add_conditional_edges("SQLValidation",sql_validation_response_parsing, {
        "Valid":"Response",
        "Invalid":"SQLCorrection",
        "Error": "Response"
    })
    graph.add_edge("SQLCorrection", "SQLValidation")
    graph.add_edge("SQLValidation", END)
    graph.add_edge("Response", END)
    return graph.compile()

# Expose the flow as a variable for direct import/use
flow = build_ada_chat_flow()
logger.debug("Flow built successfully.")
logger.debug("Text2SQL Chat Flow:")
logger.debug(flow.get_graph().draw_ascii())