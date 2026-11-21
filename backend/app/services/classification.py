from sqlalchemy.orm import Session

from app.models.email import Email
from app.models.email_analysis import EmailAnalysis
from app.models.enums import EmailCategory, PriorityLevel


def set_user_classification(
    db: Session,
    email: Email,
    category: EmailCategory | None,
    priority: PriorityLevel | None,
) -> EmailAnalysis:
    analysis = email.analysis
    if analysis is None:
        analysis = EmailAnalysis(email_id=email.id)
        db.add(analysis)

    if category is not None:
        analysis.user_category = category
        analysis.category_overridden = True
    if priority is not None:
        analysis.user_priority = priority
        analysis.priority_overridden = True

    db.commit()
    db.refresh(analysis)
    return analysis
