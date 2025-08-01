from loguru import logger
import asyncio
import snowflake.connector

class SnowflakeConnection:
    def __init__(self, conn_params):
        final_params = {
            "user": conn_params.get("user"),
            "password": conn_params.get("password"),
            "account": conn_params.get("account"),
            "database": conn_params.get("database"),
            "warehouse": conn_params.get("warehouse"),
            "role": conn_params.get("role"),
        }
        self.conn_params = final_params
        self.conn = snowflake.connector.connect(**final_params)
        self.cur = self.conn.cursor()

    async def execute_query(self, query):
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    async def execute_async_query(self, query, multi_tenant=True):
        if multi_tenant:
            set_database, query = query.split(";")
            self.cur.execute(set_database)
        self.cur.execute_async(query)
        query_id = self.cur.sfqid
        return query_id

    async def get_query_status(self, query_id):
        return self.conn.get_query_status(query_id)

    async def fetch_results(self, query_id):
        self.cur.get_results_from_sfqid(query_id)
        # * Fetch limited number of rows
        # * Need to check to check this bug
        # result = self.cur.fetchmany(self.conn_params.get("fetch_size", 500))
        result = self.cur.fetchmany(50)
        columns = [desc[0] for desc in self.cur.description]
        return {"columns": columns, "data": result}

    async def close(self):
        self.cur.close()
        self.conn.close()


class SnowflakeDatabaseFactory:
    def __init__(self, conn_params):
        self.sf = SnowflakeConnection(conn_params)
    
    async def query(self, query):
        query_id = await self.sf.execute_async_query(query)   
        logger.info(f"Query ID: {query_id}")     
        # Polling the query status
        check=True
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
            await asyncio.sleep(2)  # Poll every 2 seconds
        if failed:
            return None
        result_dict = await self.sf.fetch_results(query_id)
        return result_dict
