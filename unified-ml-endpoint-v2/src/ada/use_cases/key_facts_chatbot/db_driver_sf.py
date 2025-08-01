import asyncio

import snowflake.connector

from ada.utils.logs.logger import get_logger

logger = get_logger("db_driver_sf")


class SnowflakeConnection:
    def __init__(self, conn_params):
        self.conn_params = conn_params
        self.conn = snowflake.connector.connect(**conn_params)
        self.cur = self.conn.cursor()

    async def execute_query(self, query):
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    async def execute_async_query(self, query):
        self.cur.execute_async(query)
        query_id = self.cur.sfqid
        return query_id

    async def get_query_status(self, query_id):
        return self.conn.get_query_status(query_id)

    async def fetch_results(self, query_id):
        self.cur.get_results_from_sfqid(query_id)
        result = self.cur.fetchall()
        columns = [desc[0] for desc in self.cur.description]
        return {"columns": columns, "data": result}

    async def close(self):
        self.cur.close()
        self.conn.close()


class SnowflakeDatabaseFactory:
    def __init__(self, conn_params):
        self.sf = SnowflakeConnection(conn_params)
        logger.info("Snowflake Connection Established")

    async def query(self, query):
        query_id = await self.sf.execute_async_query(query)
        logger.info(f"Query ID: {query_id}")
        # Polling the query status
        check = True
        failed = False
        while check:
            query_status = await self.sf.get_query_status(query_id)
            logger.info(f"Query Status: {query_status}")
            if query_status.name == "SUCCESS":
                check = False
                break
            if query_status.name == "FAILED_WITH_ERROR":
                check = False
                failed = True
                break
            asyncio.sleep(2)  # Poll every 2 seconds
        if failed:
            return None
        result_dict = await self.sf.fetch_results(query_id)
        return result_dict
