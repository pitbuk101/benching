
from typing import Literal, Union
from pydantic import BaseModel


class ClassifyIntentResponse(BaseModel):
    route: Literal["Text2SQL", "GeneralPurpose"]

class OpenWorldResponse(BaseModel):
    response: Union[str, list[str]] = None

class OpenWorldSummaryResponse(BaseModel):
    response: str

class NERResponse(BaseModel):
    entities: list[str]

class Recommendation(BaseModel):
    type: Literal["Spend", "Opportunity", "Market", "Generic"]
    question: str
    description: str

class QuestionRecommendation(BaseModel):
    recommendations: list[Recommendation] = []

class StabiliseQueryResponse(BaseModel):
    fixed_query: str

# class RerankedItem(BaseModel):
#     step: int
#     sql: str
#     reason: str

# class RerankedResponse(BaseModel):
#     response: list[RerankedItem]
#     combined_strategy: str

class RankedItem(BaseModel):
    question: str
    sample: int
    confidence: float
class RerankedResponse(BaseModel):
    response: list[RankedItem]

class SchemaResponse(BaseModel):
    schema: str

class GeneratedSQLResponse(BaseModel):
    generated_sql: str

class SQLCorrectionResponse(BaseModel):
    corrected_sql: str