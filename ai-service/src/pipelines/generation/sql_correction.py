import asyncio
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

from hamilton import base
from hamilton.async_driver import AsyncDriver
from haystack import Document
from haystack.components.builders.prompt_builder import PromptBuilder
from langfuse.decorators import observe
from pydantic import BaseModel

from src.core.engine import Engine
from src.core.pipeline import BasicPipeline
from src.core.provider import LLMProvider
from src.pipelines.common import (
    TEXT_TO_SQL_RULES,
    SQLGenPostProcessor,
    sql_generation_system_prompt,
)
from src.utils import async_timer, timer

logger = logging.getLogger("wren-ai-service")


sql_correction_user_prompt_template = """
You are an ANSI SQL SERVER expert with exceptional logical thinking skills and debugging skills.

### MANDATORY TIME HANDLING RULES ### 
1. To extract year from timestamp: YEAR(CURRENT_TIMESTAMP)
2. Extract current year:  YEAR(CURRENT_DATE)
3. Extract previous quarter:  QUARTER(DATEADD(MONTH, -3, CURRENT_DATE))
4. Extract current date and time: CURRENT_TIMESTAMP
5. Extract current date: CURRENT_DATE
6. Convert a given date column to date format: TO_DATE(DIM_DATE, 'YYYYMMDD')
7. Extract year from a give column: YEAR(TO_DATE(DIM_DATE, 'YYYYMMDD'))
8. Extract month from a give column: MONTH(TO_DATE(DIM_DATE, 'YYYYMMDD'))
9. Extract quarter from a give column: QUARTER(TO_DATE(DIM_DATE, 'YYYYMMDD'))
10. ALWAYS USE DIM_DATE column to filter date, year, month and quater.
11. DO NOT PICK TXT_MONTH in WHERE CLAUSE to filter months.
    For example 
        "TXT_MONTH" IN ('October', 'November', 'December')

### DIM_DATE SAMPLE ###
Given below is a sample of DIM_DATE table and values lying inside the table.
DIM_DATE,TXT_DATE,DIM_MONTH,TXT_MONTH,DIM_QUARTER,TXT_QUARTER,DIM_YEAR,TXT_YEAR,DIM_DAY_OF_WEEK,TXT_DAY_OF_WEEK,TXT_CALENDAR_WEEK,TXT_CALENDAR_YEAR,MONTH_NUMBER,MONTH_NAME,MONTH_NAME_ABB,QUARTER_PAD,QUARTER_NUMBER,DATE_DATE,TXT_WEEK_NUMBER,TXT_DAY_NUMBER,MONTH_OFFSET,YEAR_OFFSET,QUARTER_OFFSET,FLG_TIME_INTELLIGENCE
20210313,2021-03-13,202103,2021/03,20211,2021 Q1,2021,2021,6,Saturday,2021/010,2021,3,March,Mar,Q01,1.00000,2021-03-13,10,13,null,null,null,0
20210427,2021-04-27,202104,2021/04,20212,2021 Q2,2021,2021,2,Tuesday,2021/017,2021,4,April,Apr,Q02,2.00000,2021-04-27,17,27,null,null,null,0
20210621,2021-06-21,202106,2021/06,20212,2021 Q2,2021,2021,1,Monday,2021/025,2021,6,June,Jun,Q02,2.00000,2021-06-21,25,21,null,null,null,0
20210102,2021-01-02,202101,2021/01,20211,2021 Q1,2021,2021,6,Saturday,2020/053,2020,1,January,Jan,Q01,1.00000,2021-01-02,53,2,null,null,null,0
20210428,2021-04-28,202104,2021/04,20212,2021 Q2,2021,2021,3,Wednesday,2021/017,2021,4,April,Apr,Q02,2.00000,2021-04-28,17,28,null,null,null,0 

### MANDATORY DIVISION RULES ###
1. When dividing any two columns in sql, ALWAYS put the denominator greater than 0 in where clause to avoid division by zero error.

### TASK ###
Now you are given syntactically incorrect ANSI SQL query and related error message.
With given database schema, please think step by step to correct the wrong ANSI SQL query.

### DATABASE SCHEMA ###
{% for document in documents %}
    {{ document }}
{% endfor %}

### FINAL ANSWER FORMAT ###
The final answer must be a list of corrected SQL quries in JSON format:

{
    "results": [
        {"sql": <CORRECTED_SQL_QUERY_STRING>},
    ]
}

{{ alert }}

### QUESTION ###
SQL: {{ invalid_generation_result.sql }}
Error Message: {{ invalid_generation_result.error }}

Let's think step by step.
"""


## Start of Pipeline
@timer
@observe(capture_input=False)
def prompts(
    documents: List[Document],
    invalid_generation_results: List[Dict],
    alert: str,
    prompt_builder: PromptBuilder,
) -> list[dict]:
    return [
        prompt_builder.run(
            documents=documents,
            invalid_generation_result=invalid_generation_result,
            alert=alert,
        )
        for invalid_generation_result in invalid_generation_results
    ]


@async_timer
@observe(as_type="generation", capture_input=False)
async def generate_sql_corrections(prompts: list[dict], generator: Any) -> list[dict]:
    tasks = []
    for prompt in prompts:
        task = asyncio.ensure_future(generator.run(prompt=prompt.get("prompt")))
        tasks.append(task)

    return await asyncio.gather(*tasks)


@async_timer
@observe(capture_input=False)
async def post_process(
    generate_sql_corrections: list[dict],
    post_processor: SQLGenPostProcessor,
    project_id: str | None = None,
) -> list[dict]:
    return await post_processor.run(generate_sql_corrections, project_id=project_id)


## End of Pipeline


class CorrectedSQLResult(BaseModel):
    sql: str


class CorrectedResults(BaseModel):
    results: list[CorrectedSQLResult]


SQL_CORRECTION_MODEL_KWARGS = {
    "response_format": {
        "type": "json_schema",
        "json_schema": {
            "name": "corrected_sql",
            "schema": CorrectedResults.model_json_schema(),
        },
    }
}


class SQLCorrection(BasicPipeline):
    def __init__(
        self,
        llm_provider: LLMProvider,
        engine: Engine,
        **kwargs,
    ):
        self._components = {
            "generator": llm_provider.get_generator(
                system_prompt=sql_generation_system_prompt,
                generation_kwargs=SQL_CORRECTION_MODEL_KWARGS,
            ),
            "prompt_builder": PromptBuilder(
                template=sql_correction_user_prompt_template
            ),
            "post_processor": SQLGenPostProcessor(engine=engine),
        }

        self._configs = {
            "alert": TEXT_TO_SQL_RULES,
        }

        super().__init__(
            AsyncDriver({}, sys.modules[__name__], result_builder=base.DictResult())
        )

    def visualize(
        self,
        contexts: List[Document],
        invalid_generation_results: List[Dict[str, str]],
        project_id: str | None = None,
    ) -> None:
        destination = "outputs/pipelines/generation"
        if not Path(destination).exists():
            Path(destination).mkdir(parents=True, exist_ok=True)

        self._pipe.visualize_execution(
            ["post_process"],
            output_file_path=f"{destination}/sql_correction.dot",
            inputs={
                "invalid_generation_results": invalid_generation_results,
                "documents": contexts,
                "project_id": project_id,
                **self._components,
                **self._configs,
            },
            show_legend=True,
            orient="LR",
        )

    @async_timer
    @observe(name="SQL Correction")
    async def run(
        self,
        contexts: List[Document],
        invalid_generation_results: List[Dict[str, str]],
        project_id: str | None = None,
    ):
        logger.info("SQLCorrection pipeline is running...")
        return await self._pipe.execute(
            ["post_process"],
            inputs={
                "invalid_generation_results": invalid_generation_results,
                "documents": contexts,
                "project_id": project_id,
                **self._components,
                **self._configs,
            },
        )


if __name__ == "__main__":
    from src.pipelines.common import dry_run_pipeline

    dry_run_pipeline(
        SQLCorrection,
        "sql_correction",
        invalid_generation_results=[],
        contexts=[],
    )
