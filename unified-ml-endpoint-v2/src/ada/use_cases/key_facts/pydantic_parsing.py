"""Utilities for key facts model component."""

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class FormattedDAX(BaseModel):
    """Pydantic class for answer processing with DAX query."""

    dax_query: str = Field(description="Executable DAX code")
    reasoning: str = Field(description="Explanation why query is correct")


dax_parser = PydanticOutputParser(pydantic_object=FormattedDAX)


class DaxEntityValue(BaseModel):
    """Pydantic class for entity values present in dax query"""

    raw_value: str
    actual_value: str | None = None
