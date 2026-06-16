from sqlalchemy.orm import Session
from fastapi import Depends
from app.middlewave.auth_middleware import get_current_user
from app.models.user_model import User
from app.utils.security import (
    verify_password,
    create_access_token
)
from app.services.audit_service import create_log


def login_user(
    email: str,
    password: str,
    db: Session,
    current_user = Depends(get_current_user)
):
    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        create_log(
            db,
            current_user,
            f"Failed Login: {email}"
        )
        return None

    if not verify_password(
        password,
        user.password
    ):
        create_log(
            db,
            current_user,
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