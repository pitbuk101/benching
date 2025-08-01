import os
from pathlib import Path
import sys
import logging
from typing import Any
from pydantic import BaseModel

import orjson
from hamilton import base
from hamilton.async_driver import AsyncDriver
from haystack.components.builders.prompt_builder import PromptBuilder

from src.utils import async_timer, timer
from src.pipelines.common import BasicPipeline
from src.providers import LLMProvider

logger = logging.getLogger("wren-ai-service")


query_reranker_user_prompt_template="""
# Task
You are an expert SQL analyst who is tasked with understanding all the user's questions and reranking the sample question in the order which best describes or is similar to the user's question

## User Question
User's question: "{{ user_question }}"

## Problem Solving Ontology
We have multiple suppliers, these suppliers have different materials which we buy from them.
These Suppliers have plants which are located in different countries.
The materials are bought for different categories these categories are like CIBC or Valves
Now there are spends which we do to buy these materials from suppliers.
Now we can look from the perspective of suppliers, materials, plants and countries by asking questions like:
- Spend of Suppliers
    - top spends by suppliers
    - bottom spends by suppliers
    - Supplier '<supplier_name>' spend
- Spend of Materials
    - top spends by materials
    - bottom spends by materials
    - Material '<material_name>' spend
- Spend of Plants
    - top spends by plants
    - bottom spends by plants
    - Plant '<plant_name>' spend
- Spend of Countries
    - top spends by countries
    - bottom spends by countries
    - Country '<country_name>' spend

Now comes the part where we can look to improve these spends by looking at the different metrics like:
- Price Arbitrage
- LPP
- Parametric Cost Modeling
- Supplier Consolidation
- HCC LCC Opportunity
- OEM Non-OEM Opportunity
- Payment Term Standardization
- Early payment Opportunity
- Unused Discounts
These metrics are calculated at material level and then aggregated to supplier or plant or country level.

## MANDATORY INSTRUCTIONS
1. Given the sample questions rank these questions in terms of how well they help answer the user's question.
2. Provide a confidence threshold also which can very from 0 to 1.
3. OUTPUT QUESTIONS ALWAYS SHOULD BE FROM THE SAMPLE QUESTIONS else they won't match the original question.
    For Example:
    Original Sample Question: "calculate the count of supplier with price arbitrage for current year for category [category]"
    Expected Output: "calculate the count of supplier with price arbitrage for current year for category [category]"
    Unwanted Output: "calculate the count of suppliers with price arbitrage for current year for category [category]"


## SAMPLE Questions
Here are SAMPLE SQL questions retrieved from an embedding search:
{% for sql in samples %}
SAMPLE: {{ loop.index  }} 
{{ sql }}
{% endfor %}

## JSON OUTPUT FORMAT
{
    "response": [
        {
            "question": "...",
            "confidence": 0.95
        },
        {
            "question": "...",
            "confidence": 0.90
        }
    ]
}

## Example Output
    - Question:
        calculate the oem and non oem supplier spend for current year for category [category]
    - Sample Questions:
        SAMPLE: 1
        calculate the oem non oem spend for current year for category [category]
        SAMPLE: 2
        calculate the non oem spend for current year for category [category]
        SAMPLE: 3
        calculate the oem spend for supplier for current year for category [category]
        SAMPLE: 4
        calculate the total oem non oem opportunity for current year for category [category]
        SAMPLE: 5
        calculate the top suppliers by highest oem non oem opportunity for current year for category [category]
        SAMPLE: 6
        calculate the count of oem non suppliers for current year for category [category]
        SAMPLE: 7
        calculate the oem non oem opportunity for current year for category [category]
        SAMPLE: 8
        calculate the oem non oem opportunity percentage for current year for category [category]
        SAMPLE: 9
        calculate the oem non oem opportunity for current quarter for category [category]
        SAMPLE: 10
        calculate the top materials by highest oem non oem opportunity for current year for category [category]
    - Output:
        {
            "response":[
                {
                    "question": "calculate the oem non oem spend for current year for category [category]",
                    "confidence": 0.98
                },
                {
                    "question": "calculate the non oem spend for current year for category [category]",
                    "confidence": 0.85
                },
                {
                    "question": "calculate the oem spend for supplier for current year for category [category]",
                    "confidence": 0.8
                },
                {
                    "question": "calculate the total oem non oem opportunity for current year for category [category]",
                    "confidence": 0.75
                },
                {
                    "question": "calculate the oem non oem opportunity for current year for category [category]",
                    "confidence": 0.7
                },
                {
                    "question": "calculate the top suppliers by highest oem non oem opportunity for current year for category [category]",
                    "confidence": 0.65
                },
                {
                    "question": "calculate the count of oem non suppliers for current year for category [category]",
                    "confidence": 0.6
                },
                {
                    "question": "calculate the oem non oem opportunity percentage for current year for category [category]",
                    "confidence": 0.55
                },
                {
                    "question": "calculate the oem non oem opportunity for current quarter for category [category]",
                    "confidence": 0.5
                },
                {
                    "question": "calculate the top materials by highest oem non oem opportunity for current year for category [category]",
                    "confidence": 0.45
                }
            ]
        }
"""

query_reranking_system_prompt="You are an expert SQL analyst helping to choose the most relevant question for a user question."

class QueryRerankerResult(BaseModel):
    response: list[dict]


def prepare_prompt(query: dict, tenant_id: str, samples: list[str], documents: str,  prompt_builder: PromptBuilder) -> dict:
    logger.debug("Preparing prompt for query reranking")
    logger.info(f"tenant_id: {tenant_id}")
    # prompt_file = Path(os.getenv("EXAMPLES"))/tenant_id/"querystablization_rules.txt"
    # logger.debug(f"Prompt file: {prompt_file}")
    # with open(prompt_file, "r") as f:
        # rules = f.readlines()
    return prompt_builder.run(user_question=query, samples=samples, documents=documents)

async def rerank_query(prepare_prompt: dict, generator: Any)-> dict:
    logger.debug("Reranking query")
    return await generator.run(prompt=prepare_prompt.get("prompt"))

def clean_reranking_query_result(rerank_query: dict) -> dict:
    logger.debug("Cleaning reranked query")
    return rerank_query.get("replies")


def post_processor(clean_reranking_query_result: dict ) -> QueryRerankerResult:
    logger.debug("Post processing reranked query results")
    logger.debug(f"Reranked query: {clean_reranking_query_result}")
    try:
        query = orjson.loads(clean_reranking_query_result[0])
        logger.debug(f"Parsed query: {query}")
        return QueryRerankerResult(**query)
    except Exception:
        logger.exception("Error in post processing reranked query results")
        return QueryRerankerResult(response="", combined_strategy="")


query_reranking_model_kwargs = {
    "response_format": {
        "type": "json_schema",
        "json_schema": {
            "name": "query_reranking",
            "schema": QueryRerankerResult.model_json_schema(),
        },
    }
}

class QueryReranking(BasicPipeline):
    def __init__(
            self,
            llm_provider: LLMProvider,
            **_
        ):
        self._components = {
            "generator": llm_provider.get_generator(
                system_prompt=query_reranking_system_prompt,
                generation_kwargs=query_reranking_model_kwargs
            ),
            "prompt_builder": PromptBuilder(
                template=query_reranker_user_prompt_template,
            )
        }

        super().__init__(
            AsyncDriver({}, sys.modules[__name__], result_builder=base.DictResult())
        )
    
    @async_timer
    async def run(self, query: str, samples: str, documents: str, tenant_id: str) -> QueryRerankerResult:
        return await self._pipe.execute(
            ["post_processor"],
            inputs={
                "query": query,
                "samples": samples,
                "documents": documents,
                "tenant_id": tenant_id,
                **self._components
            }
            )
