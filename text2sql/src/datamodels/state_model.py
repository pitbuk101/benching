import datetime
from typing import Optional, TypedDict
from pydantic import BaseModel

class Text2SQLState(BaseModel):
    user_query: str
    category: str
    tenant_id: str
    fixed_query: Optional[str] = None
    sql_retrieve: Optional[dict] = None
    reranked_sql: Optional[list[dict]] = None
    retrieved_sql: Optional[list[dict]] = None
    generated_sql: Optional[str] = None
    corrected_sql: Optional[str] = None
    final_sql: Optional[str] = None
    db_schema: Optional[str] = None
    text2sql_response: Optional[dict] = None
    validation_result: Optional[list[dict]] = None
    cache: dict = None
    recursion_depth: int = 0