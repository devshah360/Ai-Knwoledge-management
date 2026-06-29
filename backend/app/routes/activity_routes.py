from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.audit_model import AuditLog

router = APIRouter(
    prefix="/activity",
    tags=["Activity"]
)


@router.get("/")
def activity(db: Session = Depends(get_db)):
    logs = (
        db.query(AuditLog)
        .order_by(AuditLog.id.desc())
        .all()
    )

    return logs


@router.delete("/{log_id}")
def delete_activity_log(
    log_id: int,
    db: Session = Depends(get_db)
):
    log = (
        db.query(AuditLog)
        .filter(AuditLog.id == log_id)
        .first()
    )

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Log not found"
        )

    db.delete(log)
    db.commit()

    return {
        "message": "Log deleted successfully"
    }


@router.delete("/")
def delete_all_logs(
    db: Session = Depends(get_db)
):
    db.query(AuditLog).delete()
    db.commit()

    return {
        "message": "All logs deleted successfully"
    }