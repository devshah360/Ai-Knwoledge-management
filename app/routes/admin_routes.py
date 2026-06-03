from fastapi import APIRouter,Depends
from app.middlewave.auth_middleware import admin_required,get_current_user
from app.middlewave.admin_middleware import required_admin
from app.models.user_model import User
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.document_model import Document
from app.models.chat_model import ChatHistory
from app.models.audit_model import AuditLog
from app.models.search_model import SearchHistory


















router = APIRouter(
        prefix="/admin",
        tags=["Admin"]
)

@router.get("/users")
def total_users(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
        required_admin(current_user)
        return {"users":db.query(User).count()}

@router.get("/documents")
def total_documents(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
        required_admin(current_user)
        return {"documents":db.query(Document).count()}

@router.get("/chats")
def total_chats(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
        required_admin(current_user)
        return {"chats":db.query(ChatHistory).count()}

@router.get("/searches")
def total_searches(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
        required_admin(current_user)
        return {"searches":db.query(SearchHistory).order_by(SearchHistory.id.desc()).limit(50).all()}


@router.get("/activites")
def total_activites(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
        required_admin(current_user)
        return {"activites":db.query(AuditLog).order_by(AuditLog.id.desc()).limit(100).all()}


@router.get("/dashboard")
def dashboard(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
        required_admin(current_user)
        return {"users":db.query(User).count(),
                "documents":db.query(Document).count(),
                "chats":db.query(ChatHistory).count(),
                "seaches":db.query(SearchHistory).count(),
                }