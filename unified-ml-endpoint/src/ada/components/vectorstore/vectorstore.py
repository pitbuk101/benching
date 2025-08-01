"""Class to create vectorstores and do similarity search
on different use cases related to Tech CME."""

from typing import List, Union

import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStore
from langchain_openai import AzureOpenAIEmbeddings

from ada.components.db.pg_connector import PGConnector
from ada.components.db.pg_operations import get_content_for_doc_list_from_db
from ada.components.llm_models.generic_calls import generate_embeddings_from_string
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time
from ada.utils.metrics.context_manager import get_ai_cost_tags

log = get_logger("vectorstore")
conf = read_config("models.yml")


class VectorStoreFactory:
    """
    A class for creating and managing vector stores for document embeddings.

    """

    def __init__(self):
        """Create vectorstore object"""

        self.embedding_func = AzureOpenAIEmbeddings(
            model=conf["embedding_engine"],
            headers={"X-Aigateway-User-Defined-Tag": f"{get_ai_cost_tags()}"},
        )

    def faiss_from_embeddings(
        self,
        doc_chunk: pd.DataFrame,
    ) -> VectorStore:
        """
        Create a vector store based on the specified method.

        Args:
            doc_chunk (str): The chunks of the document to create embeddings from.

        Returns:
            VectorStore: The created vector store.

        """
        documents = doc_chunk["chunk_content"].tolist()
        embeddings = doc_chunk["embedding"].tolist()
        metadatas = doc_chunk["page"].tolist()
        metadatas = [{"source": i} for i in metadatas]

        inputs = list(tuple(zip(documents, embeddings)))
        vectorstore = FAISS.from_embeddings(inputs, self.embedding_func, metadatas=metadatas)
        return vectorstore

    def faiss_from_news_embeddings(
        self,
        news_chunk: pd.DataFrame,
    ) -> VectorStore:
        """
        Create a vector store based on the specified method.

        Args:
            news_chunk (str): The chunks of the document to create embeddings from.

        Returns:
            VectorStore: The created vector store.

        """
        news_content = news_chunk["chunk_content"].tolist()
        embeddings = news_chunk["embeddings"].tolist()
        metadatas = []
        for title, link, news_id in zip(
            news_chunk["title"],
            news_chunk["link"],
            news_chunk["news_id"],
        ):
            metadata = {
                "title": title,
                "link": link,
                "source": news_id,  # Assuming 'news_id' corresponds to the source
            }
            metadatas.append(metadata)
        inputs = list(tuple(zip(news_content, embeddings)))
        vectorstore = FAISS.from_embeddings(inputs, self.embedding_func, metadatas=metadatas)
        return vectorstore

    @log_time
    # TODO: Remove the function once faiss_from_embeddings is updated to accept doc_id list
    def faiss_from_embeddings_from_doc_list(
        self,
        tenant_id: str,
        doc_ids: List[int],
    ) -> VectorStore:
        """
        Create a vector store based on the specified method.

        Args:
            doc_ids (List): List of document ids

        Returns:
            VectorStore: The created vector store.

        """
        doc_chunk = get_content_for_doc_list_from_db(
            tenant_id=tenant_id,
            doc_ids=doc_ids,
            columns=["chunk_content", "page", "embedding"],
        )
        documents = doc_chunk["chunk_content"].tolist()
        embeddings = doc_chunk["embedding"].tolist()
        metadatas = doc_chunk["page"].tolist()
        metadatas = [{"source": i} for i in metadatas]

        inputs = list(tuple(zip(documents, embeddings)))
        vectorstore = FAISS.from_embeddings(inputs, self.embedding_func, metadatas=metadatas)
        return vectorstore

    def batch_faiss_from_document(
        self,
        chunks: Union[List[str], List[Document]],
        max_request_size=16,
        **kwargs,
    ) -> VectorStore:
        """
        Create a VectorStore from a list of chunks by batching the requests.
        This is to avoid getting timed out due to request size (rate limiting)
        Args:
            chunks (Union[List[str], List[Document]): A list of chunks or Document objects.
            embedding_module (Embeddings): The embedding function to convert data to vectors.
            max_request_size (int, optional): The maximum batch size for processing chunks.
            **kwargs: Additional arguments to pass to the faiss_method.
        Returns:
            VectorStore: A VectorStore instance containing the embeddings of the chunks.

        """
        # faiss method in this case can be either FAISS.from_documents or FAISS.from_embeddings
        # you can pass any arguments needed for these methods via kwargs.
        base_vectorstore = FAISS.from_documents(
            chunks[:max_request_size],
            self.embedding_func,
            **kwargs,
        )
        if len(chunks) > max_request_size:
            for chunk_index in range(max_request_size, len(chunks), max_request_size):
                vectorstore = FAISS.from_documents(
                    chunks[chunk_index : chunk_index + max_request_size],  # noqa: E203
                    self.embedding_func,
                    **kwargs,
                )
                base_vectorstore.merge_from(vectorstore)
        return base_vectorstore

    @log_time
    def faiss_from_pandas_df(self, data: pd.DataFrame, columns: list) -> VectorStore:
        """
        Create a vector store from a dataframe with required columns.

        Args:
            data (pandas.DataFrame): Input pandas dataframe
            columns (list): list of columns that need to be considered for creating vectorstore

        Returns:
            VectorStore: The created vector store.

        """
        df_filtered = data[columns]
        inputs = list(df_filtered.itertuples(index=False, name=None))
        vectorstore = FAISS.from_embeddings(inputs, self.embedding_func)
        return vectorstore


class PGRetriever(BaseRetriever):
    """
    A class for retrieving documents from a PostgreSQL database based on the query.
    pg_db_conn: PGConnector: The PostgreSQL connector object.
    k: int: The number of documents to retrieve.
    table_name: str: The name of the table to search for documents.
    embeddings_model: str: The name of the embeddings model to use.
    conditions: dict | None: The conditions to filter the documents.

    """

    pg_db_conn: PGConnector
    k: int
    table_name: str
    embeddings_model: str
    conditions: dict | str | None = None
    embeddings_column_name: str = "embedding"
    column_names: list[str] | None = None

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun,
    ) -> list[Document]:
        documents = self.pg_db_conn.search_by_vector_similarity(
            table_name=self.table_name,
            query_emb=generate_embeddings_from_string(
                query,
                embeddings_model=self.embeddings_model,
            ),
            emb_column_name=self.embeddings_column_name,
            num_records=self.k,
            search_type="cosine_distance",
            conditions=self.conditions,
            columns=self.column_names,
        )
        documents = [
            Document(
                page_content=dict(document).get("chunk_content", ""),
                metadata={"source": index},
            )
            for index, document in enumerate(documents)
        ]
        return documents
