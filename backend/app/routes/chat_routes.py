from fastapi import APIRouter, Depends, Request
from app.middlewave.auth_middleware import get_current_user
from app.services.agents.workflow_agent import run_workflow
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.rag_service import rag_chat
from app.core.rate_limit import limiter
from fastapi.responses import StreamingResponse
import asyncio
from app.services.notification_service import create_notification
router = APIRouter(
    prefix="/chat",
    tags=["AI Workflow Chat"]
)

@router.post("/")
def chat(
    request: Request,
    question: str,
    conversation_id: str = None,
    db: Session = Depends(get_db),
):

    return rag_chat(
        question=question,
        conversation_id=conversation_id,
        db=db
    )