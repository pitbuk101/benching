import logging
import os
import sys
from pathlib import Path
import time
from typing import Any, Dict, List

from hamilton import base
from hamilton.async_driver import AsyncDriver
from haystack.components.builders.prompt_builder import PromptBuilder
from langfuse.decorators import observe
from pydantic import BaseModel

from src.core.engine import Engine
from src.core.pipeline import BasicPipeline
from src.core.provider import LLMProvider
from src.pipelines.common import (
    TEXT_TO_SQL_RULES,
    SQLGenPostProcessor,
    construct_instructions,
    show_current_time,
    sql_generation_system_prompt,
)
from src.utils import async_timer, timer
from src.web.v1.services import Configuration

logger = logging.getLogger("wren-ai-service")


sql_generation_user_prompt_template = """
### TASK ###
Given a user query that is ambiguous in nature, your task is to interpret the query in various plausible ways and
generate one SQL statement for ANSI SQL that best potentially answer user's query.

### MANDATORY JOINING RULES ###
1. ALWAYS USE ID type of colums to join tables.
2. DO NOT USE TEXT columns to join tables unless specified.
3. ALWAYS USE JOINS MENTIONED IN `DATABASE SCHEMA` to join tables.
4. REFER `SAMPLES` for the correct join conditions.

### MANDATORY DIVISION RULES ###
1. When dividing any two columns in sql, ALWAYS put the denominator greater than 0 in where clause to avoid division by zero error.

### MANDATORY AGGREGRATION RULES ###
1. Try to AGGREGATE on CATEGORICAL AND TIME BASED columns .
2.  IF AGGREGATION is done the columns should be present in the final output.
    - For example, **supplier**, **material**, **year**, **country**, **category**, **quarter**, **plant** etc.
    - If a time dimension (like **year**, **quarter**) is mentioned, make sure it must be included in both the `WHERE` clause and `SELECT` clause to ensure accurate time-related data is returned.
    - When aggregating, always **GROUP BY** the relevant hierarchical levels (e.g., supplier, material, year, quarter, month, country, category, plant) to ensure results are grouped correctly.
3. DO NOT USE COUNT(1) or COUNT(*) in the SQL queries. Instead use COUNT(COLUMN_NAME) to avoid performance issues.
4. AVOID USING LAG and LEAD functions in the SQL queries unless specified.

### MANDATORY TIME HANDLING RULES ### 
1. Extract last nth date from current date : DATEADD(DAY, -n, CURRENT_DATE)
2. Extract year from timestamp: YEAR(CURRENT_TIMESTAMP)
3. Extract current year:  YEAR(CURRENT_DATE)
4. Extract previous quarter:  QUARTER(DATEADD(MONTH, -3, CURRENT_DATE))
5. Extract current date and time: CURRENT_TIMESTAMP
6. Extract current date: CURRENT_DATE
7. Convert a given date column to date format: TO_DATE(DIM_DATE, 'YYYYMMDD')
8. Extract year from a give column: YEAR(TO_DATE(DIM_DATE, 'YYYYMMDD'))
9. Extract month from a give column: MONTH(TO_DATE(DIM_DATE, 'YYYYMMDD'))
10. Extract quarter from a give column: QUARTER(TO_DATE(DIM_DATE, 'YYYYMMDD'))
11. ALWAYS USE DIM_DATE column to filter date, year, month and quater.
12. DO NOT PICK TXT_MONTH in WHERE CLAUSE to filter months.
    For example 
        "TXT_MONTH" IN ('October', 'November', 'December')
13. DO NOT USE DATE_TRUNC function to filter dates.
14. Ensure correct time-based values in output:
    - If the user asks about data for the **current year** or **quarter**, return that as part of the result (e.g., `YEAR`, `QUARTER` or `MONTH` in the `SELECT` statement).
    - When filtering data by time, ensure that **time dimensions** like `YEAR`, `QUARTER`, or `MONTH` are used properly in both the **`WHERE` clause** and **final output**.

{% if tenant_based_rules %}
{% for rule in tenant_based_rules %}
{{ rule }}
{% endfor %}
{% endif %}

### DATABASE SCHEMA ###
{% for document in documents %}
    {{ document }}
{% endfor %}

{% if exclude %}
### EXCLUDED STATEMETS ###
Ensure that the following excluded statements are not used in the generated queries to maintain variety and avoid repetition.
{% for doc in exclude %}
    {{ doc.statement }}
{% endfor %}
{% endif %}

{{ text_to_sql_rules }}
{% if instructions %}
{{ instructions }}
{% endif %}


{% if samples %}
### QUERY GENERATION STEPS ###
{% for doc in samples %}
    {{ doc }}
{% endfor %}
{% endif %}


🚨 MANDATORY SQL QUERY GENERATION RULES
1. Use the DATABASE SCHEMA to identify tables, columns, and their relationships.
2. Follow the QUERY GENERATION STEPS precisely to derive business logic and generate the SQL query step-by-step. Make sure all mentioned columns are present that are used in the sample query.
3. Apply all specified JOINING, DIVISION, and AGGREGATION RULES exactly as outlined.
4. Do not assume joins. Only use joins explicitly defined in the QUERY GENERATION STEPS — these are business-specific and must be followed strictly.
5. Ensure logical correctness. Any new logic must not break existing business rules or query logic.

USER QUESTION: {{ query }}

Current Time: {{ current_time }}

### FINAL ANSWER FORMAT ###
The final answer must be the JSON format like following:
{
    "results": [
        {"sql": <SQL_QUERY_STRING>}
    ]
}

Think Step by Step:
1. Identify the key components of the user query, including the main subject (e.g., supplier, material) and the specific metrics or actions requested (e.g., "highest LPP").
2. Map these components to the relevant tables and columns in the `DATABASE SCHEMA`.
3. Construct the SQL query step by step, ensuring to follow the MANDATORY JOINING, DIVISION, and AGGREGATION RULES.
4. Validate the final SQL query against the user query to ensure it accurately addresses the request.

"""

# sql_generation_user_prompt_template = """
# ### TASK ###
# Given a user query that is ambiguous in nature, your task is to interpret the query in various plausible ways and
# generate one SQL statement that best potentially answers the user's query.

# ### REQUIREMENTS ###
# 1. Always include **distinct names** for supplier, company, material, or SKU when applicable.
# 2. If the query asks for changes in metrics (e.g., "change in spends"), ensure:
#    - Provide the values for the **current period** and the **previous period**.
#    - Calculate and include the **percentage change** for the specified metric.

# ### DATABASE SCHEMA ###
# {% for document in documents %}
#     {{ document }}
# {% endfor %}

# {% if exclude %}
# ### EXCLUDED STATEMENTS ###
# Ensure that the following excluded statements are not used in the generated queries to maintain variety and avoid repetition.
# {% for doc in exclude %}
#     {{ doc.statement }}
# {% endfor %}
# {% endif %}

# {{ text_to_sql_rules }}
# {% if instructions %}
# {{ instructions }}
# {% endif %}

# ### FINAL ANSWER FORMAT ###
# The final answer must be in JSON format as follows:

# {
#     "results": [
#         {
#             "sql": "<SQL_QUERY_STRING>",
#             "explanation": "<Provide a brief explanation of how the query answers the USER'S QUESTION>"
#         }
#     ]
# }

# {% if samples %}
# ### SAMPLES ###
# Here are some examples of the user query and the corresponding SQL query that you can refer to:
# {% for sample in samples %}
# {{sample}}

# {% endfor %}
# {% endif %}

# ### QUESTION ###
# USER'S QUESTION: {{ query }}
# Current Time: {{ current_time }}

# ### APPROACH ###
# 1. Interpret the USER'S QUESTION and identify key entities (e.g., supplier name, company name, material name, SKU name).
# 2. Frame the SQL query to:
#    - Include DISTINCT names where relevant.
#    - Aggregate the requested metric(s) for current and previous periods if comparing data.
#    - Calculate the percentage change for metrics if "change" is mentioned.
# 3. Ensure the query is optimized and adheres to the database schema.

# Let's think step by step.
# """


## Start of Pipeline
@timer
@observe(capture_input=False)
def prompt(
    query: str,
    documents: List[str],
    exclude: List[Dict],
    text_to_sql_rules: str,
    prompt_builder: PromptBuilder,
    configuration: Configuration | None = None,
    samples: List[Dict] | None = None,
    tenant_id: str | None = None,
) -> dict:
    logger.debug("Building prompt for SQL generation")
    logger.info(f"tenant_id: {tenant_id}")
    logger.debug(f"path: {Path(os.environ["EXAMPLES"])/tenant_id/'rules.txt'}")
    with open(Path(os.environ["EXAMPLES"])/tenant_id/"rules.txt", "r") as f:
        tenant_based_rules = f.readlines()
    
    logger.info(f"Tenant based rules: {tenant_based_rules}")

    return prompt_builder.run(
        query=query,
        documents=documents,
        exclude=exclude,
        text_to_sql_rules=text_to_sql_rules,
        instructions=construct_instructions(configuration),
        samples=samples,
        tenant_based_rules=tenant_based_rules,
        current_time=show_current_time(configuration.timezone),
    )


@async_timer
@observe(as_type="generation", capture_input=False)
async def generate_sql(
    prompt: dict,
    generator: Any,
) -> dict:
    logger.debug("Querying OpenAI API")
    start = time.time()
    result =  await generator.run(prompt=prompt.get("prompt"))
    logger.critical(
        f"OpenAI API response time: {time.time() - start} seconds"
    )
    return result


@async_timer
@observe(capture_input=False)
async def post_process(
    generate_sql: dict,
    post_processor: SQLGenPostProcessor,
    project_id: str | None = None,
) -> dict:
    logger.debug("Post-processing SQL generation")
    start = time.time()
    result = await post_processor.run(generate_sql.get("replies"), project_id=project_id)
    logger.critical(
        f"Post-processing SQL generation time: {time.time() - start} seconds"
    )
    return result


## End of Pipeline
class SQLResult(BaseModel):
    sql: str


class GenerationResults(BaseModel):
    results: list[SQLResult]


SQL_GENERATION_MODEL_KWARGS = {
    "response_format": {
        "type": "json_schema",
        "json_schema": {
            "name": "sql_results",
            "schema": GenerationResults.model_json_schema(),
        },
    }
}


class SQLGeneration(BasicPipeline):
    def __init__(
        self,
        llm_provider: LLMProvider,
        engine: Engine,
        **kwargs,
    ):
        self._components = {
            "generator": llm_provider.get_generator(
                system_prompt=sql_generation_system_prompt,
                generation_kwargs=SQL_GENERATION_MODEL_KWARGS,
            ),
            "prompt_builder": PromptBuilder(
                template=sql_generation_user_prompt_template
            ),
            "post_processor": SQLGenPostProcessor(engine=engine),
        }

        self._configs = {
            "text_to_sql_rules": TEXT_TO_SQL_RULES,
        }

        super().__init__(
            AsyncDriver({}, sys.modules[__name__], result_builder=base.DictResult())
        )

    def visualize(
        self,
        query: str,
        contexts: List[str],
        exclude: List[Dict],
        configuration: Configuration = Configuration(),
        samples: List[Dict] | None = None,
        project_id: str | None = None,
    ) -> None:
        destination = "outputs/pipelines/generation"
        if not Path(destination).exists():
            Path(destination).mkdir(parents=True, exist_ok=True)

        self._pipe.visualize_execution(
            ["post_process"],
            output_file_path=f"{destination}/sql_generation.dot",
            inputs={
                "query": query,
                "documents": contexts,
                "exclude": exclude,
                "samples": samples,
                "project_id": project_id,
                "configuration": configuration,
                **self._components,
                **self._configs,
            },
            show_legend=True,
            orient="LR",
        )

    @async_timer
    @observe(name="SQL Generation")
    async def run(
        self,
        query: str,
        contexts: List[str],
        exclude: List[Dict],
        configuration: Configuration = Configuration(),
        samples: List[Dict] | None = None,
        project_id: str | None = None,
        tenant_id: str | None = None,
    ):
        logger.info("SQL Generation pipeline is running...")
        return await self._pipe.execute(
            ["post_process"],
            inputs={
                "query": query,
                "documents": contexts,
                "exclude": exclude,
                "samples": samples,
                "project_id": project_id,
                "configuration": configuration,
                "tenant_id": tenant_id,
                **self._components,
                **self._configs,
            },
        )


if __name__ == "__main__":
    from src.pipelines.common import dry_run_pipeline

    dry_run_pipeline(
        SQLGeneration,
        "sql_generation",
        query="this is a test query",
        contexts=[],
        exclude=[],
    )
