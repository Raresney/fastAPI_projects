from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, HttpUrl


class ScanCreate(BaseModel):
    target_url: HttpUrl


class ScanResponse(BaseModel):
    id: UUID
    project_id: UUID
    target_url: str
    status: str
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
