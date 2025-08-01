import pytest
from pydantic import BaseModel, Field

from ada.utils.format.format import (
    dict_to_list_of_items,
    exception_response,
    format_json_prompt_example,
)


class MockFormattedAnswer(BaseModel):
    """Pydantic mock class for answer processing."""

    number: str = Field(description="Number of units answering the question or NA")
    reasoning: str = Field(description="Explanation why answer is correct")

    @classmethod
    def update_number_description(cls, new_description: str):
        """Update number field description."""
        cls.__annotations__["number"] = (str, Field(description=new_description))


@pytest.mark.utils
def test_format_json_prompt_example():
    """
    Test format_json_prompt_example().
    """
    parsed_object = MockFormattedAnswer.parse_obj(
        {
            "number": "180",
            "reasoning": "Both buyer and supplier can "
            "terminate contract without any cause, therefore answer "
            "is 180 days.",
        },
    )
    assert format_json_prompt_example(parsed_object) == (
        '{{"number":"180","reasoning":"Both buyer and supplier can terminate contract without any cause,'
        ' therefore answer is 180 days."}}'
    )


@pytest.mark.utils
def test_exception_response():
    """
    Test exception_response().
    """
    response_type = "response_type"
    message = "message"
    assert exception_response(response_type, message) == {
        "response_type": response_type,
        "response_prerequisite": "",
        "owner": "ai",
        "additional_text": "",
        "message": message,
        "links": [],
    }


def test_dict_to_list_of_items():
    # Test case 1: Simple dictionary
    data1 = {"name": "Supplier A", "spend_ytd": 10000}
    expected1 = [("name", "Supplier A"), ("spend_ytd", 10000)]
    assert dict_to_list_of_items(data1) == expected1

    # Test case 2: Nested dictionary
    data2 = {
        "name": "Supplier A",
        "details": {
            "address": "123 Street",
            "contacts": {"email": "contact@supplier.com", "phone": "123-456-7890"},
        },
        "spend_ytd": 10000,
    }
    expected2 = [
        ("name", "Supplier A"),
        (
            "details",
            [
                ("address", "123 Street"),
                ("contacts", [("email", "contact@supplier.com"), ("phone", "123-456-7890")]),
            ],
        ),
        ("spend_ytd", 10000),
    ]
    assert dict_to_list_of_items(data2) == expected2

    # Test case 3: List
    data3 = ["item1", "item2", "item3"]
    expected3 = ["item1", "item2", "item3"]
    assert dict_to_list_of_items(data3) == expected3

    # Test case 4: String
    data4 = "just a string"
    expected4 = "just a string"
    assert dict_to_list_of_items(data4) == expected4

    # Test case 5: Empty dictionary
    data5 = {}
    expected5 = []
    assert dict_to_list_of_items(data5) == expected5

    # Test case 6: Dictionary with mixed types
    data6 = {"key1": 123, "key2": [1, 2, 3], "key3": {"subkey1": "value"}}
    expected6 = [("key1", 123), ("key2", [1, 2, 3]), ("key3", [("subkey1", "value")])]
    assert dict_to_list_of_items(data6) == expected6
