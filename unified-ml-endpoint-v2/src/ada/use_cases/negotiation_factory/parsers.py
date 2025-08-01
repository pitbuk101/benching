"""Parser classes for Negotiation Factory use case"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EmailOutputParser(BaseModel):
    """
    Parser class for email model output
    """

    message: str = Field(description="Input to user when email cannot be generated")
    emails: str = Field(description="email content responding to the user provided context")


class SupplierProfileOutputParser(BaseModel):
    """
    Parser class for supplier profile model output
    """

    supplier_name: str = Field(description="name of supplier found in the query if available")


class NegotiationStrategyOutputParser(BaseModel):
    """
    Parser class for NF strategy model output
    """

    market_approach: str = Field(description="market approach for negotiation")
    market_approach_detail: str = Field(
        description="""market approach name, explanation, recomendation, justification of
                    final market approach in (~60 words) and why it is recommended for
                    the supplier""",
    )
    pricing_methodology: str = Field(description="pricing methodology name")
    pricing_methodology_detail: str = Field(
        description="""pricing method name, explanation, recomendation,
                     justification of final pricing methodology in (~60 words)
                     and why it is recommended for the supplier""",
    )
    contracting_methodology: str = Field(description="contract methodology name")
    contracting_methodology_detail: str = Field(
        description="""contracting method name, explanation, recomendation,
                     justification of final contracting methodology in (~60 words)
                     and why it is recommended for the supplier""",
    )
    suggested_prompts: list = Field(
        description="list containing call to action (CTA) prompts for user actions.",
    )


class NegotiationChangeOutputParser(BaseModel):
    """
    Parser class for NF change model output
    """

    message: str = Field(
        description="""Gives the alternatives of the option changed,
          with explanation, rationale and justification for each in (100-150 words)""",
    )
    suggested_prompts: list = Field(
        description="list containing call to action (CTA) prompts for user actions.",
    )
    request_type: str = Field(description="Request type")


class NegotiationApproachOutputParser(BaseModel):
    """
    Parser class for NF strategy model output
    """

    category_positioning: str = Field(description="Category positioning for negotiation")
    category_positioning_detail: str = Field(
        description="""position of supplier within category, explanation, recommendation,
          justification of final category positioning in (~80 words) and why
            it is recommended for the supplier""",
    )
    supplier_positioning: str = Field(description="Supplier positioning for negotiation")
    supplier_positioning_detail: str = Field(
        description="""supplier positioning name, explanation, recommendation, justification of
                    final supplier positioning in (~80 words) and why it is recommended for
                    the supplier""",
    )
    suggested_prompts: list = Field(
        description="list containing call to action (CTA) prompts for user actions.",
    )


class ObjectiveOutputParser(BaseModel):
    """
    Parser class for objective model output
    """

    extracted_objectives: list | None = Field(
        description="List of objectives extracted from USER QUERY",
    )


class ArgumentOutputParser(BaseModel):
    """
    Parser class for argumentation model output
    """

    argument1: str = Field(
        description=(
            "Logical argument to supplier to achieve objective target using carrots"
            " & sticks in 50-100 words"
        ),
    )
    argument2: str = Field(
        description=(
            "Logical argument to supplier to achieve objective target using carrots"
            " & sticks in 50-100 words"
        ),
    )
    argument3: str = Field(
        description=(
            "Logical argument to supplier to achieve objective target using carrots"
            " & sticks in 50-100 words"
        ),
    )


class ArgumentModifyParser(BaseModel):
    """
    Parser class for argumentation model output
    """

    model_config = ConfigDict(extra="allow")


class ExtractedOpportunity(BaseModel):
    """
    Parser class for extracted opportunity
    """

    id: int
    opportunity_value: Optional[float] = Field(
        None,
        description="Extracted opportunity value, or None if not present.",
    )
    opportunity_scale: Optional[str] = Field(
        None,
        description="Scale of the opportunity value, or None if not present",
    )
    opportunity_currency: Optional[str] = Field(
        None,
        description="Currency of the opportunity value, or None if not present",
    )


class ExtractedOpportunityList(BaseModel):
    """
    Parser class for extracted opportunity list
    """

    extracted_opportunities: list[ExtractedOpportunity] = Field(
        description="List of extracted opportunities",
    )
