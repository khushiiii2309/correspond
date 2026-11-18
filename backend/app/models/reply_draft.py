import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ReplyStatus


class ReplyDraft(Base):
    __tablename__ = "reply_drafts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("emails.id"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    tone: Mapped[str] = mapped_column(String(50), nullable=False, default="professional")
    draft_content: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status: Mapped[ReplyStatus] = mapped_column(Enum(ReplyStatus, name="reply_status"), default=ReplyStatus.DRAFT)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    email: Mapped["Email"] = relationship(back_populates="reply_drafts")
    user: Mapped["User"] = relationship(back_populates="reply_drafts")
