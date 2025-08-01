"""This module defines the data models used in the
'source_ai_knowledge' use case for opportunities."""

from pydantic import BaseModel


class OpportunityInsight(BaseModel):
    """
    Model representing an individual opportunity insight.

    Attributes:
        insight_id (int): The unique id for the insight.
        label (str): A descriptive label for the insight.
        impact (Optional[str]): The potential impact of the opportunity
        (e.g., financial impact in currency).
    """

    insight_id: int
    label: str
    impact: str | None = None


class SourceAIOpportunityResponse(BaseModel):
    """
    Model representing the AI-generated response for opportunity-related queries.

    Attributes:
        response_type (str): The type of response, set to 'source-ai-opportunity' by default.
        message (str): The main message or summary of the response.
        additional_text (Optional[str]): Additional text or commentary for the response.
        insights (List[OpportunityInsight]): A list of insights related to the opportunity.
        response_summary (Optional[str]): A summary of the response if available. Default is None.
    """

    response_type: str = "source-ai-opportunity"
    message: str
    additional_text: str | None
    insights: list[OpportunityInsight]
    response_summary: str | None = None
