from app.database import get_db
from app.middlewave.auth_middleware import get_current_user
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session





router = APIRouter(
        prefix="/user",
        tags=["User"]
)

@router.get("/me")
def my_dashboard(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
        return{
                "my_documents" : 10,
                "my_chats":25,
                "my_searches":50
        }
        