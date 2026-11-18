import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import EmailSource


class Email(Base):
    __tablename__ = "emails"
    __table_args__ = (
        UniqueConstraint("email_account_id", "provider_message_id", name="uq_account_provider_message"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    email_account_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("email_accounts.id"), nullable=True, index=True
    )
    provider_message_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sender: Mapped[str] = mapped_column(String(320), nullable=False)
    recipient: Mapped[str] = mapped_column(String(320), nullable=False)
    subject: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    body_text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    source: Mapped[EmailSource] = mapped_column(Enum(EmailSource, name="email_source"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="emails")
    email_account: Mapped["EmailAccount | None"] = relationship(back_populates="emails")
    analysis: Mapped["EmailAnalysis | None"] = relationship(
        back_populates="email", cascade="all, delete-orphan", uselist=False
    )
    tasks: Mapped[list["Task"]] = relationship(back_populates="source_email", cascade="all, delete-orphan")
    reply_drafts: Mapped[list["ReplyDraft"]] = relationship(back_populates="email", cascade="all, delete-orphan")
