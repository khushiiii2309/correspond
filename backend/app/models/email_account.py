import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ConnectionStatus


class EmailAccount(Base):
    __tablename__ = "email_accounts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(50), nullable=False, default="gmail")
    provider_account_id: Mapped[str] = mapped_column(String(255), nullable=False)
    # Encrypted OAuth credential blob. Never store raw tokens or expose them to the frontend.
    encrypted_credentials: Mapped[str | None] = mapped_column(String, nullable=True)
    connection_status: Mapped[ConnectionStatus] = mapped_column(
        Enum(ConnectionStatus, name="connection_status"), default=ConnectionStatus.DISCONNECTED
    )
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(back_populates="email_accounts")
    emails: Mapped[list["Email"]] = relationship(back_populates="email_account")
