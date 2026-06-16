from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.services.auth_service import login_user
from app.services.audit_service import create_log
from app.models.user_model import User

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    email = form_data.username
    password = form_data.password

    token = login_user(
        email,
        password,
        db
    )

    if not token:
        # create_log(
        #     db,
        #     f"Failed Login: {email}"
        # )

        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    user = db.query(User).filter(
        User.email == email
    ).first()

    #create_log(
      #  db,
      #  f"Successful Login: {email}"
    #)

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "email": user.email,
        "username": user.username
    }