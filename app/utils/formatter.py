import json
from app.models.schemas import MongoAlert


def format_alert(alert: MongoAlert) -> str:
    return f"""
MongoDB Alert (raw JSON):

{json.dumps(alert.model_dump(), indent=2)}

Instructions:
- Identify alert type
- Classify severity (P1 to P4)
- Find root cause
- Suggest fix
"""