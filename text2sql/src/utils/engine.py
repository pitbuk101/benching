import asyncio
import re
from abc import ABCMeta, abstractmethod
import time
from typing import Any, Dict, List, Optional, Tuple
import aiohttp
import orjson
import sqlglot
from pydantic import BaseModel
from src.utils.logs import get_custom_logger

logger = get_custom_logger(__name__)


class EngineConfig(BaseModel):
    provider: str = "wren_ui"
    config: dict = {}


class Engine(metaclass=ABCMeta):
    @abstractmethod
    async def execute_sql(
        self,
        sql: str,
        session: aiohttp.ClientSession,
        dry_run: bool = True,
        **kwargs,
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        ...


def clean_generation_result(result: str) -> str:
    def _normalize_whitespace(s: str) -> str:
        return re.sub(r"\s+", " ", s).strip()

    return (
        _normalize_whitespace(result)
        .replace("\\n", " ")
        .replace("```sql", "")
        .replace("```json", "")
        .replace('"""', "")
        .replace("'''", "")
        .replace("```", "")
        .replace(";", "")
    )


def remove_limit_statement(sql: str) -> str:
    pattern = r"\s*LIMIT\s+\d+(\s*;?\s*--.*|\s*;?\s*)$"
    modified_sql = re.sub(pattern, "", sql, flags=re.IGNORECASE)
    return modified_sql

def add_quotes(sql: str) -> Tuple[str, bool]:
    try:
        logger.debug(f"Original SQL: {sql}")
        quoted_sql = sqlglot.transpile(sql, read="trino", identify=True)[0]
        logger.debug(f"Quoted SQL: {quoted_sql}")
    except Exception as e:
        logger.exception(f"Error in sqlglot.transpile to {sql}: {e}")
        return "", False
    return quoted_sql, True


class SQLGenPostProcessorV2:
    def __init__(self, engine: Engine):
        self._engine = engine
    
    async def run(self, sql: str, project_id: str | None = None):
        valid_generation_results = []
        invalid_generation_results = []

        async def _task(sql, session):
            
            quoted_sql, no_error = add_quotes(sql)

            if no_error:
                start = time.time()
                status, _, addition = await self._engine.execute_sql(
                    quoted_sql, session, project_id=project_id
                )
                logger.critical(f"SQLGenPostProcessor _task took {time.time() - start} seconds")

                if status:
                    valid_generation_results.append(
                        {
                            "sql": quoted_sql,
                            "correlation_id": addition.get("correlation_id", ""),
                        }
                    )
                else:
                    invalid_generation_results.append(
                        {
                            "sql": quoted_sql,
                            "type": "DRY_RUN",
                            "error": addition.get("error_message", ""),
                            "correlation_id": addition.get("correlation_id", ""),
                        }
                    )
            else:
                invalid_generation_results.append(
                    {
                        "sql": sql,
                        "type": "ADD_QUOTES",
                        "error": "add_quotes failed",
                    }
                )

        async with aiohttp.ClientSession() as session:
            tasks = [_task(sql, session)]
            await asyncio.gather(*tasks)

        return valid_generation_results, invalid_generation_results



class SQLGenPostProcessor:
    def __init__(self, engine: Engine):
        self._engine = engine

    # @component.output_types(
    #     valid_generation_results=List[Optional[Dict[str, Any]]],
    #     invalid_generation_results=List[Optional[Dict[str, Any]]],
    # )
    async def run(
        self,
        replies: List[str] | List[List[str]],
        project_id: str | None = None,
    ) -> dict:
        logger.debug("SQLGenPostProcessor started")
        try:
            # if isinstance(replies[0], dict):
            #     cleaned_generation_result = []
            #     for reply in replies:
            #         try:
            #             cleaned_generation_result.append(
            #                 orjson.loads(clean_generation_result(reply["replies"][0]))[
            #                     "results"
            #                 ][0]
            #             )
            #         except Exception as e:
            #             logger.exception(f"Error in SQLGenPostProcessor: {e}")
            # else:
            #     cleaned_generation_result = orjson.loads(
            #         clean_generation_result(replies[0])
            #     )["results"]

            if isinstance(cleaned_generation_result, dict):
                cleaned_generation_result = [cleaned_generation_result]
            start = time.time()
            (
                valid_generation_results,
                invalid_generation_results,
            ) = await self._classify_invalid_generation_results(
                cleaned_generation_result, project_id=project_id
            )
            logger.critical(f"SQLGenPostProcessor inside process took {time.time() - start} seconds")
            return {
                "valid_generation_results": valid_generation_results,
                "invalid_generation_results": invalid_generation_results,
            }
        except Exception as e:
            logger.exception(f"Error in SQLGenPostProcessor: {e}")

            return {
                "valid_generation_results": [],
                "invalid_generation_results": [],
            }

    async def _classify_invalid_generation_results(
        self, generation_results: List[Dict[str, str]], project_id: str | None = None
    ) -> List[Optional[Dict[str, str]]]:
        valid_generation_results = []
        invalid_generation_results = []

        async def _task(result: Dict[str, str]):
            
            quoted_sql, no_error = add_quotes(result["sql"])

            if no_error:
                start = time.time()
                status, _, addition = await self._engine.execute_sql(
                    quoted_sql, session, project_id=project_id
                )
                logger.critical(f"SQLGenPostProcessor _task took {time.time() - start} seconds")

                if status:
                    valid_generation_results.append(
                        {
                            "sql": quoted_sql,
                            "correlation_id": addition.get("correlation_id", ""),
                        }
                    )
                else:
                    invalid_generation_results.append(
                        {
                            "sql": quoted_sql,
                            "type": "DRY_RUN",
                            "error": addition.get("error_message", ""),
                            "correlation_id": addition.get("correlation_id", ""),
                        }
                    )
            else:
                invalid_generation_results.append(
                    {
                        "sql": result["sql"],
                        "type": "ADD_QUOTES",
                        "error": "add_quotes failed",
                    }
                )

        async with aiohttp.ClientSession() as session:
            tasks = [
                _task(generation_result) for generation_result in generation_results
            ]
            await asyncio.gather(*tasks)

        return valid_generation_results, invalid_generation_results


# sql_gen_post_processor = SQLGenPostProcessor(engine=)  # Engine should be set later