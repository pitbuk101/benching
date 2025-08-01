"""Tests for model_base  for LLM calls"""

import pytest

from ada.components.llm_models.model_base import Model


@pytest.mark.utils
def test_model_base_wrong_model():
    """
    TestModel base with wrong model.
    """
    with pytest.raises(ValueError, match="host not supported."):
        Model("wrong_model", temp=0).obj
