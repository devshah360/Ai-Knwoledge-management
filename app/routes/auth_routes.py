from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm 
from app.services.auth_service import login_user
from app.utils.password_validator import validate_password
from app.services.audit_service import create_log

router = APIRouter(
        prefix="/auth",
        tags=["Authentication"]
)

@router.post("/login")
def login(form_data :OAuth2PasswordRequestForm = Depends(),db :Session=Depends(get_db)):
        token = login_user(
                form_data.username,
                form_data.password,
                db
        )


        if not token:

                create_log(
                db,
                None,
                "Failed Login"
                )

                raise HTTPException(
                        status_code=401,
                        detail="Invalid Credentials"
                )

        return{
                "access_token":token,
                "token_type": "bearer"
        }
