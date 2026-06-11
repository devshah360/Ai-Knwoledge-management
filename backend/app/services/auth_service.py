from sqlalchemy.orm import Session

from app.models.user_model import User
from app.utils.security import (
    verify_password,
    create_access_token
)
from app.services.audit_service import create_log


def login_user(
    email: str,
    password: str,
    db: Session
):
    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        create_log(
            db,
            f"Failed Login: {email}"
        )
        return None

    if not verify_password(
        password,
        user.password
    ):
        create_log(
            db,
            f"Failed Login: {email}"
        )
        return None

    token = create_access_token(
        data={
            "user_id": user.id,
            "email": user.email,
            "role": user.role
        }
    )

    return token