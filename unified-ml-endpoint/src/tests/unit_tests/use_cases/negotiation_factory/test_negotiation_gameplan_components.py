from __future__ import annotations

import json
from unittest.mock import ANY, patch

import pandas as pd
import pytest
from langchain_community.chat_message_histories import ChatMessageHistory

from ada.use_cases.negotiation_factory.exception import NegotiationFactoryUserException
from ada.use_cases.negotiation_factory.negotiation_factory_utils import (
    identify_negotiation_objective,
)
from ada.use_cases.negotiation_factory.negotiation_gameplan_components import (
    generate_csb_positioning,
    generate_insights,
    generate_strategy,
)
from ada.utils.config.config_loader import read_config

negotiation_conf = read_config("use-cases.yml")["negotiation_factory"]


@pytest.fixture
def negotiation_metadata_mock():
    market_approach_data = {
        "is_auctionable": [False, True],
        "incumbency": [0, 5],
        "category_positioning": [["leverage"], ["leverage"]],
        "supplier_relationship": [["core"], ["core", "grow"]],
        "market_approach": ["market_approach 1", "market_approach 2"],
    }
    reference_data = {
        "market_approach_strategy": pd.DataFrame(market_approach_data),
    }
    category = "dummy_category"
    return reference_data, category


@pytest.fixture
def supplier_data_mock():
    supplier_name = "test supplier"
    supplier_profile = {
        "supplier_name": supplier_name,
        "number_of_sku": 6,
        "sku_list": ["sku_1", "sku_2", "sku_3", "sku_4", "sku_5"],
        "spend_ytd": 1321.99,
        "spend_last_year": 1000.0,
        "currency_symbol": "$",
        "currency_position": "prefix",
        "percentage_spend_across_category_ytd": 12.98,
        "supplier_relationship": "core",
        "number_of_supplier_in_category": 50,
    }
    pinned_elements = {"supplier_profile": supplier_profile}
    return supplier_name, supplier_profile, pinned_elements


@pytest.fixture
def insight_data_mock():
    insight_data = [
        {
            "id": "I1",
            "insight": "label_1",
            "insight_objective": "objective_1",
            "insight_objective": "objective_1",
            "insight_reinforcements": ["reinforcements_1", "reinforcements_2"],
            "list_of_skus": [],
        },
        {
            "id": "I2",
            "insight": "label_2",
            "insight_objective": "objective_2",
            "insight_reinforcements": ["reinforcements_1", "reinforcements_3"],
            "list_of_skus": [],
        },
        {
            "id": "I3",
            "insight": "label_3",
            "insight_objective": "objective_1",
            "insight_reinforcements": ["reinforcements_4", "reinforcements_3"],
            "list_of_skus": [],
        },
    ]
    return insight_data


@pytest.fixture
def objective_data_mock():
    objective_data = [
        {
            "objective_type": "objective_1",
            "objective": "summary 2",
            "list_of_skus": [],
        },
        {
            "objective_type": "objective_2",
            "objective": "summary 2",
            "list_of_skus": [],
        },
        {
            "objective_type": "objective_3",
            "objective": "summary 3",
            "list_of_skus": [],
        },
    ]
    return objective_data


@pytest.fixture
def pg_connector_mock():
    with patch(
        "ada.use_cases.negotiation_factory.negotiation_factory_utils.PGConnector",
    ) as mock_obj:
        yield mock_obj.return_value


@patch("ada.use_cases.negotiation_factory.negotiation_gameplan_components.run_conversation_chat")
@patch(
    "ada.use_cases.negotiation_factory.negotiation_gameplan_components.negotiation_strategy_prompt",
)
@patch(
    "ada.use_cases.negotiation_factory.negotiation_gameplan_components.get_negotiation_strategy_data",
)
def test_generate_strategy(
    get_negotiation_strategy_data_mock,
    negotiation_strategy_prompt_mock,
    run_conversation_chat_mock,
    pg_connector_mock,
    negotiation_metadata_mock,
    supplier_data_mock,
):
    reference_data, category = negotiation_metadata_mock
    user_query = "suggest negotiation strategy"
    _, supplier_profile, pinned_elements = supplier_data_mock
    chat_history = ChatMessageHistory(message=[])

    negotiation_strategy_data = {
        "category": category,
        "is_auctionable": True,
        "category_positioning": "leverage",
        "pricing_methodology": ["Market based pricing", "Index based pricing", "Cost plus model"],
        "contract_methodology": [
            "Framework agreement approach",
            "Long term contract",
            "Indefinite delivery",
        ],
    }

    get_negotiation_strategy_data_mock.return_value = negotiation_strategy_data

    market_approach = "market approach 1"

    response = {
        "message": (
            "Great! Based on our expertise, here is the best sourcing approach"
            " to adopt:\n**Market approach**: market approach 1 - "
            "\n**Pricing methodology**: test pricing methodology - \n"
            "**Contracting methodology**: test contracting methodology - "
        ),
        "suggested_prompts": ["prompt 1", "prompt 2"],
        "market_approach": market_approach,
        "pricing_methodology": "test pricing methodology",
        "contracting_methodology": "test contracting methodology",
    }
    run_conversation_chat_mock.return_value = json.dumps(response)

    expected_data = {
        "response_type": "negotiation_strategy",
        "message": (
            "Great! Based on our expertise, here is the best sourcing approach to "
            "adopt:\n**Market approach**: market approach 1 - \n**Pricing methodology**: test "
            "pricing methodology - \n**Contracting methodology**: test contracting methodology - "
        ),
        "suggested_prompts": [
            {
                "prompt": "Change market approach",
                "intent": "negotiation_strategy_change",
            },
            {
                "prompt": "Change pricing methodology",
                "intent": "negotiation_strategy_change",
            },
            {
                "prompt": "Change contracting methodology",
                "intent": "negotiation_strategy_change",
            },
            {
                "prompt": "Set tone & tactics",
                "intent": "negotiation_approach_tnt",
            },
        ],
        "supplier_profile": {
            "supplier_name": "test supplier",
            "number_of_sku": 6,
            "sku_list": [
                "sku_1",
                "sku_2",
                "sku_3",
                "sku_4",
                "sku_5",
            ],
            "spend_ytd": 1321.99,
            "spend_last_year": 1000,
            "currency_symbol": "$",
            "currency_position": "prefix",
            "percentage_spend_across_category_ytd": 12.98,
            "supplier_relationship": "core",
            "number_of_supplier_in_category": 50,
        },
        "negotiation_strategy": {
            "market_approach": {
                "value": "market approach 1",
                "details": "",
            },
            "pricing_methodology": {
                "value": "test pricing methodology",
                "details": "",
            },
            "contracting_methodology": {
                "value": "test contracting methodology",
                "details": "",
            },
        },
    }

    actual_data = generate_strategy(
        reference_data,
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
        chat_history,
        generation_type="negotiation_strategy",
    )

    assert expected_data == actual_data
    get_negotiation_strategy_data_mock.assert_called_once_with(
        reference_data,
        category,
    )
    negotiation_strategy_prompt_mock.assert_called_once()
    # run_conversation_chat_mock.assert_called_once_with(
    #     chat_history=chat_history,
    #     prompt=ANY,
    #     input_str=user_query,
    #     model=negotiation_conf["model"]["model_name"],
    #     memory_type="window",
    #     window_size=negotiation_conf["model"]["conversation_buffer_window"],
    #     temperature=0,
    #     input_message_key="input",
    #     history_message_key="history",
    #     session_id="",
    # )


@patch("ada.use_cases.negotiation_factory.negotiation_gameplan_components.run_conversation_chat")
@patch(
    "ada.use_cases.negotiation_factory.negotiation_gameplan_components.negotiation_set_positioning_prompt",
)
@patch(
    "ada.use_cases.negotiation_factory.negotiation_gameplan_components.get_negotiation_strategy_data",
)
def test_generate_approach_cp(
    get_negotiation_strategy_data_mock,
    negotiation_set_positioning_prompt_mock,
    run_conversation_chat_mock,
    pg_connector_mock,
    negotiation_metadata_mock,
    supplier_data_mock,
):
    reference_data, category = negotiation_metadata_mock
    user_query = "suggest negotiation approach"
    _, supplier_profile, pinned_elements = supplier_data_mock
    chat_history = ChatMessageHistory(message=[])
    negotiation_strategy_data = {
        "category": category,
        "is_auctionable": True,
        "category_positioning": "leverage",
        "pricing_methodology": ["Market based pricing", "Index based pricing", "Cost plus model"],
        "contract_methodology": [
            "Framework agreement approach",
            "Long term contract",
            "Indefinite delivery",
        ],
    }
    pinned_elements["negotiation_approach"] = {"test_aproach"}
    get_negotiation_strategy_data_mock.return_value = negotiation_strategy_data

    category_positioning = "category positioning"

    response = {
        "message": (
            "Let’s align first on our understanding of the "
            "category positioning. Based on our analysis: \n**"
            "category positioning**: category positioning - "
        ),
        "category_positioning": category_positioning,
        "category_positioning_detail": "",
    }

    run_conversation_chat_mock.return_value = json.dumps(response)

    expected_data_cp = {
        "response_type": "negotiation_approach_cp",
        "message": "Let\u2019s align first on our understanding of the category positioning. Based on our analysis: ",
        "suggested_prompts": [
            {
                "prompt": "Change category positioning",
                "intent": "negotiation_strategy_change",
            },
            {
                "prompt": "Set supplier positioning",
                "intent": "negotiation_approach_sp",
            },
            {
                "prompt": "Set buyer positioning",
                "intent": "negotiation_approach_bp",
            },
            {
                "prompt": "Set sourcing approach",
                "intent": "negotiation_strategy",
            },
            {
                "prompt": "Set tone & tactics",
                "intent": "negotiation_approach_tnt",
            },
        ],
        "supplier_profile": {
            "supplier_name": "test supplier",
            "number_of_sku": 6,
            "sku_list": [
                "sku_1",
                "sku_2",
                "sku_3",
                "sku_4",
                "sku_5",
            ],
            "spend_ytd": 1321.99,
            "spend_last_year": 1000.0,
            "currency_symbol": "$",
            "currency_position": "prefix",
            "percentage_spend_across_category_ytd": 12.98,
            "supplier_relationship": "core",
            "number_of_supplier_in_category": 50,
        },
        "category_positions": [
            {
                "value": "Category Positioning",
                "details": "",
            },
        ],
    }

    actual_data_cp = generate_csb_positioning(
        reference_data,
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
        chat_history,
        generation_type="negotiation_approach_cp",
    )

    assert expected_data_cp == actual_data_cp

    get_negotiation_strategy_data_mock.assert_called_once_with(
        reference_data,
        category,
    )
    negotiation_set_positioning_prompt_mock.assert_called_once()
    # run_conversation_chat_mock.assert_called_once_with(
    #     chat_history=ChatMessageHistory(message=[]),
    #     prompt=ANY,
    #     input_str=user_query,
    #     model=negotiation_conf["model"]["model_name"],
    #     memory_type="window",
    #     window_size=negotiation_conf["model"]["conversation_buffer_window"],
    #     temperature=0,
    #     input_message_key="input",
    #     history_message_key="history",
    #     session_id="",
    # )


@patch("ada.use_cases.negotiation_factory.negotiation_gameplan_components.run_conversation_chat")
@patch(
    "ada.use_cases.negotiation_factory.negotiation_gameplan_components.negotiation_set_positioning_prompt",
)
@patch(
    "ada.use_cases.negotiation_factory.negotiation_gameplan_components.get_negotiation_strategy_data",
)
def test_generate_approach_sp(
    get_negotiation_strategy_data_mock,
    negotiation_set_positioning_prompt,
    run_conversation_chat_mock,
    pg_connector_mock,
    negotiation_metadata_mock,
    supplier_data_mock,
):
    reference_data, category = negotiation_metadata_mock
    user_query = "suggest negotiation approach"
    _, supplier_profile, pinned_elements = supplier_data_mock
    chat_history = ChatMessageHistory(message=[])
    negotiation_strategy_data = {
        "category": category,
        "is_auctionable": True,
        "category_positioning": "leverage",
        "pricing_methodology": ["Market based pricing", "Index based pricing", "Cost plus model"],
        "contract_methodology": [
            "Framework agreement approach",
            "Long term contract",
            "Indefinite delivery",
        ],
    }
    pinned_elements["negotiation_approach"] = {"test_aproach"}
    get_negotiation_strategy_data_mock.return_value = negotiation_strategy_data

    category_positioning = "category positioning"
    supplier_positioning = "supplier positioning"

    response = {
        "message": (
            "Let’s align first on our understanding of the "
            "supplier positioning. Based on our analysis: \n**"
            "Supplier positioning**: supplier positioning - "
        ),
        "category_positioning": category_positioning,
        "category_positioning_detail": "",
        "supplier_positioning": supplier_positioning,
        "supplier_positioning_detail": "",
    }

    run_conversation_chat_mock.return_value = json.dumps(response)

    expected_data_sp = {
        "response_type": "negotiation_approach_sp",
        "message": (
            "Let’s align first on our understanding of the "
            "supplier positioning. Based on our analysis: "
        ),
        "supplier_positions": [
            {
                "value": "Supplier Positioning",
                "details": "",
            },
        ],
        "suggested_prompts": [
            {
                "prompt": "Set category positioning",
                "intent": "negotiation_approach_cp",
            },
            {
                "prompt": "Change supplier positioning",
                "intent": "negotiation_strategy_change",
            },
            {
                "prompt": "Set buyer positioning",
                "intent": "negotiation_approach_bp",
            },
            {
                "prompt": "Set sourcing approach",
                "intent": "negotiation_strategy",
            },
            {
                "prompt": "Set tone & tactics",
                "intent": "negotiation_approach_tnt",
            },
        ],
        "supplier_profile": supplier_profile,
    }

    actual_data_sp = generate_csb_positioning(
        reference_data,
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
        chat_history,
        generation_type="negotiation_approach_sp",
    )

    assert expected_data_sp == actual_data_sp

    get_negotiation_strategy_data_mock.assert_called_once_with(
        reference_data,
        category,
    )
    negotiation_set_positioning_prompt.assert_called_once()
    # run_conversation_chat_mock.assert_called_once_with(
    #     chat_history=ChatMessageHistory(message=[]),
    #     prompt=ANY,
    #     input_str=user_query,
    #     model=negotiation_conf["model"]["model_name"],
    #     window_size=negotiation_conf["model"]["conversation_buffer_window"],
    #     memory_type="window",
    #     temperature=0,
    #     input_message_key="input",
    #     history_message_key="history",
    #     session_id="",
    # )


@patch(
    "ada.use_cases.negotiation_factory.negotiation_gameplan_components.generate_chat_response_with_chain",
)
@patch(
    "ada.use_cases.negotiation_factory.negotiation_gameplan_components.get_supplier_profile_insights_objectives",
)
def test_generate_insights(
    get_supplier_profile_insights_objectives_mock,
    generate_chat_response_mock,
    pg_connector_mock,
    negotiation_metadata_mock,
    insight_data_mock,
    objective_data_mock,
    supplier_data_mock,
):
    _, category = negotiation_metadata_mock
    supplier_name, supplier_profile, pinned_elements = supplier_data_mock
    user_query = "generate insights for objective 1"

    get_supplier_profile_insights_objectives_mock.return_value = (
        supplier_name,
        supplier_profile,
        insight_data_mock,
        objective_data_mock,
    )

    objective = ["objective_1"]
    ai_response = {"extracted_objectives": objective}
    generate_chat_response_mock.return_value = json.dumps(ai_response)
    expected_data = {
        "response_type": "insights",
        "message": f"Please see below important insights for supplier {supplier_name}.",
        "suggested_prompts": [
            {
                "prompt": "Learn more about supplier",
                "intent": "negotiation_user_questions",
            },
            {
                "prompt": "Set negotiation objectives",
                "intent": "negotiation_objective",
            },
        ],
        "insights": [
            {
                "id": "I1",
                "insight": "label_1",
                "insight_objective": "objective_1",
                "insight_reinforcements": [
                    "reinforcements_1",
                    "reinforcements_2",
                ],
                "list_of_skus": [],
            },
            {
                "id": "I3",
                "insight": "label_3",
                "insight_objective": "objective_1",
                "insight_reinforcements": [
                    "reinforcements_4",
                    "reinforcements_3",
                ],
                "list_of_skus": [],
            },
        ],
        "supplier_profile": supplier_profile,
    }

    actual_data = generate_insights(
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
        "negotiation_insights",
        "negotiation_insights",
    )

    assert expected_data == actual_data
    get_supplier_profile_insights_objectives_mock.assert_called_once_with(
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
    )
    generate_chat_response_mock.assert_called_once_with(
        ANY,
        model=negotiation_conf["model"]["model_name"],
    )


@patch(
    "ada.use_cases.negotiation_factory.negotiation_gameplan_components.get_supplier_profile_insights_objectives",
)
def test_generate_insights_with_intent_begin(
    get_supplier_profile_insights_objectives_mock,
    pg_connector_mock,
    negotiation_metadata_mock,
    insight_data_mock,
    objective_data_mock,
    supplier_data_mock,
):
    _, category = negotiation_metadata_mock
    supplier_name, supplier_profile, pinned_elements = supplier_data_mock
    user_query = "generate insights for objective 1"
    intent = "negotiation_begin"

    get_supplier_profile_insights_objectives_mock.return_value = (
        supplier_name,
        supplier_profile,
        insight_data_mock,
        objective_data_mock,
    )

    expected_data = {
        "response_type": "supplier_profile",
        "message": f"Thank you for selecting supplier {supplier_name}. ",
        "suggested_prompts": [],
        "supplier_profile": supplier_profile,
    }

    actual_data = generate_insights(
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
        generation_type=intent,
        before_update_request_type=intent,
    )

    assert expected_data == actual_data
    get_supplier_profile_insights_objectives_mock.assert_called_once_with(
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
    )


@patch(
    "ada.use_cases.negotiation_factory.negotiation_gameplan_components.get_supplier_profile_insights_objectives",
)
def test_generate_insights_without_any_insights(
    get_supplier_profile_insights_objectives_mock,
    pg_connector_mock,
    negotiation_metadata_mock,
    supplier_data_mock,
):
    _, category = negotiation_metadata_mock
    supplier_name, supplier_profile, pinned_elements = supplier_data_mock
    user_query = "generate insights for objective 1"

    get_supplier_profile_insights_objectives_mock.return_value = (
        supplier_name,
        supplier_profile,
        [],
        [],
    )

    expected_data = {
        "response_type": "insights",
        "message": f"Apologies, but at the moment, we dont have any insights for supplier {supplier_name}",
        "suggested_prompts": [],
        "supplier_profile": supplier_profile,
    }

    actual_data = generate_insights(
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
        generation_type="negotiation_insights",
        before_update_request_type="negotiation_insights",
    )

    assert expected_data == actual_data


@patch(
    "ada.use_cases.negotiation_factory.negotiation_gameplan_components.generate_chat_response_with_chain",
)
@patch(
    "ada.use_cases.negotiation_factory.negotiation_gameplan_components.get_supplier_profile_insights_objectives",
)
def test_generate_insights_without_objectives(
    get_supplier_profile_insights_objectives_mock,
    generate_chat_response_mock,
    pg_connector_mock,
    negotiation_metadata_mock,
    insight_data_mock,
    objective_data_mock,
    supplier_data_mock,
):
    _, category = negotiation_metadata_mock
    supplier_name, supplier_profile, pinned_elements = supplier_data_mock
    user_query = "generate insights for objective 1"

    get_supplier_profile_insights_objectives_mock.return_value = (
        supplier_name,
        supplier_profile,
        insight_data_mock,
        objective_data_mock,
    )

    ai_response = {
        "extracted_objectives": ["objective 10"],
    }
    generate_chat_response_mock.return_value = json.dumps(ai_response)

    expected_data = {
        "response_type": "insights",
        "message": (
            "I'm sorry, but I couldn't find any insights matching with specified goal"
            f" [ i.e. objective 10 ]"
            f"for supplier {supplier_name}. Is there anything else I can assist you with ?"
        ),
        "suggested_prompts": [],
        "supplier_profile": supplier_profile,
    }

    actual_data = generate_insights(
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
        generation_type="negotiation_insights",
        before_update_request_type="negotiation_insights",
    )
    assert expected_data == actual_data
    get_supplier_profile_insights_objectives_mock.assert_called_once_with(
        pg_connector_mock,
        category,
        user_query,
        pinned_elements,
    )
    generate_chat_response_mock.assert_called_once_with(
        ANY,
        model=negotiation_conf["model"]["model_name"],
    )


def test_identify_negotiation_objective(objective_data_mock):
    pinned_elements = {
        "objectives": [
            objective
            for objective in objective_data_mock
            if objective["objective_type"] == "objective_1"
        ],
    }
    expected_data = ["objective_1"]
    objectives_in_action = identify_negotiation_objective(pinned_elements=pinned_elements)
    actual_data = [
        objective.get("objective_type", "")
        for objective in objectives_in_action
        if objective.get("objective_type", "").lower() != "key facts"
    ]

    assert actual_data == expected_data


def test_identify_negotiation_objective_without_pinned_insights():
    pinned_elements = {"objectives": []}
    expected_data = (
        "('Currently, there are no active objectives pinned.please pin some objectives "
        "which you find important so that Ada can assist you in preparing for negotiation.', "
        "[{'prompt': '"
        f"{negotiation_conf['cta_button_map']['objective']}', 'intent': 'negotiation_objective'"
        "}])"
    )

    with pytest.raises(NegotiationFactoryUserException) as negotiation_exception_with_cta:
        identify_negotiation_objective(pinned_elements)

    assert str(negotiation_exception_with_cta.value) == expected_data
