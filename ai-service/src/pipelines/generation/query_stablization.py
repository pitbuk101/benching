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

intent_classification_user_prompt_template="""
Given user's query convert and fix user's query to a  precise SQL-style intent.
User's query can be anything and it may not be in the  precise SQL-style intent.

{% if querystablization_rules  %}
{% for rule in querystablization_rules %}
{{ rule }}
{% endfor %}
{% endif %}

Query: {{ query }}

### Examples ###
Here are few examples:
1.  "what is the price of tin in asia for year [year] in category [category]"
    {
        "fixed_query": "Calculate the price of tin in asia for year [year] in category [category]"
    }

2.  "calculate the PCM Opportunity in current year in category [category]"
    {
        "fixed_query": "Calculate the PCM Opportunity in current year in category '[category]'"
    }

3. "calculate the rate harmonization for each supplier in year [year] in category [category]"
    {
        "fixed_query": "Calculate the rate harmonization for each supplier in year [year] in category '[category]'"
    }

4. "How many suppliers are there in category [category]"
    {
        "fixed_query": "Calculate the count of suppliers in category '[category]' in year [year]"
    }

5. "Is the market price for this category predicted to go up or down in the next 3 months"
    {
        "fixed_query": "Calculate the market price to go up or down in the next 3 months of year [year] in category '[category]'"
    }

6. "What is the total spend for the company Complex Assembly Safety GmbH for category '[category]'"
    {
        "fixed_query": "Calculate the total spend for the company 'Complex Assembly Safety GmbH' for category '[category]' in current year"
    }

7. "savings opportunity for material in category [category]"
    {
        "fixed_query": "calculate the total savings opportunity for material in category '[category]' in current year"
    }

8. "How many suppliers are there in category [category]"
    {
        "fixed_query": "Calculate the count of suppliers in category '[category]' in current year"
    }

9. "What is my price arbitrage in category [category]"
    {
        "fixed_query": "Calculate the rate harmonization in category '[category]' in current year"
    }

10. "How does our working marketing spend compare to industry benchmarks for this category"
    {
        "fixed_query": "calculate the working marketing spend and working benchmark for category '[category]' for year [year]"
    }

11. "Which agencies are providing the highest cost efficiency based on our spend data?"
    {
        "fixed_query": "calculate the highest agency fees benchmark spends for category '[category]' for year [year]"
    }

12. "What are the top cost-saving opportunities in our current agency contracts for category [category]"
    {
        "fixed_query": "calculate the highest agency cleansheet benchmark for category '[category]' for year [year]"
    }

13. "What is the total spend for November [year] in category '[category]'"
    {
        "fixed_query": "calculate the total spend in November [year] in category '[category]'"
    }

14. "List of single operating unit suppliers in category '[category]'"
    {
        "fixed_query": "calculate the single operating unit suppliers for category '[category]' for year [year]"
    }

15. "top 3 materials for top 3 key suppliers in category '[category]'"
    {
        "fixed_query": "calculate the top 3 materials for top 3 key suppliers for category '[category]' for year [year]"
    }

15. "Which vendor has increased the spend most in last 5 months for category '[category]'"
    {
        "fixed_query": "calculate the supplier with the highest increase in spend over the last 5 months of year [year] for category '[category]'."
    }

### OUTPUT FORMAT ###
    {
        "fixed_query": "...",
    }

"""
query_stablization_system_prompt="You are an expert at understanding and structuring natural language queries."


class QueryStablizationResult(BaseModel): 
    fixed_query: str
    # metric: str


def prepare_prompt(query: dict, tenant_id: str, prompt_builder: PromptBuilder) -> dict:
    logger.debug("Preparing prompt for query stablization")
    logger.info(f"tenant_id: {tenant_id}")
    prompt_file = Path(os.getenv("EXAMPLES"))/tenant_id/"querystablization_rules.txt"
    logger.debug(f"Prompt file: {prompt_file}")
    with open(prompt_file, "r") as f:
        rules = f.readlines()
    return prompt_builder.run(query=query, querystablization_rules=rules)

async def stablized_query(prepare_prompt: dict, generator: Any)-> dict:
    logger.debug("Stablizing query")
    return await generator.run(prompt=prepare_prompt.get("prompt"))

def clean_query_stablization_result(stablized_query: dict) -> dict:
    logger.debug("Cleaning stablized query")
    return stablized_query.get("replies")

def post_processor(clean_query_stablization_result: dict ) -> QueryStablizationResult:
    logger.debug("Post processing stablized query")
    logger.debug(f"Stablized query: {clean_query_stablization_result}")
    try:
        query = orjson.loads(clean_query_stablization_result[0])
        return QueryStablizationResult(**query)
    except Exception:
        logger.exception("Error in post processing stablized query")
        return QueryStablizationResult(fixed_query="")
        


query_stablization_model_kwargs = {
    "response_format": {
        "type": "json_schema",
        "json_schema": {
            "name": "query_stablization",
            "schema": QueryStablizationResult.model_json_schema(),
        },
    }
}


class QueryStabilization(BasicPipeline):
    def __init__(
            self,
            llm_provider: LLMProvider,
            **_
        ):
        self._components = {
            "generator": llm_provider.get_generator(
                system_prompt=query_stablization_system_prompt,
                generation_kwargs=query_stablization_model_kwargs
            ),
            "prompt_builder": PromptBuilder(
                template=intent_classification_user_prompt_template
            )
        }

        super().__init__(
            AsyncDriver({}, sys.modules[__name__], result_builder=base.DictResult())
        )
    
    @async_timer
    async def run(self, query: str, tenant_id: str) -> QueryStablizationResult:
        return await self._pipe.execute(
            ["post_processor"],
            inputs={
                "query": query,
                # TODO : Put id here for multi-tenancy # NOSONAR
                "tenant_id": tenant_id,
                **self._components
            }
            )
