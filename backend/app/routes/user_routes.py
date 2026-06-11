from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserUpdate
)
from app.services.user_service import (
    create_new_user,
    get_all_users,
    get_user_by_id,
    delete_user_by_id
)
from app.utils.password_validator import validate_password
from app.models.user_model import User
from app.services.notification_service import (
    create_notification
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/get", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):
    return get_all_users(db)


@router.post("/create", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)

):
    new_user = create_new_user(
        user,
        db
    )

    if not validate_password(user.password):
        raise HTTPException(
            status_code=400,
            detail=(
                "Password must contain at least "
                "8 characters, one uppercase letter, "
                "one lowercase letter and one number"
            )
        )

    new_user = create_new_user(user, db)

    if not new_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    if new_user:
        create_notification(
            f"New User Created: {new_user.email}",
            "success"
        )

    return new_user


@router.put("/{user_id}")
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if data.username is not None:
        user.username = data.username

    if data.email is not None:
        user.email = data.email

    if data.role is not None:
        user.role = data.role

    if data.is_active is not None:
        user.is_active = data.is_active

    db.commit()
    db.refresh(user)

    create_notification(
        f"User Updated: {user.email}",
        "info"
    )

    return {
        "message": "updated",
        "user": user
    }


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_user_by_id(user_id, db)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    create_notification(
        f"User Deleted ID: {user_id}",
        "warning"
    )

    return {
        "message": "deleted"
    }