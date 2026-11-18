import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import EmailCategory, PriorityLevel, priority_level_enum


class EmailAnalysis(Base):
    __tablename__ = "email_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("emails.id"), nullable=False, unique=True, index=True
    )
    category: Mapped[EmailCategory] = mapped_column(Enum(EmailCategory, name="email_category"), nullable=False)
    priority: Mapped[PriorityLevel] = mapped_column(priority_level_enum, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False, default="")
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Structured list of {date, label} and {task, deadline} extracted by the AI — raw AI output, not verified fact.
    extracted_dates: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    action_items: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    suggested_next_steps: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    security_flags: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    model_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    analysis_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    email: Mapped["Email"] = relationship(back_populates="analysis")
