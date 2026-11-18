from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User

# Phase 1 has no login flow yet. Every request resolves to this single seeded
# account so the data model (user_id scoping, isolation) is already real and
# won't need reshaping when real authentication is added.
DEMO_USER_EMAIL = "demo@correspond.app"


def get_current_user(db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.email == DEMO_USER_EMAIL).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Demo user not provisioned. Restart the API to run startup seeding.",
        )
    return user
