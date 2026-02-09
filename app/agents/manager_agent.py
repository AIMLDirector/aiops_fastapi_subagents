import asyncio
from app.agents.severity_agent import severity_agent
from app.agents.rca_agent import rca_agent
from app.agents.fix_agent import fix_agent
from dotenv import load_dotenv

load_dotenv()

async def analyze_alert(alert_text: str) -> dict:
    severity, rca, fix = await asyncio.gather(
        severity_agent(alert_text),
        rca_agent(alert_text),
        fix_agent(alert_text)
    )

    return {
        "severity": severity,
        "root_cause": rca,
        "fix": fix
    }