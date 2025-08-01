import asyncio
import os
from pathlib import Path

import aiohttp
import backoff
from dotenv import load_dotenv

if Path(".env.dev").exists():
    load_dotenv(".env.dev", override=True)


@backoff.on_exception(backoff.expo, aiohttp.ClientError, max_time=60, max_tries=3)
async def force_deploy():
    async with aiohttp.ClientSession() as session:
        qdrant_host = os.getenv("QDRANT_HOST", "qdrant")
        print(f"Qdrant host: {qdrant_host}")
        for collection in ["sql_examples"]:
            # async with session.delete(url=f"http://{qdrant_host}:6333/collections/{collection}") as response:
            #     if response.status == 200:
            #         print(f"✅ Deleted: {collection}")
            #     else:
            #         text = await response.text()
            #         print(f"❌ Failed to delete {collection}: {text} response code: {response.status}")
            # 
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

        async with session.post(
            f"{os.getenv("WREN_UI_ENDPOINT", "http://wren-ui:3000")}/api/graphql",
            json={
                "query": "mutation Deploy($force: Boolean) { deploy(force: $force) }",
                "variables": {"force": True},
            },
            timeout=aiohttp.ClientTimeout(total=120),  # 60 seconds
        ) as response:
            res = await response.json()
            # print(f"Forcing deployment: {res}")


# if os.getenv("ENGINE", "wren_ui") == "wren_ui":
asyncio.run(force_deploy())
