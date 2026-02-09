import os
import httpx
import asyncio
from dotenv import load_dotenv
load_dotenv()
BASE_URL = f"{os.getenv('SN_INSTANCE')}/api/now/table/incident"
AUTH = (os.getenv("SN_USER"), os.getenv("SN_PASSWORD"))



async def create_incident(short_desc: str, description: str):
    async with httpx.AsyncClient(auth=AUTH) as client:
        res = await client.post(
            BASE_URL,
            json={
                "short_description": short_desc,
                "description": description
            }
        )
        return res.json()["result"]
        #print(res.json())


async def update_incident(sys_id: str, work_notes: str):
    async with httpx.AsyncClient(auth=AUTH) as client:
        await client.patch(
            f"{BASE_URL}/{sys_id}",
            json={"work_notes": work_notes}
        )

#asyncio.run(create_incident("Test Incident", "This is a test incident"))    