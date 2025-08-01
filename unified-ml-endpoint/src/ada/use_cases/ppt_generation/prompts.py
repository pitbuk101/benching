"""PPT generation adding prompts."""

# flake8: noqa: E501
import ast
from typing import Any


def get_cleaning_instructions(chart_type: str) -> str:
    """
    Get data cleaning instructions based on the specified chart type.

    This function returns a set of instructions for cleaning data to prepare it for
    visualization in the specified chart type. The instructions vary depending on
    whether the chart is a stacked bar, line chart, or pie chart.

    Parameters:
        chart_type (str): The type of chart for which to generate cleaning instructions.
                          Accepted values are "stacked_bar", "line_chart", and "pie_chart".

    Returns:
        (str): A formatted string containing the cleaning instructions
        relevant to the specified chart type.
              If the chart type is unrecognized, default
              instructions for pie charts will be returned.
    """
    if chart_type == "stacked":
        cleaning_instructions = """
            - Clean and restructure the input_data for it to be input to python package python-pptx.
            - The output will be used to modify the stacked chart in a powerpoint template.
            - Ensure no invalid characters are present in column names or row values.
            - In case a column has the same value for all rows, discard this column.
            - Output the data as a dictionary with two items: "categories" and "series".
            - "categories" should be a list representing the categories to go to the x axis.
            - "series" should be a list of tuples. Each **tuple** contains a category name (e.g., region) and a corresponding **tuple** of numeric values for category.
            - **The second tuple must contain only floats, example (7.6, 0.5, 9.8).**
            - If any value is missing then fill 0 in place of that value.
            """
    elif chart_type == "line":
        cleaning_instructions = """
            **IMPORTANT** In case of line chart refer only to these instructions
                            and disregard any other instruction regarding data cleaning
            - Ensure data cleanliness: Remove any invalid characters from the column names or row values.
            - Rename the column that describes the time values (years, months, quarters, etc.) to "Date".
            - Sort the data by the time values in chronologically ascending order.
            - If any column contains the same value for all rows, discard that column.
            - Clean the data so that it can be added to a PPTX line chart.
            - Generate a dictionary with two items:
                categories: A list of time values (e.g., years) extracted from the data.
                series:  a list of tuples. Each **tuple** contains a category name (e.g., region) and a corresponding **tuple** of numeric values for the time value.
            - **The second tuple must contain only floats, example (7.6, 0.5, 9.8).**

            ***Ensure that the data is properly formatted and cleaned for use in a PowerPoint line chart.
                all values should be rounded to two decimal places.***
            """
    elif chart_type == "bar":
        cleaning_instructions = """
           - Clean and restructure the data for it to be input to python package python-pptx.
            - The output will be used to modify the bar chart in a powerpoint template.
            - Ensure no invalid characters are in column names or row values.
            - In case of getting the same value for all rows in a column, discard this column.
            - Output the data as a dictionary with two items: "categories" and "values".
            - "categories" should be a list of the categories to go to the x axis. .
            - "series" should be a list of tuples. Each **tuple** contains the a description string (e.g., 'string')
                and a corresponding **tuple** of numeric values.
            - In "series" make sure the first item in the tuple is a string,
                and the second item in the tuple is a tuple of the values.
            - **The second tuple must contain only floats, example (7.6, 0.5, 9.8).**

            """
    elif chart_type == "pie":
        cleaning_instructions = """
            - Clean and restructure the data for it to be input to python package python-pptx.
            - The output will be used to modify the pie chart in a powerpoint template.
            - Sort by the numeric value in descending order.
            - Calculate the percentage of total for each category.
            - Display only the percentage instead of the actual numeric value.
            - Ensure no invalid characters are in column names or row values.
            - In case of getting the same value for all rows in a column, discard this column.
            - Output the data as a dictionary with two items: "categories" and "values".
            - "categories" should be a list representing the pie chart slices (e.g., regions, items).
            - "series" should be a list of tuples. Each **tuple** contains a category name (e.g., region) and a corresponding **tuple** of numeric values for category.
            - **The second tuple must contain only floats, example (7.6, 0.5, 9.8).**

            """
    else:
        cleaning_instructions = """
            - Clean and restructure the data for it to be input to python package python-pptx.
            - The output will be used to modify the chart in a powerpoint template.
            - Sort by the numeric value in descending order.
            - Ensure no invalid characters are in column names or row values.
            - Round all numeric values to two decimal places.
            - In case of getting the same value for all rows in a column discard this column
            - **The second tuple must contain only floats, example (7.6, 0.5, 9.8).**
            """
    return cleaning_instructions


def compile_few_shot_examples(few_shot_examples: dict[str, Any], chart_type: str) -> str:
    """
    Compile few-shot examples to guide the model output.
    args:
        few_shot_examples dict[str, Any]: A dictionary containing few-shot examples.
    Returns:
        (str): A string containing few-shot examples

    """
    compiled_few_shot_examples = ""
    for i, example in enumerate(few_shot_examples["cleaning_title_insights"]):
        if example["chart_type"] == chart_type:
            compiled_few_shot_examples += f"""
Example Input {i}:
user question : {example['user_question']}

summarized output: {example['summarized_output']}

currency: {example['currency']}

chart type: {example['chart_type']}

input_data:
{example['input_data']}

Example Output {i}:
{example['output']}
\n\n\n
            """
    return compiled_few_shot_examples


def compile_few_shot_examples_for_chart_type(few_shot_examples: dict[str, Any]) -> str:
    """
    Compile few-shot examples to guide the model output.
    args:
        few_shot_examples dict[str, Any]: A dictionary containing few-shot examples.
    Returns:
        (str): A string containing few-shot examples
    """
    compiled_few_shot_examples = ""
    chart_types = ["stacked", "bar", "line", "pie"]
    for chart_type in chart_types:
        for example in few_shot_examples["cleaning_title_insights"]:
            if example["chart_type"] == chart_type:
                compiled_few_shot_examples += f"""
Example Input:
user_question :
{example['user_question']}

input_data:
{ast.literal_eval(example['input_data'])[:5]}

Example Output:
{example['chart_type']}
\n
"""
                break
    ## Add invalid example
    compiled_few_shot_examples += """
Example Input:
user_question :
what is my total spend

input_data:
[['[{"[TotalSpend]":120376511.73382051}]']]

Example Output:
Invalid"""

    ## Add more line chart example
    compiled_few_shot_examples += """
Example Input:
user_question :
What is my spend with my top company changed across the last 10 months

input_data:
['[{"[Top company name]":"Industrial Processing GmbH","[Top company spend this year]":314311051.1750001,"[Top company spend last year]":332110962.27500004,"[Change in spend this year compared to last year]":-17799911.099999964}]']]

Example Output:
line"""

    return compiled_few_shot_examples


def ppt_generate_cleaned_data_title_insights_prompt(
    data_from_answer: list[Any],
    user_question: str,
    few_shot_examples: dict[str, Any],
    chart_type: str,
    currency: str,
    summarized_output: str,
) -> list[dict[str, Any]]:
    """
    Generate a prompt for GPT to produce cleaned data, a title, and insights for a PowerPoint slide.
    Args:
        data_from_answer (Any): The raw data that needs cleaning and processing.
        user_question (str): The user's question that guides data processing and visualization.
        few_shot_examples (dict[str, Any]): A few-shot example to guide the model output.
        chart_type (str): The type of chart to be generated.
        currency (str): The currency symbol to be used in the output.
        summarized_output (Any): The summarized output of the data.
    Returns:
        (list[dict[str, Any]]): A list containing the user prompt for the GPT model.
    """
    cleaning_instructions = get_cleaning_instructions(chart_type)
    few_shot_examples_data = compile_few_shot_examples(few_shot_examples, chart_type)

    user_prompt = f"""
You are tasked with generating cleaned data, a title, insights, a chart title and rounding for a PowerPoint slide.
The final output must be a JSON object containing keys: 'cleaned_data', 'title', 'insights', 'chart_title', 'rounding'

**General Instructions**:
- Add the appropriate unit of measurement to each chart title. either currency or % etc.
- Use {currency} as the currency symbol.

**Important Instructions**:
- Do not exclude any category from the input data.
- STRICTLY BASE YOUR CALCULATIONS ONLY ON PROVIDED DATA
- For calculations of percentages, first sum up all the values and then find individual percentages

---



Output: a dictionary containing 'cleaned_data', 'title', 'insights', 'chart_title' and 'rounding' as follows:

{{{{
    "cleaned_data": {{{{"categories": [...], "series" : [...]}}}},  // dictionary with two items: "categories" and "values"
    "title": "...",  // String
    "insights": [...],  // List of strings
    "chart_title": "...", // String
    "rounding": "...", //String
}}}}

Processing Instructions:

1. **Clean the Data**:
General instructions:
- When getting monthly data or yearly data, keep the month or year name,
    don't transform it to any numbers and use the actual value
- Format the output data into a dictionary with two items: "categories" and "values".
- Adhere to the same format for the tuples in the examples.
- Categories should contain a list with the values to go on the x-axis (e.g., regions, items).
- Series should be a list of tuples, every tuple starts with a category name
    and a corresponding **tuple** of numeric values for category.
- IF THERE ARE ANY ESCAPED CHARACTERS IN THE INPUT DATA, MAINTAIN THEM IN THE OUTPUT DATA.
- **The second tuple must contain only floats, example (7.6, 0.5, 9.8).**
{cleaning_instructions}


2. **Generate a Title**:
    - Create a title for the powerpoint as a synthesis of the data with a so-what.
    - Make sure the title contains the main insight on the data.
    - Make sure it contains a number highlighting the main idea behind the data,
        like a summary or a total percentage
    - Generally keep to grammar rules while formatting the title.
        - Format the title so only the First letter is capitalized.
        - Capitalize only proper nouns.
    - Title should not include category names.
    - Title should not exceed 15 words.

3. **Generate Insights**:
    - Write 3-4 key insights in bullet-points and put them in a list.
    - Generate the insights so they're a so-what and actionable not just a summarization.
    - Make some calculations like the percentage of total for each category.
    - Make sure they add more information beside the data not just a summary of the data.
    - If chart is based on time series, make sure to include trends over time. Highlight if there are any anomalies or significant changes.
    - If chart is pie chart then highlight the cumulative proportion of top 2 or 3 categories.
    - If chart is bar chart then highlight the top 2 or 3 categories with highest values. Also add the percentage of top 2 or 3 categories.
    - Do not include insights about category #.

4. **Generate chart title**:
    - Create a concise title summarizing chart title from the cleaned data.
    - Make sure the chart title is styled to be mckinsey style.
    - Make sure the chart title contains the appropriate unit of measurement (% , USD, AED, EUR, SKUs, ... etc)
    - Make sure the chart title is not more than 10 words.
    - Chart title should contain time period if applicable. Check summarized output for time period.
    - Chart title should not include category names.

5. **Rounding**:
    - Choose the appropriate rounding for the data based on the input_data values.
    - Possible values are None, K, Mn or Bn.
    - choose the rounding such that the values are easy to read and understand. Most of the values should not be become zero after rounding.
    - If most of the values are in tens then rounding should be None.
    - This rounding is to be used for the chart title and the insights. Do not round the data in the cleaned data.


Examples:\n {few_shot_examples_data}

**IMPORTANT**: Return only the valid JSON object as the output. Do not include any explanations, instructions, or natural language text.

Inputs:
user question: {user_question}

summarized output: {summarized_output}

currency: {currency}

chart Type: {chart_type}

input_data: {data_from_answer}

Output:
"""
    return [
        {"role": "user", "content": user_prompt},
    ]


def get_prompt_chart_type(
    data_from_answer: list[Any],
    user_question: str,
    few_shot_examples: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Generate a prompt for GPT to produce the chart type.
    Args:
        data_from_answer (list[Any]): The raw data that needs cleaning and processing.
        user_question (str): The user's question that guides data processing and visualization.
        few_shot_examples (dict[str, Any]): A few-shot example to guide the model output.
    Returns:
       (list[dict[str, Any]]): A list containing the user prompt for the GPT model.
    """
    chart_type_examples = compile_few_shot_examples_for_chart_type(few_shot_examples)
    user_prompt = f"""
Your task is to choose the appropriate chart type that best represents the input_data.
The chart type should be chosen based on the type of data and the context in which it is presented.
The data may be structured as a table or it may be unstructured, in which case you will need to infer the chart type.
The ONLY chart types available are:
- stacked: use this when the data is divided into categories and subcategories.
- bar: use this when you want to compare different categories.
- line: use this when you want to show trends over time. Use this chart when comparing values year on year or month on month or quarter on quarter.
- pie: use this when you want to show the proportion of different categories to the whole.
- Invalid: use this when a single number is present input_data.

**IMPORTANT** Generate only a string with the chart type, without any natural langauge exactly like the example

{chart_type_examples}

user's question:
 {user_question}

input_data:
 {data_from_answer}

Output:"""
    return [
        {"role": "user", "content": user_prompt},
    ]
