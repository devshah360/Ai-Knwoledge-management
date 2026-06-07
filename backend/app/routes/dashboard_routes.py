from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.middlewave.auth_middleware import get_current_user
from app.services.analytics_service import get_dashboard_state
from app.services.chart_service import document_upload_chart
from app.services.insight_service import generate_dashboard_insight
from app.services.analytics_service import get_dashboard_state
from app.services.dashboard_service import (search_trend,
    upload_trend,
    activity_chart,
    top_searches,
    active_users
)
router = APIRouter(
        prefix="/dashboard",
        tags=["Dashboard"]
)

@router.get("/stats")
def dashboard_state(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
        stats = get_dashboard_state(db)
        return stats

@router.get("/charts/uploads")
def upload_chart(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
        chart = document_upload_chart(db)
        return chart

@router.get("/insights")
def ai_insights(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
        stats = get_dashboard_state(db)
        insights = generate_dashboard_insight(stats)
        return {"insights":insights}

@router.get("/search-trend")
def search_trends(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return search_trend(db)


@router.get("/upload-trend")
def upload_trends(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return upload_trend(db)


@router.get("/activity-chart")
def activity(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return activity_chart(db)


@router.get("/top-searches")
def searches(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return top_searches(db)


@router.get("/active-users")
def users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return active_users(db)

from app.services.insight_service import (
    generate_dashboard_insight,
    generate_insights
)


@router.get("/insights-v2")
def insights(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return generate_insights(db)

@router.get("/workflow-health")
def workflow_health(
    current_user=Depends(get_current_user)
):

    return {
        "postgres": "healthy",
        "mongo": "healthy",
        "elastic": "healthy",
        "redis": "healthy",
        "celery": "healthy",
        "ollama": "healthy"
    }