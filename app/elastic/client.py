# import os
# import asyncio
# # from dotenv import load_dotenv
# # load_dotenv()
# import httpx
# ELASTIC_URL = os.getenv("ELASTIC_URL", "http://localhost:9200")
# ELASTIC_INDEX = os.getenv("ELASTIC_INDEX", "mongo-alerts")
# # print(ELASTIC_URL, ELASTIC_INDEX   )
# async def fetch_recent_mongo_logs(size: int = 10):
#     url = f"{ELASTIC_URL}/{ELASTIC_INDEX}/_search"

#     query = {
#         "size": size,
#         "query": {
#             "match_all": {}
#         }
#     }

#     async with httpx.AsyncClient(timeout=10) as client:
#         response = await client.post(url, json=query)
#         response.raise_for_status()
#     #print(response.json())
#     hits = response.json()["hits"]["hits"]
#     return [hit["_source"] for hit in hits]
# #asyncio.run(fetch_recent_mongo_logs())
# app/elastic/client.py
import httpx
from app.config import ELASTIC_URL, ELASTIC_INDEX


async def fetch_recent_mongo_logs(size: int = 10):
    url = f"{ELASTIC_URL}/{ELASTIC_INDEX}/_search"

    # 🔥 TEMP DEBUG (leave this for now)
    print("DEBUG ES URL =>", repr(url))

    query = {
        "size": size,
        "query": {"match_all": {}}
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, json=query)
        response.raise_for_status()

    hits = response.json()["hits"]["hits"]
    return [hit["_source"] for hit in hits]