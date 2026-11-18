from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.api.deps import DEMO_USER_EMAIL
from app.models.email import Email
from app.models.enums import EmailSource
from app.models.user import User
from app.schemas.email import DemoSeedResult
from app.services.sample_emails_data import SAMPLE_EMAILS


def ensure_demo_user(db: Session) -> User:
    user = db.query(User).filter(User.email == DEMO_USER_EMAIL).first()
    if user is not None:
        return user

    user = User(email=DEMO_USER_EMAIL, password_hash=None)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def seed_demo_emails(db: Session, user: User) -> DemoSeedResult:
    now = datetime.now(timezone.utc)
    created = 0
    skipped = 0

    for sample in SAMPLE_EMAILS:
        exists = (
            db.query(Email)
            .filter(
                Email.user_id == user.id,
                Email.sender == sample["sender"],
                Email.subject == sample["subject"],
                Email.source == EmailSource.SAMPLE,
            )
            .first()
        )
        if exists is not None:
            skipped += 1
            continue

        email = Email(
            user_id=user.id,
            email_account_id=None,
            provider_message_id=None,
            sender=sample["sender"],
            recipient=sample["recipient"],
            subject=sample["subject"],
            body_text=sample["body_text"],
            received_at=now - timedelta(hours=sample["hours_ago"]),
            is_read=False,
            source=EmailSource.SAMPLE,
        )
        db.add(email)
        created += 1

    db.commit()
    return DemoSeedResult(created=created, skipped=skipped)
