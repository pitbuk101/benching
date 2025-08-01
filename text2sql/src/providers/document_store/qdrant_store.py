from src.env import QDRANT_HOST, QDRANT_PORT
from qdrant_client.qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range
from src.utils.logs import get_custom_logger

logger = get_custom_logger(__name__)

class QdrantStore:
    def __init__(self, host: str, port: int):
        self.client = QdrantClient(host=host, port=port)
        # Initialize Qdrant client here

    async def search_documents(self, collection: str, embedding: list, tenant_id: str, limit: int = 10):
        # Logic to search documents in Qdrant
        logger.debug(f"Searching in collection: {collection} with embedding: {len(embedding)} and limit: {limit}")
        return self.client.search(collection_name=collection, query_vector=embedding, limit=limit, 
            query_filter=Filter(must=[FieldCondition(key='tenant',match=MatchValue(value=tenant_id))]))

    async def get_all_documents(self, collection: str):
        # Logic to retrieve all documents from a collection in Qdrant
        # Fetch all points using scroll
        all_points = []
        scroll_offset = None
        while True:
            response =  self.client.scroll(
                collection_name=collection,
                scroll_filter=None,         # No filter: fetch all
                limit=100,                  # Batch size
                offset=scroll_offset,       # Offset from previous batch
                with_payload=True,          # Include payload
                with_vectors=False          # Exclude vectors
            )
            points, scroll_offset = response
            # logger.debug(f"Points fetched: {points}")
            logger.debug(f"Scroll offset: {scroll_offset}")
            all_points.extend(points)
            if not points or scroll_offset is None:
                break
        return all_points

    # def add_document(self, document: dict):
    #     # Logic to add a document to Qdrant
    #     pass
    # def delete_document(self, document_id: str):
    #     # Logic to delete a document from Qdrant
    #     pass

    # def update_document(self, document_id: str, updated_data: dict):
    #     # Logic to update a document in Qdrant
    #     pass

qdrant_document_store = QdrantStore(host=QDRANT_HOST, port=QDRANT_PORT)