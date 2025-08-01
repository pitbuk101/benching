"""Utilities for entity extraction component."""

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class FormattedAnswer(BaseModel):
    """Pydantic class for answer processing."""

    number: str = Field(description="Number of units answering the question or NA")
    reasoning: str = Field(description="Explanation why answer is correct")

    @classmethod
    def update_number_description(cls, new_description: str):
        """Update number field description."""
        cls.__annotations__["number"] = (str, Field(description=new_description))


FormattedAnswer.update_number_description(
    new_description="Number of days answering the question or NA",
)
days_parser = PydanticOutputParser(pydantic_object=FormattedAnswer)

FormattedAnswer.update_number_description(
    new_description="Number of months answering the question or NA",
)
months_parser = PydanticOutputParser(pydantic_object=FormattedAnswer)
