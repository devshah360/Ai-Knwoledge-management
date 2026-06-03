from app.models.user_model import User
from app.models.document_model import Document
from app.models.search_model import SearchHistory
from app.models.chat_model import ChatHistory
from sqlalchemy import func
from app.models.audit_model import (
    AuditLog
)

def get_kpis(db):

    return {

        "total_users":
            db.query(User).count(),

        "total_documents":
            db.query(Document).count(),

        "total_searches":
            db.query(SearchHistory).count(),

        "total_chats":
            db.query(ChatHistory).count()
    }

def search_trend(db):

    result = (

        db.query(

            func.date(
                SearchHistory.created_at
            ),

            func.count(
                SearchHistory.id
            )
        )

        .group_by(
            func.date(
                SearchHistory.created_at
            )
        )

        .all()
    )

    return result

def upload_trend(db):

    result = (

        db.query(

            func.date(
                Document.created_at
            ),

            func.count(
                Document.id
            )
        )

        .group_by(
            func.date(
                Document.created_at
            )
        )

        .all()
    )

    return result

def activity_chart(db):

    result = (

        db.query(

            AuditLog.action,

            func.count(
                AuditLog.id
            )
        )

        .group_by(
            AuditLog.action
        )

        .all()
    )

    return result

def top_searches(db):

    result = (

        db.query(

            SearchHistory.query,

            func.count(
                SearchHistory.id
            )
        )

        .group_by(
            SearchHistory.query
        )

        .order_by(
            func.count(
                SearchHistory.id
            ).desc()
        )

        .limit(10)

        .all()
    )

    return result

def active_users(db):

    result = (

        db.query(

            AuditLog.user_id,

            func.count(
                AuditLog.id
            )
        )

        .group_by(
            AuditLog.user_id
        )

        .order_by(
            func.count(
                AuditLog.id
            ).desc()
        )

        .limit(10)

        .all()
    )

    return result
