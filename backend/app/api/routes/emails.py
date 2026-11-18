import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.email import Email
from app.models.enums import EmailCategory, PriorityLevel
from app.models.user import User
from app.schemas.email import DemoSeedResult, EmailDetail, EmailListItem, ReadStatusUpdate
from app.services.demo_seed import ensure_demo_user, seed_demo_emails

router = APIRouter(prefix="/emails", tags=["emails"])

_PRIORITY_ORDER = {PriorityLevel.HIGH: 0, PriorityLevel.MEDIUM: 1, PriorityLevel.LOW: 2}


def _preview(body_text: str, length: int = 140) -> str:
    collapsed = " ".join(body_text.split())
    return collapsed[:length] + ("…" if len(collapsed) > length else "")


def _to_list_item(email: Email) -> EmailListItem:
    analysis = email.analysis
    return EmailListItem(
        id=email.id,
        sender=email.sender,
        subject=email.subject,
        preview=_preview(email.body_text),
        received_at=email.received_at,
        is_read=email.is_read,
        source=email.source,
        category=analysis.category if analysis else None,
        priority=analysis.priority if analysis else None,
        has_analysis=analysis is not None,
    )


@router.post("/demo/seed", response_model=DemoSeedResult)
def seed_demo_inbox(db: Session = Depends(get_db)) -> DemoSeedResult:
    user = ensure_demo_user(db)
    return seed_demo_emails(db, user)


@router.get("", response_model=list[EmailListItem])
def list_emails(
    category: EmailCategory | None = Query(default=None),
    priority: PriorityLevel | None = Query(default=None),
    unread_only: bool = Query(default=False),
    search: str | None = Query(default=None, max_length=200),
    sort: str = Query(default="date", pattern="^(date|priority)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[EmailListItem]:
    query = db.query(Email).filter(Email.user_id == current_user.id)

    if unread_only:
        query = query.filter(Email.is_read.is_(False))

    if search:
        like = f"%{search}%"
        query = query.filter((Email.subject.ilike(like)) | (Email.sender.ilike(like)) | (Email.body_text.ilike(like)))

    if category is not None:
        query = query.filter(Email.analysis.has(category=category))

    if priority is not None:
        query = query.filter(Email.analysis.has(priority=priority))

    if sort == "date":
        query = query.order_by(desc(Email.received_at))
    else:
        query = query.order_by(asc(Email.received_at))

    emails = query.all()

    items = [_to_list_item(email) for email in emails]
    if sort == "priority":
        items.sort(key=lambda item: _PRIORITY_ORDER.get(item.priority, 99))

    return items


@router.get("/{email_id}", response_model=EmailDetail)
def get_email(
    email_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> EmailDetail:
    email = db.query(Email).filter(Email.id == email_id, Email.user_id == current_user.id).first()
    if email is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    return email


@router.patch("/{email_id}/read-status", response_model=EmailDetail)
def update_read_status(
    email_id: uuid.UUID,
    payload: ReadStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> EmailDetail:
    email = db.query(Email).filter(Email.id == email_id, Email.user_id == current_user.id).first()
    if email is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")

    email.is_read = payload.is_read
    db.commit()
    db.refresh(email)
    return email
