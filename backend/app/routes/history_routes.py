from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.chat_model import ChatHistory

router = APIRouter(
        prefix="/history",
        tags=["History"]
)

@router.get("/")
def history(db:Session = Depends(get_db)):

        return (db.query(ChatHistory).order_by(ChatHistory.id.desc()).all())