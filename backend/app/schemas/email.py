import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import EmailCategory, EmailSource, PriorityLevel


class AnalysisSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category: EmailCategory
    priority: PriorityLevel
    summary: str
    confidence: float | None = None


class EmailListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    sender: str
    subject: str
    preview: str
    received_at: datetime
    is_read: bool
    source: EmailSource
    category: EmailCategory | None = None
    priority: PriorityLevel | None = None
    has_analysis: bool


class EmailDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    sender: str
    recipient: str
    subject: str
    body_text: str
    received_at: datetime
    is_read: bool
    source: EmailSource
    analysis: AnalysisSummary | None = None


class ReadStatusUpdate(BaseModel):
    is_read: bool


class DemoSeedResult(BaseModel):
    created: int
    skipped: int
