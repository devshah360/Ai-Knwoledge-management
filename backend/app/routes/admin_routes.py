from fastapi import APIRouter, Depends
from app.middlewave.auth_middleware import admin_required, get_current_user
from app.middlewave.admin_middleware import required_admin
from app.models.user_model import User
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.document_model import Document
from app.models.chat_model import ChatHistory
from app.models.audit_model import AuditLog
from app.models.search_model import SearchHistory
from app.services.audit_service import create_log

router = APIRouter(
        prefix="/admin",
        tags=["Admin"]
)

@router.get("/users")
def total_users(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
        required_admin(current_user)

        create_log(
                db,
                current_user.id,
                "Admin Access"
        )

        return {
                "users": db.query(User).count()
        }


@router.get("/documents")
def total_documents(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
        required_admin(current_user)

        create_log(
                db,
                current_user.id,
                "Admin Access"
        )

        return {
                "documents": db.query(Document).count()
        }


@router.get("/chats")
def total_chats(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
        required_admin(current_user)

        create_log(
                db,
                current_user.id,
                "Admin Access"
        )

        return {
                "chats": db.query(ChatHistory).count()
        }


@router.get("/searches",response_model=dict)
def total_searches(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
        required_admin(current_user)

        create_log(
                db,
                current_user.id,
                "Admin Access"
        )

        searches = (db.query(SearchHistory).order_by(SearchHistory.id.desc()).limit(50).all())
        return {
                "searches": [{
                        "id":s.id,
                        "query":s.query,
                        "created_at":s.created_at
                }
                for s in searches
        ]
        
}


@router.get("/activites")
def total_activites(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
        required_admin(current_user)

        create_log(
                db,
                current_user.id,
                "Admin Access"
        )

        return {
                "activites": db.query(AuditLog)
                .order_by(AuditLog.id.desc())
                .limit(100)
                .all()
        }


@router.get("/dashboard")
def dashboard(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
        required_admin(current_user)

        create_log(
                db,
                current_user.id,
                "Admin Access"
        )

        return {
                "users": db.query(User).count(),
                "documents": db.query(Document).count(),
                "chats": db.query(ChatHistory).count(),
                "seaches": db.query(SearchHistory).count(),
        }

@router.get("/logs")
def activity_logs(db: Session = Depends(get_db)):

        logs = (db.query(AuditLog).order_by(AuditLog.id.desc()).limit(100).all())

        return {
                "logs":[{
                        "id": log.id,
                        "action": log.action,
                        "created_at": log.created_at
                }
                for log in logs
        ]
}