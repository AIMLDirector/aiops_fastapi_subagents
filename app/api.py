from fastapi import APIRouter, BackgroundTasks
from typing import List

from app.models.schemas import MongoAlert, AIResult
from app.utils.formatter import format_alert
from app.agents.manager_agent import analyze_alert
from app.integrations.servicenow import create_incident, update_incident
from app.integrations.slack import notify_slack
from app.elastic.client import fetch_recent_mongo_logs

router = APIRouter(prefix="/api", tags=["AIOps"])


# ---------------------------
# 1️⃣ Common processing logic
# ---------------------------
async def process_alert(alert: MongoAlert) -> AIResult:
    llm_input = format_alert(alert)

    result = await analyze_alert(llm_input)

    incident = await create_incident(
        short_desc=f"{result['severity']} - MongoDB Alert",
        description=result["root_cause"]
    )

    await update_incident(
        incident["sys_id"],
        f"🤖 AI Suggested Fix:\n{result['fix']}"
    )

    await notify_slack(
        f"""
🚨 MongoDB Alert
Severity: {result['severity']}

Root Cause:
{result['root_cause']}

Fix:
{result['fix']}
"""
    )

    return AIResult(**result)


# ----------------------------------
# 2️⃣ API: Push ANY MongoDB alert
# ----------------------------------
@router.post("/alert", response_model=AIResult)
async def ingest_mongo_alert(alert: MongoAlert):
    """
    Accept ANY MongoDB alert/log (schema-less).
    """
    return await process_alert(alert)


# -------------------------------------------------
# 3️⃣ API: Fetch & process alerts from Elasticsearch
# -------------------------------------------------
@router.post("/elasticsearch/process", response_model=List[AIResult])
async def process_elasticsearch_alerts(size: int = 10):
    raw_logs = await fetch_recent_mongo_logs(size=size)

    results: List[AIResult] = []

    for raw in raw_logs:
        alert = MongoAlert.model_validate(raw)
        result = await process_alert(alert)
        results.append(result)

    return results