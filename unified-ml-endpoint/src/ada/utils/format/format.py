"""Formatting utils for knowledge extraction application."""

import json
import re
from typing import Any, Union

from langchain_core.documents import Document

from ada.utils.logs.logger import get_logger

log = get_logger("format_util")


def format_docs(docs: Document) -> str:
    """
    Formats the retrieved documents into a string for prompts

    Args:
        docs (Document): Retrieved langchain documents
    Returns:
        (str) : Concatenated string
    """
    return "\n\n".join([d.page_content for d in docs])


def format_json_prompt_example(parsed_object) -> str:
    """Format pydantic parsed model for usage in prompt."""
    return parsed_object.json().replace("{", "{{").replace("}", "}}")


def exception_response(response_type: str, message: str) -> dict[str, Any]:
    """Standard exception format."""
    return {
        "response_type": response_type,
        "response_prerequisite": "",
        "owner": "ai",
        "additional_text": "",
        "message": message,
        "links": [],
    }


def check_empty_or_non_word_text(text: str) -> bool:
    """check string is not meaningful or useful"""
    text = text.strip()
    return text == "" or bool(re.compile(r'^[ \n\t!@#$%^&*(),.?":{}|<>]*$').match(text))


def replace_quotes(match: re.Match) -> str:
    """
    Replace single quotes with double quotes for the matched group.

    Args:
        match (re.Match): A match group based on the provided regex pattern.

    Returns:
        str: A string with double quotes replacing single quotes in the match group.
    """
    group = match.group(0)
    # Replace single quotes with double quotes
    return group.replace("'", '"')


def replace_dict_str_to_json_str(dict_str: str) -> str:
    """
    Replace (\') with (') and enclose keys and values of the dictionary with double quotes
    if they are originally enclosed in single quotes.

    Args:
        dict_str (str): Input string representing a dictionary.

    Returns:
        str: String that can be converted to a JSON object.
    """
    dict_str = dict_str.replace("\\'", "'")
    return re.sub(r"{'|':( |\n|\t)*'|',( |\n|\t)*'|'}", replace_quotes, dict_str)


def format_price(price: str) -> float:
    """
    This function cleanses the price data from a string
    by removing the currency symbol and other non-numeric details.

    Args:
        price (str): A string containing price in digit along
            with other optional details suh as currency synbol

    Returns:
        float: clean and formatted price value in float, each upto two decimal places.

    """
    price_from_regex_match = re.findall(
        r"\b(\d+(?:,\d{3})*)(?:[\.\,](\d{1,2}))?\b",
        price,
    )
    if len(price_from_regex_match):
        extracted_price = (
            re.sub(
                r"[,.]",
                "",
                price_from_regex_match[0][0],
            )
            + "."
        )
        extracted_price += cent if (cent := price_from_regex_match[0][1]) != "" else "00"
        return round(float(extracted_price), 2)
    else:
        log.info(" Not Able to convert the price %s", price)
        return 0


def str_to_dict(dict_str: str) -> dict[str, Any] | None:
    """Converts a string representation of a dictionary to a dictionary object.

    Args:
        dict_str (str): The string representation of the dictionary.

    Returns:
        (dict[str, Any] | None): The dictionary object extracted from the string, or None if no valid dictionary is found.
    """
    match = re.search(r"\{(?:[^{}]*\{[^{}]*\}[^{}]*|[^{}]*)*\}", dict_str) #NOSONAR
    if match:
        extracted_json = match.group()
        return json.loads(extracted_json)
    return None


def extract_text_in_quotes(content: str) -> str:
    """
    Extracts a string enclosed in double quotes from the given content.

    Args:
        content (str): The string containing the quoted text.

    Returns:
        str: The text enclosed in double quotes, or the original content if no quotes are found.
    """
    match = re.search(r'"(.*?)"', content)
    if match:
        return match.group()
    else:
        return content


def get_difference_between_lists(list1: list, list2: list) -> list:
    """
    Gets the difference between two lists
    Args:
        list1 (str): The first list with the super set
        list2 (str): The second list with the subset
    Returns:
        (list): The difference between the two lists
    """
    return list(set(list1).difference(set(list2)))


def dict_to_list_of_items(
    data: Union[dict, list, str],
) -> Union[list[tuple[Any, Any]], list[Any], str]:
    """
    Convert a dictionary to a list of items, recursively handling nested dictionaries.

    This function is useful for converting JSON or dictionary objects to a string representation
    without curly braces, which can be helpful in avoiding issues with prompts that contain curly
    braces.
    Args:
        data (Union[dict, list, str]): The data to convert. It can be a dictionary, list, or string.If it's a dictionary,
              it will be recursively converted. Lists and strings are returned as-is.
    Returns:
        Union[list[tuple[Any, Any]], list[Any], str]: The converted data. If the input is a
            dictionary, a list of key-value pairs (with nested dictionaries also converted) is
            returned. If the input is a list or string, it is returned as-is.

    """
    if isinstance(data, dict):
        return [(key, dict_to_list_of_items(value)) for key, value in data.items()]
    else:
        return data


def transform_json(data: dict) -> dict:
    """
    transform the keys of dictionary from camel case to snake case
    Args:
        data (dict): Payload as a dict
    Returns:
        (dict): Transformed data.
    """
    if isinstance(data, dict):
        return {
            re.sub(r"(?<!^)(?=[A-Z])", "_", k).lower(): transform_json(v) for k, v in data.items()
        }
    elif isinstance(data, list):
        return [transform_json(item) for item in data]
    return data


def parse_llm_json_response(
    response: str,
    json_keys: list[str],
) -> dict[str, str | list[str] | None]:
    """
    Parses the JSON response from LLM and extracts the specified keys.

    Args:
        response (str): The raw JSON response from the LLM.
        json_keys (list[str]): A list of keys to extract values from the parsed JSON response.

    Returns:
        dict: A dictionary containing the extracted values for the specified keys.
              If a key is not found or the value is invalid, it will return `None` for that key.
              If the response cannot be parsed as JSON, it returns an empty dictionary."""
    try:
        response = response.strip()
        response = response.encode("utf-8").decode("utf-8")
        parsed_response = json.loads(response)
        return_json_value = {}
        for key in json_keys:
            key_value = parsed_response.get(key, None)
            if key_value and key_value != "NONE":
                return_json_value[key] = key_value
            else:
                return_json_value[key] = None
        return return_json_value
    except json.JSONDecodeError as ex:
        log.info("Failed to decode LLM JSON response: %s due to error %s", response, ex)
        return {}


def convert_currency_to_numeric(value: str, currency: str = "EUR") -> float:
    """Converts a currency string to its numeric equivalent in float format.

    Args:
        value (str): The currency value as a string (e.g., "EUR 1.5M", "EUR 500K").
        currency (str, optional): The currency symbol to remove from the value. Default is "EUR".

    Returns:
        float: The numeric value of the currency string.
               Returns 0 if the value is null or if an error occurs during conversion."""
    try:
        if value in ["null", None]:
            return 0
        elif "M" in value:
            return float(value.replace(f"{currency} ", "").replace("M", "")) * 1e6
        elif "K" in value:
            return float(value.replace(f"{currency} ", "").replace("K", "")) * 1e3
        return float(value.replace(f"{currency} ", ""))
    except Exception as ex:
        error_msg = f"Error in coverting currency string {value} to numeric value in {currency}"
        log.error(error_msg + " - %s", ex)
        return 0
