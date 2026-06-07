from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.audit_model import AuditLog

router = APIRouter(
        prefix="/activity",
        tags=["Activity"]
)

@router.get("/")
def activity(db:Session = Depends(get_db)):
        return (db.query(AuditLog).order_by(AuditLog.id.desc()).all())