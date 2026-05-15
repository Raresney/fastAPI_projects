from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class FindingResponse(BaseModel):
    id: UUID
    scan_id: UUID
    title: str
    description: str
    severity: str
    category: str
    evidence: str | None
    remediation: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
