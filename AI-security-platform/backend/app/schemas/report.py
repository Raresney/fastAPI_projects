from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class ReportCreate(BaseModel):
    report_type: str = "executive"


class ReportResponse(BaseModel):
    id: UUID
    scan_id: UUID
    report_type: str
    content: dict | None
    ai_summary: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
