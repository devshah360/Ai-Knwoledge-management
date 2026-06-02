from fastapi import APIRouter,Depends
from app.middlewave.auth_middleware import get_current_user
from app.services.agents.workflow_agent import run_workflow
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.rag_service import rag_chat
router = APIRouter(
        prefix="/chat",
        tags=["AI Workflow Chat"]
)

@router.post("/")
def chat(question:str , db: Session = Depends(get_db),current_user = Depends(get_current_user)):
        return rag_chat(
                question,
                db,
                current_user.id
        )

        
