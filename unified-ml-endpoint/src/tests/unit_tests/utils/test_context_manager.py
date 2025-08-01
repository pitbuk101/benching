import pytest

from ada.utils.metrics.context_manager import (
    UseCase,
    get_ai_cost_tags,
    set_intent_flow_context,
    set_tenant_and_intent_flow_context,
    set_tenant_context,
)


def test_setting_multiple_use_case_context_and_getting_the_values_concatenated():
    set_intent_flow_context(
        UseCase.CONTRACT_BENCHMARKING,
        UseCase.CONTRACT_ENTITY_EXTRACTION,
        UseCase.FUNC,
    )
    cost_tags = get_ai_cost_tags()
    assert cost_tags == "NA-CB_CEE_FUNC"


def test_setting_many_use_case_context_and_tenant_id_then_the_tenant_id_istruncated_to_8_chars_getting_the_values_concatenated():
    set_tenant_context("tenant123")
    set_intent_flow_context(
        UseCase.CONTRACT_BENCHMARKING,
        UseCase.CONTRACT_ENTITY_EXTRACTION,
        UseCase.FUNC,
    )
    cost_tags = get_ai_cost_tags()
    assert cost_tags == "tenant12-CB_CEE_FUNC"


def test_setting_both_tenant_id_and_list_of_use_case_together():
    set_tenant_and_intent_flow_context(
        "tenant123",
        UseCase.CONTRACT_BENCHMARKING,
        UseCase.CONTRACT_ENTITY_EXTRACTION,
        UseCase.FUNC,
    )
    cost_tags = get_ai_cost_tags()
    assert cost_tags == "tenant12-CB_CEE_FUNC"


def test_setting_both_tenant_id_and_single_use_case_together():
    set_tenant_and_intent_flow_context("tenant123", UseCase.CONTRACT_BENCHMARKING)
    cost_tags = get_ai_cost_tags()
    assert cost_tags == "tenant12-CB"


def test_setting_context_in_futures_should_work_with_context_set_separately():

    set_tenant_and_intent_flow_context("tenant123", UseCase.CONTRACT_BENCHMARKING)
    cost_tags = get_ai_cost_tags()
    assert cost_tags == "tenant12-CB"
