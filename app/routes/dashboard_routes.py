from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.middlewave.auth_middleware import get_current_user
from app.services.analytics_service import get_dashboard_state
from app.services.chart_service import document_upload_chart
from app.services.insight_service import generate_dashboard_insight

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
