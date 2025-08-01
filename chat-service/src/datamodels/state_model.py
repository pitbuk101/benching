import datetime
from typing import Annotated, Any, Literal, Optional, TypedDict, Union

from pydantic import BaseModel

class ChatState(TypedDict):
    user_input: str
    auth_token: str
    session_id: str
    thread_id: Optional[str] = None
    language: str
    tenant_id: str
    preferred_currency: str
    category: str
    region: str
    intent: Optional[Literal["Text2SQL", "GeneralPurpose"]] = None
    kf_response: Optional[dict] = {}
    kf_summary: Optional[str] = None
    ow_summary: Optional[str] = None
    final_response: Optional[dict] = {}
    location: Optional[str] = None
    history: Optional[list[dict]] = []
    time: datetime.datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    route: Optional[str] = None
    openworld_type: Optional[Literal["General", "Internet"]]= None
    open_world_response: Optional[Union[ str, list[str]]] = None
    entities: Optional[list[str]] = None
    ner_tagged_input: Optional[str] = None
    kf_response_failure: Optional[bool] = False
    fixed_query: str = None
    sql_retrieve: Optional[dict] = None
    reranked_sql: Optional[list[dict]] = None
    retrieved_sql: Optional[list[dict]] = None
    generated_sql: Optional[str] = None
    corrected_sql: Optional[str] = None
    final_sql: Optional[str] = None
    db_schema: Optional[dict] = None
    text2sql_response: Optional[dict] = None
    validate_sql: Optional[bool] = None
    kf_data: Optional[dict] = None
    cache: Optional[dict] = {}

class RecommendationState(TypedDict):
    previous_questions: list[str] = []
    session_id: str
    tenant_id: str
    preferred_currency: str
    category: str
    language: str
    region: str
    n: Optional[int] = 20
    recommendations: Optional[list[dict]] = []

class ChartState(TypedDict):
    user_question: str
    category: str
    tenant_id: str
    data: list[list[Any, ...]]
    columns: list[str]
    preferred_language: str
    preferred_currency: str
    charts: list[dict]