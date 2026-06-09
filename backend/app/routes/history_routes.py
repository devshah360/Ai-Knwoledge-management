from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.chat_model import ChatHistory

router = APIRouter(
    prefix="/chat/history",
    tags=["History"]
)


@router.get("/")
def history(
    page: int = 1,
    db: Session = Depends(get_db)
):
    page_size = 10

    chats = (
        db.query(ChatHistory)
        .order_by(ChatHistory.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return [
    {
        "id": chat.id,
        "title": chat.question,
        "created_at": chat.created_at
    }
    for chat in chats
]


@router.get("/{chat_id}")
def get_chat(
    chat_id: int,
    db: Session = Depends(get_db)
):
    chat = (
        db.query(ChatHistory)
        .filter(ChatHistory.id == chat_id)
        .first()
    )

    if not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )

    return {
    "id": chat.id,
    "title": chat.question,
    "question": chat.question,
    "answer": chat.answer,
    "sources": chat.sources,
    "created_at": chat.created_at
}


@router.delete("/{chat_id}")
def delete_chat(
    chat_id: int,
    db: Session = Depends(get_db)
):
    chat = (
        db.query(ChatHistory)
        .filter(ChatHistory.id == chat_id)
        .first()
    )

    if not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )

    db.delete(chat)
    db.commit()

    return {
        "message": "Chat deleted successfully"
    }