from pydantic import BaseModel

class ChatState(BaseModel):
    user_query: str
    session_id: str
    tenant_id: str
    preferred_currency: str
    category: str
    language: str

from typing import Optional
from pydantic import BaseModel, model_validator

# default request schema
class QueryRequest(BaseModel):
    user_query: str
    tenant_id: Optional[str] = None
    region: Optional[str] = "eu"
    tenant_id: str
    session_id: str
    category: str
    
# default response schema
class QueryResponse(BaseModel):
    original_query: str
    result: Optional[dict] = None
    fixed_query: Optional[str] = None
    status_code: int
    sql: str
    thread_id: Optional[int] = 0
    count: int = 0
    
    @model_validator(mode='after')
    def set_count(self):
        self.count = len(self.result['data'])
        return self


#  default error response schema
class ErrorResponse(BaseModel):
    error: str
    status_code: int

class RecommendationRequest(BaseModel):
    previous_questions: list[str]
    tenant_id: Optional[str] = None
    region: Optional[str] = "eu"
    session_id: str
    preferred_currency: str
    category: str
    language: str