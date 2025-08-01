from src.env import (
    PGUSER,
    PGPASSWORD,
    PGHOST,
    PGPORT,
    PGDATABASE
)
from src.utils.logs import get_custom_logger
import asyncio
import asyncpg

logger = get_custom_logger(__name__)

class PostgresConnection:
    def __init__(self, conn_params):
        self.pool = None

    async def connect(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(**self.conn_params, min_size=1, max_size=10)

    async def execute(self, query, *args):
        """
        Execute a query (SELECT/INSERT/UPDATE/DELETE) with optional parameters.
        Returns the result for SELECT, or status for others.
        """
        await self.connect()
        async with self.pool.acquire() as conn:
            if query.strip().lower().startswith("select"):
                return await conn.fetch(query, *args)
            else:
                return await conn.execute(query, *args)

    async def execute_async(self, query, *args):
        """
        Execute a query asynchronously. Returns an asyncio.Task.
        """
        await self.connect()
        async def fetch_task():
            async with self.pool.acquire() as conn:
                return await conn.fetch(query, *args)
        task = asyncio.create_task(fetch_task())
        return task

    async def get_query_status(self, task):
        if task.done():
            return "SUCCESS" if not task.exception() else "FAILED_WITH_ERROR"
        return "RUNNING"

    async def fetch_results(self, task):
        result = await task
        columns = result[0].keys() if result else []
        data = [tuple(row.values()) for row in result]
        return {"columns": columns, "data": data}

    async def close(self):
        if self.pool:
            await self.pool.close()
            self.pool = None


class PostgresDatabaseFactory:
    def __init__(self, conn_params):
        self.pg = PostgresConnection(conn_params)

    async def query(self, query, *args):
        """
        Run a query and return results as a dict (columns, data).
        """
        task = await self.pg.execute_async(query, *args)
        logger.info(f"Query Task: {task}")
        check = True
        failed = False
        while check:
            status = await self.pg.get_query_status(task)
            logger.info(f"Query Status: {status}")
            if status == "SUCCESS":
                check = False
                break
            if status == "FAILED_WITH_ERROR":
                check = False
                failed = True
                break
            await asyncio.sleep(2)
        if failed:
            return None
        result_dict = await self.pg.fetch_results(task)
        return result_dict

    async def insert(self, table_name, columns, values, schema=None):
        """
        Insert multiple rows into a table. Generic for any table/schema.
        """
        if not columns or not values:
            logger.error("Columns and values must be provided for insert.")
            return None
        cols = ', '.join(columns)
        placeholders = ', '.join([f"${i+1}" for i in range(len(columns))])
        qualified_table = f"{schema}.{table_name}" if schema else table_name
        query = f"INSERT INTO {qualified_table} ({cols}) VALUES ({placeholders})"
        try:
            await self.pg.connect()
            async with self.pg.pool.acquire() as conn:
                await conn.executemany(query, values)
            logger.info(f"Inserted {len(values)} rows into {qualified_table}.")
            return { "status": "success", "rows_inserted": len(values) }
        except Exception as e:
            logger.exception(f"Insert failed: {e}")
            return { "status": "error", "message": str(e) }

    async def create_schema(self, schema_name):
        """
        Create a schema if it does not exist.
        Args:
            schema_name (str): Name of the schema to create.
        Returns:
            dict: Status and message.
        """
        if not schema_name:
            logger.error("Schema name must be provided.")
            return {"status": "error", "message": "Schema name is required."}
        query = f"CREATE SCHEMA IF NOT EXISTS {schema_name}"
        try:
            await self.pg.connect()
            async with self.pg.pool.acquire() as conn:
                await conn.execute(query)
            logger.info(f"Schema '{schema_name}' created or already exists.")
            return {"status": "success", "message": f"Schema '{schema_name}' created or already exists."}
        except Exception as e:
            logger.exception(f"Failed to create schema: {e}")
            return {"status": "error", "message": str(e)}

    async def table_exists(self, table_name, schema=None):
        """
        Check if a table exists in the database (optionally in a schema).
        """
        if not table_name:
            logger.error("Table name must be provided.")
            return False
        schema = schema or 'public'
        query = (
            "SELECT EXISTS ("
            "  SELECT 1 FROM information_schema.tables "
            "  WHERE table_schema = $1 AND table_name = $2"
            ") AS exists;"
        )
        try:
            await self.pg.connect()
            async with self.pg.pool.acquire() as conn:
                result = await conn.fetchrow(query, schema, table_name)
            exists = result['exists'] if result else False
            logger.info(f"Table '{schema}.{table_name}' exists: {exists}")
            return exists
        except Exception as e:
            logger.exception(f"Failed to check if table exists: {e}")
            return False

    async def execute_in_schema(self, query, schema=None, *args):
        """
        Execute a query in the specified schema (optionally set search_path).
        """
        try:
            await self.pg.connect()
            async with self.pg.pool.acquire() as conn:
                if schema:
                    await conn.execute(f'SET search_path TO {schema}')
                result = await conn.fetch(query, *args)
            logger.info(f"Executed query in schema '{schema or 'public'}'.")
            return result
        except Exception as e:
            logger.exception(f"Failed to execute query in schema: {e}")
            return {"status": "error", "message": str(e)}

    async def schema_exists(self, schema_name):
        """
        Check if a schema exists in the database.
        Args:
            schema_name (str): Name of the schema to check.
        Returns:
            bool: True if schema exists, False otherwise.
        """
        if not schema_name:
            logger.error("Schema name must be provided.")
            return False
        query = (
            "SELECT EXISTS ("
            "  SELECT 1 FROM information_schema.schemata "
            "  WHERE schema_name = $1"
            ") AS exists;"
        )
        try:
            await self.pg.connect()
            async with self.pg.pool.acquire() as conn:
                result = await conn.fetchrow(query, schema_name)
            exists = result['exists'] if result else False
            logger.info(f"Schema '{schema_name}' exists: {exists}")
            return exists
        except Exception as e:
            logger.exception(f"Failed to check if schema exists: {e}")
            return False

    async def get_table_results(self, table_name, schema=None):
        """
        Get all rows from a table.
        """
        if not table_name:
            logger.error("Table name must be provided.")
            return None
        schema = schema or 'public'
        query = f"SELECT * FROM {schema}.{table_name} ORDER BY batch_date desc limit 50"
        try:
            await self.pg.connect()
            async with self.pg.pool.acquire() as conn:
                result = await conn.fetch(query)
            logger.info(f"Fetched results from '{schema}.{table_name}'.")
            return result
        except Exception as e:
            logger.exception(f"Failed to fetch results from table: {e}")
            return None
        
