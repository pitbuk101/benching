"""Tests for ppt generation workflow"""

from pathlib import Path
from unittest.mock import ANY, patch

from pptx import Presentation

from ada.use_cases.ppt_generation.ppt_generation import (
    generate_chart_type,
    generate_cleaned_data_title_insights,
    generate_ppt_slide,
)


# write unit test case for generate_chart_type
def test_generate_chart_type_bar():
    """
    Test the generate_chart_type function with a sample user question and data.
    """
    user_question = "what is my spend last year by region"
    data_from_answer = """[{"Supplier country[txt_region]":"#",
                        "Period[TXT_YEAR]":2022,"[TotalSpend]":7.105427357601002e-15},
                        {"Supplier country[txt_region]":"Western Asia","Period[TXT_YEAR]":2022,
                        "[TotalSpend]":2717004.923564413},
                        {"Supplier country[txt_region]":"Southern Asia",
                        "Period[TXT_YEAR]":2022,"[TotalSpend]":2457597.3465688797},
                        {"Supplier country[txt_region]":"South America",
                        "Period[TXT_YEAR]":2022,"[TotalSpend]":8969941.484531658},
                        {"Supplier country[txt_region]":"European Union",
                        "Period[TXT_YEAR]":2022,"[TotalSpend]":146040123.08978263},
                        {"Supplier country[txt_region]":"Northern America",
                        "Period[TXT_YEAR]":2022,"[TotalSpend]":4794115.256177726},
                        {"Supplier country[txt_region]":"Southern Africa",
                        "Period[TXT_YEAR]":2022,"[TotalSpend]":2135603.493008537},
                        {"Supplier country[txt_region]":"Western Europe",
                        "Period[TXT_YEAR]":2022,"[TotalSpend]":307446.1097},
                        {"Supplier country[txt_region]":"Eastern Asia",
                        "Period[TXT_YEAR]":2022,"[TotalSpend]":24152947.994658224},
                        {"Supplier country[txt_region]":"Northern Africa",
                        "Period[TXT_YEAR]":2022,"[TotalSpend]":7736.1}]
                        """

    response = generate_chart_type(user_question, data_from_answer)

    assert response == "bar"


@patch("ada.use_cases.ppt_generation.ppt_generation.generate_chat_response")
def test_generate_cleaned_data_title_insights(mock_generate_chat_response):
    # Mock response from generate_chat_response
    mock_generate_chat_response.return_value = """{"cleaned_data": {
        "categories": [
            "European Union",
            "South America",
            "Eastern Asia",
            "Western Asia",
            "Western Europe",
        ],
         'display_labels': ['European Union',
                    'South America',
                    'Eastern Asia',
                    'Western Europe',
                    'Western Asia'],
        "series": [
            ("Spending", (146040123.09, 145040123.09, 24152947.99, 7816698.22, 24052947.99)),
        ],
    },
        "title": "Eastern Asia is top region by spend with 100+ Mn USD per year",
        "insights": ["Eastern and Southern Asia dominate spending, capturing over 70% of the total."],
        "chart_title": "Spend distribution by region, Mn USD",
        "rounding":"Mn",
        "footnote": "Disclaimer: GenAI responses may contain biases, inaccuracies, or misinterpretations."}"""

    user_question = "what is my spend last year by region"
    data_from_answer = [
        tuple(
            [
                """[{"Supplier country[txt_region]":"#",
                            "Period[TXT_YEAR]":2022,"[TotalSpend]":7.105427357601002e-15},
                            {"Supplier country[txt_region]":"Western Asia","Period[TXT_YEAR]":2022,
                            "[TotalSpend]":2717004.923564413},
                            {"Supplier country[txt_region]":"Southern Asia",
                            "Period[TXT_YEAR]":2022,"[TotalSpend]":2457597.3465688797},
                            {"Supplier country[txt_region]":"South America",
                            "Period[TXT_YEAR]":2022,"[TotalSpend]":8969941.484531658},
                            {"Supplier country[txt_region]":"European Union",
                            "Period[TXT_YEAR]":2022,"[TotalSpend]":146040123.08978263},
                            {"Supplier country[txt_region]":"Northern America",
                            "Period[TXT_YEAR]":2022,"[TotalSpend]":4794115.256177726},
                            {"Supplier country[txt_region]":"Southern Africa",
                            "Period[TXT_YEAR]":2022,"[TotalSpend]":2135603.493008537},
                            {"Supplier country[txt_region]":"Western Europe",
                            "Period[TXT_YEAR]":2022,"[TotalSpend]":307446.1097},
                            {"Supplier country[txt_region]":"Eastern Asia",
                            "Period[TXT_YEAR]":2022,"[TotalSpend]":24152947.994658224},
                            {"Supplier country[txt_region]":"Northern Africa",
                            "Period[TXT_YEAR]":2022,"[TotalSpend]":7736.1}]""",
            ],
        ),
    ]

    chart_type = "bar"
    currency = "USD"
    summarized_output = "mock response"

    cleaned_data, title, insights, chart_title, rounding, footnote, chart_type = (
        generate_cleaned_data_title_insights(
            user_question,
            data_from_answer,
            chart_type,
            currency,
            summarized_output,
        )
    )

    assert cleaned_data == {
        "categories": [
            "European Union",
            "South America",
            "Eastern Asia",
            "Western Europe",
            "Western Asia",
        ],
        "display_labels": [
            "European Union",
            "South America",
            "Eastern Asia",
            "Western Europe",
            "Western Asia",
        ],
        "original_series": [
            (
                "Spending",
                (
                    146040123.09,
                    145040123.09,
                    24152947.99,
                    24052947.99,
                    7816698.22,
                ),
            ),
        ],
        "series": [("Spending", (146.04, 145.04, 24.15, 24.05, 7.82))],
    }

    assert title == "Eastern Asia is top region by spend with 100+ Mn USD per year"
    assert insights == [
        "Eastern and Southern Asia dominate spending, capturing over 70% of the total.",
    ]

    assert chart_title == "Spend distribution by region, Mn USD"
    assert rounding == "Mn"
    assert footnote == ""

    mock_generate_chat_response.assert_called_once()


@patch("ada.use_cases.ppt_generation.ppt_generation.populate_charts")
# @patch("ada.use_cases.ppt_generation.ppt_generation.find_index_of_element")
def test_generate_ppt_slide(
    # mock_find_index_of_element,
    mock_populate_charts,
):

    # Define the inputs to the function
    chart_type = "bar"
    cleaned_data = {
        "categories": [
            "European Union",
            "South America",
            "Eastern Asia",
            "Western Asia",
            "Western Europe",
            "Others",
        ],
        "series": [
            ("Spending", (146040123.09, 146040123.09, 24152947.99, 7816698.22, 24152947.99)),
        ],
    }
    title = "Sales Trends"
    insights = """
        Eastern and Southern Asia dominate spending, capturing over 70% of the total.
        Western Asia sees significant investment, reflecting strong supplier relationships.
    """
    chart_title = "Sales by Region"
    footnote = "Generated on 2024-09-27"
    template_path = Path(
        Path(__file__).parents[5],
        "data/ppt_generation/templates/template_bar.pptx",
        Path(__file__).parents[5],
        "data/ppt_generation/templates/template_bar.pptx",
    )
    user_question = "what is my total spend"
    category = "Bearings"
    footnote = "test"

    # Create a mock Presentation object with at least one slide
    prs = Presentation(template_path)

    # Patch the Presentation class to return the mocked Presentation object
    with patch("pptx.Presentation", return_value=prs):
        ppt_bytes = generate_ppt_slide(
            chart_type,
            cleaned_data,
            title,
            insights,
            chart_title,
            template_path,
            user_question,
            category,
            footnote,
        )

    # Assertions to check if the function works as expected
    assert isinstance(ppt_bytes, bytes), "The output should be bytes."
    assert len(ppt_bytes) > 0, "The generated PPT should not be empty."

    # Ensure that other populate chart functions were not called
    # mock_populate_pie_chart.assert_not_called_with()
    # mock_populate_stacked_chart.assert_not_called()
    mock_populate_charts.assert_called_with(
        ANY,
        cleaned_data,
        chart_type,
    )
