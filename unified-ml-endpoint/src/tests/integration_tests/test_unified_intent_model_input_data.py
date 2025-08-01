def get_uniformed_input_json() -> dict:
    return {
        "contract-qa": {
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "category": "Bearings",
            "page_id": "idea-generation",
            "chat_id": "123_QA",
            "request_id": "0",
            "document_id": 1002,
            "user_query": "What is the payment terms for this contract?",
            "request_type": "user_input",
            "pinned_elements": {
                "insights": [
                    {
                        "insight": "The total cleansheet gap identified in last 12 months for bearings is up to 2.9M EUR.",
                        "is_main": "1",
                        "insight_id": "2083021635",
                    },
                ],
            },
        },
        "idea-generation": {
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "category": "Bearings",
            "page_id": "idea-generation",
            "chat_id": "123_KB",
            "request_id": "1",
            "user_query": "Define Net Sales terms in the cotext of agreements.",
            "request_type": "user_input",
            "pinned_elements": {
                "insights": [
                    {
                        "insight": "The total cleansheet gap identified in last 12 months for bearings is up to 2.9M EUR.",
                        "is_main": "1",
                        "insight_id": "2083021635",
                    },
                ],
            },
        },
        "key-facts-v2": {
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "category": "Bearings",
            "page_id": "idea-generation",
            "chat_id": "123_KF",
            "request_id": "2",
            "user_query": "What is spend break down across different sub-categories for last 4 months?",
            "request_type": "user_input",
            "pinned_elements": {
                "insights": [
                    {
                        "insight": "The total cleansheet gap identified in last 12 months for bearings is up to 2.9M EUR.",
                        "is_main": "1",
                        "insight_id": "2083021635",
                    },
                ],
            },
        },
        "idea-generation-v3": {
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "chat_id": "123_IG",
            "category": "Bearings",
            "request_type": "rca",
            "page_id": "idea-generation",
            "request_id": "4",
            "pinned_elements": {
                "insights": [
                    {
                        "insight": "The total cleansheet gap identified in last 12 months for bearings is up to 2.9M EUR.",
                        "is_main": "1",
                        "insight_id": "2083021635",
                    },
                ],
            },
            "user_query": "Can you expand on the root causes?",
        },
        "negotiation-factory": {
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "category": "Bearings",
            "chat_id": "123_NF",
            "page_id": "negotiation",
            "request_id": "5",
            "user_query": "Generate arguments",
            "negotiation_objective": "spend",
            "pinned_elements": {
                "supplier_profile": {
                    "supplier_name": "SKF FRANCE",
                    "total_spend": "33993184.36259999",
                    "number_of_sku": "15",
                    "spend_across_category": "16.2%",
                    "number_of_category_suppliers": "50",
                    "supplier_relationship": "core",
                    "recommend_negotiation_strategy": "in-person negotiation",
                    "target_savings": "",
                },
                "insights": [
                    {
                        "insight_id": "1000460",
                        "insight": "SKF bearings- analysis Increasing up to 10% in the volume allocated \
                            to the selected supplier could have an impact of up to 90.6K EUR.",
                        "insight_objective": "spend",
                    },
                ],
            },
        },
    }
