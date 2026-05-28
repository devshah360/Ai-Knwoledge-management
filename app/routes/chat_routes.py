from fastapi import APIRouter,Depends
from app.middlewave.auth_middleware import get_current_user
from app.services.agents.workflow_agent import run_workflow

router = APIRouter(
        prefix="/chat",
        tags=["AI Workflow Chat"]
)

@router.post("/")
def chat(question:str , current_user = Depends(get_current_user)):
        result = run_workflow(question)

        return result
