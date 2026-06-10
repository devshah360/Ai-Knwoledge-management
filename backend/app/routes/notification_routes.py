from fastapi import APIRouter
from app.services.notification_service import (
    get_notifications,
    mark_as_read
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get("/")
def notifications():
    return get_notifications()


@router.put("/{notification_id}/read")
def mark_read(notification_id: str):

    mark_as_read(notification_id)

    return {
        "message": "updated"
    }


@router.get("/history")
def history():
    return get_notifications()