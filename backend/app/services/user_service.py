from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.utils.security import hash_password

def create_new_user(user:UserCreate,db:Session):
        existing_user = db.query(User).filter(
                User.email==user.email).first()

        if existing_user:
                return None
        
        new_user = User(
                username = user.username,
                email = user.email,
                password = hash_password(user.password)
        )
        db.add(new_user)

        db.commit()

        db.refresh(new_user)

        return new_user