
from typing import Any, Literal, Optional, Union
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

class RerankedItem(BaseModel):
    step: int
    sql: str
    reason: str

class RerankedResponse(BaseModel):
    response: list[RerankedItem]
    combined_strategy: str

class SchemaResponse(BaseModel):
    schema: str

class GeneratedSQLResponse(BaseModel):
    generated_sql: str

class SQLCorrectionResponse(BaseModel):
    corrected_sql: str

class ChartData(BaseModel):
    label: Union[str, float, int]
    value: Union[str, float, int]
class Chart(BaseModel):
    type: Literal["bar", "line", "pie", "scatter", "area", "grouped-bar"]
    data: list[ChartData]
    xKey: Optional[str] = None
    yKey: Optional[str] = None
    xLabel: Optional[str] = None
    yLabel: Optional[str] = None
    labelKey: Optional[str] = None
    valueKey: Optional[str] = None
    groupKey: Optional[str] = None
    seriesKeys: Optional[list[str]] = None
class ChartRecommendation(BaseModel):
    charts: list[Chart]