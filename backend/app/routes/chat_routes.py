from fastapi import APIRouter, Depends, Request
from app.middlewave.auth_middleware import get_current_user
from app.services.agents.workflow_agent import run_workflow
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.rag_service import rag_chat
from app.core.rate_limit import limiter
from fastapi.responses import StreamingResponse
import asyncio

router = APIRouter(
    prefix="/chat",
    tags=["AI Workflow Chat"]
)

@router.post("/")
@limiter.limit("20/minute")
def chat(
    request: Request,
    question: str,
    db: Session = Depends(get_db),
):
    return rag_chat(
        question,
        db,
    )

@router.post("/stream")
async def stream_chat():

    async def generate():

        text = """
        Employee receive
        12 casual leaves,
        12 sick leave,
        and 15 annual leaves.
        """

        for word in text.split():

            yield word + " "

            await asyncio.sleep(0.1)

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )