import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import EmailCategory, EmailSource, PriorityLevel


class AnalysisSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # Effective values: the user's choice if they've made one, else the AI's suggestion.
    category: EmailCategory | None
    priority: PriorityLevel | None
    ai_category: EmailCategory | None = None
    ai_priority: PriorityLevel | None = None
    category_overridden: bool
    priority_overridden: bool
    summary: str
    confidence: float | None = None


class ClassificationUpdate(BaseModel):
    category: EmailCategory | None = None
    priority: PriorityLevel | None = None


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
