from sqlalchemy.orm import Session
from app.models.user_model import User
from app.utils.security import(
        verify_password,
        create_access_token
)

def login_user(email,password,db:Session):
        user = db.query(User).filter(
                User.email==email).first()
        
        if not user:
                return None
        
        valid_password = verify_password(
                password,
                user.password
        )

        if not valid_password:
                return None
        
        token = create_access_token(
                data ={
                        "user_id":user.id,
                        "email":user.email
                }
        )
        return token