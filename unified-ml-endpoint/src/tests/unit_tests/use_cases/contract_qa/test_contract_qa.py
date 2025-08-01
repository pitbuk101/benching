from ada.use_cases.contract_qa.contract_qa_util import is_integer


def test_is_integer():
    assert is_integer(None) is False
