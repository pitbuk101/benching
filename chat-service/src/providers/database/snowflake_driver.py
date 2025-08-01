import time
from src.utils.logs import get_custom_logger
import snowflake.connector
logger = get_custom_logger(__name__)

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

    def execute_query(self, query):
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def execute_async_query(self, query, multi_tenant=True):
        if multi_tenant:
            set_database, query = query.split(";")
            self.cur.execute(set_database)
        self.cur.execute_async(query)
        query_id = self.cur.sfqid
        return query_id

    def get_query_status(self, query_id):
        return self.conn.get_query_status(query_id)

    def fetch_results(self, query_id):
        self.cur.get_results_from_sfqid(query_id)
        # * Fetch limited number of rows
        # * Need to check to check this bug
        # result = self.cur.fetchmany(self.conn_params.get("fetch_size", 500))
        result = self.cur.fetchmany(50)
        columns = [desc[0] for desc in self.cur.description]
        return {"columns": columns, "data": result}

    def close(self):
        self.cur.close()
        self.conn.close()


class SnowflakeDatabaseFactory:
    def __init__(self, conn_params):
        self.sf = SnowflakeConnection(conn_params)
    
    def query(self, query):
        try:
            query_id = self.sf.execute_async_query(query)   
            logger.info(f"Query ID: {query_id}")     
            # Polling the query status
            check=True
            failed = False
            error_message = None
            while check:
                query_status = self.sf.get_query_status(query_id)
                logger.info(f"Query Status: {query_status}")
                if query_status.name == "SUCCESS":
                    check = False
                    break
                if query_status.name == "FAILED_WITH_ERROR":
                    check = False
                    failed = True
                    # Try to fetch error details if available
                    try:
                        error_message = getattr(query_status, 'error_message', None)
                    except Exception as e:
                        error_message = str(e)
                    break
                # await asyncio.sleep(2)  # Poll every 2 seconds
                time.sleep(2)
            if failed:
                logger.error(f"Query failed. Error: {error_message}")
                print(f"Query failed. Error: {error_message}")
                return None
            result_dict = self.sf.fetch_results(query_id)
            return result_dict
        except Exception as e:
            logger.error(f"Exception during query execution: {e}")
            print(f"Exception during query execution: {e}")
            return None