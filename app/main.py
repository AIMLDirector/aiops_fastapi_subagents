import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
load_dotenv()
from app.api import router
from app.elastic.client import fetch_recent_mongo_logs
from app.models.schemas import MongoAlert
from app.utils.formatter import format_alert
from app.agents.manager_agent import analyze_alert
from app.integrations.servicenow import create_incident, update_incident
from app.integrations.slack import notify_slack


async def poll_elasticsearch():
    """
    Background task:
    - Fetch MongoDB logs from Elasticsearch
    - Analyze with sub-agents
    - Create/update incidents
    - Notify Slack
    """
    print("🚀 Started Elasticsearch polling loop")

    try:
        while True:
            try:
                logs = await fetch_recent_mongo_logs()

                for raw in logs:
                    alert = MongoAlert.model_validate(raw)
                    llm_input = format_alert(alert)

                    result = await analyze_alert(llm_input)

                    incident = await create_incident(
                        f"{result['severity']} - MongoDB Alert",
                        result["root_cause"]
                    )

                    await update_incident(
                        incident["sys_id"],
                        f"🤖 AI Suggested Fix:\n{result['fix']}"
                    )

                    await notify_slack(
                        f"""
MongoDB Alert (from Elasticsearch)
Severity: {result['severity']}

Root Cause:
{result['root_cause']}

Fix:
{result['fix']}
"""
                    )

            except Exception as e:
                print("Elasticsearch polling error:", e)

            await asyncio.sleep(60)

    except asyncio.CancelledError:
        print("Elasticsearch polling task cancelled")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔹 Startup
    task = asyncio.create_task(poll_elasticsearch())
    yield
    # 🔹 Shutdown
    task.cancel()
    await task


app = FastAPI(
    title="AIOps MongoDB Alert Processor",
    lifespan=lifespan
)

app.include_router(router)