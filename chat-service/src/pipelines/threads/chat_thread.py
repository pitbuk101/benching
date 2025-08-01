import json
from src.providers.database.postgres_driver_v2 import postgres_client
from src.utils.logs import get_custom_logger

logger = get_custom_logger(__name__)

class Thread:
    def __init__(self, tenant_id: str, category: str, thread_id: list[str]) -> None:
        self.tenant_id = tenant_id
        self.category = category
        self.thread_id = thread_id
        self.client = postgres_client
    
    def save_thread(self, chat):
        thread_id = self.thread_id[0]
        chat = chat.replace('\\', '\\\\').replace("'", "''")
        query = f"""
        INSERT INTO "{self.tenant_id}"."threads" (
            thread_id, 
            category, 
            chat
        )
        VALUES (
            '{thread_id}',
            '{self.category}',
            '{chat}'
            )
        ON CONFLICT (thread_id) DO UPDATE
        SET chat = EXCLUDED.chat, updated_at = now()
        """
        logger.debug(f"Query to be executed: {query}")
        status = self.client.execute(query)
        logger.debug(f"Status of Query: {status}")

    def list_thread(self):
        query = f"""
        SELECT DISTINCT thread_id from "{self.tenant_id}"."threads"
        """
        logger.debug(f"Query to be executed: {query}")
        status = self.client.execute(query)
        logger.debug(f"Status of Query: {status}")
        final_output = []
        for data in status["data"]:
            temp = {}
            for column, element in zip(status["columns"], data):
                temp[column] = element
            final_output.append(temp)
        return final_output
    
    def get_thread(self):
        thread_id = "','".join(self.thread_id)
        query = f"""
        SELECT * 
        FROM  "{self.tenant_id}"."threads"
        WHERE thread_id in ('{thread_id}')
        ORDER BY updated_at DESC, created_at DESC
        """
        logger.debug(f"Query to be executed: {query}")
        status = self.client.execute(query)
        logger.debug(f"Status of Query: {status}")
        final_output = []
        for data in status["data"]:
            temp = {}
            for column, element in zip(status["columns"], data):
                temp[column] = element
            final_output.append(temp)
        return final_output
    
    def update_thread(self, chat):
        thread_id = self.thread_id[0]
        chat = chat.replace('\\', '\\\\').replace("'", "''")
        query = f"""
        UPDATE "{self.tenant_id}"."threads"
        SET chat='{chat}',
            updated_at = now()
        WHERE thread_id='{thread_id}'
        """
        logger.debug(f"Query to be executed: {query}")
        status = self.client.execute(query)
        logger.debug(f"Status of Query: {status}")
    
    def delete_thread(self):
        thread_id = self.thread_id[0]
        query = f"""
        DELETE FROM "{self.tenant_id}"."threads"
        WHERE thread_id='{thread_id}'
        """
        logger.debug(f"Query to be executed: {query}")
        status = self.client.execute(query)
        logger.debug(f"Status of Query: {status}")