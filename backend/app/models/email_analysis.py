import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import functions as sql_functions

from app.core.database import Base
from app.models.enums import EmailCategory, PriorityLevel, email_category_enum, priority_level_enum


class EmailAnalysis(Base):
    __tablename__ = "email_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("emails.id"), nullable=False, unique=True, index=True
    )
    # AI-suggested classification. Null until Phase 2's classifier has run on this email.
    ai_category: Mapped[EmailCategory | None] = mapped_column(email_category_enum, nullable=True)
    ai_priority: Mapped[PriorityLevel | None] = mapped_column(priority_level_enum, nullable=True)
    # Explicit user choice, set only when the user edits the classification themselves.
    # Kept separate from ai_category/ai_priority (rather than overwriting them) so a
    # future re-run of the AI classifier never silently clobbers a human decision.
    user_category: Mapped[EmailCategory | None] = mapped_column(email_category_enum, nullable=True)
    user_priority: Mapped[PriorityLevel | None] = mapped_column(priority_level_enum, nullable=True)
    category_overridden: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    priority_overridden: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
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

    @hybrid_property
    def category(self) -> EmailCategory | None:
        """Effective category: the user's choice if they've made one, else the AI's."""
        return self.user_category if self.user_category is not None else self.ai_category

    @category.inplace.expression
    @classmethod
    def _category_expression(cls):
        return sql_functions.coalesce(cls.user_category, cls.ai_category)

    @hybrid_property
    def priority(self) -> PriorityLevel | None:
        """Effective priority: the user's choice if they've made one, else the AI's."""
        return self.user_priority if self.user_priority is not None else self.ai_priority

    @priority.inplace.expression
    @classmethod
    def _priority_expression(cls):
        return sql_functions.coalesce(cls.user_priority, cls.ai_priority)
