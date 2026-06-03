from sqlalchemy.orm import Session
from app.models.user_model import User
from app.utils.security import (
    verify_password,
    create_access_token
)
from app.services.audit_service import create_log


def login_user(email, password, db: Session):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:

        create_log(
            db,
            None,
            "Failed Login"
        )

        return None

    valid_password = verify_password(
        password,
        user.password
    )

    if not valid_password:

        create_log(
            db,
            user.id,
            "Failed Login"
        )

        return None

    token = create_access_token(
        data={
            "user_id": user.id,
            "email": user.email
        }
    )

    return token