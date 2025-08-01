from asgiref.sync import async_to_sync
from langgraph.graph import END, START, StateGraph
from src.datamodels.state_model import ChatState, RecommendationState
from src.pipelines.generation.chat import (
    api_bridge, 
    classify_intent,
    final_response, 
    kf_output_summary,
    ner_tag_process,
    ner_tagging,
    open_world,
    query_sql_data,
    check_history
)
from src.pipelines.threads.chat_thread import Thread
from src.utils.logs import get_custom_logger
from src.datamodels.state_model import ( 
    ChatState,
    RecommendationState,
    ChartState
    )
from src.pipelines.generation.question_recommendation import question_recommendation
from src.pipelines.generation.charts import chart_recommendation
from src.utils.logs import get_custom_logger

from src.pipelines.docs_ai.entity_pipeline import process_snowflake_entities

logger = get_custom_logger(__name__)

# Define a function to build and return the flow
def build_ada_chat_flow():
    graph = StateGraph(ChatState)
    # Nodes
    graph.add_node("LoadHistory", check_history)
    graph.add_node("ClassifyIntent", classify_intent)
    graph.add_node("OpenWorld", open_world)
    # graph.add_node("Text2SQL", dummy_api_bridge)
    graph.add_node("Text2SQL", api_bridge)
    graph.add_node("KFSummary", kf_output_summary)
    graph.add_node("NERTagging", ner_tagging)
    graph.add_node("NERTagProcess", ner_tag_process)
    graph.add_node("QuerySFData", query_sql_data)
    graph.add_node("Join", lambda state: state, defer=True)  # Simple pass-through join node
    graph.add_node("FinalResponse", final_response)
    # Graph 
    graph.add_edge(START, "ClassifyIntent")
    graph.add_edge(START, "NERTagging")
    graph.add_edge(START, "LoadHistory")
    graph.add_edge("NERTagging", "NERTagProcess")
    graph.add_edge("NERTagProcess", "Join")
    graph.add_edge("ClassifyIntent", "Join")
    graph.add_edge("LoadHistory", "Join")
    graph.add_conditional_edges("Join", lambda state: state["route"], {
        "Text2SQL": "Text2SQL",
        "GeneralPurpose": "OpenWorld"})
    graph.add_conditional_edges("Text2SQL", lambda state: "Hit" if state["cache"] else "Miss",{
        "Hit": "FinalResponse",
        "Miss": "QuerySFData"
    })
    graph.add_edge("QuerySFData", "KFSummary")
    graph.add_edge("KFSummary", "FinalResponse")
    graph.add_edge("OpenWorld", "FinalResponse")
    graph.add_edge("FinalResponse", END)
    return graph.compile()

def build_ada_question_recommendation_flow():
    graph = StateGraph(RecommendationState)
    # Nodes
    graph.add_node("QuestionRecommendation", question_recommendation)
    # Edges
    graph.add_edge(START, "QuestionRecommendation")
    graph.add_edge("QuestionRecommendation", END)
    return graph.compile()

def build_chart_recommendation_flow():
    graph = StateGraph(ChartState)
    graph.add_node("ChartRecommendation", chart_recommendation)
    graph.add_edge(START, "ChartRecommendation")
    graph.add_edge("ChartRecommendation", END)
    return graph.compile()

def orchestrate_snowflake_entities(tenant_id, upload_ids):
    return async_to_sync(process_snowflake_entities)(tenant_id, upload_ids)

def orchestrate_thread_pipeline(**kwargs):
    thread = Thread(
        tenant_id=kwargs["tenant_id"],
        category=kwargs["category"],
        thread_id=kwargs["thread_id"]
        )
    return thread

# Expose the flow as a variable for direct import/use
flow = build_ada_chat_flow()
question_recommendation_flow = build_ada_question_recommendation_flow()
chart_recommendation_flow = build_chart_recommendation_flow()
logger.debug("Flow built successfully.")
logger.debug("ADA Chat Flow:")
logger.debug(flow.get_graph().draw_ascii())
logger.debug("ADA Question Recommendation Flow:")
logger.debug(question_recommendation_flow.get_graph().draw_ascii())
logger.debug("ADA Chart Recommendation Flow:")
logger.debug(chart_recommendation_flow.get_graph().draw_ascii())
