import os
from pathlib import Path
from typing import List
import uuid
import aiohttp
import backoff
from langchain_openai.embeddings.base import OpenAIEmbeddings
from langchain.globals import set_llm_cache
from langchain_community.cache import RedisCache

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from tqdm import tqdm

from src.env import METADATA_LOCATION, LLM_OPENAI_API_KEY, OPENAI_BASE_URL, QDRANT_HOST, QDRANT_PORT
from src.utils.logs import get_custom_logger
from src.providers.cache_store.redis_cache import RedisCacheProvider
import redis

logger = get_custom_logger(__name__)

cache = RedisCacheProvider(REDIS_DB=0)
client = cache.get_client()
logger.debug(f"Client Type: {type(client)}")
logger.debug(f"Client URL: {cache.get_url()}")
set_llm_cache( RedisCache(redis_=redis.Redis.from_url(cache.get_url(mask_password=False))))
model = OpenAIEmbeddings(api_key=LLM_OPENAI_API_KEY, base_url=OPENAI_BASE_URL, model="text-embedding-3-large", dimensions=3072, show_progress_bar=True, )

logger.info(f"Qdrant Host: {QDRANT_HOST}")

async def embedding_model(query: list[str]):
    embeddings = await model.aembed_documents(query)
    return embeddings


def read_query_files(file_path: str) -> List[str]:
    logger.info(f"Reading files from {file_path}")
    data = []
    file_path = Path(file_path)
    # For each folder in the file path
    for folder in os.listdir(file_path):
        applicable = folder
        dir_path = file_path / folder
        logger.info(f"Reading folder: {dir_path}")
        for subfolder in os.listdir(dir_path):
            dir_path_temp = dir_path / subfolder
            logger.info(f"Reading subfolder: {dir_path_temp}")
            # For each subfolder in the folder
            # For each file in the folder
            if os.path.isdir(dir_path_temp):
                for file in os.listdir(dir_path_temp):
                    # logger.info(f"Reading file: {dir_path_temp/file}")
                    if file.endswith(".sql"):
                        logger.info(f"Reading file: {dir_path/file} for indexing")
                        with open(dir_path_temp / file, "r") as f:
                            file_data = f.read()
                            file = (
                                file
                                .split(".")[0]
                                .replace("_", " ")
                                .replace("'","")
                                .replace(",","")
                                .replace("bearings","[category]")
                                .replace("marketing svcs","[category]")
                                .replace("cibc","[category]")
                                .replace("valves","[category]")
                                )
                            data.append({"user_question": file, "solution_example": file_data, "question_type": subfolder, "tenant": applicable})
    return data

async def upload_sql_examples_qdrant():
    data = read_query_files(METADATA_LOCATION)
    logger.info(f"Number of queries: {len(data)}")
    client = AsyncQdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    result = await client.recreate_collection(
        collection_name="sql_examples",
        vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
    )
    BATCH_SIZE = 128
    batches = [data[i:i+BATCH_SIZE] for i in range(0, len(data), BATCH_SIZE)]

    all_points = []
    for batch in tqdm(batches):
        # Generate embeddings for the batch
        embeddings = await embedding_model([element["user_question"] for element in batch])
        logger.info(f"Embedding Created: {len(embeddings)}")
        for element, embedding in zip(batch, embeddings):
            all_points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "content": element["user_question"],
                        "solution_example": element["solution_example"],
                        "question_type": element["question_type"],
                        "tenant": element["tenant"]
                    }
                )
            )

    # Upload all points in one go (in batches if needed by Qdrant limits)
    # Qdrant recommends up to 1024 points per upsert, so chunk if needed
    MAX_QDRANT_BATCH = 256
    point_batches = [all_points[i:i+MAX_QDRANT_BATCH] for i in range(0, len(all_points), MAX_QDRANT_BATCH)]
    for pbatch in point_batches:
        result = await client.upsert(
            collection_name="sql_examples",
            points=pbatch,
        )
        logger.info(f"Upserted batch of {len(pbatch)} points. Result: {result}")


@backoff.on_exception(backoff.expo, aiohttp.ClientError, max_time=60, max_tries=3)
async def force_deploy_semantics():
    async with aiohttp.ClientSession() as session:
        qdrant_host = os.getenv("QDRANT_HOST", "qdrant")
        print(f"Qdrant host: {qdrant_host}")
        for collection in ["sql_examples"]:
            url = f"http://{qdrant_host}:6333/collections/{collection}/points/delete"
            payload = {
                "filter": {
                    "must": []  # Matches all points
                }
            }
            async with session.post(url, json=payload) as response:
                result = await response.json()
                if response.status == 200:
                    print(f"✅ Successfully deleted all points in '{collection}' collection.")
                else:
                    print(f"❌ Error: {result}")
            await upload_sql_examples_qdrant()
            logger.info("Query Upload is Done.")
        async with session.post(
            f"{os.getenv("WREN_UI_ENDPOINT", "http://wren-ui:3000")}/api/graphql",
            json={
                "query": "mutation Deploy($force: Boolean) { deploy(force: $force) }",
                "variables": {"force": True},
            },
            timeout=aiohttp.ClientTimeout(total=120),  # 60 seconds
        ) as response:
            res = await response.json()

