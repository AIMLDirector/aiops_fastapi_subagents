import os
import httpx
from dotenv import load_dotenv
load_dotenv()

WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")


async def notify_slack(message: str):
    async with httpx.AsyncClient() as client:
        await client.post(WEBHOOK, json={"text": message})