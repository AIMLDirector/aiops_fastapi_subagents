from pydantic import BaseModel
from typing import Dict, Any, Optional


class MongoAlert(BaseModel):
    t: Optional[Any] = None
    s: Optional[str] = None
    c: Optional[str] = None
    id: Optional[int] = None
    ctx: Optional[str] = None
    msg: Optional[str] = None
    attr: Optional[Dict[str, Any]] = None

    # Accept ANY future MongoDB fields
    model_config = {"extra": "allow"}


class AIResult(BaseModel):
    severity: str
    root_cause: str
    fix: str