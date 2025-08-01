import pytest

from ada.utils.io.misc import (
    clean_string,
    fetch_string_within_triple_quote,
    import_csv_sheet_for_clauses,
    move_dict_key_to_top,
    num_tokens_from_messages,
    sort_dict_by_key,
)


@pytest.mark.utils
def test_sort_dict_by_key():
    """
    Test sort_dict_by_key().
    """
    unsorted_dict = {"b": 2, "a": 1, "c": 3}
    sorted_dict = {"a": 1, "b": 2, "c": 3}
    assert sort_dict_by_key(unsorted_dict) == sorted_dict


@pytest.mark.utils
def test_move_dict_key_to_top():
    """
    Test move_dict_key_to_top().
    """
    unsorted_dict = {"b": 2, "a": 1, "c": 3}
    sorted_dict = {"b": 2, "c": 3, "a": 1}
    assert move_dict_key_to_top("a", unsorted_dict) == sorted_dict


@pytest.mark.utils
def test_num_tokens_from_messages():
    """
    Test num_tokens_from_messages().
    """
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "bot", "content": "I'm doing well, thanks!"},
    ]
    assert num_tokens_from_messages(messages) == 26


@pytest.mark.utils
def test_num_tokens_from_messages_wrong_model():
    """
    Test num_tokens_from_messages() with wrong model.
    """
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "bot", "content": "I'm doing well, thanks!"},
    ]
    with pytest.raises(NotImplementedError):
        num_tokens_from_messages(messages, model="wrong_model")


@pytest.mark.utils
def test_import_csv_sheet_for_clauses():
    """
    Test import_csv_sheet_for_clauses().
    """
    csv_file = "data/contract_benchmarks/clause_questions_20231102.csv"
    list_clauses, list_questions = import_csv_sheet_for_clauses(csv_file)
    assert len(list_clauses) == len(list_questions)
    assert len(list_clauses) == 40


@pytest.mark.utils
def test_clean_string():
    """
    Test clean_string().
    """
    string = "This is a string to be used as a filename"
    assert clean_string(string) == "this-is-a-string-to-be-used-as-a-filename"


@pytest.mark.utils
def test_fetch_string_within_triple_quotes():
    """
    Test fetch_string_within_triple_quotes().
    """
    string = "```This is a string surrounded by triple quotes.```"
    assert (
        fetch_string_within_triple_quote(string) == "This is a string surrounded by triple quotes."
    )
