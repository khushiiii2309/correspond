import enum

from sqlalchemy import Enum as SAEnum


class EmailSource(str, enum.Enum):
    SAMPLE = "sample"
    GMAIL = "gmail"


class EmailCategory(str, enum.Enum):
    IMPORTANT = "important"
    REQUIRES_ACTION = "requires_action"
    INFORMATIONAL = "informational"
    PROMOTIONAL = "promotional"
    POTENTIALLY_SUSPICIOUS = "potentially_suspicious"


class PriorityLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskStatus(str, enum.Enum):
    SUGGESTED = "suggested"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DISMISSED = "dismissed"


class ReplyStatus(str, enum.Enum):
    DRAFT = "draft"
    EDITED = "edited"
    APPROVED = "approved"


class ConnectionStatus(str, enum.Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"


class ActorType(str, enum.Enum):
    AI = "ai"
    USER = "user"
    SYSTEM = "system"


# Shared SQLAlchemy Enum instances for types referenced by more than one table,
# so Alembic/metadata only ever see a single "CREATE TYPE" for each Postgres enum.
priority_level_enum = SAEnum(PriorityLevel, name="priority_level")
email_category_enum = SAEnum(EmailCategory, name="email_category")
