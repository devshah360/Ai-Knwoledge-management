from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate,UserResponse
from app.database import get_db
from app.utils.security import hash_password
from app.services.user_service import (create_new_user)

router = APIRouter()

@router.post("/users",response_model=UserResponse)

def create_user(user: UserCreate,db : Session = Depends(get_db)):
        new_user = create_new_user(user,db)

        if not new_user:
                raise HTTPException(
                        status_code=400,
                        detail= "Email already exists"
                )

        return new_user

        