from typing import Optional
from pydantic import BaseModel, model_validator

# default request schema
class QueryRequest(BaseModel):
    query: str
    tenant_id: Optional[str] = None
    region: Optional[str] = "eu"

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
